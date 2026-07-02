import re
from typing import Any

SSH_FAILED_PATTERN = re.compile(
    r"Failed password for (?:invalid user )?(?P<user>\w+) from (?P<ip>[\d\.]+) port (?P<port>\d+)"
)

SSH_ACCEPTED_PATTERN = re.compile(
    r"Accepted password for (?P<user>\w+) from (?P<ip>[\d\.]+) port (?P<port>\d+)"
)

WEB_ACCESS_PATTERN = re.compile(
    r'(?P<ip>[\d\.]+) - - \[(?P<timestamp>[^\]]+)\] "(?P<method>\w+) (?P<path>[^ ]+) (?P<protocol>[^"]+)" (?P<status>\d+) (?P<size>\d+) "[^"]*" "(?P<user_agent>[^"]*)"'
)


def parse_ssh_log_line(line: str) -> dict[str, Any]:
    event: dict[str, Any] = {
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


def parse_web_log_line(line: str) -> dict[str, Any]:
    event: dict[str, Any] = {
        "raw": line.strip(),
        "event_type": "unknown",
        "source_ip": None,
        "method": None,
        "path": None,
        "status": None,
        "user_agent": None,
    }

    match = WEB_ACCESS_PATTERN.search(line)
    if match:
        event["event_type"] = "web_access"
        event["source_ip"] = match.group("ip")
        event["method"] = match.group("method")
        event["path"] = match.group("path")
        event["status"] = int(match.group("status"))
        event["user_agent"] = match.group("user_agent")
        return event

    return event


def load_ssh_logs(file_path: str) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                events.append(parse_ssh_log_line(line))

    return events


def load_web_logs(file_path: str) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                events.append(parse_web_log_line(line))

    return events
