import re
from typing import Dict, List


SSH_FAILED_PATTERN = re.compile(
    r"Failed password for (?:invalid user )?(?P<user>\w+) from (?P<ip>[\d\.]+) port (?P<port>\d+)"
)

SSH_ACCEPTED_PATTERN = re.compile(
    r"Accepted password for (?P<user>\w+) from (?P<ip>[\d\.]+) port (?P<port>\d+)"
)


def parse_ssh_log_line(line: str) -> Dict:
    """
    Parse une ligne de log SSH simple et retourne un événement structuré.
    """
    event = {
        "raw": line.strip(),
        "event_type": "unknown",
        "user": None,
        "source_ip": None,
        "port": None,
    }

    failed_match = SSH_FAILED_PATTERN.search(line)
    if failed_match:
        event["event_type"] = "ssh_failed_login"
        event["user"] = failed_match.group("user")
        event["source_ip"] = failed_match.group("ip")
        event["port"] = failed_match.group("port")
        return event

    accepted_match = SSH_ACCEPTED_PATTERN.search(line)
    if accepted_match:
        event["event_type"] = "ssh_success_login"
        event["user"] = accepted_match.group("user")
        event["source_ip"] = accepted_match.group("ip")
        event["port"] = accepted_match.group("port")
        return event

    return event


def load_ssh_logs(file_path: str) -> List[Dict]:
    """
    Charge un fichier de logs SSH et retourne une liste d'événements structurés.
    """
    events = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                events.append(parse_ssh_log_line(line))

    return events