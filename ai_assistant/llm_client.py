from typing import Optional
import requests


def query_ollama(
    prompt: str,
    model: str = "llama3.2",
    base_url: str = "http://localhost:11434"
) -> Optional[str]:
    """
    Envoie un prompt à un modèle local Ollama.

    Cette fonction suppose qu'Ollama tourne en local.
    Aucune donnée n'est envoyée à une API externe.
    """
    endpoint = f"{base_url}/api/generate"

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }

    try:
        response = requests.post(endpoint, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data.get("response")
    except requests.RequestException as error:
        print(f"Erreur lors de l'appel au modèle IA local : {error}")
        return None