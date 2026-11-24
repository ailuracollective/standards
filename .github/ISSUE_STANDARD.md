# GitHub Issue Standard

> **The canonical contract is [CONTRACT.yml](CONTRACT.yml).** This file is
> human-readable documentation of that contract. If this file and CONTRACT.yml
> disagree, CONTRACT.yml wins and this file is wrong.
>
> The contract is machine-checked against the templates by CI
> (`scripts/validate_contract.py`). Drift fails the build.

## Purpose

Every issue is the **task contract**. It answers:

1. Why the work exists.
2. What observable outcome is required.
3. What work is included.
4. How completion will be objectively recognized.

An issue describes the desired result, not the implementation, unless the
implementation itself is a requirement.

## Canonical contract

The canonical issue contract is defined in [CONTRACT.yml](CONTRACT.yml). In
summary:

### Common sections (all types)

| Section             | Required | Purpose                                                                |
| ------------------- | -------- | ---------------------------------------------------------------------- |
| Context             | yes      | Why the work exists, with evidence when it materially affects the task |
| Goal                | yes      | The observable outcome required                                        |
| Scope               | yes      | What this issue includes                                               |
| Acceptance criteria | yes      | Observable conditions that establish completion                        |
| Non-goals           | no       | Only when an explicit boundary prevents ambiguity                      |
| Constraints         | no       | Only constraints that materially limit valid solutions                 |
| References          | no       | Links or paths to authoritative context                                |

Optional sections are conditional: an irrelevant section should be absent (left
empty), not populated with "N/A".

### Type-specific deltas

Only two types add sections beyond the common contract:

- **Bug** (`fix:`): Observed behavior, Expected behavior, Reproduction
- **Spike** (`spike:`): Question, Deliverable

All other types use the common contract alone.

## Issue types

| Type          | Template            | `title:`          | Label                |
| ------------- | ------------------- | ----------------- | -------------------- |
| `feat`        | `feat.yml`          | `"feat: "`        | `type/feature`       |
| `fix`         | `bug.yml`           | `"fix: "`         | `type/bug`           |
| `improvement` | `improvement.yml`   | `"improvement: "` | `type/improvement`   |
| `chore`       | `maintenance.yml`   | `"chore: "`       | `type/task`          |
| `test`        | `test.yml`          | `"test: "`        | `type/task`          |
| `docs`        | `docs.yml`          | `"docs: "`        | `type/documentation` |
| `spike`       | `investigation.yml` | `"spike: "`       | `type/task`          |

Do not derive an issue type from the template filename: some filenames are
historical (`bug.yml`, `maintenance.yml`, `investigation.yml`).

## Complexity classification

Issues carry exactly one canonical complexity label. Complexity expresses
implementation uncertainty and difficulty independent of effort estimates and
AI providers. Classification can change as evidence emerges.

| Label                | Meaning                                                                                 |
| -------------------- | --------------------------------------------------------------------------------------- |
| `complexity/low`     | Scope and approach are clear; implementation risk is low with no significant unknowns.  |
| `complexity/medium`  | Scope is understood, but work involves bounded design choices or limited coordination.  |
| `complexity/high`    | Scope or approach has significant unknowns, cross-cutting impact, or elevated risk.     |
| `complexity/unknown` | Evidence is insufficient to classify; use until evidence supports low, medium, or high. |

Rules:

- At most one complexity label is permitted per issue.
- Exactly one complexity label is required for `status/ready`, including
  `complexity/unknown` as a valid classification.
- Change the complexity label when evidence changes; do not leave conflicting
  complexity labels on an issue.

## Writing principles

- Prefer outcomes over implementation steps.
- Keep issues understandable without a separate conversation.
- Make acceptance criteria observable and testable.
- Explicitly separate included and excluded work.
- Do not prescribe implementation unless the implementation itself is a requirement.
- Avoid unnecessary detail.
- Split unrelated work into separate issues.
- Link dependencies instead of duplicating their content.
- A path listed under References is a navigation hint unless the issue explicitly
  states that modifying that file is required.

## AI-agent contract

> Do not invent repository-specific facts. Inspect authoritative repository
> instructions and referenced files before implementation. If required
> information is still unavailable, state the uncertainty instead of guessing.

The contract distinguishes:

- **Facts** supplied by the issue.
- **Requirements** (Goal, Acceptance criteria).
- **Constraints** (Constraints).
- **References** to authoritative sources (References).
- **Unresolved questions** (omitted optional sections).
- **Implementation choices** (not prescribed by the issue).

Agents must not infer that:

- Every referenced file must be changed.
- Every omitted section has a value of "none".
- An implementation approach is required merely because it is mentioned as an example.
- Missing repository facts can be reconstructed from conventions.

## Migration

Existing issue bodies are not rewritten. Only newly created issues use the
current body contract. Old template filenames remain as compatibility aliases.

For complexity classification adoption, existing issues also keep their current
bodies. Repositories should audit existing issues, especially those carrying
`status/ready`, and add exactly one `complexity/*` label. When evidence is
insufficient, use `complexity/unknown` until evidence supports `low`, `medium`,
or `high`. If an issue has conflicting complexity labels, keep the one supported
by current evidence and remove the others. No automatic organization-wide
relabeling is performed.
