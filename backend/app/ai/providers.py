from abc import ABC, abstractmethod

import httpx

from app.core.config import get_settings

settings = get_settings()


class AIProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str: ...


class OllamaProvider(AIProvider):
    def generate(self, prompt: str) -> str:
        response = httpx.post(
            f"{settings.ollama_base_url}/api/generate",
            json={"model": "llama3.1", "prompt": prompt, "stream": False},
            timeout=120,
        )
        response.raise_for_status()
        return response.json().get("response", "")


class OpenAIProvider(AIProvider):
    def generate(self, prompt: str) -> str:
        if not settings.openai_api_key:
            raise RuntimeError("OpenAI fallback requested but API key is missing")
        response = httpx.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {settings.openai_api_key}"},
            json={
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=120,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]


def get_provider(prefer_openai: bool = False) -> AIProvider:
    if prefer_openai:
        return OpenAIProvider()
    return OllamaProvider()
