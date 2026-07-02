from dataclasses import dataclass
from pathlib import Path
from typing import Any

from detection.log_parser import load_ssh_logs, load_web_logs
from detection.rules_engine import (
    detect_prompt_injection_attempt,
    detect_ssh_bruteforce,
    detect_web_reconnaissance,
)

DEFAULT_DATA_DIR = Path("data/sample_logs")


@dataclass(frozen=True)
class GroundTruthCase:
    """
    Expected alert labels for one versioned sample log file.
    """

    log_file: str
    log_type: str
    expected_alert_types: frozenset[str]


@dataclass(frozen=True)
class GroundTruthEvaluationResult:
    """
    Comparison between expected alert labels and observed alert labels.
    """

    log_file: str
    expected_alert_types: frozenset[str]
    observed_alert_types: frozenset[str]
    missing_alert_types: frozenset[str]
    unexpected_alert_types: frozenset[str]

    @property
    def passed(self) -> bool:
        return not self.missing_alert_types and not self.unexpected_alert_types


GROUND_TRUTH_CASES = (
    GroundTruthCase(
        log_file="ssh_auth.log",
        log_type="ssh",
        expected_alert_types=frozenset({"SSH_BRUTE_FORCE"}),
    ),
    GroundTruthCase(
        log_file="web_access.log",
        log_type="web",
        expected_alert_types=frozenset(
            {"WEB_RECONNAISSANCE", "PROMPT_INJECTION_ATTEMPT"}
        ),
    ),
    GroundTruthCase(
        log_file="benign_ssh_auth.log",
        log_type="ssh",
        expected_alert_types=frozenset(),
    ),
    GroundTruthCase(
        log_file="benign_web_access.log",
        log_type="web",
        expected_alert_types=frozenset(),
    ),
)


def get_alert_types(alerts: list[dict[str, Any]]) -> frozenset[str]:
    """
    Extract alert types from generated alert dictionaries.
    """
    alert_types = set()

    for alert in alerts:
        alert_type = alert.get("alert_type")

        if isinstance(alert_type, str):
            alert_types.add(alert_type)

    return frozenset(alert_types)


def detect_alerts_for_case(
    ground_truth_case: GroundTruthCase,
    data_dir: Path | str = DEFAULT_DATA_DIR,
) -> list[dict[str, Any]]:
    """
    Run the relevant detection rules for a ground truth case.
    """
    data_path = Path(data_dir)
    log_path = data_path / ground_truth_case.log_file

    if ground_truth_case.log_type == "ssh":
        ssh_events = load_ssh_logs(str(log_path))
        return detect_ssh_bruteforce(ssh_events)

    if ground_truth_case.log_type == "web":
        web_events = load_web_logs(str(log_path))
        return [
            *detect_web_reconnaissance(web_events),
            *detect_prompt_injection_attempt(web_events),
        ]

    raise ValueError(f"Unsupported log type: {ground_truth_case.log_type}")


def evaluate_ground_truth_case(
    ground_truth_case: GroundTruthCase,
    data_dir: Path | str = DEFAULT_DATA_DIR,
) -> GroundTruthEvaluationResult:
    """
    Compare observed alerts with the expected labels for one log file.
    """
    alerts = detect_alerts_for_case(ground_truth_case, data_dir)
    observed_alert_types = get_alert_types(alerts)

    missing_alert_types = ground_truth_case.expected_alert_types - observed_alert_types
    unexpected_alert_types = observed_alert_types - ground_truth_case.expected_alert_types

    return GroundTruthEvaluationResult(
        log_file=ground_truth_case.log_file,
        expected_alert_types=ground_truth_case.expected_alert_types,
        observed_alert_types=observed_alert_types,
        missing_alert_types=missing_alert_types,
        unexpected_alert_types=unexpected_alert_types,
    )


def evaluate_all_ground_truth_cases(
    data_dir: Path | str = DEFAULT_DATA_DIR,
) -> list[GroundTruthEvaluationResult]:
    """
    Evaluate all versioned sample logs against their expected labels.
    """
    return [
        evaluate_ground_truth_case(ground_truth_case, data_dir)
        for ground_truth_case in GROUND_TRUTH_CASES
    ]


def has_ground_truth_failures(
    results: list[GroundTruthEvaluationResult],
) -> bool:
    """
    Return True when at least one ground truth comparison failed.
    """
    return any(not result.passed for result in results)
