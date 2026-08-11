"""Local LLM client using llama-cpp-python (Qwen2.5-7B-Instruct).

Provides a drop-in replacement for the MiniMax AIClient, running inference
100% on-premise with zero data leaving the machine.
"""

import os
import re
from dotenv import load_dotenv

load_dotenv()

# Configuration
LLM_MODEL_PATH = os.getenv("LLM_MODEL_PATH", "models/qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf")
LLM_N_CTX = int(os.getenv("LLM_N_CTX", "4096"))
LLM_N_THREADS = int(os.getenv("LLM_N_THREADS", "8"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "1024"))

# Resolve model path relative to project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if not os.path.isabs(LLM_MODEL_PATH):
    LLM_MODEL_PATH = os.path.join(PROJECT_ROOT, LLM_MODEL_PATH)


class LocalAIClient:
    """Local LLM client using Qwen2.5-7B via llama-cpp-python.
    
    Singleton pattern to avoid loading the model multiple times (~5.5GB RAM).
    Provides the same .ask() interface as the MiniMax AIClient.
    
    Usage:
        client = LocalAIClient.get_instance()
        answer = client.ask("你好，請回答問題...")
    """

    _instance = None
    _initialized = False

    def __init__(self, model_path=None, n_ctx=None, n_threads=None):
        model_path = model_path or LLM_MODEL_PATH
        n_ctx = n_ctx or LLM_N_CTX
        n_threads = n_threads or LLM_N_THREADS

        if not os.path.exists(model_path):
            raise RuntimeError(f"Model file not found: {model_path}")

        print(f"🔄 Loading local LLM: {os.path.basename(model_path)} (n_ctx={n_ctx}, threads={n_threads})...")
        try:
            from llama_cpp import Llama
            self.llm = Llama(
                model_path=model_path,
                n_ctx=n_ctx,
                n_threads=n_threads,
                n_gpu_layers=0,  # CPU only
                verbose=False,
            )
            self._initialized = True
            print(f"✅ Local LLM loaded: {os.path.basename(model_path)}")
        except Exception as e:
            self._initialized = False
            raise RuntimeError(f"Failed to load local LLM: {e}")

    @classmethod
    def get_instance(cls):
        """Get or create singleton instance. Returns None if loading fails."""
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
        if cls._instance and cls._instance._initialized:
            del cls._instance.llm
        cls._instance = None

    @property
    def is_ready(self):
        return self._initialized

    def ask(self, prompt, temperature=0.3, history=None):
        """Send a prompt to the local LLM and return the response.
        
        Args:
            prompt: The user prompt (same format as MiniMax AIClient).
            temperature: Sampling temperature (0.0-1.0).
            history: Optional conversation history [{role, content}].
            
        Returns:
            Generated text response, or error message string.
        """
        if not self._initialized:
            return "❌ Local LLM not initialized"

        messages = []
        
        # System message for consistent behavior
        messages.append({
            "role": "system",
            "content": "你是一位專業的工程知識助理。請使用繁體中文回答，條列重點，簡潔明確。"
        })

        # Add conversation history
        if history:
            for h in history:
                messages.append({"role": h["role"], "content": h["content"]})

        # Add current prompt
        messages.append({"role": "user", "content": prompt})

        try:
            response = self.llm.create_chat_completion(
                messages=messages,
                temperature=temperature,
                max_tokens=LLM_MAX_TOKENS,
                stop=["<|im_end|>", "<|endoftext|>"],
            )
            text = response["choices"][0]["message"]["content"]

            # Remove <think> tags if present
            text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
            return text.strip()
        except Exception as e:
            return f"⚠️ Local LLM error: {str(e)}"

    def fallback_summarize(self, docs):
        """Simple fallback summary when LLM is unavailable."""
        text = "\n".join(docs)
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        return "⚠️ Fallback Mode (No AI)\n\n" + "\n".join(lines[:10])
