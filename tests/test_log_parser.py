from detection.log_parser import parse_ssh_log_line, parse_web_log_line


def test_parse_failed_ssh_login() -> None:
    line = "Jun 24 10:01:12 server01 sshd[1201]: Failed password for invalid user admin from 185.12.45.10 port 53321 ssh2"

    event = parse_ssh_log_line(line)

    assert event["event_type"] == "ssh_failed_login"
    assert event["user"] == "admin"
    assert event["source_ip"] == "185.12.45.10"
    assert event["port"] == "53321"


def test_parse_successful_ssh_login() -> None:
    line = "Jun 24 10:15:42 server01 sshd[1301]: Accepted password for bastien from 192.168.1.42 port 50110 ssh2"

    event = parse_ssh_log_line(line)

    assert event["event_type"] == "ssh_success_login"
    assert event["user"] == "bastien"
    assert event["source_ip"] == "192.168.1.42"
    assert event["port"] == "50110"


def test_parse_web_access_log() -> None:
    line = '185.12.45.10 - - [24/Jun/2026:11:01:12 +0000] "GET /admin HTTP/1.1" 404 512 "-" "curl/8.0"'

    event = parse_web_log_line(line)

    assert event["event_type"] == "web_access"
    assert event["source_ip"] == "185.12.45.10"
    assert event["method"] == "GET"
    assert event["path"] == "/admin"
    assert event["status"] == 404
    assert event["user_agent"] == "curl/8.0"
