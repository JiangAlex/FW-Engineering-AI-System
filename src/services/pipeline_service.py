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

    # Step 3: Rebuild chunk index for QA
    chunk_count = _rebuild_chunks(force=force_reindex or processed_count > 0)
    print(f"🔍 Built {chunk_count} chunks for QA search")
    
    return {
        "found": len(files),
        "processed": processed_count,
        "failed": failed_files,
        "indexed": indexed,
        "chunks": chunk_count,
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
