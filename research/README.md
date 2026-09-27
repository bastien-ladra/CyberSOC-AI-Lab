# Reproducible SOC AI benchmark

This directory contains the research-evidence workflow used to compare a transparent deterministic triage baseline with a bounded local-Ollama decision-support method.

## Current status

- Dataset source selected: CIC-IDS2017.
- v1 labels: `BENIGN` and `SSH-Patator` only.
- Deterministic baseline implemented.
- Binary metrics implemented without external ML dependencies.
- Deterministic balanced evaluation-row selection implemented.
- Local-Ollama runner implemented with a label-free input allowlist and strict JSON response validation.
- The runner captures the exact local Ollama model digest/runtime version before scoring and refuses to run if it cannot resolve them.
- AI generation defaults are preregistered: temperature 0.0, seed 20260927, num_predict 128.
- No benchmark result is claimed until the exact local dataset file SHA-256 is frozen.

## 1. Obtain the dataset

Use the official CIC-IDS2017 source documented in `DATASET.md`. Keep raw data outside the repository.

## 2. Validate and freeze provenance

```bash
python -m research.cicids2017_validate /path/to/labelled_flows.csv \
  --output research/results/dataset_manifest.json
```

Review the manifest and keep the exact file SHA-256.

## 3. Freeze the exact evaluation rows

Benchmark v1 is preregistered as **100 BENIGN + 100 SSH-Patator** rows. Within each class, the selector chooses the 100 canonical rows with the smallest SHA-256 values, then evaluates the combined set in original source order.

```bash
python -m research.cicids2017_selection /path/to/labelled_flows.csv \
  --rows-per-class 100 \
  --output research/results/evaluation_selection.json
```

The selection manifest is bound to the exact dataset SHA-256. If the CSV changes, the benchmark refuses to use the old manifest.

## 4. Run the deterministic baseline

```bash
python -m research.cicids2017_baseline /path/to/labelled_flows.csv \
  --selection-manifest research/results/evaluation_selection.json \
  --output research/results/baseline.json
```

The baseline is deliberately fixed as TCP destination port 22 -> escalate. Do not tune it after viewing results.

## 5. Run the local AI method

Start Ollama locally with the preregistered model, then run the **same 200 frozen rows**:

```bash
python -m research.cicids2017_ai /path/to/labelled_flows.csv \
  --selection-manifest research/results/evaluation_selection.json \
  --max-scored-rows 200 \
  --model <local-ollama-model-name> \
  --temperature 0.0 \
  --seed 20260927 \
  --num-predict 128 \
  --output research/results/ai.json
```

Before scoring, the runner resolves the exact local model digest from Ollama and records it with the Ollama version and generation options in the result JSON. If no digest can be resolved, the scored run stops instead of producing ambiguous evidence.

## 6. Interpret results

Use `REPORT.md`. Report precision, recall, F1, false-positive rate, false-negative rate, latency, model failures and representative failure cases. A negative result is valid evidence; do not post-hoc tune the experiment solely to force the AI method to win.

## Safety and research integrity

- Dataset labels are never included in the AI prompt.
- Unsupported CIC-IDS2017 labels are excluded rather than treated as benign.
- Raw datasets are not committed.
- Baseline and AI score the exact same frozen rows.
- AI output is decision support only and must explicitly preserve human validation.
- No autonomous remediation is evaluated or claimed.
