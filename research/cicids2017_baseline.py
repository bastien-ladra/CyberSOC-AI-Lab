import argparse
import csv
import json
from pathlib import Path
from time import perf_counter
from typing import Any

from research.metrics import compute_binary_metrics
from utils.cic_ids2017_sample_parser import parse_cic_ids2017_sample_row


def predict_ssh_port_baseline(protocol: str, destination_port: int) -> bool:
    """Transparent v1 baseline: escalate TCP flows targeting SSH port 22."""
    return protocol.upper() == "TCP" and destination_port == 22


def evaluate_baseline(
    csv_path: Path,
    max_rows: int | None = None,
) -> dict[str, Any]:
    if not csv_path.is_file():
        raise ValueError(f"dataset file does not exist: {csv_path}")
    if max_rows is not None and max_rows <= 0:
        raise ValueError("max_rows must be greater than zero")

    expected: list[bool] = []
    predicted: list[bool] = []
    rows_seen = 0
    scored_rows = 0
    unsupported_rows = 0
    prediction_latency_seconds = 0.0

    with csv_path.open(newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            if max_rows is not None and rows_seen >= max_rows:
                break
            rows_seen += 1

            event = parse_cic_ids2017_sample_row(row)
            if not event.is_supported_label:
                unsupported_rows += 1
                continue

            truth = event.expected_alert_type is not None
            started = perf_counter()
            prediction = predict_ssh_port_baseline(
                event.protocol,
                event.destination_port,
            )
            prediction_latency_seconds += perf_counter() - started

            expected.append(truth)
            predicted.append(prediction)
            scored_rows += 1

    if scored_rows == 0:
        raise ValueError("no supported CIC-IDS2017 v1 rows were available for scoring")

    metrics = compute_binary_metrics(expected, predicted)
    average_latency_ms = prediction_latency_seconds / scored_rows * 1000

    return {
        "method": "deterministic_ssh_port_baseline_v1",
        "rows_seen": rows_seen,
        "scored_rows": scored_rows,
        "unsupported_rows": unsupported_rows,
        "average_prediction_latency_ms": average_latency_ms,
        "metrics": metrics.to_dict(),
        "limitations": [
            "The baseline uses only protocol and destination port.",
            "Unsupported CIC-IDS2017 labels are excluded rather than treated as benign.",
            "This is a transparent reference baseline, not a production detector.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Evaluate the deterministic CIC-IDS2017 benchmark v1 baseline."
    )
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--max-rows", type=int, default=None)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    result = evaluate_baseline(args.csv_path, args.max_rows)
    serialized = json.dumps(result, indent=2, sort_keys=True)

    if args.output is None:
        print(serialized)
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized + "\n", encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
