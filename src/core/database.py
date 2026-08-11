import sqlite3
import os

# Define absolute path to database
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(PROJECT_ROOT, "knowledge", "index.db")

def get_connection():
    """Returns a connection to the SQLite database with WAL mode for concurrent access."""
    conn = sqlite3.connect(DB_PATH, timeout=60)
    conn.execute("PRAGMA journal_mode=WAL")
    return conn

def init_db():
    """Initializes the FTS5 virtual table for document search."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
    CREATE VIRTUAL TABLE IF NOT EXISTS docs USING fts5(
        filename,
        content
    )
    """)
    conn.commit()
    conn.close()

def clear_db():
    """Clears all records from the docs table."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM docs")
    conn.commit()
    conn.close()

def insert_doc(filename, content):
    """Inserts a new document into the database."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO docs (filename, content) VALUES (?, ?)", (filename, content))
    conn.commit()
    conn.close()

def search_docs(query, limit=5):
    """Searches the database using FTS5 and returns matching filenames."""
    conn = get_connection()
    c = conn.cursor()
    
    import re
    words = re.findall(r"[\u4e00-\u9fffA-Za-z0-9\.]+", query)
    
    if not words:
        clean_query = query.replace("'", "''") 
    else:
        clean_query = " OR ".join([f"{w}*" for w in words])
    
    sql = "SELECT filename FROM docs WHERE docs MATCH ? LIMIT ?"
    try:
        c.execute(sql, (clean_query, limit))
        results = [row[0] for row in c.fetchall()]
    except sqlite3.OperationalError:
        results = []
    
    conn.close()
    return results


# --- Chunks table for paragraph-level QA ---

def init_chunks_db():
    """Creates the chunks FTS5 table for paragraph-level search."""
    conn = get_connection()
    c = conn.cursor()
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
    conn.close()

def clear_chunks():
    """Drops and recreates the chunks table to handle schema changes."""
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("DROP TABLE IF EXISTS chunks")
    except sqlite3.OperationalError:
        pass
    conn.commit()
    conn.close()

def insert_chunk(filename, chunk_text, model, date_str, source_type="mail"):
    """Inserts a chunk into the chunks FTS5 table."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO chunks (filename, chunk_text, model, date_str, source_type) VALUES (?, ?, ?, ?, ?)",
              (filename, chunk_text, model, date_str, source_type))
    conn.commit()
    conn.close()

def search_chunks(query, model=None, date_from=None, source_type=None, limit=5):
    """Searches chunks with BM25 ranking, optional model/date/source_type filters. Returns [{filename, snippet, chunk_text, model, date_str}]."""
    import re
    conn = get_connection()
    c = conn.cursor()

    words = re.findall(r"[\u4e00-\u9fffA-Za-z0-9\.]+", query)
    if not words:
        conn.close()
        return []
    clean_query = " OR ".join([f"{w}*" for w in words])

    sql = "SELECT filename, snippet(chunks, 1, '<b>', '</b>', '...', 30), chunk_text, model, date_str, source_type FROM chunks WHERE chunks MATCH ?"
    params = [clean_query]

    # If source_type specified, add it to the FTS5 query for efficient filtering
    if source_type:
        clean_query = f"({clean_query}) AND source_type:{source_type}"
        params = [clean_query]

    # Apply filters via subquery on rowid since FTS5 content columns aren't directly filterable with AND
    # We filter post-query instead
    sql += " ORDER BY rank LIMIT ?"
    params.append(limit * 10)  # fetch more to allow post-filter

    try:
        c.execute(sql, params)
        rows = c.fetchall()
    except sqlite3.OperationalError:
        rows = []

    conn.close()

    results = []
    for filename, snippet, chunk_text, m, d, src in rows:
        if model and model.upper() not in (m or "").upper():
            continue
        if date_from and (d or "") < date_from:
            continue
        if source_type and (src or "mail") != source_type:
            continue
        results.append({"filename": filename, "snippet": snippet, "chunk_text": chunk_text, "model": m, "date_str": d, "source_type": src or "mail"})
        if len(results) >= limit:
            break
    return results

def get_all_models():
    """Returns distinct model values from chunks table."""
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("SELECT DISTINCT model FROM chunks WHERE model != ''")
        models = set()
        for row in c.fetchall():
            for m in row[0].split(","):
                m = m.strip()
                if m:
                    models.add(m)
    except sqlite3.OperationalError:
        models = set()
    conn.close()
    return sorted(models)


# --- Notes table ---

def init_notes_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def insert_note(title, content):
    from datetime import datetime
    conn = get_connection()
    c = conn.cursor()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO notes (title, content, created_at) VALUES (?, ?, ?)", (title, content, created_at))
    note_id = c.lastrowid
    conn.commit()
    conn.close()
    return {"id": note_id, "title": title, "content": content, "created_at": created_at}

def get_all_notes():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, title, content, created_at FROM notes ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return [{"id": r[0], "title": r[1], "content": r[2], "created_at": r[3]} for r in rows]

def delete_note(note_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()

def update_note(note_id, title, content):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE notes SET title = ?, content = ? WHERE id = ?", (title, content, note_id))
    conn.commit()
    conn.close()


# --- Vector embedding tables (sqlite-vec) ---

def get_vec_connection():
    """Returns a connection with sqlite-vec extension loaded."""
    import sqlite_vec
    conn = sqlite3.connect(DB_PATH, timeout=60)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.enable_load_extension(True)
    sqlite_vec.load(conn)
    conn.enable_load_extension(False)
    return conn


def init_vec_db(dimension=1024):
    """Creates the vec_chunks virtual table and chunk_meta table."""
    conn = get_vec_connection()
    c = conn.cursor()
    c.execute(f"""
    CREATE VIRTUAL TABLE IF NOT EXISTS vec_chunks USING vec0(
        embedding float[{dimension}]
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS chunk_meta (
        id INTEGER PRIMARY KEY,
        filename TEXT NOT NULL,
        chunk_text TEXT NOT NULL,
        model TEXT DEFAULT '',
        date_str TEXT DEFAULT '',
        source_type TEXT DEFAULT 'mail'
    )
    """)
    c.execute("CREATE INDEX IF NOT EXISTS idx_chunk_meta_model ON chunk_meta(model)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_chunk_meta_source ON chunk_meta(source_type)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_chunk_meta_date ON chunk_meta(date_str)")
    conn.commit()
    conn.close()


def clear_vec_chunks():
    """Drops and recreates vec_chunks and chunk_meta tables."""
    conn = get_vec_connection()
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS vec_chunks")
    c.execute("DROP TABLE IF EXISTS chunk_meta")
    conn.commit()
    conn.close()


def insert_vec_chunk(chunk_id, filename, chunk_text, model, date_str, source_type, embedding):
    """Inserts a chunk with its embedding vector.
    
    Args:
        chunk_id: Integer ID (rowid for vec_chunks).
        filename: Source filename.
        chunk_text: The chunk content.
        model: Product model extracted from chunk.
        date_str: Date string (YYYY-MM-DD).
        source_type: Source type (mail/trd/log/note/image/report).
        embedding: numpy array or list of floats (dimension,).
    """
    import struct
    conn = get_vec_connection()
    c = conn.cursor()
    # Insert metadata
    c.execute("""
    INSERT OR REPLACE INTO chunk_meta (id, filename, chunk_text, model, date_str, source_type)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (chunk_id, filename, chunk_text, model, date_str, source_type))
    # Insert vector
    vec_bytes = struct.pack(f"{len(embedding)}f", *embedding)
    c.execute("INSERT OR REPLACE INTO vec_chunks (rowid, embedding) VALUES (?, ?)",
              (chunk_id, vec_bytes))
    conn.commit()
    conn.close()


def insert_vec_chunks_batch(chunks_data):
    """Batch insert chunks with embeddings.
    
    Args:
        chunks_data: list of dicts with keys:
            id, filename, chunk_text, model, date_str, source_type, embedding
    """
    import struct
    if not chunks_data:
        return
    conn = get_vec_connection()
    c = conn.cursor()
    meta_batch = []
    vec_batch = []
    for chunk in chunks_data:
        meta_batch.append((
            chunk["id"], chunk["filename"], chunk["chunk_text"],
            chunk["model"], chunk["date_str"], chunk["source_type"]
        ))
        vec_bytes = struct.pack(f"{len(chunk['embedding'])}f", *chunk["embedding"])
        vec_batch.append((chunk["id"], vec_bytes))
    c.executemany("""
    INSERT OR REPLACE INTO chunk_meta (id, filename, chunk_text, model, date_str, source_type)
    VALUES (?, ?, ?, ?, ?, ?)
    """, meta_batch)
    c.executemany("INSERT OR REPLACE INTO vec_chunks (rowid, embedding) VALUES (?, ?)", vec_batch)
    conn.commit()
    conn.close()


def search_vec_chunks(query_embedding, model=None, date_from=None, source_type=None, limit=15):
    """KNN vector search with optional metadata filtering.
    
    Args:
        query_embedding: numpy array or list of floats (dimension,).
        model: Optional model filter.
        date_from: Optional date_str lower bound (YYYY-MM-DD).
        source_type: Optional source type filter.
        limit: Max results to return.
        
    Returns:
        List of dicts: {filename, chunk_text, model, date_str, source_type, distance}
    """
    import struct
    conn = get_vec_connection()
    c = conn.cursor()

    vec_bytes = struct.pack(f"{len(query_embedding)}f", *query_embedding)

    # Fetch more candidates than needed to allow post-filtering
    fetch_limit = limit * 5 if (model or date_from or source_type) else limit

    try:
        c.execute("""
        SELECT v.rowid, v.distance
        FROM vec_chunks v
        WHERE v.embedding MATCH ?
        ORDER BY v.distance
        LIMIT ?
        """, (vec_bytes, fetch_limit))
        knn_results = c.fetchall()
    except sqlite3.OperationalError:
        conn.close()
        return []

    if not knn_results:
        conn.close()
        return []

    # Fetch metadata for matched rowids
    rowids = [r[0] for r in knn_results]
    distances = {r[0]: r[1] for r in knn_results}

    placeholders = ",".join("?" * len(rowids))
    c.execute(f"""
    SELECT id, filename, chunk_text, model, date_str, source_type
    FROM chunk_meta
    WHERE id IN ({placeholders})
    """, rowids)
    meta_rows = c.fetchall()
    conn.close()

    # Build results with filtering
    results = []
    for row in meta_rows:
        rid, fname, text, m, d, src = row
        # Apply filters
        if model and model.upper() not in (m or "").upper():
            continue
        if date_from and (d or "") < date_from:
            continue
        if source_type and (src or "mail") != source_type:
            continue
        results.append({
            "filename": fname,
            "chunk_text": text,
            "model": m,
            "date_str": d,
            "source_type": src or "mail",
            "distance": distances.get(rid, 999),
            "snippet": text[:200],
        })

    # Sort by distance (closest first) and limit
    results.sort(key=lambda x: x["distance"])
    return results[:limit]


def get_vec_chunk_count():
    """Returns the number of vectors in vec_chunks table."""
    try:
        conn = get_vec_connection()
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM chunk_meta")
        count = c.fetchone()[0]
        conn.close()
        return count
    except (sqlite3.OperationalError, Exception):
        return 0
