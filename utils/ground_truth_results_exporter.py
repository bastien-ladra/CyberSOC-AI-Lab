import json
from collections.abc import Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from utils.ground_truth_evaluator import (
    GroundTruthEvaluationResult,
    evaluate_all_ground_truth_cases,
)

DEFAULT_EVALUATION_DIR = Path("runtime/evaluation")
JSON_FILE_NAME = "ground_truth_results.json"
MARKDOWN_FILE_NAME = "ground_truth_results.md"


def get_generated_at(generated_at: str | None = None) -> str:
    """
    Return a stable timestamp when provided or generate a UTC timestamp.
    """
    if generated_at is not None:
        return generated_at

    return datetime.now(timezone.utc).isoformat()


def format_alert_types(alert_types: frozenset[str]) -> str:
    """
    Format alert labels for Markdown output.
    """
    if not alert_types:
        return "Aucun"

    return ", ".join(sorted(alert_types))


def serialize_ground_truth_result(
    result: GroundTruthEvaluationResult,
) -> dict[str, Any]:
    """
    Serialize one ground truth comparison result for JSON output.
    """
    return {
        "log_file": result.log_file,
        "expected_alert_types": sorted(result.expected_alert_types),
        "observed_alert_types": sorted(result.observed_alert_types),
        "missing_alert_types": sorted(result.missing_alert_types),
        "unexpected_alert_types": sorted(result.unexpected_alert_types),
        "passed": result.passed,
    }


def build_ground_truth_results_payload(
    results: Sequence[GroundTruthEvaluationResult],
    generated_at: str | None = None,
) -> dict[str, Any]:
    """
    Build a JSON-serializable payload for ground truth evaluation results.
    """
    timestamp = get_generated_at(generated_at)
    passed_count = sum(1 for result in results if result.passed)
    failed_count = len(results) - passed_count

    return {
        "generated_at": timestamp,
        "summary": {
            "total": len(results),
            "passed": passed_count,
            "failed": failed_count,
            "status": "passed" if failed_count == 0 else "failed",
        },
        "results": [serialize_ground_truth_result(result) for result in results],
    }


def build_ground_truth_results_markdown(
    results: Sequence[GroundTruthEvaluationResult],
    generated_at: str | None = None,
) -> str:
    """
    Build a Markdown report for ground truth evaluation results.
    """
    timestamp = get_generated_at(generated_at)
    passed_count = sum(1 for result in results if result.passed)
    failed_count = len(results) - passed_count
    status = "PASSED" if failed_count == 0 else "FAILED"

    lines = [
        "# CyberSOC-AI-Lab — Résultats vérité terrain",
        "",
        f"Généré le : `{timestamp}`",
        "",
        "## Résumé",
        "",
        f"- Statut : `{status}`",
        f"- Cas évalués : {len(results)}",
        f"- Cas passants : {passed_count}",
        f"- Cas en échec : {failed_count}",
        "",
        "## Détail des comparaisons",
        "",
        "| Fichier | Labels attendus | Labels observés | Manquants | Inattendus | Résultat |",
        "|---|---|---|---|---|---|",
    ]

    for result in results:
        result_label = "OK" if result.passed else "ÉCHEC"
        lines.append(
            "| "
            + " | ".join(
                [
                    result.log_file,
                    format_alert_types(result.expected_alert_types),
                    format_alert_types(result.observed_alert_types),
                    format_alert_types(result.missing_alert_types),
                    format_alert_types(result.unexpected_alert_types),
                    result_label,
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Interprétation",
            "",
            "Un résultat `OK` signifie que les alertes observées correspondent aux labels attendus.",
            "Un résultat `ÉCHEC` doit être investigué avant de présenter la version comme stable.",
            "",
        ]
    )

    return "\n".join(lines)


def write_ground_truth_results(
    results: Sequence[GroundTruthEvaluationResult] | None = None,
    output_dir: Path | str = DEFAULT_EVALUATION_DIR,
    generated_at: str | None = None,
) -> dict[str, Path]:
    """
    Write ground truth evaluation results as JSON and Markdown files.
    """
    resolved_results = list(results) if results is not None else evaluate_all_ground_truth_cases()
    timestamp = get_generated_at(generated_at)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    json_path = output_path / JSON_FILE_NAME
    markdown_path = output_path / MARKDOWN_FILE_NAME

    payload = build_ground_truth_results_payload(resolved_results, timestamp)
    markdown = build_ground_truth_results_markdown(resolved_results, timestamp)

    json_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(markdown + "\n", encoding="utf-8")

    return {
        "json": json_path,
        "markdown": markdown_path,
    }
