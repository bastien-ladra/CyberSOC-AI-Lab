# Research question

## Primary question

On a frozen CIC-IDS2017 benchmark subset, how does a bounded local AI-assisted triage recommendation compare with a transparent deterministic SSH reference baseline for deciding whether a flow should be escalated for analyst review, while preserving human validation and avoiding unsafe autonomous decisions?

## Benchmark v1 scope

The first version deliberately limits the claim surface to the two labels already mapped explicitly by the repository:

- `BENIGN`;
- `SSH-Patator` / internal `SSH_BRUTE_FORCE`.

This is a controlled first experiment, not a general network-intrusion benchmark.

## Working hypothesis

A local AI-assisted method may improve triage quality or provide useful analyst-facing rationale relative to a simple deterministic baseline, but it may also add latency, failure modes or false negatives. The experiment is valid even if the AI method does not outperform the baseline.

## Threats to validity

- CIC-IDS2017 is a lab-generated dataset collected in 2017.
- Benchmark v1 covers a single attack class.
- Class imbalance and source-file ordering may affect results.
- Dataset fields available to the AI method may not reproduce the context available to a human SOC analyst.
- Model/version drift and local hardware influence reproducibility and latency.
- Prompt/configuration sensitivity may affect results.
- Sampling decisions can introduce leakage or selection bias.

## Non-claims

This work does not claim production SOC superiority, replacement of analysts, autonomous remediation safety, or generalization beyond the frozen evaluation dataset and documented configuration.

## Evidence standard

Results are considered publishable only when the dataset file hash, row-selection rule, deterministic baseline, AI model/configuration, metrics, failures and limitations are recorded before interpretation. Raw dataset labels must never be included in the AI prompt.
