import sqlite3
import os

# Define absolute path to database
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(PROJECT_ROOT, "knowledge", "index.db")

def get_connection():
    """Returns a connection to the SQLite database."""
    return sqlite3.connect(DB_PATH)

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

def search_chunks(query, model=None, date_from=None, limit=5):
    """Searches chunks with BM25 ranking, optional model/date filters. Returns [{filename, snippet, chunk_text, model, date_str}]."""
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

    # Apply filters via subquery on rowid since FTS5 content columns aren't directly filterable with AND
    # We filter post-query instead
    sql += " ORDER BY rank LIMIT ?"
    params.append(limit * 5)  # fetch more to allow post-filter

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
