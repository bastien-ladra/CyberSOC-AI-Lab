# SOC AI benchmark report

Status: **template — no benchmark results are claimed yet**.

## Executive summary

To be completed only after the CIC-IDS2017 source file SHA-256, frozen 200-row evaluation manifest and exact local Ollama model identity have been recorded and both methods have been executed.

## Research question

See `QUESTION.md`.

## Dataset

- Source: CIC-IDS2017, Canadian Institute for Cybersecurity, University of New Brunswick.
- v1 labels: `BENIGN` and `SSH-Patator` only.
- Target file: `Tuesday-WorkingHours.pcap_ISCX.csv` from Generated Labelled Flows; exact local filename must be confirmed after download.
- SHA-256: **TBD from the exact local bytes**.
- Scored row-selection rule: **frozen — 100 BENIGN + 100 SSH-Patator rows selected by lowest canonical row SHA-256 per class, then evaluated in source order**.

See `DATASET.md` and the generated dataset manifest in `research/results/`.

## Compared methods

- Deterministic baseline: TCP destination port 22 -> `ESCALATE`.
- AI-assisted method: bounded local Ollama triage over an allowlisted, label-free feature set and the same frozen 200 rows.
- AI generation defaults: temperature `0.0`, seed `20260927`, `num_predict=128`.
- Exact local model digest and Ollama runtime version: **captured automatically at scored runtime; TBD until the local model is available**.

## Results

Do not populate this section manually from ad-hoc experiments. Link machine-generated result artifacts from `research/results/`.

| Metric | Baseline | AI-assisted | Notes |
| --- | ---: | ---: | --- |
| Precision | TBD | TBD | |
| Recall | TBD | TBD | |
| F1 | TBD | TBD | |
| False-positive rate | TBD | TBD | |
| False-negative rate | TBD | TBD | |
| Average decision latency | TBD | TBD | |
| Model/parse failures | n/a | TBD | AI failures are counted as `DO_NOT_ESCALATE` |

## Failure cases

Document representative errors, especially:

- benign SSH-like false positives;
- `SSH-Patator` false negatives;
- cases where baseline and AI disagree;
- model timeout/invalid-JSON failures;
- cases with insufficient evidence.

## Interpretation

Discuss trade-offs rather than presenting a single metric as proof of superiority. A null or negative AI result remains valid experimental evidence if the protocol was followed.

## Limitations

At minimum address:

- CIC-IDS2017 age and lab-generated nature;
- v1 restriction to one attack class;
- class imbalance and source-file ordering;
- limited feature visibility in the prompt;
- model/version dependence;
- difference between a benchmark and a production SOC;
- inability to infer safe autonomous remediation from this experiment.

## Non-claims

This benchmark is evidence about the documented evaluation setup only. It does not establish production SOC superiority, autonomous response safety or replacement of human analysts.

## Reproduction

See `research/README.md` for the validation, baseline and AI-run commands. Final release evidence must include the dataset manifest, frozen selection manifest, machine-generated result JSON files, commit SHA, exact local Ollama model digest/runtime version and generation options.
