from collections.abc import Mapping
from typing import Any, Optional

import requests


def query_ollama(
    prompt: str,
    model: str = "llama3.2",
    base_url: str = "http://localhost:11434",
    options: Mapping[str, Any] | None = None,
) -> Optional[str]:
    """
    Envoie un prompt à un modèle local Ollama.

    Cette fonction suppose qu'Ollama tourne en local.
    Aucune donnée n'est envoyée à une API externe.
    """
    endpoint = f"{base_url}/api/generate"

    payload: dict[str, Any] = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }
    if options is not None:
        payload["options"] = dict(options)

    try:
        response = requests.post(endpoint, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data.get("response")
    except requests.RequestException as error:
        print(f"Erreur lors de l'appel au modèle IA local : {error}")
        return None


def get_ollama_model_metadata(
    model: str,
    base_url: str = "http://localhost:11434",
) -> dict[str, Any] | None:
    """Resolve the exact local Ollama model digest and runtime version."""
    try:
        version_response = requests.get(f"{base_url}/api/version", timeout=10)
        version_response.raise_for_status()
        version_payload = version_response.json()

        tags_response = requests.get(f"{base_url}/api/tags", timeout=10)
        tags_response.raise_for_status()
        tags_payload = tags_response.json()
    except requests.RequestException as error:
        print(f"Erreur lors de la lecture des métadonnées Ollama : {error}")
        return None

    models = tags_payload.get("models")
    if not isinstance(models, list):
        return None

    matched_model: dict[str, Any] | None = None
    for item in models:
        if not isinstance(item, dict):
            continue
        if item.get("name") == model or item.get("model") == model:
            matched_model = item
            break

    if matched_model is None:
        return None

    digest = matched_model.get("digest")
    if not isinstance(digest, str) or not digest:
        return None

    return {
        "requested_model": model,
        "resolved_name": matched_model.get("name"),
        "resolved_model": matched_model.get("model"),
        "digest": digest,
        "modified_at": matched_model.get("modified_at"),
        "size": matched_model.get("size"),
        "details": matched_model.get("details"),
        "ollama_version": version_payload.get("version"),
    }
