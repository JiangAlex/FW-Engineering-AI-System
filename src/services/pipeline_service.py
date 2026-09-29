import os
import sys
import sqlite3

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.core.parser import MsgParser, extract_chunks, parse_docx, parse_cap_txt, extract_project_version
from src.core.database import init_db, clear_db, insert_doc, get_connection, init_chunks_db, clear_chunks, insert_chunk

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INPUT_DIR = os.path.join(PROJECT_ROOT, "knowledge/raw_msg")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "knowledge/md")
TRD_DIR = os.path.join(PROJECT_ROOT, "knowledge/TRD")
LOG_DIR = os.path.join(PROJECT_ROOT, "knowledge/ProductLogFiles")
IMAGE_DIR = os.path.join(PROJECT_ROOT, "knowledge/image")
REPORT_DIR = os.path.join(PROJECT_ROOT, "knowledge/report")

def run_pipeline(force_reindex=False):
    """Runs the full pipeline: MSG -> MD -> SQLite.
    Returns dict with {processed, failed, found, indexed, chunks} counts.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    init_db()
    
    if force_reindex:
        clear_db()

    # Step 1: Convert any new .msg files to .md
    files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".msg")]
    print(f"🔍 Found {len(files)} msg files")

    processed_count = 0
    failed_files = []
    for f in files:
        msg_path = os.path.join(INPUT_DIR, f)
        md_filename = f.replace(".msg", ".md")
        out_path = os.path.join(OUTPUT_DIR, md_filename)
        
        if os.path.exists(out_path) and not force_reindex:
            if os.path.getmtime(msg_path) <= os.path.getmtime(out_path):
                os.remove(msg_path)
                continue

        try:
            filename, content = MsgParser.msg_to_md(msg_path)
            with open(out_path, "w", encoding="utf-8") as file:
                file.write(content)
            
            insert_doc(filename, content)
            os.remove(msg_path)
            print(f"✅ Processed: {f}")
            processed_count += 1
        except Exception as e:
            print(f"❌ Failed {f}: {e}")
            failed_files.append({"file": f, "error": str(e)})

    # Step 2: Ensure all existing .md files are indexed in DB
    indexed = _reindex_existing(force_reindex)
    print(f"📄 Indexed {indexed} existing md files into DB")

    # Step 3: Rebuild chunk index for QA.
    # Do NOT force here just because files were processed: _rebuild_chunks
    # already detects source changes via fingerprint and rebuilds when needed.
    # (force is reserved for an explicit full reindex.)
    chunk_count = _rebuild_chunks(force=force_reindex)
    print(f"🔍 Built {chunk_count} chunks for QA search")

    # Step 4: Rebuild embedding index for vector search.
    # Likewise incremental: _rebuild_embeddings uses content-hash diffing to
    # encode only new chunks and drop stale ones. Forcing on processed_count>0
    # caused a full re-encode every sync AND wiped the vector store first
    # (clear_vec_chunks), leaving chunk_meta at 0 whenever the long CPU encode
    # was interrupted by a restart/next sync. See Redmine #66.
    embedding_count = _rebuild_embeddings(force=force_reindex)
    print(f"🧠 Built {embedding_count} embeddings for vector search")
    
    return {
        "found": len(files),
        "processed": processed_count,
        "failed": failed_files,
        "indexed": indexed,
        "chunks": chunk_count,
        "embeddings": embedding_count,
    }


def _reindex_existing(force=False):
    """Indexes any .md files not yet in the database."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT filename FROM docs")
    existing = {row[0] for row in c.fetchall()}
    conn.close()

    count = 0
    for f in os.listdir(OUTPUT_DIR):
        if not f.endswith(".md"):
            continue
        if f in existing and not force:
            continue
        path = os.path.join(OUTPUT_DIR, f)
        with open(path, "r", encoding="utf-8") as file:
            insert_doc(f, file.read())
        count += 1
    return count

def _rebuild_chunks(force=False):
    """Rebuilds the chunks FTS5 index from all sources. Skips if no changes detected."""
    from src.core.database import get_connection

    # Check if rebuild is needed by comparing source file fingerprint
    if not force:
        try:
            current_fingerprint = _compute_source_fingerprint()
            fingerprint_path = os.path.join(PROJECT_ROOT, "knowledge", ".chunks_fingerprint")
            if os.path.exists(fingerprint_path):
                with open(fingerprint_path, "r") as f:
                    saved_fingerprint = f.read().strip()
                if saved_fingerprint == current_fingerprint:
                    conn = get_connection()
                    c = conn.cursor()
                    c.execute("SELECT COUNT(*) FROM chunks")
                    existing_count = c.fetchone()[0]
                    conn.close()
                    if existing_count > 0:
                        print(f"⏭️ Chunks up-to-date (fingerprint match, {existing_count} chunks), skipping rebuild")
                        return existing_count
        except (sqlite3.OperationalError, OSError):
            pass  # Table doesn't exist or fingerprint file issue, proceed with rebuild

    # Drop and recreate in a single connection to avoid race conditions
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("DROP TABLE IF EXISTS chunks")
    except sqlite3.OperationalError:
        pass
    c.execute("""
    CREATE VIRTUAL TABLE IF NOT EXISTS chunks USING fts5(
        filename,
        chunk_text,
        model,
        date_str,
        source_type
    )
    """)
    conn.commit()

    count = 0
    batch = []
    BATCH_SIZE = 200

    def flush_batch():
        nonlocal batch
        if batch:
            c.executemany("INSERT INTO chunks (filename, chunk_text, model, date_str, source_type) VALUES (?, ?, ?, ?, ?)", batch)
            conn.commit()
            batch = []

    # Index mail .md files
    for f in os.listdir(OUTPUT_DIR):
        if not f.endswith(".md"):
            continue
        path = os.path.join(OUTPUT_DIR, f)
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()
        result = extract_chunks(content, f)
        for chunk in result["chunks"]:
            batch.append((f, chunk, result["model"], result["date_str"], "mail"))
            count += 1
            if len(batch) >= BATCH_SIZE:
                flush_batch()

    # Index TRD .docx files
    if os.path.isdir(TRD_DIR):
        for f in os.listdir(TRD_DIR):
            if not f.endswith(".docx"):
                continue
            path = os.path.join(TRD_DIR, f)
            try:
                content = parse_docx(path)
                model, version = extract_project_version(f, content)
                date_str = _file_date(path)
                # Split into chunks
                lines = [l for l in content.split("\n") if l.strip()]
                for i in range(0, len(lines), 30):
                    chunk = "\n".join(lines[i:i+30])
                    batch.append((f, chunk, model, date_str, "trd"))
                    count += 1
                    if len(batch) >= BATCH_SIZE:
                        flush_batch()
            except Exception as e:
                print(f"❌ TRD failed {f}: {e}")

    # Index ProductLogFiles .cap/.txt
    if os.path.isdir(LOG_DIR):
        for f in os.listdir(LOG_DIR):
            if not f.endswith((".cap", ".txt")):
                continue
            path = os.path.join(LOG_DIR, f)
            try:
                content = parse_cap_txt(path)
                model, version = extract_project_version(f, content)
                date_str = _file_date(path)
                # Only index header section (first 50 lines) for logs
                lines = [l.strip() for l in content.split("\n") if l.strip()][:50]
                chunk = "\n".join(lines)
                if chunk:
                    batch.append((f, chunk, model, date_str, "log"))
                    count += 1
                    if len(batch) >= BATCH_SIZE:
                        flush_batch()
            except Exception as e:
                print(f"❌ Log failed {f}: {e}")

    # Index FW image filenames (binary files, index name only)
    if os.path.isdir(IMAGE_DIR):
        for f in os.listdir(IMAGE_DIR):
            if f.startswith("."):
                continue
            path = os.path.join(IMAGE_DIR, f)
            if not os.path.isfile(path):
                continue
            model, version = extract_project_version(f)
            date_str = _file_date(path)
            # Use filename as chunk text (contains model + version info)
            chunk_text = f"FW Image: {f}"
            if version:
                chunk_text += f"\nVersion: V{version}"
            if model:
                chunk_text += f"\nModel: {model}"
            batch.append((f, chunk_text, model, date_str, "image"))
            count += 1
            if len(batch) >= BATCH_SIZE:
                flush_batch()

    # Index weekly reports
    if os.path.isdir(REPORT_DIR):
        for f in os.listdir(REPORT_DIR):
            if not f.endswith(".md"):
                continue
            path = os.path.join(REPORT_DIR, f)
            try:
                with open(path, "r", encoding="utf-8") as file:
                    content = file.read()
                date_str = _file_date(path)
                # Split into chunks (30 lines each)
                lines = [l for l in content.split("\n") if l.strip()]
                for i in range(0, len(lines), 30):
                    chunk = "\n".join(lines[i:i+30])
                    batch.append((f, chunk, "", date_str, "report"))
                    count += 1
                    if len(batch) >= BATCH_SIZE:
                        flush_batch()
            except Exception as e:
                print(f"❌ Report failed {f}: {e}")

    # Index notes from DB
    from src.core.database import init_notes_db, get_all_notes
    init_notes_db()
    for n in get_all_notes():
        batch.append((f"note_{n['id']}.md", n["content"], "", n["created_at"][:10], "note"))
        count += 1

    # Final flush
    flush_batch()
    conn.close()

    # Save fingerprint so next run can skip rebuild if sources unchanged
    try:
        fingerprint_path = os.path.join(PROJECT_ROOT, "knowledge", ".chunks_fingerprint")
        with open(fingerprint_path, "w") as f:
            f.write(_compute_source_fingerprint())
    except OSError:
        pass

    return count


def _compute_source_fingerprint():
    """Computes a hash of all source filenames + modification times.
    Any file added, removed, or modified will change the fingerprint."""
    import hashlib
    entries = []

    # MD files
    if os.path.isdir(OUTPUT_DIR):
        for f in sorted(os.listdir(OUTPUT_DIR)):
            if f.endswith(".md"):
                path = os.path.join(OUTPUT_DIR, f)
                entries.append(f"{f}:{os.path.getmtime(path):.0f}")

    # TRD files
    if os.path.isdir(TRD_DIR):
        for f in sorted(os.listdir(TRD_DIR)):
            if f.endswith(".docx"):
                path = os.path.join(TRD_DIR, f)
                entries.append(f"{f}:{os.path.getmtime(path):.0f}")

    # Log files
    if os.path.isdir(LOG_DIR):
        for f in sorted(os.listdir(LOG_DIR)):
            if f.endswith((".cap", ".txt")):
                path = os.path.join(LOG_DIR, f)
                entries.append(f"{f}:{os.path.getmtime(path):.0f}")

    # Image files
    if os.path.isdir(IMAGE_DIR):
        for f in sorted(os.listdir(IMAGE_DIR)):
            if not f.startswith(".") and os.path.isfile(os.path.join(IMAGE_DIR, f)):
                path = os.path.join(IMAGE_DIR, f)
                entries.append(f"{f}:{os.path.getmtime(path):.0f}")

    # Report files
    if os.path.isdir(REPORT_DIR):
        for f in sorted(os.listdir(REPORT_DIR)):
            if f.endswith(".md"):
                path = os.path.join(REPORT_DIR, f)
                entries.append(f"{f}:{os.path.getmtime(path):.0f}")

    # Notes (use id + content hash)
    try:
        from src.core.database import init_notes_db, get_all_notes
        init_notes_db()
        for n in get_all_notes():
            entries.append(f"note_{n['id']}:{n['created_at']}")
    except Exception:
        pass

    fingerprint_str = "\n".join(entries)
    return hashlib.sha256(fingerprint_str.encode()).hexdigest()


def _file_date(path):
    """取得檔案修改日期 YYYY-MM-DD。"""
    from datetime import datetime
    ts = os.path.getmtime(path)
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d")


if __name__ == "__main__":
    run_pipeline(force_reindex=True)


def _rebuild_embeddings(force=False):
    """Builds vector embeddings for all chunks. Incremental by default.
    
    Reads chunks from the FTS5 chunks table (source of truth) and encodes them
    into vectors stored in vec_chunks (sqlite-vec).
    
    Gracefully skips if embedding model is unavailable (disabled, download failed, etc.)
    
    Returns:
        Number of embeddings in the index, or 0 if skipped.
    """
    from src.core.embedder import LocalEmbedder, EMBEDDING_ENABLED
    from src.core.database import (
        get_connection, init_vec_db, clear_vec_chunks,
        insert_vec_chunks_batch, get_vec_chunk_count,
        get_existing_chunk_hashes, get_max_chunk_meta_id,
        delete_vec_chunks_by_ids,
    )
    import hashlib

    if not EMBEDDING_ENABLED:
        print("⏭️ Embedding disabled (EMBEDDING_ENABLED=false), skipping")
        return 0

    # Check fingerprint to decide if rebuild is needed
    if not force:
        try:
            fingerprint_path = os.path.join(PROJECT_ROOT, "knowledge", ".embeddings_fingerprint")
            chunks_fingerprint_path = os.path.join(PROJECT_ROOT, "knowledge", ".chunks_fingerprint")
            if os.path.exists(fingerprint_path) and os.path.exists(chunks_fingerprint_path):
                with open(fingerprint_path, "r") as f:
                    saved_emb_fp = f.read().strip()
                with open(chunks_fingerprint_path, "r") as f:
                    current_chunks_fp = f.read().strip()
                # If chunks haven't changed since last embedding build, skip
                if saved_emb_fp == current_chunks_fp:
                    existing = get_vec_chunk_count()
                    if existing > 0:
                        print(f"⏭️ Embeddings up-to-date ({existing} vectors), skipping")
                        return existing
        except (OSError, Exception):
            pass

    # Try to load embedder (may fail if model not downloaded yet)
    embedder = LocalEmbedder.get_instance()
    if embedder is None or not embedder.is_ready:
        print("⚠️ Embedding model not available, skipping vector index build")
        return 0

    # Read all chunks from FTS5 table (source of truth)
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("SELECT rowid, filename, chunk_text, model, date_str, source_type FROM chunks")
        all_chunks = c.fetchall()
    except sqlite3.OperationalError:
        conn.close()
        print("⚠️ Chunks table not found, skipping embedding build")
        return 0
    conn.close()

    if not all_chunks:
        print("⚠️ No chunks to embed")
        return 0

    # Initialize vector tables
    init_vec_db(dimension=embedder.dimension)

    if force:
        clear_vec_chunks()
        init_vec_db(dimension=embedder.dimension)

    def _content_hash(filename, chunk_text, source_type):
        # Stable key independent of FTS5 rowid (which is reassigned on rebuild).
        h = hashlib.sha1()
        h.update((source_type or "").encode("utf-8"))
        h.update(b"\x00")
        h.update((filename or "").encode("utf-8"))
        h.update(b"\x00")
        h.update((chunk_text or "").encode("utf-8"))
        return h.hexdigest()

    # Compute content hash for every current chunk
    current = []  # list of (content_hash, row)
    current_hashes = set()
    for row in all_chunks:
        _, filename, chunk_text, _, _, source_type = row
        ch = _content_hash(filename, chunk_text, source_type)
        current.append((ch, row))
        current_hashes.add(ch)

    # Existing embedded chunks: {content_hash: id}
    existing = {} if force else get_existing_chunk_hashes()

    # Determine chunks to add (new hashes) and stale ids to remove
    to_encode = [(ch, row) for ch, row in current if ch not in existing]
    stale_ids = [cid for ch, cid in existing.items() if ch not in current_hashes]

    # Remove stale vectors (source content deleted/changed)
    if stale_ids:
        removed = delete_vec_chunks_by_ids(stale_ids)
        print(f"🗑️ Removed {removed} stale embeddings")

    if not to_encode:
        total = get_vec_chunk_count()
        print(f"⏭️ Embeddings incremental: 0 new chunks ({total} vectors total)")
        # Still refresh fingerprint so future runs can fast-skip
        _save_embeddings_fingerprint()
        return total

    mode = "full" if force else "incremental"
    print(f"🧠 Building embeddings for {len(to_encode)} chunks ({mode}, {len(all_chunks)} total)...")

    # Assign fresh ids above current max so they don't collide
    next_id = get_max_chunk_meta_id() + 1

    # Batch encode only the new chunk texts
    texts = [row[2] for _, row in to_encode]  # chunk_text column
    try:
        embeddings = embedder.encode(texts, show_progress=True)
    except Exception as e:
        print(f"❌ Embedding encode failed: {e}")
        return get_vec_chunk_count()

    # Batch insert into vec_chunks + chunk_meta
    BATCH_SIZE = 200
    count = 0
    for i in range(0, len(to_encode), BATCH_SIZE):
        batch = to_encode[i:i + BATCH_SIZE]
        batch_embeddings = embeddings[i:i + BATCH_SIZE]

        chunks_data = []
        for (ch, row), emb in zip(batch, batch_embeddings):
            _, filename, chunk_text, model, date_str, source_type = row
            chunks_data.append({
                "id": next_id,
                "filename": filename,
                "chunk_text": chunk_text,
                "model": model or "",
                "date_str": date_str or "",
                "source_type": source_type or "mail",
                "content_hash": ch,
                "embedding": emb.tolist(),
            })
            next_id += 1

        insert_vec_chunks_batch(chunks_data)
        count += len(chunks_data)

    # Save fingerprint (use chunks fingerprint as reference)
    _save_embeddings_fingerprint()

    total = get_vec_chunk_count()
    print(f"✅ Built {count} new embeddings (dim={embedder.dimension}, {total} vectors total)")
    return total


def _save_embeddings_fingerprint():
    """Copies the current chunks fingerprint into the embeddings fingerprint file."""
    try:
        chunks_fingerprint_path = os.path.join(PROJECT_ROOT, "knowledge", ".chunks_fingerprint")
        embeddings_fingerprint_path = os.path.join(PROJECT_ROOT, "knowledge", ".embeddings_fingerprint")
        if os.path.exists(chunks_fingerprint_path):
            with open(chunks_fingerprint_path, "r") as f:
                current_fp = f.read().strip()
            with open(embeddings_fingerprint_path, "w") as f:
                f.write(current_fp)
    except OSError:
        pass
