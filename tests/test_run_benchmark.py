import csv
import json
from pathlib import Path

from research.run_benchmark import run_benchmark

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


def test_run_benchmark_writes_reproducible_evidence_bundle(
    tmp_path: Path,
) -> None:
    csv_path = tmp_path / "Tuesday-WorkingHours.pcap_ISCX.csv"
    rows = [
        [
            "t1",
            "192.0.2.1",
            "192.0.2.20",
            "50000",
            "22",
            "6",
            "100",
            "SSH-Patator",
        ],
        [
            "t2",
            "192.0.2.2",
            "192.0.2.20",
            "50001",
            "443",
            "6",
            "200",
            "BENIGN",
        ],
        [
            "t3",
            "192.0.2.3",
            "192.0.2.20",
            "50002",
            "22",
            "6",
            "300",
            "SSH-Patator",
        ],
        [
            "t4",
            "192.0.2.4",
            "192.0.2.20",
            "50003",
            "80",
            "6",
            "400",
            "BENIGN",
        ],
    ]

    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(FIELDNAMES)
        writer.writerows(rows)

    def fake_query(prompt: str) -> str:
        escalate = '"destination port": "22"' in prompt
        return json.dumps(
            {
                "decision": "ESCALATE" if escalate else "DO_NOT_ESCALATE",
                "confidence": 0.9,
                "rationale": "Synthetic deterministic test response.",
                "human_validation_required": True,
            }
        )

    output_dir = tmp_path / "results"
    summary = run_benchmark(
        csv_path=csv_path,
        output_dir=output_dir,
        model="llama-test:3b",
        rows_per_class=1,
        query=fake_query,
        model_metadata={
            "requested_model": "llama-test:3b",
            "resolved_name": "llama-test:3b",
            "resolved_model": "llama-test:3b",
            "digest": "sha256-test",
            "ollama_version": "0.12.0",
        },
    )

    assert summary["selected_row_count"] == 2
    assert summary["model"]["digest"] == "sha256-test"
    assert summary["baseline_metrics"]["f1"] == 1.0
    assert summary["ai_metrics"]["f1"] == 1.0

    expected_artifacts = {
        "dataset_manifest.json",
        "evaluation_selection.json",
        "baseline.json",
        "ai.json",
        "benchmark_summary.json",
    }
    assert {path.name for path in output_dir.iterdir()} == expected_artifacts

    ai_result = json.loads((output_dir / "ai.json").read_text(encoding="utf-8"))
    assert ai_result["model_runtime"]["digest"] == "sha256-test"
    assert ai_result["selection"]["selected_row_count"] == 2
