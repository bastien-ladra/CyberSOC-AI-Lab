# Benchmark protocol

Status: **preregistration scaffold — values marked TBD must be fixed before result interpretation**.

## 1. Compared methods

### Deterministic baseline
A transparent rules/scoring baseline must be defined from documented alert features. Exact rules and thresholds: **TBD after dataset selection**.

### AI-assisted method
One AI-assisted prioritization method will produce a suggested priority and, where applicable, a rationale. Model/provider/version, prompt/configuration and decoding settings: **TBD and must be pinned before scored runs**.

The final human-approved decision must remain separate from raw model output.

## 2. Evaluation set

Dataset/version: **TBD**.

The baseline and AI-assisted method must be evaluated on the same frozen evaluation records. Any tuning data must remain separate from the final evaluation set.

## 3. Primary metrics

- Precision.
- Recall.
- F1 score.
- False-positive rate.
- False-negative rate.
- Decision latency.

Where priority is multi-class, the report must state whether metrics are macro, micro or weighted and include the confusion matrix.

## 4. Reproducibility controls

- Fixed dependency versions.
- Fixed dataset/version or immutable retrieval manifest.
- Fixed random seeds where applicable.
- Recorded model/version and configuration.
- Machine-readable run metadata.
- Same input split for compared methods.
- Clean-environment reproduction command.

## 5. Acceptance criteria

No claim of improvement will be made solely from a higher aggregate F1. Interpretation must consider false negatives, false positives, latency and failure cases together.

Numerical acceptance thresholds are **TBD** and, if used, must be committed before examining final evaluation results.

## 6. Failure-case analysis

After metrics are generated, inspect at least:

- High-confidence false positives.
- False negatives involving high-priority alerts.
- Cases where baseline and AI disagree.
- Cases with ambiguous or insufficient evidence.

Do not alter the frozen evaluation set to remove difficult cases after results are known.

## 7. Reporting

Each run should export a machine-readable metrics artifact and metadata describing commit SHA, dataset version, method configuration and timestamp. `REPORT.md` will contain interpretation, limitations and non-claims.