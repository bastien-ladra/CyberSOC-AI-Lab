from typing import Any

import requests
from pytest import MonkeyPatch

from ai_assistant.llm_client import (
    get_ollama_model_metadata,
    query_ollama,
)


class FakeResponse:
    def __init__(self, payload: dict[str, Any]) -> None:
        self.payload = payload

    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict[str, Any]:
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


def test_query_ollama_passes_frozen_generation_options(
    monkeypatch: MonkeyPatch,
) -> None:
    captured_payload: dict[str, Any] = {}

    def fake_post(
        url: str,
        json: dict[str, Any],
        timeout: int,
    ) -> FakeResponse:
        captured_payload["json"] = json
        return FakeResponse({"response": "ok"})

    monkeypatch.setattr("ai_assistant.llm_client.requests.post", fake_post)

    response = query_ollama(
        "Analyse.",
        options={"temperature": 0.0, "seed": 20260927, "num_predict": 128},
    )

    assert response == "ok"
    assert captured_payload["json"]["options"] == {
        "temperature": 0.0,
        "seed": 20260927,
        "num_predict": 128,
    }


def test_get_ollama_model_metadata_records_digest_and_version(
    monkeypatch: MonkeyPatch,
) -> None:
    def fake_get(url: str, timeout: int) -> FakeResponse:
        if url.endswith("/api/version"):
            return FakeResponse({"version": "0.12.0"})
        if url.endswith("/api/tags"):
            return FakeResponse(
                {
                    "models": [
                        {
                            "name": "llama3.2:3b",
                            "model": "llama3.2:3b",
                            "digest": "sha256-test-digest",
                            "modified_at": "2026-09-27T12:00:00Z",
                            "size": 123,
                            "details": {"parameter_size": "3B"},
                        }
                    ]
                }
            )
        raise AssertionError(f"unexpected URL: {url}")

    monkeypatch.setattr("ai_assistant.llm_client.requests.get", fake_get)

    metadata = get_ollama_model_metadata(
        "llama3.2:3b",
        base_url="http://ollama.local",
    )

    assert metadata is not None
    assert metadata["digest"] == "sha256-test-digest"
    assert metadata["ollama_version"] == "0.12.0"
    assert metadata["resolved_name"] == "llama3.2:3b"


def test_get_ollama_model_metadata_returns_none_when_model_missing(
    monkeypatch: MonkeyPatch,
) -> None:
    def fake_get(url: str, timeout: int) -> FakeResponse:
        if url.endswith("/api/version"):
            return FakeResponse({"version": "0.12.0"})
        return FakeResponse({"models": []})

    monkeypatch.setattr("ai_assistant.llm_client.requests.get", fake_get)

    assert get_ollama_model_metadata("missing-model") is None


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
