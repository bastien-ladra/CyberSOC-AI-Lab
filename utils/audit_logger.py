import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def write_audit_event(
    audit_file: Path,
    event_type: str,
    details: dict[str, Any]
) -> None:
    """
    Écrit un événement d'audit au format JSON Lines.
    Chaque ligne représente une action traçable du système.
    """
    audit_file.parent.mkdir(parents=True, exist_ok=True)

    audit_event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        "details": details,
    }

    with audit_file.open("a", encoding="utf-8") as file:
        file.write(json.dumps(audit_event, ensure_ascii=False) + "\n")
