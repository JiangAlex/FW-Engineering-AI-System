import os
import re
import email.utils
import zipfile
import xml.etree.ElementTree as ET
import extract_msg
from bs4 import BeautifulSoup

MODEL_RE = re.compile(r"\b(EAP\d{3}[a-zA-Z]?\s?(?:\([A-Z]+\))?|ECS\d{4}[a-zA-Z]?|AP\d{4}|SW\d{4}[A-Z]?|JWS\d{4}[A-Z]?|JioWave\d+|MLTG[-\w]*|SC\d{2}[A-Z]?|Vnet\d{4}[A-Z]?)(?:\b|(?=[\s,;:).\-]|$))", re.IGNORECASE)
MODEL_ALIASES = {
    "EAP115A": "EAP115",
    "EAP115B": "EAP115",
    "JIOWAVE62420": "EAP111",
    "JWS62420": "EAP111",
    "EAP104L": "EAP104",
    "JWS2261": "JWS2261P",
}

def _normalize_model(name):
    """Normalize: apply alias, preserve parenthetical SKU like (TE), (T). Unify spacing."""
    n = name.strip().upper()
    # Unify spacing: "EAP104 (TE)" and "EAP104(TE)" → "EAP104(TE)"
    n = re.sub(r"\s+\(", "(", n)
    # Split base + suffix for alias lookup: EAP115A(TE) → base=EAP115A, suffix=(TE)
    m = re.match(r"^([A-Z0-9-]+?)(\(.+\))?$", n)
    if m:
        base, suffix = m.group(1), m.group(2) or ""
        # Strip trailing lowercase from base if no suffix already handled
        base_clean = re.sub(r"[a-z]+$", "", name.split("(")[0]).strip().upper()
        base = MODEL_ALIASES.get(base_clean, base_clean)
        return base + suffix
    # Fallback
    if "(" not in n:
        n = re.sub(r"[a-z]+$", "", name).strip().upper()
    return MODEL_ALIASES.get(n, n)


def extract_chunks(md_content, filename=""):
    """Extract Clean Content section from .md, return {chunks, model, date_str}."""
    # Extract date
    date_str = ""
    date_match = re.search(r"^- Date:\s*(.+)$", md_content, re.MULTILINE)
    if date_match:
        try:
            dt = email.utils.parsedate_to_datetime(date_match.group(1).strip())
            date_str = dt.strftime("%Y-%m-%d")
        except Exception:
            pass

    # Extract Clean Content section (between ## ✅ Clean Content and next ## ✅ or EOF)
    clean_match = re.search(r"## ✅ Clean Content\s*\n(.*?)(?=\n## ✅|\Z)", md_content, re.DOTALL)
    text = clean_match.group(1).strip() if clean_match else ""

    if not text:
        # fallback: use everything after metadata
        lines = md_content.split("\n")
        text = "\n".join(lines[6:])  # skip header/metadata

    # Extract models from filename + full content
    models = set()
    for m in MODEL_RE.findall(filename + " " + text):
        normalized = _normalize_model(m)
        # Skip overly long match artifacts (e.g. filenames with version embedded)
        if len(normalized) <= 20:
            models.add(normalized)
    model_str = ",".join(sorted(models))

    # Split into chunks: filter empty/separator lines, group into ~20-line chunks
    lines = [l for l in text.split("\n") if l.strip() and l.strip() != "---"]
    chunks = []
    for i in range(0, len(lines), 20):
        chunk = "\n".join(lines[i:i+20]).strip()
        if chunk:
            chunks.append(chunk)

    # If very short, keep as single chunk (but not if only separators)
    if not chunks and lines:
        chunks = ["\n".join(lines)]

    return {"chunks": chunks, "model": model_str, "date_str": date_str}

class MsgParser:
    @staticmethod
    def safe_str(val):
        if val is None:
            return ""
        if isinstance(val, bytes):
            return val.decode("utf-8", "ignore")
        return str(val)

    @staticmethod
    def clean_filename(text):
        invalid = set('\\/:*?"<>|：\x00')
        return "".join(c for c in MsgParser.safe_str(text) if c not in invalid)[:80] or "no_subject"

    @staticmethod
    def html_to_text(html):
        if not html: return ""
        if isinstance(html, bytes):
            html = html.decode("utf-8", "ignore")
        try:
            soup = BeautifulSoup(html, "html.parser")
            for tag in soup(["script", "style"]):
                tag.decompose()
            return soup.get_text(separator="\n").strip()
        except:
            return html

    @staticmethod
    def normalize_text(text):
        text = text.replace("\xa0", " ").replace("\u3000", " ")
        text = text.replace("", "")
        return text.strip()

    @staticmethod
    def remove_reply_chain(text):
        keys = ["From:", "Sent:", "To:", "Subject:", "-----Original Message-----"]
        for k in keys:
            if k in text:
                return text.split(k)[0].strip()
        return text

    @staticmethod
    def remove_recipients(text):
        text = "\n".join(l for l in text.split("\n") if not re.match(r"^\s*(To:|Cc:|副本)", l, re.IGNORECASE))
        # Remove email addresses
        text = re.sub(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", "", text)
        # Remove phone numbers (Taiwan mobile, international, office)
        text = re.sub(r"(\+?\d{1,4}[-\s]?)?\(?\d{2,4}\)?[-\s]?\d{3,4}[-\s]?\d{3,4}", "", text)
        # Remove ext/分機 numbers
        text = re.sub(r"ext[.:]?\s*\d{3,5}", "", text, flags=re.IGNORECASE)
        text = re.sub(r"分機[：:]?\s*\d{3,5}", "", text)
        # Remove WeChat/微信/LINE IDs
        text = re.sub(r"(WeChat|微信|LINE)[：:\s]*\S+", "", text, flags=re.IGNORECASE)
        # Remove Mobile/手機/Cell label lines left empty
        text = re.sub(r"(Mobile|手機|Cell|Office|Tel|Phone)[：:\s]*\s*$", "", text, flags=re.IGNORECASE | re.MULTILINE)
        return text

    @staticmethod
    def remove_noise(text):
        return re.sub(r"[^\w\s\-\.,:/@()\n]", "", text)

    @staticmethod
    def msg_to_md(file_path):
        msg = extract_msg.Message(file_path)
        subject = MsgParser.normalize_text(MsgParser.safe_str(msg.subject))
        sender = MsgParser.safe_str(msg.sender)
        date = MsgParser.safe_str(msg.date or "")
        body_raw = MsgParser.safe_str(msg.htmlBody or msg.body or "")
        msg.close()

        full_content = MsgParser.normalize_text(MsgParser.html_to_text(body_raw))
        full_content = MsgParser.remove_recipients(full_content)
        clean_content = MsgParser.remove_noise(MsgParser.remove_reply_chain(full_content))
        summary = "\n".join([l.strip() for l in clean_content.split("\n") if l.strip()][:5])

        md_content = f"""# {subject}

- Sender: {sender}
- Date: {date}
- Source File: {os.path.basename(file_path)}

---

## ✅ Summary
{summary}

---

## ✅ Clean Content
{clean_content}

---

## ✅ Full Content
{full_content}
"""
        filename = MsgParser.clean_filename(subject) + ".md"
        return filename, md_content


def parse_docx(file_path):
    """解析 .docx 檔案，回傳純文字內容。使用 zipfile 標準庫，不需 python-docx。"""
    z = zipfile.ZipFile(file_path)
    tree = ET.parse(z.open('word/document.xml'))
    ns = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    paragraphs = []
    for p in tree.iter(f'{{{ns}}}p'):
        texts = [t.text for t in p.iter(f'{{{ns}}}t') if t.text]
        if texts:
            paragraphs.append(''.join(texts))
    z.close()
    return '\n'.join(paragraphs)


def parse_cap_txt(file_path):
    """解析 .cap 或 .txt log 檔案，回傳純文字內容。"""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()


def extract_project_version(filename, content=""):
    """從檔名和內容自動辨識專案名稱和版本號。回傳 (model, version)。"""
    model = ""
    version = ""
    source = filename + " " + content[:500]

    # 從檔名或內容提取 model
    m = MODEL_RE.search(source)
    if m:
        model = _normalize_model(m.group(0))

    # 提取版本號: V1.2.3 或 v1.2.3.4
    ver_match = re.search(r'[Vv](\d+\.\d+[\.\d]*)', source)
    if ver_match:
        version = ver_match.group(1)

    return model, version
