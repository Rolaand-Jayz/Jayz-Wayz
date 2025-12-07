# Security Policy

This repository follows a simple, novice-friendly security policy.

Reporting a Vulnerability
-------------------------
- Email: security@example.com (replace with project contact) or open a GitHub Issue with label `security` (private if needed).
- Provide: steps to reproduce, affected versions, and any PoC if available.

Response
--------
- Triaged within 72 hours.
- If a fix is required, a patch or advisory will be prepared and a coordinated disclosure discussed.

Dependency management
---------------------
- CI runs `pip-audit` and `bandit` on each PR. Failures block merges.
- Weekly dependency checks are recommended; Dependabot is enabled by default.

Local checks
------------
- Run `bash scripts/checks/run_checks.sh` in an activated venv to run tests, linter, and pip-audit.
