# Benchmark protocol

Status: **dataset source and deterministic baseline selected; AI configuration and final frozen evaluation manifest remain TBD**.

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

The following must be committed before the first scored AI run:

- Ollama model name and immutable model/version identifier where available;
- prompt template;
- decoding/generation settings;
- exact input-field allowlist;
- parser for the binary recommendation;
- timeout/failure policy;
- fixed evaluation rows shared with the baseline.

These values remain **TBD** until the exact dataset file is frozen. No AI metric may be interpreted before that commit.

## 3. Dataset and evaluation set

Dataset source: **CIC-IDS2017**, Canadian Institute for Cybersecurity, University of New Brunswick. See `DATASET.md`.

Before scoring, `research/cicids2017_validate.py` must record:

- exact local file name;
- SHA-256;
- row count;
- label distribution;
- presence of both v1 classes.

The exact evaluation sampling/splitting rule must be committed after inspecting metadata but **before** looking at method results. The baseline and AI-assisted method must score the same frozen evaluation rows.

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
- Fixed selection/split rule.
- Fixed model/version and configuration for AI runs.
- Machine-readable run metadata.
- Same evaluation rows for compared methods.
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

Each scored run must export machine-readable metrics and metadata under `research/results/`, including repository commit SHA, dataset SHA-256, method configuration, run timestamp and latency measurement. `REPORT.md` will contain interpretation, limitations and non-claims.
