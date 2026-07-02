from pathlib import Path

from detection.log_parser import load_ssh_logs, load_web_logs
from detection.rules_engine import (
    detect_prompt_injection_attempt,
    detect_ssh_bruteforce,
    detect_web_reconnaissance,
)

DATA_DIR = Path("data/sample_logs")


def test_benign_ssh_logs_do_not_trigger_bruteforce() -> None:
    events = load_ssh_logs(str(DATA_DIR / "benign_ssh_auth.log"))

    alerts = detect_ssh_bruteforce(events)

    assert alerts == []


def test_benign_web_logs_do_not_trigger_reconnaissance_or_prompt_injection() -> None:
    events = load_web_logs(str(DATA_DIR / "benign_web_access.log"))

    reconnaissance_alerts = detect_web_reconnaissance(events)
    prompt_injection_alerts = detect_prompt_injection_attempt(events)

    assert reconnaissance_alerts == []
    assert prompt_injection_alerts == []
