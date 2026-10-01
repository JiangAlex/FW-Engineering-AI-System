"""Local LLM client using Ollama (OpenAI-compatible API).

Provides a drop-in replacement for the MiniMax AIClient, running inference
100% on-premise via Ollama. Supports any model available in Ollama
(e.g., qwen2.5:7b, qwen3:14b, gemma4).
"""

import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

# Configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "1024"))
LLM_TIMEOUT = int(os.getenv("LLM_TIMEOUT", "300"))
# Context window (prompt + completion) the Ollama model is loaded with.
# Ollama defaults to 4096, which overflows on RAG prompts (retrieved chunks +
# question) and especially the weekly-report prompt. qwen3:4b-instruct supports
# long context, so we raise this. Tune via OLLAMA_NUM_CTX.
OLLAMA_NUM_CTX = int(os.getenv("OLLAMA_NUM_CTX", "32768"))
# Whether to sanitize (de-identify) prompts before sending to the on-premise
# Ollama server. Defaults to on: even though Ollama runs on the internal
# network, we strip personal info (emails, phones, names, sender headers) as
# defense-in-depth. Set SANITIZE_LOCAL=false to send raw text.
SANITIZE_LOCAL = os.getenv("SANITIZE_LOCAL", "true").lower() not in ("false", "0", "no")


class LocalAIClient:
    """Local LLM client using Ollama's OpenAI-compatible API.

    Singleton pattern to maintain a single client instance.
    Provides the same .ask() interface as the MiniMax AIClient.

    Usage:
        client = LocalAIClient.get_instance()
        answer = client.ask("你好，請回答問題...")
    """

    _instance = None
    _initialized = False

    def __init__(self, base_url=None, model=None):
        self.base_url = base_url or OLLAMA_BASE_URL
        self.model = model or OLLAMA_MODEL
        self.api_url = f"{self.base_url}/v1/chat/completions"

        # Verify Ollama is reachable and model is available
        print(f"🔄 Connecting to Ollama: {self.base_url} (model={self.model})...")
        try:
            resp = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if resp.status_code != 200:
                raise RuntimeError(f"Ollama not reachable at {self.base_url}")

            models = [m["name"] for m in resp.json().get("models", [])]
            # Check model availability (handle tag variations like "qwen2.5:7b" vs "qwen2.5:7b-instruct")
            model_base = self.model.split(":")[0]
            if not any(model_base in m for m in models):
                available = ", ".join(models) if models else "none"
                raise RuntimeError(
                    f"Model '{self.model}' not found in Ollama. Available: {available}. "
                    f"Run: ollama pull {self.model}"
                )

            self._initialized = True
            print(f"✅ Ollama connected: {self.model}")
        except requests.ConnectionError:
            self._initialized = False
            raise RuntimeError(
                f"Cannot connect to Ollama at {self.base_url}. "
                "Is Ollama running? Start with: ollama serve"
            )
        except RuntimeError:
            self._initialized = False
            raise

    @classmethod
    def get_instance(cls):
        """Get or create singleton instance. Returns None if connection fails."""
        if cls._instance is None:
            try:
                cls._instance = cls()
            except RuntimeError as e:
                print(f"⚠️ Local LLM unavailable: {e}")
                return None
        return cls._instance

    @classmethod
    def reset(cls):
        """Reset singleton (for testing or model switching)."""
        cls._instance = None

    @property
    def is_ready(self):
        return self._initialized

    def ask(self, prompt, temperature=0.3, history=None):
        """Send a prompt to Ollama and return the response.

        Args:
            prompt: The user prompt (same format as MiniMax AIClient).
            temperature: Sampling temperature (0.0-1.0).
            history: Optional conversation history [{role, content}].

        Returns:
            Generated text response, or error message string.
        """
        if not self._initialized:
            return "❌ Local LLM not initialized"

        # De-identify prompt before sending to the on-premise Ollama server.
        # Reuses the same sanitize() rules as the MiniMax path. Delayed import
        # to avoid a circular import (ai_client imports local_llm lazily).
        if SANITIZE_LOCAL:
            from src.core.ai_client import sanitize
            prompt = sanitize(prompt)

        messages = []

        # System message for consistent behavior (centralized in core.prompts)
        from src.core.prompts import SYSTEM_MESSAGE
        messages.append({
            "role": "system",
            "content": SYSTEM_MESSAGE
        })

        # Add conversation history
        if history:
            for h in history:
                messages.append({"role": h["role"], "content": h["content"]})

        # Add current prompt
        messages.append({"role": "user", "content": prompt})

        try:
            resp = requests.post(
                self.api_url,
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": LLM_MAX_TOKENS,
                    "stream": False,
                    # Raise context window above Ollama's 4096 default so RAG /
                    # report prompts don't hit exceed_context_size_error.
                    "options": {"num_ctx": OLLAMA_NUM_CTX},
                },
                timeout=LLM_TIMEOUT,
            )

            if resp.status_code != 200:
                return f"⚠️ Ollama API error: {resp.status_code} - {resp.text[:200]}"

            data = resp.json()
            text = data["choices"][0]["message"]["content"]

            # Remove <think> tags if present
            text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
            return text.strip()
        except requests.ConnectionError:
            return "⚠️ Ollama connection lost. Is Ollama still running?"
        except requests.Timeout:
            return f"⚠️ Ollama request timed out ({LLM_TIMEOUT}s)"
        except Exception as e:
            return f"⚠️ Local LLM error: {str(e)}"

    def fallback_summarize(self, docs):
        """Simple fallback summary when LLM is unavailable."""
        text = "\n".join(docs)
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        return "⚠️ Fallback Mode (No AI)\n\n" + "\n".join(lines[:10])
