# GitHub Issue Standard

> **This file is prose, not data.** It was previously `ISSUE_STANDARD.yml` and it
> did not parse as YAML: the numbered list under Purpose reads as mapping keys, so
> the file failed to load from its first numbered line onward. It was renamed
> rather than repaired, because it is a document meant to be read. Do not convert
> it back to YAML and do not point a parser at it.
>
> The consequence is accepted deliberately: the type list and the section
> vocabulary below are **not** machine-checked against the templates, so they can
> drift. They already have — `bug.yml` and `investigation.yml` ask for four
> sections this document does not define. Closing that gap needs a real schema
> and a CI check, not a better indent.

## Purpose

Every issue must communicate:

1. Why the work exists.
2. What outcome is expected.
3. What work is included.
4. How completion will be verified.

## Issue Types

- `feat`: New capability or behavior.
- `fix`: Correction of incorrect behavior.
- `improvement`: Improvement to existing behavior without being a bug fix.
- `chore`: Technical maintenance with no intended functional change.
- `test`: Work whose primary purpose is test coverage.
- `docs`: Documentation work.
- `spike`: Investigation or research required before implementation.

## Title Convention

Use:

`<type>: <short imperative description>`

Examples:

- `feat: expose incoming sponsor letters through the admin API`
- `fix: make receiving a sponsor letter atomic`
- `improvement: simplify configuration loading`
- `chore: remove redundant controller abstractions`
- `test: cover incoming correspondence flows`
- `docs: document public API identifier handling`
- `spike: evaluate distributed translation caching`

Prefer describing the outcome or problem rather than the implementation.

## Core Sections

Issues should use these sections when relevant:

- Context
- Objective
- Scope
- Out of scope
- Acceptance criteria

Optional sections:

- Dependencies
- Constraints
- How to reproduce
- Impact
- Scenarios
- Notes

Not every issue needs every optional section.

## Writing Principles

- Prefer outcomes over implementation steps.
- Keep issues understandable without a separate conversation.
- Make acceptance criteria observable and testable.
- Explicitly separate included and excluded work.
- Do not prescribe implementation unless the implementation itself is a requirement.
- Avoid unnecessary detail.
- Split unrelated work into separate issues.
- Link dependencies instead of duplicating their content.
- Explicitly preserve existing behavior when a change must be non-breaking.
- For defects and architectural problems, use evidence when available.
- An implementation detail that belongs inside another issue should not become a separate issue.

## Issue Quality Check

Before creating an issue, verify:

- [ ] The title clearly describes the work.
- [ ] The reason for the work is understandable.
- [ ] The expected outcome is explicit.
- [ ] The scope is bounded.
- [ ] Related work that is excluded is identified when necessary.
- [ ] Completion can be objectively verified.
- [ ] Dependencies are linked.
- [ ] The issue is not duplicating existing work.
