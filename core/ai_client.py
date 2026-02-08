from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

import urllib.request


@dataclass
class AiRequest:
    prompt: str
    model: str = "llama3.1"


@dataclass
class AiResponse:
    content: str
    raw: dict[str, Any]


class LocalAiClient:
    """Offline/local LLM client (Ollama-compatible)."""

    def __init__(self, base_url: str = "http://127.0.0.1:11434") -> None:
        self.base_url = base_url.rstrip("/")

    def generate(self, request: AiRequest) -> AiResponse:
        url = f"{self.base_url}/api/generate"
        payload = json.dumps({"model": request.model, "prompt": request.prompt, "stream": False}).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return AiResponse(content=data.get("response", ""), raw=data)
