# SOC AI benchmark report

Status: **template — no benchmark results are claimed yet**.

## Executive summary

To be completed only after the CIC-IDS2017 source file, SHA-256, evaluation-row selection rule, deterministic baseline and local-Ollama configuration have been frozen and executed.

## Research question

See `QUESTION.md`.

## Dataset

- Source: CIC-IDS2017, Canadian Institute for Cybersecurity, University of New Brunswick.
- v1 labels: `BENIGN` and `SSH-Patator` only.
- Exact file name: **TBD**.
- SHA-256: **TBD**.
- Scored row-selection rule: **TBD before result interpretation**.

See `DATASET.md` and the generated dataset manifest in `research/results/`.

## Compared methods

- Deterministic baseline: TCP destination port 22 -> `ESCALATE`.
- AI-assisted method: bounded local Ollama triage over an allowlisted, label-free feature set; exact model/version and final row count **TBD before scored run**.

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

See `research/README.md` for the validation, baseline and AI-run commands. Final release evidence must include the dataset manifest, machine-generated result JSON files, commit SHA and exact local model identifier.
