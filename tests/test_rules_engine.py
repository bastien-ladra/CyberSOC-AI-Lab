from detection.rules_engine import detect_ssh_bruteforce, detect_web_reconnaissance


def test_detect_ssh_bruteforce() -> None:
    events = [
        {
            "event_type": "ssh_failed_login",
            "user": f"user{i}",
            "source_ip": "185.12.45.10",
            "port": str(50000 + i),
            "raw": f"failed login {i}",
        }
        for i in range(6)
    ]

    alerts = detect_ssh_bruteforce(events, threshold=5)

    assert len(alerts) == 1
    assert alerts[0]["alert_type"] == "SSH_BRUTE_FORCE"
    assert alerts[0]["severity"] == "HIGH"
    assert alerts[0]["source_ip"] == "185.12.45.10"
    assert alerts[0]["failed_attempts"] == 6
    assert alerts[0]["human_validation_required"] is True


def test_no_ssh_bruteforce_below_threshold() -> None:
    events = [
        {
            "event_type": "ssh_failed_login",
            "user": f"user{i}",
            "source_ip": "185.12.45.10",
            "port": str(50000 + i),
            "raw": f"failed login {i}",
        }
        for i in range(3)
    ]

    alerts = detect_ssh_bruteforce(events, threshold=5)

    assert alerts == []


def test_detect_web_reconnaissance() -> None:
    events = [
        {
            "event_type": "web_access",
            "source_ip": "185.12.45.10",
            "method": "GET",
            "path": path,
            "status": 404,
            "user_agent": "curl/8.0",
            "raw": f"GET {path}",
        }
        for path in ["/admin", "/wp-admin", "/.env", "/phpmyadmin", "/backup.zip", "/config.php"]
    ]

    alerts = detect_web_reconnaissance(events, threshold=5)

    assert len(alerts) == 1
    assert alerts[0]["alert_type"] == "WEB_RECONNAISSANCE"
    assert alerts[0]["severity"] == "MEDIUM"
    assert alerts[0]["source_ip"] == "185.12.45.10"
    assert alerts[0]["suspicious_requests"] == 6
    assert alerts[0]["human_validation_required"] is True