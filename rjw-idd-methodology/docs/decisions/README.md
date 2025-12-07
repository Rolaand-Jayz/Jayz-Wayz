# Method-Level Decision Log Directory

This directory holds the governing `DEC-####.md` records that capture how the RJW-IDD methodology itself evolves.

## Usage Rules
1. **Reserve IDs Sequentially:** Start at `DEC-0001.md` and increment for every method decision. Downstream projects must never reuse the method namespace; they work in their own repositories.
2. **Clone the Template:** Copy `../templates/PROJECT-DEC-template.md` when drafting a new decision. Keep the original template pristine.
3. **Link the Evidence:** Each decision references supporting research (`EVD-####`), specs (`METHOD-####`), and any audit notes (`LOG-####`).
4. **Update the Change Log:** After approving a decision, add the companion entry to `docs/change-log.md` with validator and audit references.
5. **Retire Superseded Guidance:** When a decision replaces older doctrine, note the deprecated artefacts in the Follow-Up Actions section and update the relevant method documents.

Maintain this directory under source control so auditors can trace how the methodology progressed.
