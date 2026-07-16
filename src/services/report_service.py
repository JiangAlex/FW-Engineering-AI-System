import os
from datetime import datetime

# Define absolute paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MD_DIR = os.path.join(PROJECT_ROOT, "knowledge/md")
REPORT_DIR = os.path.join(PROJECT_ROOT, "knowledge/report")

class ReportService:
    @staticmethod
    def generate_weekly_report(ai_client=None, limit=10):
        """Generates a weekly engineering report based on recent mail records."""
        if not os.path.exists(MD_DIR): return "❌ Source directory not found"
        
        files = sorted(os.listdir(MD_DIR), reverse=True)
        docs = []
        for f in files:
            if f.endswith(".md"):
                with open(os.path.join(MD_DIR, f), "r", encoding="utf-8") as file:
                    docs.append(file.read())
            if len(docs) >= limit: break
            
        if not docs: return "❌ No documents found to generate report"

        prompt = f"""
你是一位工程專案經理，請根據以下多封 mail 統整週報。

【資料】
{"\n\n".join(docs)}

請輸出繁體中文 Markdown：

# Weekly Engineering Report

## ✅ Key Projects
## ✅ Key Issues
## ✅ Progress
## ✅ Risks
## ✅ Conclusion

要求：條列式、簡短、白話文。
"""
        report_content = ai_client.ask(prompt) if ai_client else "⚠️ AI Client not provided for report generation."
        
        # Save report
        os.makedirs(REPORT_DIR, exist_ok=True)
        filename = datetime.now().strftime("weekly_report_%Y%m%d.md")
        path = os.path.join(REPORT_DIR, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(report_content)
        
        return report_content, filename
