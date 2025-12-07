# PROMPT-3D-0004 — IDD Pacts Generator

**Mission:**
Draft cross-discipline pacts covering input, physics, ECS, rendering, animation, networking, audio, and build/importer pipelines for the active profile.

**Instructions to assistant:**
1. Load `docs/pacts_examples.md` for canonical format.
2. For each pairing, define: shared objective, interface contract, latency/budget expectations, escalation triggers, and trace IDs (`INTEG-3D-*`).
3. Reference profile tolerances (movement, rollback) and asset rules when defining guardrails.
4. Output structured Markdown sections that can be copied into `docs/pacts_examples.md` or project-specific ledgers.

**Output Requirements:**
- Minimum five pact drafts with unique `PACT-3D-####` identifiers.
- Each pact lists upstream `DEC-3D-*` references and downstream `TEST-3D-*` verification hooks.
