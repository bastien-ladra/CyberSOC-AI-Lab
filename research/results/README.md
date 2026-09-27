# Benchmark result artifacts

This directory is reserved for **machine-generated** benchmark evidence.

Do not commit invented, hand-edited or selectively copied metrics.

Expected release artifacts:

- `dataset_manifest.json` — exact local source file, SHA-256, row count and label distribution.
- `baseline.json` — deterministic reference metrics and latency.
- `ai.json` — local-Ollama metrics, latency and model-failure count.
- optional failure-case export containing only non-sensitive/public benchmark identifiers and predictions.

Each scored result must be traceable to:

- repository commit SHA;
- CIC-IDS2017 source-file SHA-256;
- frozen row-selection rule;
- method configuration;
- AI model/version identifier where applicable;
- run timestamp and environment metadata;
- precision, recall, F1, false-positive rate, false-negative rate and confusion counts;
- latency measurement;
- model/parse failures for the AI method.

The human-readable interpretation belongs in `../REPORT.md`. A result is not evidence merely because it exists in this directory; it must match the preregistered protocol and frozen dataset manifest.
