import csv
import json
from pathlib import Path

import pytest

from research.cicids2017_ai import (
    build_ai_features,
    build_ai_prompt,
    evaluate_ai_method,
    parse_ai_response,
)
from research.cicids2017_selection import build_selection_manifest

FIELDNAMES = [
    "Timestamp",
    "Source IP",
    "Destination IP",
    "Source Port",
    "Destination Port",
    "Protocol",
    "Flow Duration",
    "Label",
]


def test_build_ai_features_excludes_ground_truth_label() -> None:
    features = build_ai_features(
        {
            "Source IP": "192.0.2.1",
            "Destination Port": "22",
            "Flow Duration": "1234",
            "Label": "SSH-Patator",
            "Unexpected Secret": "do-not-pass",
        }
    )

    assert features == {
        "destination port": "22",
        "flow duration": "1234",
        "source ip": "192.0.2.1",
    }
    assert "SSH-Patator" not in build_ai_prompt(features)


def test_parse_ai_response_requires_strict_safe_schema() -> None:
    prediction, confidence, rationale = parse_ai_response(
        json.dumps(
            {
                "decision": "ESCALATE",
                "confidence": 0.8,
                "rationale": "Repeated SSH-like activity requires analyst review.",
                "human_validation_required": True,
            }
        )
    )

    assert prediction is True
    assert confidence == pytest.approx(0.8)
    assert "analyst" in rationale


def test_parse_ai_response_rejects_missing_human_validation() -> None:
    with pytest.raises(ValueError, match="human validation"):
        parse_ai_response(
            json.dumps(
                {
                    "decision": "DO_NOT_ESCALATE",
                    "confidence": 0.6,
                    "rationale": "Insufficient evidence.",
                    "human_validation_required": False,
                }
            )
        )


def test_evaluate_ai_method_uses_failure_as_no_escalation(tmp_path: Path) -> None:
    csv_path = tmp_path / "cicids.csv"
    rows = [
        [
            "2017-07-04 14:00:00",
            "192.0.2.1",
            "192.0.2.20",
            "50000",
            "22",
            "6",
            "100",
            "SSH-Patator",
        ],
        [
            "2017-07-04 14:00:01",
            "192.0.2.2",
            "192.0.2.20",
            "50001",
            "443",
            "6",
            "200",
            "BENIGN",
        ],
    ]

    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(FIELDNAMES)
        writer.writerows(rows)

    responses = iter(
        [
            json.dumps(
                {
                    "decision": "ESCALATE",
                    "confidence": 0.9,
                    "rationale": "Suspicious SSH flow.",
                    "human_validation_required": True,
                }
            ),
            None,
        ]
    )

    result = evaluate_ai_method(
        csv_path,
        max_scored_rows=2,
        query=lambda _prompt: next(responses),
    )

    assert result["scored_rows"] == 2
    assert result["model_failures"] == 1
    assert result["metrics"]["true_positive"] == 1
    assert result["metrics"]["true_negative"] == 1


def test_evaluate_ai_method_consumes_same_frozen_selection(tmp_path: Path) -> None:
    csv_path = tmp_path / "cicids.csv"
    rows = [
        ["t1", "192.0.2.1", "192.0.2.20", "50000", "22", "6", "100", "SSH-Patator"],
        ["t2", "192.0.2.2", "192.0.2.20", "50001", "443", "6", "200", "BENIGN"],
        ["t3", "192.0.2.3", "192.0.2.20", "50002", "22", "6", "300", "SSH-Patator"],
        ["t4", "192.0.2.4", "192.0.2.20", "50003", "80", "6", "400", "BENIGN"],
    ]

    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(FIELDNAMES)
        writer.writerows(rows)

    manifest = build_selection_manifest(csv_path, rows_per_class=1)
    manifest_path = tmp_path / "selection.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    responses = iter(
        [
            json.dumps(
                {
                    "decision": "ESCALATE",
                    "confidence": 0.7,
                    "rationale": "Analyst review recommended.",
                    "human_validation_required": True,
                }
            ),
            json.dumps(
                {
                    "decision": "DO_NOT_ESCALATE",
                    "confidence": 0.7,
                    "rationale": "No SSH brute-force evidence.",
                    "human_validation_required": True,
                }
            ),
        ]
    )

    result = evaluate_ai_method(
        csv_path,
        max_scored_rows=2,
        query=lambda _prompt: next(responses),
        selection_manifest=manifest_path,
    )

    assert result["scored_rows"] == 2
    assert result["selection"]["selected_row_count"] == 2
    assert result["selection"]["dataset_sha256"] == manifest["dataset_sha256"]
