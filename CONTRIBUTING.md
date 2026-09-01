# Contributing

CyberSOC-AI-Lab is an experimental cybersecurity and AI project. Contributions should improve observable engineering value rather than inflate maturity claims.

## Environment

Install the development environment from the hash-locked dependency set:

```bash
python -m pip install --require-hashes -r requirements-dev.lock
```

Direct dependencies live in `requirements.in` and `requirements-dev.in`. If one of those inputs changes, regenerate both lockfiles with the same toolchain as CI:

```bash
python -m pip install "pip==26.1.2" "pip-tools==7.6.0"
python -m piptools compile --generate-hashes --resolver=backtracking --no-header --no-emit-index-url --no-emit-trusted-host --output-file=requirements.lock requirements.in
python -m piptools compile --generate-hashes --resolver=backtracking --no-header --no-emit-index-url --no-emit-trusted-host --output-file=requirements-dev.lock requirements-dev.in
```

Do not hand-edit resolved package versions or hashes in the `.lock` files.

## Before opening a pull request

Run the same core checks as CI:

```bash
python -m pip check
pip-audit -r requirements.lock --strict
black --check .
ruff check .
mypy .
bandit -r ai_assistant dashboard detection utils main.py -q
pytest --cov=ai_assistant --cov=detection --cov=utils --cov-report=term-missing --cov-fail-under=90 -q
docker build -t cybersoc-ai-lab .
```

GitHub Actions additionally verifies lockfile drift, full-history secret scanning, the non-root container runtime, the Streamlit health endpoint, Trivy HIGH/CRITICAL findings and CycloneDX SBOM generation.

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
