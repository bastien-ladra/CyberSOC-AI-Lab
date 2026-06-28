import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def save_json_file(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(exist_ok=True)
    path.write_text(
        json.dumps(data, indent=4, ensure_ascii=False),
        encoding="utf-8",
    )


def append_jsonl(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(exist_ok=True)

    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(data, ensure_ascii=False) + "\n")


def build_human_review(
    alert_number: str,
    alert: dict[str, Any],
    decision: str,
    analyst_note: str,
) -> dict[str, Any]:
    mitre_attack = alert.get("mitre_attack", {})

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "alert_number": alert_number,
        "alert_type": alert.get("alert_type"),
        "severity": alert.get("severity"),
        "priority_score": alert.get("priority_score"),
        "priority_label": alert.get("priority_label"),
        "source_ip": alert.get("source_ip"),
        "mitre_framework": mitre_attack.get("framework"),
        "mitre_tactic": mitre_attack.get("tactic"),
        "mitre_technique": mitre_attack.get("technique"),
        "mitre_technique_id": mitre_attack.get("technique_id"),
        "decision": decision,
        "analyst_note": analyst_note,
        "human_validation_required": alert.get("human_validation_required"),
    }


def save_human_review(
    alert_number: str,
    alert: dict[str, Any],
    decision: str,
    analyst_note: str,
    review_dir: Path = Path("human_reviews"),
    audit_file: Path = Path("audit/human_review_log.jsonl"),
) -> Path:
    review = build_human_review(
        alert_number=alert_number,
        alert=alert,
        decision=decision,
        analyst_note=analyst_note,
    )

    review_path = review_dir / f"review_{alert_number}.json"
    save_json_file(review_path, review)

    audit_event = {
        "timestamp": review["timestamp"],
        "event_type": "human_review_submitted",
                "details": {
            "alert_number": alert_number,
            "alert_type": alert.get("alert_type"),
            "severity": alert.get("severity"),
            "priority_score": alert.get("priority_score"),
            "priority_label": alert.get("priority_label"),
            "source_ip": alert.get("source_ip"),
            "decision": decision,
            "review_file": str(review_path),
        },
    }

    append_jsonl(audit_file, audit_event)

    return review_path