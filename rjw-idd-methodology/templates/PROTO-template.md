# PROTO-XXXX — [Prototype Title]

> Copy this file into your project (for example `docs/prototypes/`) and rename it to the next available `PROTO-####`. Use this template for all prototype work under METHOD-0002 Section 6 (Prototype Mode).

**Created:** YYYY-MM-DD
**Owner:** [Name/Role]
**Time-Box:** [End Date] (max 4 weeks from creation)
**Status:** Active | Promoted | Archived | Abandoned

## 1. Goal

What are we trying to prove or learn?

[One to three sentences describing the hypothesis, question, or capability being explored. Be specific about what success looks like.]

## 2. Success Criteria

How will we know if this prototype succeeded?

- [ ] Criterion 1: [Specific, measurable outcome]
- [ ] Criterion 2: [Specific, measurable outcome]
- [ ] Criterion 3: [Optional additional criteria]

**Assessment Method:** [How will you evaluate these criteria? Manual testing, metrics, user feedback, etc.]

## 3. Scope Boundaries

### In Scope

What is explicitly included in this prototype?

- [Feature/capability 1]
- [Feature/capability 2]
- [Integration point or dependency]

### Out of Scope

What is explicitly excluded from this prototype?

- [Feature/capability deferred to production implementation]
- [Edge case not being addressed]
- [Quality attribute not being optimized]

### Constraints

- Time: [End date from time-box]
- Resources: [Any limitations on people, infrastructure, etc.]
- Dependencies: [External systems, data, or approvals needed]

## 4. Key Components

Document the major components of the prototype with Keep/Flex/Unknown tags.

### Tagged Elements

| Component | Tag | Notes |
|-----------|-----|-------|
| [Component name] | ⟦keep⟧ | Why this is essential to the proof-of-concept |
| [Component name] | ⟦flex⟧ | What shortcut was taken; what should change for production |
| [Component name] | ⟦unknown⟧ | Why uncertain; what evaluation is needed |

### Architecture Notes

[Optional: Include rough architecture diagram, sequence diagram, or prose description of how components interact. Keep it lightweight—this is a prototype.]

```text
[ASCII diagram or brief description]
```

## 5. Known Limitations

Document shortcuts, technical debt, and gaps consciously accepted for prototype speed.

### Shortcuts Taken

- [Shortcut 1]: [Why taken and impact]
- [Shortcut 2]: [Why taken and impact]

### Technical Debt Accepted

- [Debt item]: [What would need to change for production]

### Security/Performance Gaps

- [Gap]: [Why acceptable for prototype; what would need to change]

### Assumptions Made

- [Assumption 1]: [What we assumed without verification]
- [Assumption 2]: [Risk if assumption is wrong]

## 6. Exit Decision

**Decision:** Promote | Archive | Abandon
**Date:** YYYY-MM-DD
**Rationale:** [Why this exit path was chosen]

---

### If Promoting to Production

Complete this section when promoting to full METHOD-0002 pathway.

**Decision Record:**

- [ ] `DEC-####` created referencing this PROTO record
- [ ] Risk level classified: Minimal | Low | Medium | High | Critical
- [ ] METHOD-0002 pathway initiated

**Component Review:**

- [ ] Keep-tagged elements identified for preservation
- [ ] Flex-tagged elements queued for replacement
- [ ] Unknown-tagged elements classified (keep or flex)

**Production Readiness Gaps:**

| Gap | Priority | Assigned To |
|-----|----------|-------------|
| [Gap from Section 5] | High/Medium/Low | [Owner] |
| [Security gap] | | |
| [Performance gap] | | |

**Link to Production Work:** [Link to DEC-#### or issue tracker]

---

### If Archiving

Complete this section when archiving for future reference.

**Learnings Captured:**

- What worked well: [Summary]
- What didn't work: [Summary]
- Surprises or discoveries: [Summary]

**Why Not Promoting Now:**

[Explain why this isn't being productionized: deprioritized, different approach chosen, waiting for dependencies, etc.]

**Code Preservation:**

- Location: [Path, branch, or "deleted"]
- Retrievability: [How to find this code later if needed]

**Potential Future Use:**

[When might this be revisited? What would need to change?]

---

### If Abandoning

Complete this section when abandoning the approach.

**Why This Approach Failed:**

[Be specific about what went wrong or why this path isn't viable]

**Lessons Learned:**

- [Lesson 1]: [What we learned that prevents others from repeating this]
- [Lesson 2]: [Insight gained from the failure]

**Alternative Approaches:**

[If known, what approaches might work instead?]

**Code Disposition:**

- [ ] Code deleted
- [ ] Code retained at: [location] for reference

---

## 7. Activity Log

Track significant progress and decisions during the prototype. Keep it lightweight.

| Date | Activity | Outcome |
|------|----------|---------|
| YYYY-MM-DD | Started prototype | Initial setup complete |
| YYYY-MM-DD | [Milestone] | [Result] |
| YYYY-MM-DD | [Decision point] | [Choice made and why] |
| YYYY-MM-DD | Exit decision | [Promote/Archive/Abandon] |

## Related Links

- **Originating Request:** [Link to issue, discussion, or decision that spawned this prototype]
- **Evidence Used:** [Any EVD-#### or external references consulted]
- **Related Prototypes:** [Any prior or parallel PROTO-#### records]
- **Production Decision:** [DEC-#### if promoted]
