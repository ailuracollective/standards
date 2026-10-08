# AGENTS.md

Working instructions for agents and contributors.

`README.md` is the human entry point. This file holds only the invariants and
conventions specific to this repository, plus pointers to the shared rules and to
`docs/`.

## Organization standards

The organisation's conventions live in
[.agents/organization-conventions.md](.agents/organization-conventions.md). They
are mandatory and apply to every repository in the organisation; read them before
this file. Where this file and that one state the same rule, that one is
authoritative.

## Repository

This repository is the source of the GitHub issue and pull-request
standards shared across `ailuracollective`. There is no application
code, build, or test suite.

It owns the shared standard — the five `.github/` artifacts listed in the
organisation conventions — and the infrastructure that serves them:
`.github/workflows/`, the release files, `templates/` (the skeletons an adopting
repository completes), and `.github/standards.local.example.yml`. The file map, the
sync model, and the copy divergences are in docs/architecture.md.

Root documents: `README.md` (human entry point), `CONTRIBUTING.md` (how to
contribute), `CHANGELOG.md` (written by release-please).

## Critical invariants

### Issues

Each of the seven issue types in `.github/ISSUE_STANDARD.md` has exactly one
template and one `title:` prefix.

Do not derive an issue type from the template filename: some filenames are
historical (`bug.yml`, `maintenance.yml`, `investigation.yml`).

Every issue template preserves existing field IDs and follows the common field
structure unless the type genuinely needs an exception. What a template must
apply, and which labels it may name, is in the organisation conventions.

`ISSUE_STANDARD.md` is prose. Do not parse it as YAML.

### Pull requests

The title and branch vocabularies are in the organisation conventions. The policy
action has two deliberately different inputs:

- `type-labels` — the GitHub `type/*` labels;
- `title-types` — the pull-request title types and template resolution.

Do not combine these vocabularies. `breaking-change` is a PR/commit type, not an
issue type and not a `type/breaking-change` label.

The PR policy resolves the body template from the title, not from the label.

The four common PR headings listed in the organisation conventions must remain
identical across all thirteen PR templates; change one, change all thirteen.

`## Test plan` remains a TODO in this repository; adopting repositories replace it
with their own commands. Do not put repository-specific commands into the shared
PR templates.

### Labels

`chore`, `test`, and `spike` use `type/task`; the reasoning is in
docs/architecture.md. The manifest's role, the six families, and the rules for
`type/*` are in the organisation conventions.

### Release PRs

Release-please PRs are deliberately exempt from PR policy validation.
Their head ref starts with `release-please--branches--`, and
`policy.yml` exempts them by head ref, not by actor. Do not replace
this exemption with `skip-actors`: the release identity can also open
normal pull requests.

Release-please runs on pushes to `main`, opens a release PR when a
release is required, and creates the tag and GitHub release when that
PR is merged. The release configuration requires `release-type: simple`,
`initial-version: 0.1.0`, and a `packages` entry matching the manifest.
See docs/releases.md.

### Automation tokens

PR policy comments use `AILURA_PR_COMPLIANCE_TOKEN`; release automation
uses a separate `AILURA_RELEASE_TOKEN`. Keep these identities separate
and grant each only the permissions it needs. Do not replace the PR
comment token with a write permission on the workflow's `GITHUB_TOKEN`.
See docs/releases.md.

### Customization model

This repository is the canonical source for the shared standard, but adopting
repositories may intentionally diverge. The rule and the levels are in the
organisation conventions; docs/customization.md carries the detail behind them.

## Security and workflow rules

`policy.yml` checks repository policy without executing code from the PR head. Do
not change this property without explicitly reviewing the security impact. The PR
policy and CI workflows intentionally remain safe for fork pull requests.

The organisation-wide workflow rules are in the organisation conventions. Every
job here uses `timeout-minutes: 10`.

## Editing conventions

YAML: two-space indentation, no tabs, no CRLF, every file starts with
`---`, workflow trigger keys use `"on":`, label colors are quoted
six-digit hexadecimal strings without `#`, and the established ordering
of label families and fields is preserved. Do not let formatting tools
rewrite `.github/standards.local.example.yml`.

Issue templates: preserve top-level key order, unique kebab-case field
IDs, existing field IDs, required/optional validation semantics, and the
common field order. A field ID is part of the public interface: changing
it can break bookmarked or prefilled issue URLs.

PR templates: preserve the four common headings exactly. When adding a
PR type, add the template, add its title/branch vocabulary where
required, assign an existing `type/*` label, keep `## Test plan` as
TODO, and update every consuming policy configuration if the new type is
a branch type.

CODEOWNERS: keep the catch-all rule, which owns every path nothing else names.
The matching and enforcement rules are in the organisation conventions; see
docs/enforcement.md for this repository.

For formatting:

```sh
uv run yamlfix -i '*.yml' -e '.cache/**' -e '.github/standards.local.example.yml' .
uv run mdlint check --fix --select MD060 . .github
```

A green linter is not sufficient verification. Several important
invariants cross file boundaries — issue type ↔ issue template,
template labels ↔ labels.yml, PR title types ↔ PR templates,
type-labels ↔ remote labels, release configuration ↔ release manifest,
CODEOWNERS ↔ repository permissions, required status checks ↔ actual
workflow job names.

## Before changing the standard

Ask whether the change affects every adopting repository, the label
vocabulary, issue or PR template structure, PR policy inputs, release
behavior, workflow permissions, or CODEOWNERS and branch protection. If
it does, update the corresponding documentation and validation procedure
in the same change.

Never assume a configured rule is enforced. Branch protection and
rulesets are repository-specific and must be checked through the GitHub
API. See docs/enforcement.md.

## Where to find details

- docs/architecture.md — the file map, the sync model, copy divergences, and recipes for adding a type or label.
- docs/releases.md — release-please configuration, the release-PR exemption, and the automation tokens.
- docs/enforcement.md — CODEOWNERS, branch protection, and how to verify enforcement.
- docs/customization.md — the customization record and its deviation levels.

## Do not

- Do not parse `ISSUE_STANDARD.md` as YAML.
- Do not introduce a second issue-title vocabulary.
- Do not change PR template field IDs casually.
- Do not let the common PR headings drift.
- Do not put repository-specific CI commands into shared templates.
- Do not exempt release PRs by actor.
- Do not merge the PR and release automation tokens.
- Do not treat a green lint run as cross-file verification.
- Do not overwrite an adopting repository's customized standard without reconciling its local changes.
