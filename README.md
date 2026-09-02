# CyberSOC-AI-Lab

> SOC / SecOps laboratory focused on explainable detection, human-controlled AI assistance, reproducible evidence, and secure software delivery.

CyberSOC-AI-Lab demonstrates an end-to-end security workflow: parse security-relevant logs, apply deterministic detection rules, enrich alerts with transparent prioritization and MITRE ATT&CK context, optionally ask a **local** AI assistant to summarize evidence, require a human review decision, and export auditable results.

## Research benchmark

A documentation-first, reproducible SOC AI benchmark is being developed under `research/`. The current v1 work selects CIC-IDS2017 as the public research source, restricts scoring to explicitly supported `BENIGN` and `SSH-Patator` labels, fixes a transparent deterministic reference baseline, and provides a bounded local-Ollama runner with label-free inputs and machine-computed metrics. No benchmark result is claimed until the exact dataset file hash, evaluation rows and model configuration are frozen.

See [`research/README.md`](research/README.md), [`research/PROTOCOL.md`](research/PROTOCOL.md) and [`research/REPORT.md`](research/REPORT.md).

## What this repository shows

- Deterministic detection logic for SSH brute force and web reconnaissance.
- Prompt-injection-aware handling of untrusted log content.
- MITRE ATT&CK / AI-security mapping for alert context.
- Explainable priority scoring and human review state.
- Local Ollama integration so alert evidence does not need to be sent to an external model API.
- Ground-truth fixtures, CIC-IDS2017 mapping utilities and automated tests.
- Machine-readable exports for evidence and review.
- Hash-locked dependencies and container / software-supply-chain security controls.

## Human-in-the-loop principle

The AI component is decision support only. It must not invent evidence, silently convert a suggestion into an operational decision, or perform irreversible remediation. Human validation remains separate from raw model output.

## Repository navigation

- `detection/` — log parsing and deterministic rules.
- `ai_assistant/` — prompt construction, local Ollama client and response checks.
- `utils/` — analytics, ground-truth evaluation, CIC-IDS2017 adapters, review and exports.
- `data/sample_logs/` — versioned non-sensitive demonstration logs.
- `research/` — reproducible benchmark question, dataset card, protocol, runners, metrics and report.
- `tests/` — automated verification.
- `docs/` — supporting documentation and evidence-oriented material.

## Quick start

Install the hash-locked runtime dependencies:

```bash
python -m pip install --require-hashes -r requirements.lock
```

Run the application according to the existing project entry point, and run the test suite with:

```bash
pytest -q
```

For the research benchmark workflow, use the commands in `research/README.md`; raw public datasets must stay outside the repository.

## Research integrity and limitations

This repository is a laboratory and portfolio artifact, not a claim of production SOC superiority. Sample logs and public benchmark datasets differ from real enterprise telemetry. Metrics must be tied to a frozen dataset/protocol and machine-generated result artifacts, with failure cases and limitations reported explicitly.

## Security

See [`SECURITY.md`](SECURITY.md) for vulnerability-reporting guidance. The repository intentionally separates untrusted inputs, deterministic rules, AI-generated assistance and final human decisions.
