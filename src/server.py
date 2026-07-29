import os
import sys
import re

# Add project root to sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

from fastapi import FastAPI, Query, File, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List

from src.core.database import search_docs, search_chunks, get_all_models, init_notes_db, insert_note, get_all_notes, delete_note, update_note
from src.core.ai_client import AIClient
from src.services.fw_service import FWService
from src.services.report_service import ReportService
from src.services.pipeline_service import run_pipeline

import asyncio

app = FastAPI(title="FW Engineering AI System API")
ai_client = AIClient()
conversation_history: list[dict] = []
MAX_HISTORY = 5


@app.on_event("startup")
async def startup_sync():
    """Run pipeline on startup in background and schedule hourly sync."""
    import threading
    def _run_pipeline_safe():
        try:
            run_pipeline()
        except Exception as e:
            print(f"❌ Pipeline startup error: {e}")
    t = threading.Thread(target=_run_pipeline_safe, daemon=True)
    t.start()
    asyncio.create_task(_hourly_sync())


async def _hourly_sync():
    while True:
        await asyncio.sleep(3600)
        import threading
        def _run():
            try:
                run_pipeline()
            except Exception as e:
                print(f"❌ Pipeline hourly error: {e}")
        t = threading.Thread(target=_run, daemon=True)
        t.start()


class QARequest(BaseModel):
    question: str
    model: Optional[str] = None
    date_from: Optional[str] = None


class NoteRequest(BaseModel):
    title: str
    content: str


@app.get("/")
def read_root():
    template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")
    return FileResponse(template_path)

@app.get("/favicon.ico")
def favicon():
    favicon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "favicon.ico")
    return FileResponse(favicon_path, media_type="image/x-icon")


@app.get("/api/models")
def list_models():
    return {"models": get_all_models()}


@app.get("/api/search")
def search(q: str = Query(..., min_length=1), model: Optional[str] = None, date_from: Optional[str] = None):
    results = search_chunks(q, model=model, date_from=date_from, limit=10)
    return {"results": [{"filename": r["filename"], "snippet": r["snippet"], "model": r["model"], "date_str": r["date_str"]} for r in results]}


@app.post("/api/ask")
def ask(req: QARequest):
    # Detect source type hints in question
    q_lower = req.question.lower()
    source_hint = None
    if any(kw in q_lower for kw in ["logfile", "log file", "產測", "cap", "test log"]):
        source_hint = "log"
    elif any(kw in q_lower for kw in ["trd", "測試需求"]):
        source_hint = "trd"
    elif any(kw in q_lower for kw in ["image", "firmware image", "binary", "fw image"]):
        source_hint = "image"

    # Search with mixed sources: general + source-specific
    results = search_chunks(req.question, model=req.model, date_from=req.date_from, limit=5)

    if source_hint:
        # Auto-detect model from question for typed search
        import re as _re
        from src.core.parser import _normalize_model
        detected_model = req.model
        if not detected_model:
            # Use looser regex that works with CJK characters
            m = _re.search(r'(EAP\d{3}[a-zA-Z]?|OAP\d{3}|ECS\d{4}[a-zA-Z]?|JWS\d{4}[A-Z]?|JioWave\d+|SW\d{4}[A-Z]?)', req.question, _re.IGNORECASE)
            if m:
                detected_model = _normalize_model(m.group(0))
        # Also search specifically in the hinted source type
        typed_results = search_chunks(req.question, model=detected_model, date_from=req.date_from, source_type=source_hint, limit=3)
        # Merge: add typed results not already in general results
        existing_filenames = {r["filename"] for r in results}
        for r in typed_results:
            if r["filename"] not in existing_filenames:
                results.append(r)
        # Cap at 8
        results = results[:8]

    if not results:
        return {"answer": "❌ 資料中無相關記錄。", "sources": []}

    sources = [{"filename": r["filename"], "snippet": r["snippet"], "date_str": r["date_str"], "source_type": r.get("source_type", "mail")} for r in results]
    chunks_text = "\n\n---\n".join([f"[{r['filename']}]\n{r['chunk_text']}" for r in results])

    prompt = f"""你是一位工程知識助理，請嚴格根據以下 mail 記錄回答問題。若資料中找不到答案，請回答「資料中無相關記錄」。

【資料】
{chunks_text}

【問題】
{req.question}

要求：繁體中文回答，條列重點，最後一句總結。"""

    answer = ai_client.ask(prompt, history=conversation_history)
    if answer.startswith("⚠️") or answer.startswith("❌"):
        # Fallback: organize matched chunks into bullet points
        answer = _fallback_answer(results, req.question)
    else:
        conversation_history.append({"role": "user", "content": req.question})
        conversation_history.append({"role": "assistant", "content": answer})
        while len(conversation_history) > MAX_HISTORY * 2:
            conversation_history.pop(0)

    return {"answer": answer, "sources": sources}


def _fallback_answer(results, question):
    """Fallback: extract key lines from chunks containing query keywords."""
    import re
    words = re.findall(r"[\u4e00-\u9fffA-Za-z0-9]+", question)
    sections = []
    for r in results:
        lines = r["chunk_text"].split("\n")
        key_lines = [l.strip() for l in lines if l.strip() and any(w.lower() in l.lower() for w in words)][:3]
        if key_lines:
            sections.append(f"📎 {r['filename']} ({r['date_str']})\n" + "\n".join(f"  • {l}" for l in key_lines))
    if not sections:
        sections = [f"📎 {r['filename']} ({r['date_str']})\n  • {r['snippet']}" for r in results[:3]]
    return "⚠️ Fallback Mode (No AI)\n\n" + "\n\n".join(sections)


class AdoptRequest(BaseModel):
    question: str
    answer: str


@app.post("/api/ask/adopt")
def adopt_answer(req: AdoptRequest):
    """採納 AI 回答：將 Q&A 存為 note，供未來搜尋使用。"""
    from datetime import datetime
    init_notes_db()
    title = f"✅ 採納: {req.question[:40]}"
    content = f"## 問題\n{req.question}\n\n## 回答\n{req.answer}"
    note = insert_note(title, content)
    # 即時寫入 chunks
    from src.core.database import init_chunks_db, insert_chunk
    init_chunks_db()
    insert_chunk(f"note_{note['id']}.md", content, "", note["created_at"][:10], "note")
    return {"status": "adopted", "note_id": note["id"]}


@app.get("/api/fw/summary")
def get_fw_summary():
    return FWService.get_fw_summary()

@app.get("/api/fw/compare")
def compare_fw(model: str, v1: str, v2: str):
    return {"comparison": FWService.compare_versions(model, v1, v2, ai_client)}

@app.get("/api/report/generate")
def generate_report():
    report, filename = ReportService.generate_weekly_report(ai_client)
    return {"report": report, "filename": filename}

@app.get("/api/pipeline/sync")
def sync_data():
    result = run_pipeline()
    if result["failed"] and result["processed"] == 0 and result["found"] > 0:
        status = "failed"
    elif result["failed"]:
        status = "partial"
    elif result["found"] == 0:
        status = "no_new_files"
    else:
        status = "success"
    return {
        "status": status,
        "found": result["found"],
        "processed": result["processed"],
        "failed": result["failed"],
        "indexed": result["indexed"],
        "chunks": result["chunks"],
    }


NOTES_DIR = os.path.join(PROJECT_ROOT, "knowledge", "notes")
ATTACHMENTS_DIR = os.path.join(PROJECT_ROOT, "knowledge", "notes", "attachments")
os.makedirs(ATTACHMENTS_DIR, exist_ok=True)
app.mount("/attachments", StaticFiles(directory=ATTACHMENTS_DIR), name="attachments")

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
app.mount("/static", StaticFiles(directory=TEMPLATES_DIR), name="static")


@app.get("/api/notes")
def list_notes():
    init_notes_db()
    return {"notes": get_all_notes()}


@app.post("/api/notes")
def create_note(title: str = Form(...), content: str = Form(...), files: List[UploadFile] = File(default=[])):
    init_notes_db()
    # 儲存附檔
    attachments = []
    for f in files:
        if f.filename:
            safe_name = re.sub(r'[\\/:*?"<>|]', '_', f.filename)
            save_path = os.path.join(ATTACHMENTS_DIR, safe_name)
            with open(save_path, "wb") as out:
                out.write(f.file.read())
            attachments.append(safe_name)
    # 附檔名加入 content
    full_content = content
    if attachments:
        full_content += "\n\n附件: " + ", ".join(attachments)
    note = insert_note(title, full_content)
    # 同步寫入 .md
    os.makedirs(NOTES_DIR, exist_ok=True)
    safe_title = re.sub(r'[\\/:*?"<>|]', '_', title)[:40]
    md_path = os.path.join(NOTES_DIR, f"{note['id']}_{safe_title}.md")
    with open(md_path, "w", encoding="utf-8") as out:
        out.write(f"# {title}\n\n{full_content}\n")
    # 加入 chunks 索引
    from src.core.database import init_chunks_db, insert_chunk
    init_chunks_db()
    insert_chunk(f"note_{note['id']}.md", full_content, "", note["created_at"][:10], "note")
    return note


@app.put("/api/notes/{note_id}")
def edit_note(note_id: int, title: str = Form(...), content: str = Form(...), files: List[UploadFile] = File(default=[])):
    init_notes_db()
    # 儲存新附檔
    attachments = []
    for f in files:
        if f.filename:
            safe_name = re.sub(r'[\\/:*?"<>|]', '_', f.filename)
            save_path = os.path.join(ATTACHMENTS_DIR, safe_name)
            with open(save_path, "wb") as out:
                out.write(f.file.read())
            attachments.append(safe_name)
    full_content = content
    if attachments:
        full_content += "\n\n附件: " + ", ".join(attachments)
    update_note(note_id, title, full_content)
    # 更新 .md
    import glob
    for f in glob.glob(os.path.join(NOTES_DIR, f"{note_id}_*")):
        os.remove(f)
    os.makedirs(NOTES_DIR, exist_ok=True)
    safe_title = re.sub(r'[\\/:*?"<>|]', '_', title)[:40]
    with open(os.path.join(NOTES_DIR, f"{note_id}_{safe_title}.md"), "w", encoding="utf-8") as out:
        out.write(f"# {title}\n\n{full_content}\n")
    # 同步 GUIDE.md（如果是 GUIDE 筆記）
    if "GUIDE" in title:
        guide_path = os.path.join(PROJECT_ROOT, "knowledge", "GUIDE.md")
        with open(guide_path, "w", encoding="utf-8") as out:
            out.write(full_content)
    # 更新 chunks
    from src.core.database import get_connection, insert_chunk, init_chunks_db
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("DELETE FROM chunks WHERE filename = ?", (f"note_{note_id}.md",))
    except Exception:
        pass
    conn.commit()
    conn.close()
    init_chunks_db()
    insert_chunk(f"note_{note_id}.md", full_content, "", "", "note")
    return {"status": "updated"}


@app.delete("/api/notes/{note_id}")
def remove_note(note_id: int):
    init_notes_db()
    # 檢查是否為 GUIDE 筆記（不可刪除）
    from src.core.database import get_all_notes
    notes = get_all_notes()
    for n in notes:
        if n["id"] == note_id and "GUIDE" in n["title"]:
            raise HTTPException(status_code=403, detail="GUIDE 筆記不可刪除")
    # 刪除對應 .md
    import glob
    for f in glob.glob(os.path.join(NOTES_DIR, f"{note_id}_*")):
        os.remove(f)
    delete_note(note_id)
    # 刪除 chunks 中對應記錄
    from src.core.database import get_connection
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("DELETE FROM chunks WHERE filename = ?", (f"note_{note_id}.md",))
    except Exception:
        pass
    conn.commit()
    conn.close()
    return {"status": "deleted"}

@app.get("/api/download/{filename}")
def download_file(filename: str):
    paths = [
        os.path.join(PROJECT_ROOT, "knowledge/report", filename),
        os.path.join(PROJECT_ROOT, "knowledge/output", filename)
    ]
    for path in paths:
        if os.path.exists(path):
            return FileResponse(path, filename=filename)
    raise HTTPException(status_code=404, detail="File not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8010, timeout_graceful_shutdown=3)
