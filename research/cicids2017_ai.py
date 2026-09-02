import argparse
import csv
import json
from pathlib import Path
from time import perf_counter
from typing import Any, Callable

from ai_assistant.llm_client import query_ollama
from research.metrics import compute_binary_metrics
from utils.cic_ids2017_sample_parser import (
    normalize_cic_ids2017_column_name,
    parse_cic_ids2017_sample_row,
)

MAX_AI_SCORED_ROWS = 500

ALLOWED_INPUT_FIELDS = {
    "timestamp",
    "source ip",
    "destination ip",
    "source port",
    "destination port",
    "protocol",
    "flow duration",
    "total fwd packets",
    "total backward packets",
    "flow bytes/s",
    "flow packets/s",
    "fwd packets/s",
    "bwd packets/s",
    "syn flag count",
    "ack flag count",
    "rst flag count",
    "psh flag count",
    "urg flag count",
    "average packet size",
    "packet length mean",
    "packet length std",
    "min packet length",
    "max packet length",
}

AIQuery = Callable[[str], str | None]


def build_ai_features(row: dict[str, object]) -> dict[str, str]:
    """Return an allowlisted, label-free feature dictionary for the model."""
    features: dict[str, str] = {}

    for raw_name, raw_value in row.items():
        normalized_name = normalize_cic_ids2017_column_name(raw_name)
        if normalized_name not in ALLOWED_INPUT_FIELDS:
            continue

        value = str(raw_value).strip()
        if not value:
            continue

        features[normalized_name] = value[:200]

    return dict(sorted(features.items()))


def build_ai_prompt(features: dict[str, str]) -> str:
    serialized_features = json.dumps(features, sort_keys=True, ensure_ascii=False)
    return (
        "You are a SOC triage decision-support model. "
        "Classify whether this network-flow record should be escalated for analyst review "
        "as a possible SSH brute-force event. The ground-truth dataset label is not provided. "
        "Use only the supplied fields. Do not invent evidence and do not recommend autonomous "
        "remediation. Return one JSON object and nothing else with exactly these keys: "
        '"decision" ("ESCALATE" or "DO_NOT_ESCALATE"), '
        '"confidence" (number from 0 to 1), "rationale" (short string), '
        '"human_validation_required" (true).\n\n'
        f"FLOW={serialized_features}"
    )


def parse_ai_response(response: str) -> tuple[bool, float, str]:
    try:
        payload = json.loads(response)
    except json.JSONDecodeError as error:
        raise ValueError("AI response is not strict JSON") from error

    if not isinstance(payload, dict):
        raise ValueError("AI response must be a JSON object")

    decision = payload.get("decision")
    if decision not in {"ESCALATE", "DO_NOT_ESCALATE"}:
        raise ValueError("AI response has an invalid decision")

    confidence = payload.get("confidence")
    if not isinstance(confidence, (int, float)) or isinstance(confidence, bool):
        raise ValueError("AI response confidence must be numeric")
    if not 0 <= float(confidence) <= 1:
        raise ValueError("AI response confidence must be between 0 and 1")

    rationale = payload.get("rationale")
    if not isinstance(rationale, str) or not rationale.strip():
        raise ValueError("AI response rationale must be a non-empty string")

    if payload.get("human_validation_required") is not True:
        raise ValueError("AI response must require human validation")

    return decision == "ESCALATE", float(confidence), rationale.strip()


def _default_query(model: str, base_url: str) -> AIQuery:
    def query(prompt: str) -> str | None:
        return query_ollama(prompt, model=model, base_url=base_url)

    return query


def evaluate_ai_method(
    csv_path: Path,
    max_scored_rows: int,
    query: AIQuery,
) -> dict[str, Any]:
    if not csv_path.is_file():
        raise ValueError(f"dataset file does not exist: {csv_path}")
    if max_scored_rows <= 0 or max_scored_rows > MAX_AI_SCORED_ROWS:
        raise ValueError(
            f"max_scored_rows must be between 1 and {MAX_AI_SCORED_ROWS}"
        )

    expected: list[bool] = []
    predicted: list[bool] = []
    rows_seen = 0
    scored_rows = 0
    unsupported_rows = 0
    model_failures = 0
    total_latency_seconds = 0.0

    with csv_path.open(newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            if scored_rows >= max_scored_rows:
                break
            rows_seen += 1

            event = parse_cic_ids2017_sample_row(row)
            if not event.is_supported_label:
                unsupported_rows += 1
                continue

            truth = event.expected_alert_type is not None
            features = build_ai_features(row)
            prompt = build_ai_prompt(features)

            started = perf_counter()
            response = query(prompt)
            total_latency_seconds += perf_counter() - started

            prediction = False
            if response is None:
                model_failures += 1
            else:
                try:
                    prediction, _, _ = parse_ai_response(response)
                except ValueError:
                    model_failures += 1

            expected.append(truth)
            predicted.append(prediction)
            scored_rows += 1

    if scored_rows == 0:
        raise ValueError("no supported CIC-IDS2017 v1 rows were available for scoring")

    metrics = compute_binary_metrics(expected, predicted)

    return {
        "method": "local_ollama_triage_v1",
        "rows_seen": rows_seen,
        "scored_rows": scored_rows,
        "unsupported_rows": unsupported_rows,
        "model_failures": model_failures,
        "failure_policy": "timeout/None/invalid JSON counts as DO_NOT_ESCALATE",
        "average_prediction_latency_ms": total_latency_seconds / scored_rows * 1000,
        "metrics": metrics.to_dict(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Evaluate bounded local-Ollama CIC-IDS2017 triage recommendations."
    )
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--max-scored-rows", type=int, required=True)
    parser.add_argument("--model", default="llama3.2")
    parser.add_argument("--base-url", default="http://localhost:11434")
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    result = evaluate_ai_method(
        csv_path=args.csv_path,
        max_scored_rows=args.max_scored_rows,
        query=_default_query(args.model, args.base_url),
    )
    result["model"] = args.model
    result["base_url"] = args.base_url
    serialized = json.dumps(result, indent=2, sort_keys=True)

    if args.output is None:
        print(serialized)
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized + "\n", encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
