import json
from pathlib import Path
from typing import Any

from utils.ground_truth_evaluator import GroundTruthEvaluationResult
from utils.ground_truth_results_exporter import (
    JSON_FILE_NAME,
    MARKDOWN_FILE_NAME,
    build_ground_truth_results_markdown,
    build_ground_truth_results_payload,
    format_alert_types,
    serialize_ground_truth_result,
    write_ground_truth_results,
)


def make_result(
    log_file: str = "ssh_auth.log",
    expected_alert_types: frozenset[str] = frozenset({"SSH_BRUTE_FORCE"}),
    observed_alert_types: frozenset[str] = frozenset({"SSH_BRUTE_FORCE"}),
) -> GroundTruthEvaluationResult:
    return GroundTruthEvaluationResult(
        log_file=log_file,
        expected_alert_types=expected_alert_types,
        observed_alert_types=observed_alert_types,
        missing_alert_types=expected_alert_types - observed_alert_types,
        unexpected_alert_types=observed_alert_types - expected_alert_types,
    )


def test_format_alert_types_returns_aucun_for_empty_labels() -> None:
    assert format_alert_types(frozenset()) == "Aucun"


def test_format_alert_types_sorts_labels() -> None:
    assert format_alert_types(frozenset({"B_LABEL", "A_LABEL"})) == "A_LABEL, B_LABEL"


def test_serialize_ground_truth_result_sorts_alert_types() -> None:
    result = make_result(
        expected_alert_types=frozenset({"B_LABEL", "A_LABEL"}),
        observed_alert_types=frozenset({"B_LABEL"}),
    )

    serialized = serialize_ground_truth_result(result)

    assert serialized["log_file"] == "ssh_auth.log"
    assert serialized["expected_alert_types"] == ["A_LABEL", "B_LABEL"]
    assert serialized["observed_alert_types"] == ["B_LABEL"]
    assert serialized["missing_alert_types"] == ["A_LABEL"]
    assert serialized["unexpected_alert_types"] == []
    assert serialized["passed"] is False


def test_build_ground_truth_results_payload_contains_summary() -> None:
    results = [
        make_result(log_file="ssh_auth.log"),
        make_result(
            log_file="web_access.log",
            expected_alert_types=frozenset({"WEB_RECONNAISSANCE"}),
            observed_alert_types=frozenset(),
        ),
    ]

    payload = build_ground_truth_results_payload(
        results,
        generated_at="2026-01-01T00:00:00+00:00",
    )

    assert payload["generated_at"] == "2026-01-01T00:00:00+00:00"
    assert payload["summary"] == {
        "total": 2,
        "passed": 1,
        "failed": 1,
        "status": "failed",
    }
    assert len(payload["results"]) == 2


def test_build_ground_truth_results_markdown_contains_table() -> None:
    markdown = build_ground_truth_results_markdown(
        [make_result()],
        generated_at="2026-01-01T00:00:00+00:00",
    )

    assert "# CyberSOC-AI-Lab — Résultats vérité terrain" in markdown
    assert "Statut : `PASSED`" in markdown
    assert "ssh_auth.log" in markdown
    assert "SSH_BRUTE_FORCE" in markdown
    assert "| Fichier | Labels attendus | Labels observés" in markdown


def test_write_ground_truth_results_creates_json_and_markdown(tmp_path: Path) -> None:
    result = make_result()

    paths = write_ground_truth_results(
        results=[result],
        output_dir=tmp_path,
        generated_at="2026-01-01T00:00:00+00:00",
    )

    json_path = tmp_path / JSON_FILE_NAME
    markdown_path = tmp_path / MARKDOWN_FILE_NAME

    assert paths == {"json": json_path, "markdown": markdown_path}
    assert json_path.exists()
    assert markdown_path.exists()

    payload: dict[str, Any] = json.loads(json_path.read_text(encoding="utf-8"))

    assert payload["summary"]["status"] == "passed"
    assert payload["results"][0]["log_file"] == "ssh_auth.log"
    assert "Résultats vérité terrain" in markdown_path.read_text(encoding="utf-8")
