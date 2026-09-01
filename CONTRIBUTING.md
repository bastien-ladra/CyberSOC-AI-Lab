# Contributing

CyberSOC-AI-Lab is an experimental cybersecurity and AI project. Contributions should improve observable engineering value rather than inflate maturity claims.

## Before opening a pull request

Run the same checks as CI:

```bash
black --check .
ruff check .
mypy .
bandit -r ai_assistant dashboard detection utils main.py -q
pytest --cov=ai_assistant --cov=detection --cov=utils --cov-report=term-missing --cov-fail-under=90 -q
```

## Data rules

Do not commit:

- real SOC or production logs;
- credentials, API keys or tokens;
- personal/confidential data;
- raw external datasets unless redistribution rights and repository scope explicitly allow it;
- generated runtime evidence derived from private environments.

Demo fixtures must use synthetic data and documentation-reserved addressing where public IP-like values are needed.

## AI safety boundary

Log content is untrusted evidence. Contributions must not make model output authoritative, execute remediation automatically, or bypass human review for final incident decisions.

## Claims

A new README or portfolio claim must map to implementation, tests, CI evidence or a clearly identified experiment. Do not describe experimental behavior as production validation.
