from typing import Any

import requests
from pytest import MonkeyPatch

from ai_assistant.llm_client import query_ollama


class FakeResponse:
    def __init__(self, payload: dict[str, str]) -> None:
        self.payload = payload

    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict[str, str]:
        return self.payload


def test_query_ollama_returns_model_response(monkeypatch: MonkeyPatch) -> None:
    captured_payload: dict[str, Any] = {}

    def fake_post(
        url: str,
        json: dict[str, Any],
        timeout: int,
    ) -> FakeResponse:
        captured_payload["url"] = url
        captured_payload["json"] = json
        captured_payload["timeout"] = timeout
        return FakeResponse({"response": "Analyse SOC générée."})

    monkeypatch.setattr("ai_assistant.llm_client.requests.post", fake_post)

    response = query_ollama(
        "Analyse cette alerte.",
        model="llama-test",
        base_url="http://ollama.local",
    )

    assert response == "Analyse SOC générée."
    assert captured_payload["url"] == "http://ollama.local/api/generate"
    assert captured_payload["json"] == {
        "model": "llama-test",
        "prompt": "Analyse cette alerte.",
        "stream": False,
    }
    assert captured_payload["timeout"] == 60


def test_query_ollama_returns_none_on_request_error(monkeypatch: MonkeyPatch) -> None:
    def fake_post(
        url: str,
        json: dict[str, Any],
        timeout: int,
    ) -> FakeResponse:
        raise requests.RequestException("connection refused")

    monkeypatch.setattr("ai_assistant.llm_client.requests.post", fake_post)

    response = query_ollama("Analyse cette alerte.")

    assert response is None
