import argparse
import json
from collections.abc import Mapping
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ai_assistant.llm_client import get_ollama_model_metadata, query_ollama
from research.cicids2017_ai import (
    AIQuery,
    DEFAULT_AI_NUM_PREDICT,
    DEFAULT_AI_SEED,
    DEFAULT_AI_TEMPERATURE,
    evaluate_ai_method,
)
from research.cicids2017_baseline import evaluate_baseline
from research.cicids2017_selection import build_selection_manifest
from research.cicids2017_validate import inspect_dataset


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def run_benchmark(
    csv_path: Path,
    output_dir: Path,
    model: str,
    base_url: str = "http://localhost:11434",
    rows_per_class: int = 100,
    temperature: float = DEFAULT_AI_TEMPERATURE,
    seed: int = DEFAULT_AI_SEED,
    num_predict: int = DEFAULT_AI_NUM_PREDICT,
    query: AIQuery | None = None,
    model_metadata: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Run the frozen CIC-IDS2017 v1 benchmark and persist all evidence artifacts."""
    if num_predict <= 0:
        raise ValueError("num_predict must be greater than zero")

    output_dir.mkdir(parents=True, exist_ok=True)

    dataset_manifest = inspect_dataset(csv_path)
    dataset_manifest_path = output_dir / "dataset_manifest.json"
    _write_json(dataset_manifest_path, dataset_manifest)

    selection_manifest = build_selection_manifest(
        csv_path,
        rows_per_class=rows_per_class,
    )
    selection_manifest_path = output_dir / "evaluation_selection.json"
    _write_json(selection_manifest_path, selection_manifest)

    baseline_result = evaluate_baseline(
        csv_path,
        selection_manifest=selection_manifest_path,
    )
    baseline_path = output_dir / "baseline.json"
    _write_json(baseline_path, baseline_result)

    resolved_model_metadata = (
        dict(model_metadata)
        if model_metadata is not None
        else get_ollama_model_metadata(model, base_url)
    )
    if resolved_model_metadata is None:
        raise ValueError(
            "could not resolve the local Ollama model digest; "
            "refusing to run a scored benchmark without frozen model metadata"
        )

    generation_options = {
        "temperature": temperature,
        "seed": seed,
        "num_predict": num_predict,
    }

    query_fn = query
    if query_fn is None:

        def default_query(prompt: str) -> str | None:
            return query_ollama(
                prompt,
                model=model,
                base_url=base_url,
                options=generation_options,
            )

        query_fn = default_query

    ai_result = evaluate_ai_method(
        csv_path=csv_path,
        max_scored_rows=int(selection_manifest["selected_row_count"]),
        query=query_fn,
        selection_manifest=selection_manifest_path,
    )
    ai_result["model_runtime"] = resolved_model_metadata
    ai_result["generation_options"] = generation_options
    ai_result["base_url"] = base_url
    ai_path = output_dir / "ai.json"
    _write_json(ai_path, ai_result)

    summary = {
        "schema_version": 1,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "dataset_sha256": dataset_manifest["sha256"],
        "selected_row_count": selection_manifest["selected_row_count"],
        "selection_rule": selection_manifest["selection_rule"],
        "model": {
            "requested": model,
            "digest": resolved_model_metadata.get("digest"),
            "ollama_version": resolved_model_metadata.get("ollama_version"),
        },
        "generation_options": generation_options,
        "baseline_metrics": baseline_result["metrics"],
        "ai_metrics": ai_result["metrics"],
        "model_failures": ai_result["model_failures"],
        "artifacts": {
            "dataset_manifest": dataset_manifest_path.name,
            "selection_manifest": selection_manifest_path.name,
            "baseline": baseline_path.name,
            "ai": ai_path.name,
        },
    }
    _write_json(output_dir / "benchmark_summary.json", summary)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Run the frozen CIC-IDS2017 v1 benchmark and write all evidence artifacts."
        )
    )
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--model", required=True)
    parser.add_argument("--base-url", default="http://localhost:11434")
    parser.add_argument("--rows-per-class", type=int, default=100)
    parser.add_argument("--temperature", type=float, default=DEFAULT_AI_TEMPERATURE)
    parser.add_argument("--seed", type=int, default=DEFAULT_AI_SEED)
    parser.add_argument("--num-predict", type=int, default=DEFAULT_AI_NUM_PREDICT)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("research/results"),
    )
    args = parser.parse_args()

    try:
        summary = run_benchmark(
            csv_path=args.csv_path,
            output_dir=args.output_dir,
            model=args.model,
            base_url=args.base_url,
            rows_per_class=args.rows_per_class,
            temperature=args.temperature,
            seed=args.seed,
            num_predict=args.num_predict,
        )
    except ValueError as error:
        parser.error(str(error))

    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
