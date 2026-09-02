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
        ["2017-07-04 14:00:00", "192.0.2.1", "192.0.2.20", "50000", "22", "6", "100", "SSH-Patator"],
        ["2017-07-04 14:00:01", "192.0.2.2", "192.0.2.20", "50001", "443", "6", "200", "BENIGN"],
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
