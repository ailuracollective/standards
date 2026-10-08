# AGENTS.md

Working instructions for agents and contributors.

`README.md` is the human entry point. This file holds only
repository-wide invariants, conventions, and pointers to detailed
procedures. Detailed procedures live in `docs/`.

## Repository

This repository is the source of the GitHub issue and pull-request
standards shared across `ailuracollective`. There is no application
code, build, or test suite.

The standard, copied by hand into adopting repositories:

- `.github/ISSUE_STANDARD.md` — the issue-writing standard (prose).
- `.github/labels.yml` — the reviewed label manifest; GitHub does not read it.
- `.github/ISSUE_TEMPLATE/` — the issue forms.
- `.github/PULL_REQUEST_TEMPLATE/` — the pull-request templates.
- `.github/CODEOWNERS` — code ownership.

Repository-only infrastructure, not copied:

- `.github/workflows/policy.yml` — PR policy enforcement.
- `.github/workflows/ci.yml` — lint and format checks.
- `.github/workflows/release.yml` — release-please.
- `release-please-config.json` and `.release-please-manifest.json` — release configuration.
- `.github/standards.local.example.yml` — the shape of a customization record.

Root documents: `README.md` (human entry point), `CONTRIBUTING.md`
(how to contribute), `CHANGELOG.md` (written by release-please).

Adopting repositories copy the standard files; changes here do not
propagate automatically. The file map, the sync model, and the
copy divergences are in docs/architecture.md.

## Critical invariants

### Issues

Issue types: `feat`, `fix`, `improvement`, `chore`, `test`, `docs`, `spike`.

Each type has exactly one issue template and one `title:` prefix.

Do not derive an issue type from the template filename: some
filenames are historical (`bug.yml`, `maintenance.yml`, `investigation.yml`).

Every issue template:

- applies `status/needs-review` itself, so an issue is never briefly unlabelled;
- uses only labels declared in `.github/labels.yml`;
- preserves existing field IDs;
- follows the common field structure unless the type genuinely needs an exception.

`ISSUE_STANDARD.md` is prose. Do not parse it as YAML.

### Pull requests

Pull-request titles use the Conventional Commit vocabulary: `feat`,
`fix`, `chore`, `docs`, `style`, `refactor`, `perf`, `test`,
`build`, `ci`, `revert`, `breaking-change`. Branch validation
accepts the same vocabulary except `breaking-change`.

The policy action has two deliberately different inputs:

- `type-labels` — the GitHub `type/*` labels;
- `title-types` — the pull-request title types and template resolution.

Do not combine these vocabularies. `breaking-change` is a PR/commit
type, not an issue type and not a `type/breaking-change` label.

The PR policy resolves the body template from the title, not from
the label.

The four common PR headings must remain identical across all PR
templates: `## Linked issue (required)`, `## Type (required)`,
`## Test plan`, `## Contributor checklist`.

`## Test plan` remains a TODO in this repository; adopting
repositories replace it with their own commands. Do not put
repository-specific commands into the shared PR templates.

### Labels

`.github/labels.yml` is a reviewed manifest, not GitHub configuration.

The core `type/*` vocabulary is frozen at five: `type/bug`,
`type/feature`, `type/improvement`, `type/task`, `type/documentation`.
`chore`, `test`, and `spike` use `type/task`.

Never reference a label that is not declared in the manifest: GitHub
silently drops unknown labels from issue and pull-request forms.

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

The repository is the canonical source for the shared standard, but
adopting repositories may intentionally diverge.

`.github/standards.local.yml` is an optional declaration of deviations.
It is not configuration and no workflow reads it. A deviation must
include a reason.

Core label families: `type/`, `status/`, `scope/`, `meta/`,
`github_actions`, `release/`. Do not add a new core `type/*` label for
a repository-specific concern; use an existing type plus an `extensions`
entry in the local customization record. See docs/customization.md.

## Security and workflow rules

`policy.yml` checks repository policy without executing code from the
PR head. Do not change this property without explicitly reviewing the
security impact.

Keep workflow permissions minimal. Every workflow job uses
`timeout-minutes: 10`, and the CI checkout uses `persist-credentials: false`.
Do not introduce secrets into workflows that execute untrusted PR code.
The PR policy and CI workflows intentionally remain safe for fork pull requests.

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

CODEOWNERS: the last matching rule wins and ownership is not additive.
Keep the catch-all rule — every repository path that needs code-owner
protection must match an owner. CODEOWNERS only has enforcement effect
through branch protection or rulesets. See docs/enforcement.md.

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
- Do not invent labels outside `.github/labels.yml`.
- Do not introduce a second issue-title vocabulary.
- Do not use `type/*` as a project-specific extension mechanism.
- Do not change PR template field IDs casually.
- Do not let the common PR headings drift.
- Do not put repository-specific CI commands into shared templates.
- Do not exempt release PRs by actor.
- Do not merge the PR and release automation tokens.
- Do not treat `labels.yml` or `standards.local.yml` as executable configuration.
- Do not claim a rule is enforced without checking branch protection or rulesets.
- Do not treat a green lint run as cross-file verification.
- Do not remove the CODEOWNERS catch-all.
- Do not assume CODEOWNERS rules are additive.
- Do not overwrite an adopting repository's customized standard without reconciling its local changes.
