from ai_assistant.incident_summarizer import build_incident_analysis_prompt


def test_build_incident_analysis_prompt_contains_alert_context() -> None:
    alert = {
        "alert_type": "SSH_BRUTE_FORCE",
        "severity": "HIGH",
        "source_ip": "185.12.45.10",
        "evidence": [
            "Failed password for invalid user admin from 185.12.45.10",
        ],
        "recommended_actions": [
            "Vérifier les comptes ciblés.",
        ],
        "human_validation_required": True,
    }

    prompt = build_incident_analysis_prompt(alert)

    assert "Tu es un assistant cybersécurité intégré dans un SOC." in prompt
    assert '"alert_type": "SSH_BRUTE_FORCE"' in prompt
    assert '"severity": "HIGH"' in prompt
    assert "Failed password for invalid user admin" in prompt
    assert "Vérifier les comptes ciblés." in prompt
    assert "Toujours rappeler qu'une validation humaine est nécessaire." in prompt


def test_build_incident_analysis_prompt_excludes_raw_lists_from_context_json() -> None:
    alert = {
        "alert_type": "WEB_RECONNAISSANCE",
        "evidence": ["GET /admin"],
        "recommended_actions": ["Corréler avec les logs applicatifs."],
    }

    prompt = build_incident_analysis_prompt(alert)
    context_section = prompt.split("## Preuves observées")[0]

    assert '"alert_type": "WEB_RECONNAISSANCE"' in context_section
    assert '"evidence"' not in context_section
    assert '"recommended_actions"' not in context_section
    assert "- GET /admin" in prompt
    assert "- Corréler avec les logs applicatifs." in prompt
