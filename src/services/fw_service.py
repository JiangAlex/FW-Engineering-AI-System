import os
import re
import email.utils
from datetime import datetime, timezone
from collections import defaultdict
from src.core.database import get_connection

# Define absolute path to md directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MD_DIR = os.path.join(PROJECT_ROOT, "knowledge", "md")

MODEL_ALIASES = {
    "EAP115A": "EAP115",
    "JIOWAVE62420": "EAP111",
    "JWS62420": "EAP111",
    "EAP104L": "EAP104",
}

def normalize_model(name):
    """Normalize model name: strip suffix, parenthetical, apply alias."""
    n = re.sub(r"\(.*?\)", "", name).strip().upper()
    n = re.sub(r"[a-z]+$", "", name).strip().upper()  # EAP115a -> EAP115
    return MODEL_ALIASES.get(n, n)


class FWService:
    @staticmethod
    def extract_info(text):
        """DEPRECATED: Use extract_info_by_line() instead."""
        models = re.findall(r"\b(EAP\d+|ECS\d+|AP\d+|SW\d+)\b", text, re.IGNORECASE)
        fws = re.findall(r"\b[vV]?(\d+\.\d+(?:\.\d+)?)\b", text)
        return list(set([m.upper() for m in models])), list(set(fws))

    @staticmethod
    def extract_info_by_line(text, proximity=10):
        """Context-aware extraction: pairs models with versions by line proximity."""
        lines = text.split("\n")
        result = defaultdict(set)

        model_re = re.compile(r"\b(EAP\d+[a-zA-Z]?|ECS\d+|AP\d+|SW\d+|JWS\d+[A-Z]?|JioWave\d+)\b", re.IGNORECASE)
        embedded_re = re.compile(r"(EAP\d+|ECS\d+|AP\d+|SW\d+|JWS\d+[A-Z]?)[-_]\S*?[vV](\d+(?:\.\d+[A-Za-z]?)+)(?=[_\s.]|$)", re.IGNORECASE)
        hi_ver_re = re.compile(r"(?:FW\s*)?[vV]\s*(\d+\.\d+(?:\.\d+)*)")
        lo_ver_re = re.compile(r"\b(\d+\.\d+(?:\.\d+)+)\b")

        # Pass 1: embedded model_version strings
        for line in lines:
            for m in embedded_re.finditer(line):
                result[normalize_model(m.group(1))].add(m.group(2))

        # Pass 2: model positions
        model_positions = defaultdict(list)
        for i, line in enumerate(lines):
            for m in model_re.finditer(line):
                model_positions[normalize_model(m.group(1))].append(i)

        all_models = set(model_positions.keys())

        # Pass 3: version positions + pairing
        for i, line in enumerate(lines):
            # High confidence: has V/v prefix (possibly with FW)
            for m in hi_ver_re.finditer(line):
                ver = m.group(1)
                for model in all_models:
                    result[model].add(ver)

            # Low confidence: bare numbers with 3+ segments, only if NOT already matched by hi_ver_re
            hi_spans = [m.span() for m in hi_ver_re.finditer(line)]
            for m in lo_ver_re.finditer(line):
                # Skip if overlaps with a high-confidence match
                if any(s <= m.start() < e for s, e in hi_spans):
                    continue
                ver = m.group(1)
                for model, positions in model_positions.items():
                    if any(abs(i - p) <= proximity for p in positions):
                        result[model].add(ver)

        return dict(result)

    @staticmethod
    def parse_date(date_str):
        """Parses email date strings into datetime objects."""
        try:
            dt = email.utils.parsedate_to_datetime(date_str)
            if dt.tzinfo is not None:
                dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
            return dt
        except:
            return None

    @staticmethod
    def get_fw_summary():
        """Aggregates all models and their associated firmware versions."""
        summary = defaultdict(set)
        if not os.path.exists(MD_DIR): return {}
        
        for f in os.listdir(MD_DIR):
            if f.endswith(".md"):
                with open(os.path.join(MD_DIR, f), "r", encoding="utf-8") as file:
                    pairs = FWService.extract_info_by_line(file.read())
                    for model, versions in pairs.items():
                        summary[model].update(versions)
        return {m: sorted(list(fws)) for m, fws in summary.items()}

    @staticmethod
    def get_timeline():
        """Generates a version history timeline for each model."""
        timeline = defaultdict(list)
        if not os.path.exists(MD_DIR): return {}

        for f in os.listdir(MD_DIR):
            if f.endswith(".md"):
                with open(os.path.join(MD_DIR, f), "r", encoding="utf-8") as file:
                    content = file.read()
                    date_match = re.search(r"- Date: (.*)", content)
                    date_val = FWService.parse_date(date_match.group(1)) if date_match else None
                    date_display = (date_val.strftime("%Y-%m-%d") if date_val else "Unknown")
                    pairs = FWService.extract_info_by_line(content)
                    for model, versions in pairs.items():
                        for fw in versions:
                            timeline[model].append({
                                "date": date_val,
                                "date_str": date_display,
                                "fw": fw,
                                "file": f
                            })
        
        # Sort and deduplicate
        result = {}
        for m, entries in timeline.items():
            sorted_entries = sorted(entries, key=lambda x: x["date"] if x["date"] else datetime.min)
            seen = set()
            unique_entries = []
            for e in sorted_entries:
                if (e["fw"], e["date_str"]) not in seen:
                    unique_entries.append(e)
                    seen.add((e["fw"], e["date_str"]))
            result[m] = unique_entries
        return result

    @staticmethod
    def compare_versions(model, v1, v2, ai_client=None):
        """Compares two firmware versions using AI or fallback logic."""
        # Find docs mentioning both versions
        conn = get_connection()
        c = conn.cursor()
        query = f"{model} {v1} {v2}"
        # We use a simple like or match here for comparison context
        c.execute("SELECT content FROM docs WHERE content LIKE ? AND content LIKE ?", 
                  (f"%{v1}%", f"%{v2}%"))
        docs = [row[0] for row in c.fetchall()]
        conn.close()

        if not docs:
            return f"❌ No matching records found for {model} comparing {v1} and {v2}."

        from src.core.prompts import fw_compare
        prompt = fw_compare(model, v1, v2, "".join(docs[:3]))
        if ai_client:
            return ai_client.ask(prompt)
        return "⚠️ Fallback: Manual review required. Found matches in multiple documents."


if __name__ == "__main__":
    summary = FWService.get_fw_summary()
    # Write to timestamped file
    output_dir = os.path.join(PROJECT_ROOT, "knowledge", "output")
    os.makedirs(output_dir, exist_ok=True)
    filename = f"fw_summary_{datetime.now().strftime('%Y%m%d')}.md"
    path = os.path.join(output_dir, filename)

    lines = ["# FW Summary\n"]
    for model in sorted(summary.keys()):
        lines.append(f"- {model} → FW: {', '.join(summary[model])}")
    content = "\n".join(lines) + "\n"

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(content)
    print(f"✅ Written to {path}")
