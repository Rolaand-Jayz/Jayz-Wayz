# RJW-IDD Methodology Pack

This pack houses the source-of-truth guidance for Rolaand Jayz Wayz – Coding with Natural Language: Intelligence Driven Development (RJW-IDD).

## Directory Layout

- `core/` — enduring principles and lifecycle design (`METHOD-0001`).
- `governance/` — phase control, checklists, and role handbooks (`METHOD-0002`, `METHOD-0003`).
- `operations/` — execution playbooks for specialised use cases such as AI coding agents (`METHOD-0004`, `METHOD-0005`).
- `templates/` — boilerplates for all artefact types; organised by category (decisions, requirements, specs, evidence, testing, documentation, governance).
- `addons/` — domain-specific methodology extensions (3D game development, video AI).
- `docs/` — method-level change log and decision records.
- `logs/` — stage audit reflections.

## Templates

The `templates/` directory provides ready-to-use boilerplates for every artefact type referenced in the methodology:

| Category | Template | Purpose |
|----------|----------|---------|
| **Decisions** | `DEC-template.md` | Capture strategic choices with options and rationale |
| **Requirements** | `REQ-template.md` | Define system requirements with acceptance criteria |
| **Specifications** | `SPEC-template.md` | Technical design addressing requirements |
| **Evidence** | `EVD-template.md` | Research findings supporting decisions |
| **Testing** | `TEST-template.md` | Verify specifications meet acceptance criteria |
| **Documentation** | `DOC-template.md` | Standards, runbooks, guides, and references |
| **Governance** | `CHANGE-LOG-template.md` | Track methodology/project changes |
| **Governance** | `STAGE-AUDIT-LOG-template.md` | Phase gate audit reflections |
| **Governance** | `REQ-LEDGER-template.md` | Requirement traceability matrix |
| **Governance** | `LIVING-DOCS-RECONCILIATION-template.md` | Documentation debt tracking |

See `templates/README.md` for detailed usage instructions.

## How to Use

1. Treat every file as method-level doctrine. Only modify after capturing a new `DEC-####` in your project evidence stream.
2. Copy templates into a project workspace before editing; do **not** customise the originals.
3. Keep project artefacts (decisions, specs, ledgers, prompts) under a project-specific prefix to avoid collisions with the `METHOD-####` namespace.
4. Maintain traceability by linking artefacts using their identifiers (`REQ-####`, `SPEC-####`, `TEST-####`, etc.).

RJW-IDD deliberately keeps method guidance separate from project execution assets. This pack describes *how* to operate; downstream projects implement the methodology with their own IDs and evidence.

## Add-ons

- [3D Game Core](addons/3d-game-core/README.md) — specs and templates for 3D game development.
- [Video AI Enhancer](addons/video-ai-enhancer/README.md) — quality gates for real-time video enhancement.
