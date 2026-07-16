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
    """Run pipeline on startup and schedule hourly sync."""
    run_pipeline()
    asyncio.create_task(_hourly_sync())


async def _hourly_sync():
    while True:
        await asyncio.sleep(3600)
        run_pipeline()


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


@app.get("/api/models")
def list_models():
    return {"models": get_all_models()}


@app.get("/api/search")
def search(q: str = Query(..., min_length=1), model: Optional[str] = None, date_from: Optional[str] = None):
    results = search_chunks(q, model=model, date_from=date_from, limit=10)
    return {"results": [{"filename": r["filename"], "snippet": r["snippet"], "model": r["model"], "date_str": r["date_str"]} for r in results]}


@app.post("/api/ask")
def ask(req: QARequest):
    results = search_chunks(req.question, model=req.model, date_from=req.date_from, limit=5)

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
    count = run_pipeline()
    return {"status": "success", "processed_files": count}


NOTES_DIR = os.path.join(PROJECT_ROOT, "knowledge", "notes")
ATTACHMENTS_DIR = os.path.join(PROJECT_ROOT, "knowledge", "notes", "attachments")
os.makedirs(ATTACHMENTS_DIR, exist_ok=True)
app.mount("/attachments", StaticFiles(directory=ATTACHMENTS_DIR), name="attachments")


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
    uvicorn.run(app, host="0.0.0.0", port=8010)
