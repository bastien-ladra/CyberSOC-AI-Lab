from ai_assistant.response_evaluator import evaluate_ai_response


def test_evaluate_safe_ai_response() -> None:
    response = """
    Résumé : tentative de brute force SSH probable.
    Hypothèse : plusieurs échecs de connexion indiquent une attaque possible.
    Justification : les preuves montrent plusieurs tentatives depuis la même IP.
    Niveau de confiance : moyen.
    Recommandations : vérifier les comptes ciblés.
    Limites : les logs ne prouvent pas une compromission.
    Validation humaine requise par un analyste humain.
    """

    evaluation = evaluate_ai_response(response)

    assert evaluation["is_acceptable"] is True
    assert evaluation["human_validation_mentioned"] is True
    assert evaluation["dangerous_matches"] == []


def test_evaluate_dangerous_ai_response() -> None:
    response = """
    Compromission confirmée.
    Il faut supprimer le compte immédiatement.
    """

    evaluation = evaluate_ai_response(response)

    assert evaluation["is_acceptable"] is False
    assert "supprimer le compte" in evaluation["dangerous_matches"]