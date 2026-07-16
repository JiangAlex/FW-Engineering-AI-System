import os
import requests
import re
from dotenv import load_dotenv

load_dotenv()

def sanitize(text):
    """Remove sensitive info (emails, phones, names, internal IDs) before sending to external API."""
    # Remove email addresses
    text = re.sub(r'[\w.-]+@[\w.-]+\.\w+', '[EMAIL]', text)
    # Remove phone numbers (Taiwan format)
    text = re.sub(r'\+?886[-\s]?\d{2,4}[-\s]?\d{3}[-\s]?\d{3}', '[PHONE]', text)
    # Remove metadata header lines (From/To/Cc/Sender with personal info)
    text = re.sub(r'^(From|To|Cc|Sent|Sender):.*$', '', text, flags=re.MULTILINE)
    # Remove Chinese names (2-4 CJK chars between known patterns)
    text = re.sub(r'[\u4e00-\u9fff]{2,4}(?=\s*<|\s*\[)', '[NAME]', text)
    # Remove lines that are just signatures (Regards + name)
    text = re.sub(r'^(Regards|Best Regards),?\s*\n.*$', '', text, flags=re.MULTILINE | re.IGNORECASE)
    # Remove Cell/Email signature lines
    text = re.sub(r'^(Cell|Email|Phone|Tel):.*$', '', text, flags=re.MULTILINE)
    # Remove - Sender: header from md metadata
    text = re.sub(r'^- Sender:.*$', '- Sender: [REDACTED]', text, flags=re.MULTILINE)
    return text


class AIClient:
    def __init__(self, model="MiniMax-M2.7"):
        self.api_key = os.getenv("MINIMAX_API_KEY")
        self.url = "https://api.minimax.io/v1/chat/completions"
        self.model = model

    def ask(self, prompt, temperature=0.3, history=None):
        """Sends a prompt to the AI and returns the cleaned response."""
        if not self.api_key:
            return "❌ API Key not set"

        prompt = sanitize(prompt)

        messages = list(history) if history else []
        messages.append({"role": "user", "content": prompt})

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature
        }

        try:
            res = requests.post(self.url, headers=headers, json=payload)
            if res.status_code != 200:
                return f"⚠️ API Error: {res.status_code}"
            
            data = res.json()
            text = data["choices"][0]["message"]["content"]
            
            # Remove <think> tags if present
            text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
            return text.strip()
        except Exception as e:
            return f"⚠️ Exception: {str(e)}"

    def fallback_summarize(self, docs):
        """Simple fallback summary when AI is unavailable."""
        text = "\n".join(docs)
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        return "⚠️ Fallback Mode (No AI)\n\n" + "\n".join(lines[:10])
