from pathlib import Path

from utils.ground_truth_evaluator import (
    DEFAULT_DATA_DIR,
    GROUND_TRUTH_CASES,
    GroundTruthCase,
    evaluate_all_ground_truth_cases,
    evaluate_ground_truth_case,
    get_alert_types,
    has_ground_truth_failures,
)


def test_ground_truth_cases_cover_versioned_sample_logs() -> None:
    log_files = {ground_truth_case.log_file for ground_truth_case in GROUND_TRUTH_CASES}

    assert log_files == {
        "ssh_auth.log",
        "web_access.log",
        "benign_ssh_auth.log",
        "benign_web_access.log",
    }


def test_ground_truth_evaluation_passes_for_versioned_sample_logs() -> None:
    results = evaluate_all_ground_truth_cases()

    assert len(results) == 4
    assert has_ground_truth_failures(results) is False
    assert all(result.passed for result in results)


def test_ground_truth_evaluation_detects_missing_expected_label() -> None:
    ground_truth_case = GroundTruthCase(
        log_file="benign_web_access.log",
        log_type="web",
        expected_alert_types=frozenset({"WEB_RECONNAISSANCE"}),
    )

    result = evaluate_ground_truth_case(ground_truth_case)

    assert result.passed is False
    assert result.missing_alert_types == frozenset({"WEB_RECONNAISSANCE"})
    assert result.unexpected_alert_types == frozenset()


def test_ground_truth_evaluation_detects_unexpected_label() -> None:
    ground_truth_case = GroundTruthCase(
        log_file="web_access.log",
        log_type="web",
        expected_alert_types=frozenset({"WEB_RECONNAISSANCE"}),
    )

    result = evaluate_ground_truth_case(ground_truth_case)

    assert result.passed is False
    assert result.missing_alert_types == frozenset()
    assert result.unexpected_alert_types == frozenset({"PROMPT_INJECTION_ATTEMPT"})


def test_get_alert_types_ignores_invalid_alert_type_values() -> None:
    alerts = [
        {"alert_type": "SSH_BRUTE_FORCE"},
        {"alert_type": None},
        {"alert_type": 123},
        {"unexpected": "ignored"},
    ]

    assert get_alert_types(alerts) == frozenset({"SSH_BRUTE_FORCE"})


def test_ground_truth_evaluator_accepts_custom_data_dir() -> None:
    results = evaluate_all_ground_truth_cases(Path(DEFAULT_DATA_DIR))

    assert all(result.passed for result in results)
