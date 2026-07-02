import json
from pathlib import Path

from utils.audit_logger import write_audit_event


def test_write_audit_event_creates_parent_directories(tmp_path: Path) -> None:
    audit_file = tmp_path / "runtime" / "audit" / "audit.jsonl"

    write_audit_event(
        audit_file,
        "review_saved",
        {"alert_type": "SSH_BRUTE_FORCE", "decision": "confirmed"},
    )

    assert audit_file.exists()

    lines = audit_file.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1

    audit_event = json.loads(lines[0])

    assert audit_event["event_type"] == "review_saved"
    assert audit_event["details"] == {
        "alert_type": "SSH_BRUTE_FORCE",
        "decision": "confirmed",
    }
    assert "timestamp" in audit_event


def test_write_audit_event_appends_json_lines(tmp_path: Path) -> None:
    audit_file = tmp_path / "audit.jsonl"

    write_audit_event(audit_file, "first_event", {"count": 1})
    write_audit_event(audit_file, "second_event", {"count": 2})

    lines = audit_file.read_text(encoding="utf-8").splitlines()
    events = [json.loads(line) for line in lines]

    assert [event["event_type"] for event in events] == [
        "first_event",
        "second_event",
    ]
    assert [event["details"]["count"] for event in events] == [1, 2]
