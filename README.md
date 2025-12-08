# Rolaand Jayz Wayz – Coding with Natural Language: Intelligence Driven Development (RJW-IDD)

> **A disciplined methodology for AI-assisted software development** with a reference implementation demonstrating the principles in practice.

## 🎉 Phase 1 Complete

This repository now includes a **working reference implementation** of the RJW-IDD methodology:

- ✅ **Async LangGraph Runner** - Execute graph workflows with timeout/retry behavior
- ✅ **Enhanced Checkpointing** - Save, list, and rollback conversation states
- ✅ **FIPA-ACL Messaging** - Standards-compliant agent communication
- ✅ **Policy Enforcement Point (PEP)** - OPA HTTP enforcer with fail-closed fallback
- ✅ **Supervisor (Jayz Wayz)** - Integrated facade for all components
- ✅ **CLI Tools** - Demo execution and checkpoint management
- ✅ **Comprehensive Tests** - Full test coverage for all components

See the [Quick Start](#quick-start) section below to get started!

## What is RJW-IDD?

RJW-IDD (Intelligence Driven Development) is a methodology that replaces vibe-driven AI coding with a disciplined loop where **reality** (fresh research, explicit trade-offs) leads specification and implementation. It provides:

- **Traceable decisions** captured in individual Markdown records
- **Research-first development** with curated evidence driving requirements
- **Specification-driven design** before implementation begins
- **Test-driven execution** with living documentation

## Quick Start

```bash
# 1. Clone and setup
git clone https://github.com/Rolaand-Jayz/Jayz-Wayz.git
cd Jayz-Wayz
./scripts/bootstrap.sh
source .venv/bin/activate

# 2. Run tests
pytest -q

# 3. Try the demo
python -m jayz_wayz.orchestrator demo --conversation-id my-conversation

# 4. List checkpoints
python -m jayz_wayz.orchestrator checkpoints list

# 5. Rollback to a checkpoint (interactive)
python -m jayz_wayz.orchestrator checkpoints rollback
```

## Repository Structure

This repository contains the **RJW-IDD methodology**, **templates**, and a **reference implementation**.

```text
# Methodology
rjw-idd-methodology/
├── core/                    # Core method principles
│   └── METHOD-0001-core-method.md
├── governance/              # Phase checklists and role handbooks
│   ├── METHOD-0002-phase-driver-checklists.md (Unified Lifecycle & Checklists)
│   └── METHOD-0003-role-handbook.md
├── operations/              # Execution playbooks
│   ├── METHOD-0004-ai-agent-workflows.md (Unified Agent Handbook)
│   └── METHOD-0005-operations-production-support.md
├── templates/               # Artifact templates (organised by category)
│   ├── decisions/           # Decision record templates
│   ├── requirements/        # Requirement templates
│   ├── specs/               # Specification templates
│   ├── evidence/            # Research evidence templates
│   ├── testing/             # Test case templates
│   ├── documentation/       # Standards, runbooks, guides
│   └── governance/          # Change logs, audit logs, ledgers
├── addons/                  # Domain-specific methodology extensions
│   ├── 3d-game-core/
│   └── video-ai-enhancer/
├── docs/                    # Method-level documentation
│   ├── change-log.md
│   └── decisions/
└── logs/                    # Stage audit reflections

# Reference Implementation (Phase 1)
src/jayz_wayz/
├── __init__.py              # Package exports
├── state.py                 # Graph state management
├── fipa.py                  # FIPA-ACL message support
├── checkpoint.py            # Enhanced checkpoint store
├── policy.py                # Policy enforcement (OPA + LocalDeny)
├── langgraph_core.py        # Async graph runner
├── nodes.py                 # Node wrappers and common nodes
├── supervisor.py            # Supervisor facade (Jayz Wayz)
└── orchestrator.py          # CLI interface

tests/                       # Test suite
├── test_async_graph.py      # Async runner tests
├── test_checkpoint.py       # Checkpoint tests
├── test_fipa.py             # FIPA message tests
└── test_policy_enforcer.py  # Policy enforcer tests

scripts/                     # Development scripts
└── bootstrap.sh             # Environment setup

docs/                        # Reference documentation
└── README.md
```

## Core Methodology Components

The methodology is organized into **five core documents**:

### 1. Core Method (`METHOD-0001`)

The foundational document describing:

- **Discovery Layer** — Research intake, evidence curation, and specification synthesis
- **Execution Layer** — Test-driven development, living documentation, integration-first delivery
- **Stage Gates** — Checkpoints ensuring each phase completes before the next begins

### 2. Unified Lifecycle & Checklists (`METHOD-0002`)

The **single source of truth** for all process checklists:

- **Risk Selection Logic** — Entry point for classifying change risk level
- **Streamlined Pathways** — Fast tracks for Minimal/Low/Medium risk changes
- **Full Discovery→Execution Loop** — High/Critical risk change processes
- **Prototype Mode** — Keep/Flex/Unknown tagging and relaxed gates for POC/spike work
- **Agent Trust Integration** — Trust levels linked to pathway access

### 3. Role Handbook (`METHOD-0003`)

Responsibilities for:

- Agent Conductor
- Spec Curator
- Doc Steward
- Governance Sentinel

### 4. Unified Agent Handbook (`METHOD-0004`)

The **single source of truth** for all AI agent rules and behaviors:

- **Trust Ladder Model** — Four levels from Supervised to Trusted Partner
- **Behavioral Contracts** — Explicit commitments agents make for transparency, quality, and safety
- **Continuous Verification** — Automated checks that build trust evidence
- **Graduated Response Protocol** — Proportionate responses to trust violations
- **Workflow Selection** — Trust levels linked to process pathways

### 5. Operations & Production Support (`METHOD-0005`)

Guidance for post-deployment phases including:

- Deployment strategies (blue-green, canary)
- SLO management
- Incident response
- User feedback collection

## Templates

Copy these templates into your project when applying RJW-IDD:

| Category | Template | Purpose |
|----------|----------|---------|
| **Decisions** | `templates/decisions/DEC-template.md` | Capture strategic choices with options and rationale |
| **Decisions** | `templates/DEC-LITE-template.md` | Lightweight decision record for Low/Medium risk |
| **Prototypes** | `templates/PROTO-template.md` | Prototype record for POC/spike work |
| **Agent Trust** | `templates/AGENT-TRUST-template.md` | Document agent trust level changes |
| **Requirements** | `templates/requirements/REQ-template.md` | Define system requirements with acceptance criteria |
| **Specifications** | `templates/specs/SPEC-template.md` | Technical design addressing requirements |
| **Evidence** | `templates/evidence/EVD-template.md` | Research findings supporting decisions |
| **Testing** | `templates/testing/TEST-template.md` | Verify specifications meet acceptance criteria |
| **Documentation** | `templates/documentation/DOC-template.md` | Standards, runbooks, guides, and references |
| **Governance** | `templates/governance/CHANGE-LOG-template.md` | Track methodology/project changes |
| **Governance** | `templates/governance/STAGE-AUDIT-LOG-template.md` | Phase gate audit reflections |
| **Governance** | `templates/governance/REQ-LEDGER-template.md` | Requirement traceability matrix |
| **Governance** | `templates/governance/LIVING-DOCS-RECONCILIATION-template.md` | Documentation debt tracking |

See `rjw-idd-methodology/templates/README.md` for detailed usage instructions.

## Using This Methodology

1. **Study the core method** — Read `rjw-idd-methodology/core/METHOD-0001-core-method.md` to understand the lifecycle
2. **Copy templates** — Clone templates from `rjw-idd-methodology/templates/` into your project workspace; never modify the originals
3. **Classify risk level** — Use the Risk Selection Logic in `METHOD-0002` Section 1 to determine the appropriate pathway
4. **Apply the checklists** — Use `METHOD-0002` to guide each phase transition
5. **Assign roles** — Follow `METHOD-0003` to establish ownership
6. **Document decisions** — Create `DEC-####` records using the decision template for every strategic choice
7. **Track requirements** — Use the requirement ledger template to maintain traceability
8. **Maintain governance** — Update change logs and audit logs at each phase gate

## Addons (Domain Extensions)

The methodology includes optional extensions for specific domains:

- **3D Game Core** — Specs and checklists for game development with Unity, Unreal, Godot
- **Video AI Enhancer** — Quality gates for real-time video enhancement pipelines

## Contributing

Methodology changes require a new decision record (`DEC-####`) justifying the modification. See `CONTRIBUTING.md` for details.

## License

See `LICENSE` for terms.
