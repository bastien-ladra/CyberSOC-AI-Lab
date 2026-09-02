# Reproducible SOC AI benchmark

This directory contains the research-evidence workflow used to compare a transparent deterministic triage baseline with a bounded local-Ollama decision-support method.

## Current status

- Dataset source selected: CIC-IDS2017.
- v1 labels: `BENIGN` and `SSH-Patator` only.
- Deterministic baseline implemented.
- Binary metrics implemented without external ML dependencies.
- Local-Ollama runner implemented with a label-free input allowlist and strict JSON response validation.
- No benchmark result is claimed until the exact local dataset file and evaluation rows are frozen.

## 1. Obtain the dataset

Use the official CIC-IDS2017 source documented in `DATASET.md`. Keep raw data outside the repository.

## 2. Validate and freeze provenance

```bash
python -m research.cicids2017_validate /path/to/labelled_flows.csv \
  --output research/results/dataset_manifest.json
```

Review the manifest, then commit the exact SHA-256, row distribution and final evaluation-selection rule before interpreting results.

## 3. Run the deterministic baseline

```bash
python -m research.cicids2017_baseline /path/to/labelled_flows.csv \
  --output research/results/baseline.json
```

The baseline is deliberately fixed as TCP destination port 22 -> escalate. Do not tune it after viewing results.

## 4. Run the local AI method

Start Ollama locally with the preregistered model, then run a bounded evaluation:

```bash
python -m research.cicids2017_ai /path/to/labelled_flows.csv \
  --max-scored-rows 200 \
  --model llama3.2 \
  --output research/results/ai.json
```

The final value of `--max-scored-rows`, the exact row-selection rule and the model/version identifier must be frozen before a scored comparison is treated as evidence.

## 5. Interpret results

Use `REPORT.md`. Report precision, recall, F1, false-positive rate, false-negative rate, latency, model failures and representative failure cases. A negative result is valid evidence; do not post-hoc tune the experiment solely to force the AI method to win.

## Safety and research integrity

- Dataset labels are never included in the AI prompt.
- Unsupported CIC-IDS2017 labels are excluded rather than treated as benign.
- Raw datasets are not committed.
- AI output is decision support only and must explicitly preserve human validation.
- No autonomous remediation is evaluated or claimed.
