import os
import sys

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.core.parser import MsgParser, extract_chunks, parse_docx, parse_cap_txt, extract_project_version
from src.core.database import init_db, clear_db, insert_doc, get_connection, init_chunks_db, clear_chunks, insert_chunk

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INPUT_DIR = os.path.join(PROJECT_ROOT, "knowledge/raw_msg")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "knowledge/md")
TRD_DIR = os.path.join(PROJECT_ROOT, "knowledge/TRD")
LOG_DIR = os.path.join(PROJECT_ROOT, "knowledge/ProductLogFiles")

def run_pipeline(force_reindex=False):
    """Runs the full pipeline: MSG -> MD -> SQLite."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    init_db()
    
    if force_reindex:
        clear_db()

    # Step 1: Convert any new .msg files to .md
    files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".msg")]
    print(f"🔍 Found {len(files)} msg files")

    processed_count = 0
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

    # Step 2: Ensure all existing .md files are indexed in DB
    indexed = _reindex_existing(force_reindex)
    print(f"📄 Indexed {indexed} existing md files into DB")

    # Step 3: Rebuild chunk index for QA
    chunk_count = _rebuild_chunks()
    print(f"🔍 Built {chunk_count} chunks for QA search")
    
    return processed_count


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

def _rebuild_chunks():
    """Rebuilds the chunks FTS5 index from all sources."""
    clear_chunks()
    init_chunks_db()
    count = 0

    # Index mail .md files
    for f in os.listdir(OUTPUT_DIR):
        if not f.endswith(".md"):
            continue
        path = os.path.join(OUTPUT_DIR, f)
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()
        result = extract_chunks(content, f)
        for chunk in result["chunks"]:
            insert_chunk(f, chunk, result["model"], result["date_str"], "mail")
            count += 1

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
                    insert_chunk(f, chunk, model, date_str, "trd")
                    count += 1
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
                    insert_chunk(f, chunk, model, date_str, "log")
                    count += 1
            except Exception as e:
                print(f"❌ Log failed {f}: {e}")

    # Index notes from DB
    from src.core.database import init_notes_db, get_all_notes
    init_notes_db()
    for n in get_all_notes():
        insert_chunk(f"note_{n['id']}.md", n["content"], "", n["created_at"][:10], "note")
        count += 1

    return count


def _file_date(path):
    """取得檔案修改日期 YYYY-MM-DD。"""
    from datetime import datetime
    ts = os.path.getmtime(path)
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d")


if __name__ == "__main__":
    run_pipeline(force_reindex=True)
