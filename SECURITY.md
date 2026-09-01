# Security Policy

CyberSOC-AI-Lab is an experimental security/AI laboratory. It processes synthetic log data by default and is **not intended for production SOC use**.

## Reporting a vulnerability

Please do not open a public issue for a vulnerability that could expose sensitive information or enable abuse.

Report security concerns privately to **ladra.bastien@gmail.com** with:

- the affected file or component;
- reproduction steps;
- expected and observed behavior;
- potential impact;
- a suggested remediation, if available.

Do not include real credentials, private logs, personal data, exploit payloads against third-party systems or other sensitive evidence in a public report.

## Data boundary

Only synthetic/demo logs belong in this repository. Real SOC logs, credentials, tokens, model secrets, private datasets and generated evidence derived from real environments must remain outside version control.

The following paths are intentionally ignored for future private or external data:

```text
data/raw/
data/external/
data/real/
data/private/
runtime/
```

## Security model

The project's assumptions, AI trust boundaries and explicit non-guarantees are documented in:

- `docs/SECURITY_MODEL.md`
- `docs/threat_model.md`

The AI component is advisory. It must not execute remediation actions or replace human validation.
