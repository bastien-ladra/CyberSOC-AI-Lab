# Benchmark result artifacts

This directory is reserved for **machine-generated** benchmark outputs.

Do not commit invented, hand-edited or selectively copied metrics as evidence.

Each scored run should record at minimum:

- Repository commit SHA.
- Dataset name/version.
- Baseline configuration.
- AI method/model/version/configuration.
- Random seed where applicable.
- Precision, recall, F1, false-positive rate and false-negative rate.
- Decision latency measurement method and result.
- Confusion matrix or equivalent class-level evidence.
- Run timestamp and environment/dependency metadata.

Recommended formats: JSON or CSV for metrics plus a small metadata JSON file. The human-readable interpretation belongs in `../REPORT.md`.