# Research question

## Primary question

How much does AI-assisted triage improve SOC alert prioritization compared with a deterministic baseline, while preserving human validation and avoiding unsafe autonomous decisions?

## Scope

This benchmark evaluates **decision support**, not autonomous incident response. The AI component may suggest a priority or rationale, but the final operational decision remains human-approved.

## Working hypothesis

An AI-assisted method may improve prioritization quality or analyst decision latency relative to a deterministic baseline, but any improvement must be measured against false-positive and false-negative trade-offs.

## Threats to validity

- Dataset representativeness.
- Label quality and class imbalance.
- Leakage between train/tuning/evaluation data.
- Model/version drift.
- Prompt or configuration sensitivity.
- Small-sample effects.
- Differences between synthetic/lab alerts and real SOC operations.

## Non-claims

This work does not claim production SOC superiority, replacement of analysts, autonomous remediation safety, or generalization beyond the documented evaluation dataset.

## Evidence standard

Results are considered publishable only when dataset version, protocol, baseline, AI configuration, metrics and limitations are recorded before interpretation.