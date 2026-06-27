import json
from pathlib import Path

from utils.human_review import build_human_review, save_human_review


def test_build_human_review() -> None:
    alert = {
        "alert_type": "SSH_BRUTE_FORCE",
        "severity": "HIGH",
        "source_ip": "185.12.45.10",
        "human_validation_required": True,
    }

    review = build_human_review(
        alert_number="001",
        alert=alert,
        decision="Validée",
        analyst_note="Tentative probable de brute force SSH.",
    )

    assert review["alert_number"] == "001"
    assert review["alert_type"] == "SSH_BRUTE_FORCE"
    assert review["severity"] == "HIGH"
    assert review["source_ip"] == "185.12.45.10"
    assert review["decision"] == "Validée"
    assert review["analyst_note"] == "Tentative probable de brute force SSH."
    assert review["human_validation_required"] is True
    assert "timestamp" in review


def test_save_human_review(tmp_path: Path) -> None:
    alert = {
        "alert_type": "WEB_RECONNAISSANCE",
        "severity": "MEDIUM",
        "source_ip": "185.12.45.10",
        "human_validation_required": True,
    }

    review_dir = tmp_path / "human_reviews"
    audit_file = tmp_path / "audit" / "human_review_log.jsonl"

    review_path = save_human_review(
        alert_number="002",
        alert=alert,
        decision="À revoir",
        analyst_note="Activité de reconnaissance web à corréler avec les logs firewall.",
        review_dir=review_dir,
        audit_file=audit_file,
    )

    assert review_path.exists()
    assert audit_file.exists()

    review_data = json.loads(review_path.read_text(encoding="utf-8"))

    assert review_data["alert_number"] == "002"
    assert review_data["alert_type"] == "WEB_RECONNAISSANCE"
    assert review_data["decision"] == "À revoir"

    audit_content = audit_file.read_text(encoding="utf-8")

    assert "human_review_submitted" in audit_content
    assert "WEB_RECONNAISSANCE" in audit_content