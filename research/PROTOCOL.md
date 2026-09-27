# Benchmark protocol

Status: **dataset source, deterministic baseline and evaluation-row selection rule are frozen; exact dataset file and local AI model configuration remain TBD**.

## 1. Research target

Benchmark v1 is a binary SOC-triage task over the explicitly supported CIC-IDS2017 labels:

- positive / escalate: `SSH-Patator` -> `SSH_BRUTE_FORCE`;
- negative / do not escalate: `BENIGN`.

All other CIC-IDS2017 labels are excluded from v1 scoring. They must never be silently converted into negative examples.

## 2. Compared methods

### Deterministic baseline — locked before scored results

The reference baseline is intentionally simple and transparent:

`ESCALATE = protocol == TCP AND destination_port == 22`

Implementation: `research/cicids2017_baseline.py`.

This baseline is not presented as a production detector. It establishes a reproducible reference point that uses no model and no hidden parameters. Its likely false positives on legitimate SSH traffic are part of the experiment rather than something to tune away after viewing results.

### AI-assisted method

One local Ollama-assisted triage method will produce a binary recommendation plus a short rationale from **non-label input fields only**. The final operational decision remains conceptually human-approved; the benchmark measures recommendation quality, not autonomous response.

Implementation scaffold: `research/cicids2017_ai.py`.

The v1 runner fixes these integrity constraints:

- explicit input-field allowlist;
- dataset label excluded from model input;
- strict JSON response schema;
- explicit `human_validation_required: true` requirement;
- bounded maximum of 500 scored records per invocation;
- timeout, missing response or invalid JSON is recorded as a model failure and counted operationally as `DO_NOT_ESCALATE`.

The following must still be committed before the first scored AI comparison:

- exact Ollama model identifier/digest where available;
- final model invocation/generation configuration supported by the local runtime;
- exact CIC-IDS2017 file name and SHA-256.

No AI metric may be interpreted before those values are frozen.

## 3. Dataset and frozen evaluation selection

Dataset source: **CIC-IDS2017**, Canadian Institute for Cybersecurity, University of New Brunswick. See `DATASET.md`.

Before scoring, `research/cicids2017_validate.py` records:

- exact local file name;
- SHA-256;
- row count;
- label distribution;
- presence of both v1 classes.

The benchmark v1 row-selection rule is now preregistered and implemented in `research/cicids2017_selection.py`:

1. use only supported labels `BENIGN` and `SSH-Patator`;
2. require at least 100 rows from each class;
3. canonicalize every candidate CSV row;
4. compute SHA-256 for each canonical row;
5. within each class, select the 100 rows with the lexicographically smallest row hashes;
6. combine the two classes into a 200-row evaluation set;
7. evaluate those exact selected row numbers in original source order;
8. bind the manifest to the exact dataset SHA-256.

This rule is deterministic, balanced and independent of source-file ordering. It is fixed before any benchmark result is interpreted. If either class has fewer than 100 rows, benchmark v1 fails rather than silently changing sample size.

Generate the frozen manifest with:

```bash
python -m research.cicids2017_selection /path/to/labelled_flows.csv \
  --rows-per-class 100 \
  --output research/results/evaluation_selection.json
```

Both the baseline and AI-assisted method must consume the same manifest.

## 4. Primary metrics

Machine-computed metrics are implemented in `research/metrics.py`:

- precision;
- recall;
- F1 score;
- false-positive rate;
- false-negative rate;
- confusion counts (TP, TN, FP, FN);
- decision latency measured separately by each runner.

No manual metric transcription is considered source evidence.

## 5. Reproducibility controls

- Fixed dependency versions from the repository lockfiles.
- Fixed dataset file SHA-256 or immutable retrieval manifest.
- Fixed deterministic balanced row-selection rule.
- Frozen row manifest shared by both compared methods.
- Fixed model/version and configuration for AI runs.
- Machine-readable run metadata.
- No raw public dataset committed into the repository.
- Clean-environment reproduction commands documented before release.

## 6. Acceptance and interpretation rules

No claim of improvement will be made solely from a higher aggregate F1. Interpretation must consider false negatives, false positives, latency and failure cases together.

There is **no predeclared requirement that the AI method must beat the baseline**. A null or negative result remains publishable evidence if the protocol was followed. This prevents post-hoc tuning solely to manufacture a positive result.

## 7. Failure-case analysis

After metrics are generated, inspect at least:

- false positives on benign SSH-like traffic;
- false negatives on `SSH-Patator` rows;
- cases where baseline and AI disagree;
- AI parse failures/timeouts;
- cases with ambiguous or insufficient evidence.

Do not remove difficult records from the frozen evaluation set after results are known.

## 8. Reporting

Each scored run must export machine-readable metrics and metadata under `research/results/`, including repository commit SHA, dataset SHA-256, selection rule/manifest, method configuration, run timestamp and latency measurement. `REPORT.md` will contain interpretation, limitations and non-claims.
