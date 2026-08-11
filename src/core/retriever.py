"""Hybrid retriever combining BM25 (FTS5) and vector similarity search.

Uses Reciprocal Rank Fusion (RRF) to merge results from both retrieval paths,
providing both keyword precision and semantic understanding.
"""

import os
from dotenv import load_dotenv

load_dotenv()

BM25_WEIGHT = float(os.getenv("BM25_WEIGHT", "0.4"))
VEC_WEIGHT = float(os.getenv("VEC_WEIGHT", "0.6"))


class HybridRetriever:
    """Combines BM25 (FTS5) and vector KNN search with RRF fusion.
    
    Falls back to BM25-only when embedding model is unavailable.
    
    Usage:
        retriever = HybridRetriever()
        results = retriever.search("EAP111 重工原因", model="EAP111", limit=15)
    """

    def __init__(self, bm25_weight=None, vec_weight=None):
        self.bm25_weight = bm25_weight or BM25_WEIGHT
        self.vec_weight = vec_weight or VEC_WEIGHT
        self._embedder = None  # Lazy load

    @property
    def embedder(self):
        """Lazy-load embedder to avoid loading model on import."""
        if self._embedder is None:
            from src.core.embedder import LocalEmbedder
            self._embedder = LocalEmbedder.get_instance()
        return self._embedder

    @property
    def embedding_available(self):
        """Check if embedding model is loaded and vector index exists."""
        emb = self.embedder
        if emb is None or not emb.is_ready:
            return False
        from src.core.database import get_vec_chunk_count
        return get_vec_chunk_count() > 0

    def search(self, query, model=None, date_from=None,
               source_type=None, limit=15) -> list:
        """Hybrid search: BM25 + Vector + RRF merge.
        
        Falls back to BM25-only if embedding is unavailable.
        
        Args:
            query: Search query string.
            model: Optional product model filter.
            date_from: Optional date lower bound (YYYY-MM-DD).
            source_type: Optional source type filter.
            limit: Maximum number of results.
            
        Returns:
            List of dicts with keys: filename, chunk_text, model, date_str,
            source_type, snippet, score.
        """
        from src.core.database import search_chunks

        # BM25 path (always available)
        bm25_results = search_chunks(
            query, model=model, date_from=date_from,
            source_type=source_type, limit=limit * 2
        )

        # Vector path (may be unavailable)
        if self.embedding_available:
            query_vec = self.embedder.encode_query(query)
            vec_results = self._vector_search(
                query_vec, model=model, date_from=date_from,
                source_type=source_type, limit=limit * 2
            )
        else:
            vec_results = []

        # If no vector results, return BM25 only
        if not vec_results:
            for r in bm25_results:
                r["score"] = 1.0 / (60 + bm25_results.index(r) + 1)
            return bm25_results[:limit]

        # RRF fusion
        merged = self._rrf_merge(bm25_results, vec_results, k=60)
        return merged[:limit]

    def search_with_supplement(self, query, model=None, date_from=None,
                               source_type=None, limit=15) -> list:
        """Hybrid search with multi-source supplement (preserves existing logic).
        
        Ensures diverse source types in results by supplementing from
        underrepresented sources (log, trd, report).
        """
        from src.core.database import search_chunks

        # Main search
        results = self.search(query, model=model, date_from=date_from,
                              source_type=source_type, limit=limit)

        # Multi-source supplement
        existing_sources = {r.get("source_type", "mail") for r in results}
        existing_filenames = {r["filename"] for r in results}
        supplement_results = []

        supplement_types = ["log", "trd", "report"]
        if source_type and source_type not in supplement_types:
            supplement_types.append(source_type)

        for stype in supplement_types:
            if stype not in existing_sources:
                extra = self._search_single_source(
                    query, model=model, date_from=date_from,
                    source_type=stype, limit=3
                )
                for r in extra:
                    if r["filename"] not in existing_filenames:
                        supplement_results.append(r)
                        existing_filenames.add(r["filename"])

        # Merge: reserve up to 5 slots for supplement
        max_supplement = min(len(supplement_results), 5)
        max_general = limit - max_supplement
        return results[:max_general] + supplement_results[:max_supplement]

    def _vector_search(self, query_vec, model=None, date_from=None,
                       source_type=None, limit=30) -> list:
        """KNN search on sqlite-vec with metadata filtering."""
        from src.core.database import search_vec_chunks
        return search_vec_chunks(
            query_vec, model=model, date_from=date_from,
            source_type=source_type, limit=limit
        )

    def _search_single_source(self, query, model=None, date_from=None,
                              source_type=None, limit=3) -> list:
        """Search a specific source type using hybrid or BM25."""
        if self.embedding_available:
            return self.search(query, model=model, date_from=date_from,
                              source_type=source_type, limit=limit)
        else:
            from src.core.database import search_chunks
            return search_chunks(query, model=model, date_from=date_from,
                                source_type=source_type, limit=limit)

    def _rrf_merge(self, bm25_results, vec_results, k=60) -> list:
        """Reciprocal Rank Fusion: score = sum(weight_i / (k + rank_i)).
        
        Combines rankings from BM25 and vector search into a unified ranking.
        Documents appearing in both lists get boosted scores.
        
        Args:
            bm25_results: Results from BM25 search (ordered by BM25 rank).
            vec_results: Results from vector search (ordered by distance).
            k: RRF constant (default 60, standard value from literature).
            
        Returns:
            Merged results sorted by fused score (descending).
        """
        # Use filename + first 80 chars of chunk_text as dedup key
        def _key(r):
            return f"{r['filename']}::{r['chunk_text'][:80]}"

        scores = {}
        data = {}

        # Score from BM25
        for rank, r in enumerate(bm25_results):
            key = _key(r)
            scores[key] = scores.get(key, 0) + self.bm25_weight / (k + rank + 1)
            if key not in data:
                data[key] = r

        # Score from Vector
        for rank, r in enumerate(vec_results):
            key = _key(r)
            scores[key] = scores.get(key, 0) + self.vec_weight / (k + rank + 1)
            if key not in data:
                data[key] = r

        # Sort by fused score descending
        sorted_keys = sorted(scores.keys(), key=lambda k: scores[k], reverse=True)

        results = []
        for key in sorted_keys:
            item = data[key].copy()
            item["score"] = scores[key]
            # Ensure snippet exists
            if "snippet" not in item:
                item["snippet"] = item.get("chunk_text", "")[:200]
            results.append(item)

        return results
