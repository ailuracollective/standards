# Architecture

Where everything lives, how copies drift, and how to extend the
standard. `AGENTS.md` holds the invariants; this file holds the detail
behind them.

## What this repository is

The origin of the GitHub issue and pull request standards shared
across `ailuracollective`. There is no application code, no build, and
no test suite.

| File                                                           | Owns                                      | Read by                                                                |
| -------------------------------------------------------------- | ----------------------------------------- | ---------------------------------------------------------------------- |
| `.github/CONTRACT.yml`                                         | the canonical issue and PR contract       | humans, agents, and CI (`scripts/validate_contract.py`)                |
| `.github/ISSUE_STANDARD.md`                                    | how an issue is written                   | humans and agents drafting issues                                      |
| `.github/labels.yml`                                           | the label set                             | anything that reads or applies labels                                  |
| `.github/ISSUE_TEMPLATE/*.yml` (7 templates + config)          | the forms in the issue chooser            | GitHub                                                                 |
| `.github/PULL_REQUEST_TEMPLATE/*.md` (12 + default)            | the form per pull request type            | GitHub                                                                 |
| `.github/CODEOWNERS`                                           | who reviews a change                      | GitHub, via branch protection                                          |
| `scripts/validate_contract.py`                                 | contract drift detection                  | GitHub Actions, on every pull request                                  |
| `.github/standards.local.example.yml`                          | the shape of a customization record       | a reader — or a checker, once one exists                               |
| `.github/workflows/policy.yml`                                 | the standard applied to this repository   | GitHub Actions, on every non-draft pull request and every opened issue |
| `.github/workflows/ci.yml`                                     | lint and format checks                    | GitHub Actions, on every pull request that is not a draft              |
| `.github/workflows/release.yml`                                | when a release is cut                     | GitHub Actions, on every push to `main`                                |
| `release-please-config.json` + `.release-please-manifest.json` | the release type, and the current version | release-please                                                         |

The first seven rows are **the standard**: what an adopting repository
copies. The example file is opt-in (docs/customization.md). The last
four serve this repository only and are not copied.

`templates/` holds the parts of an adoption that are **skeletons**, not
copies of a working file: `AGENTS.md`, and the `ci.yml` / `release.yml`
workflows. Everything else — `policy.yml`, `scripts/validate_contract.py`,
and the standard artifacts — is copied verbatim from the real files at the
repository root. Nothing is duplicated, so nothing can drift.

Facts that are easy to get wrong:

- **`CONTRACT.yml` is the source of truth.** It defines the canonical
  issue and PR contract. CI validates that templates match it. If
  CONTRACT.yml and a template disagree, the template is wrong.
- **`ISSUE_STANDARD.md` is documentation, not data.** It describes the
  contract for humans. It is not parsed by any tool.
- **`labels.yml` is a reviewed record, not configuration.** GitHub does not read it
  and no CI parses it. Editing it changes no remote.
- **`policy.yml` never runs code under review.** The action checks out the base
  branch, so nothing from the head reaches a runner holding a token.
- **`release.yml` is the only workflow that writes**, and the release files are the
  only ones a machine rewrites without a human-authored pull request (docs/releases.md).

### What is named here, and what is not

This file names `ailuracollective/actions`, because the gate lives
there and every input discussed below (`type-labels`, `title-types`,
`approved-label`, `auto-label-name`, `enable-body-structure`,
`default-template`, the `v2` tag) belongs to that action.

It names **no adopting repository**, on purpose: such a list is true
when written and wrong a week later, and a stale list reads as
authoritative. docs/enforcement.md carries the method for checking any
one repository instead.

"Here" means this repository. "An adopting repository" means any
repository that copied these files — there may be none, one, or many.

## Automation identities

Two secrets run the workflows, one per function. No secret value
lives in the repository; this file names them only.

| Secret                       | Where                         | Function                                         |
| ---------------------------- | ----------------------------- | ------------------------------------------------ |
| `AILURA_PR_COMPLIANCE_TOKEN` | `policy.yml`, `comment-token` | the status comment on every pull request         |
| `AILURA_RELEASE_TOKEN`       | `release.yml`, `token`        | release-please: the release PR, tag, and release |

The compliance token is a PAT of the **AiluraKitty** account,
because `comment-author: AiluraKitty` is verified before the
action writes. The release token's holder authors the release
commits — release-please has no author setting. `GITHUB_TOKEN`
is deliberately not used for either: a `github-actions[bot]`
comment cannot be edited by anyone, and release commits would be
attributed to the bot. Each token's scope, revocation, and the
rules that keep the split meaningful are in docs/releases.md.

## The canonical contract

[CONTRACT.yml](../.github/CONTRACT.yml) is the source of truth for the
issue and PR contract. It defines:

- **Issue common sections**: Context, Goal, Scope, Acceptance criteria,
  Non-goals (optional), Constraints (optional), References (optional)
- **Issue type-specific deltas**: only Bug and Spike add sections
- **PR common sections**: Linked issue, Summary, Changes, Verification,
  Risk / compatibility (optional), Migration (optional)
- **PR type-specific deltas**: only breaking-change, perf, ci, and build
  add sections
- **Taxonomy mappings**: the relationship between issue types, PR title
  types, branch types, and labels
- **AI-agent contract**: rules for agents consuming issues and PRs

CI validates that templates match the contract:

```sh
uv run python scripts/validate_contract.py
```

### Contract validation

`scripts/validate_contract.py` is part of the standard: an adopting
repository copies it by hand alongside `CONTRACT.yml` and the templates.
It imports PyYAML, so run it in an environment that provides it:

```sh
uv run --with PyYAML python scripts/validate_contract.py
```

Wire the same command into the repository's CI (here, the *Contract
validation* step in `.github/workflows/ci.yml`). The check fails when a
template's sections, headings, labels, or taxonomy mappings drift from
`CONTRACT.yml`. Because it runs against the copied files, an adopter gets
the same drift detection this repository does.

### The invariant: one type, one template, one title prefix

Every type in CONTRACT.yml has exactly one template, whose
`title:` is the type token plus a colon and one space.

| Type          | Template            | `title:`          | `labels:` (+ `status/needs-review`) | Extra sections                                     |
| ------------- | ------------------- | ----------------- | ----------------------------------- | -------------------------------------------------- |
| `feat`        | `feat.yml`          | `"feat: "`        | `type/feature`                      | —                                                  |
| `fix`         | `bug.yml`           | `"fix: "`         | `type/bug`                          | Observed behavior, Expected behavior, Reproduction |
| `improvement` | `improvement.yml`   | `"improvement: "` | `type/improvement`                  | —                                                  |
| `chore`       | `maintenance.yml`   | `"chore: "`       | `type/task`                         | —                                                  |
| `test`        | `test.yml`          | `"test: "`        | `type/task`                         | —                                                  |
| `docs`        | `docs.yml`          | `"docs: "`        | `type/documentation`                | —                                                  |
| `spike`       | `investigation.yml` | `"spike: "`       | `type/task`                         | Question, Deliverable                              |

- **Only 3 of 7 filenames match their type token.** The filename only drives chooser
  ordering. Do not derive a type from it, and do not "fix" it by renaming.
- Every template applies `status/needs-review` itself, so an issue is never briefly
  unlabelled while waiting for the triage job.

### Why three templates map to `type/task`

Every `labels:` value must be a member of `labels.yml`: GitHub drops an
unknown label **without an error**. That used to be the case for every
template — they applied `enhancement`, `bug`, `documentation`,
`maintenance`, `testing` and `investigation`, none of which were declared,
so every issue arrived with no type label. (`enhancement` was also shared
by `feat.yml` and `improvement.yml`.)

Three types have no label of their own, and the mapping is a judgement call:

- `chore` → `type/task`. Unambiguous: `type/task` was declared and applied by
  nothing, which marks it as `chore`'s intended home.
- `test` → `type/task`. `scope/testing` exists but is a scope, and using a scope as a
  type is a category error. A test-only change is "a defined piece of work that is
  not a feature or bug" — the manifest's own description of `type/task`.
- `spike` → `type/task`. The weakest of the three, and the first to revisit if the
  family grows. It is the least-wrong available answer, not a claim that a spike is
  a task.

## Three vocabularies

Keeping these apart is the most common source of confusion here.

| Vocabulary            | Members                                                           | Where it applies                                                   |
| --------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------ |
| Label family `type/*` | 5: `bug`, `feature`, `improvement`, `task`, `documentation`       | the PR type-label gate                                             |
| Issue title types     | 7: `feat`, `fix`, `improvement`, `chore`, `test`, `docs`, `spike` | this standard and the issue chooser                                |
| Conventional Commit   | 12 (the pull request template filenames)                          | PR titles, release tooling; branch names (minus `breaking-change`) |

- `breaking-change` is a Conventional Commit type only. It is not an issue type, and
  there is deliberately no `type/breaking-change`.
- `type/` is **frozen at five** (docs/customization.md). Growing it is not forbidden by
  any gate — each repository declares its own `type-labels` — but it is a change to
  every adopting repository's manifest and `policy.yml`, all copies that nothing
  synchronizes.

### `type-labels` and `title-types`

`type-labels` once fed three checks: the label check, the title grammar, and pull
request template resolution. No value could satisfy all three:

| Value of `type-labels` | Label check                                      | Title grammar                          | Template resolution                      |
| ---------------------- | ------------------------------------------------ | -------------------------------------- | ---------------------------------------- |
| `feat,fix,…` (bare)    | **unsatisfiable** — no such labels on any remote | works                                  | works                                    |
| `type/feature,…`       | works                                            | **rejects every `feat:`/`fix:` title** | **hard error** — `/` is a path character |

So `ailuracollective/actions` gained `title-types`, which feeds the grammar and
template resolution; `type-labels` feeds the label check alone. `title-types`
defaults to `type-labels`. An adopting repository declares both:

- `type-labels`: the five `type/*` labels;
- `title-types`: the twelve Conventional Commit types;
- `approved-label: status/ready` and `auto-label-name: status/needs-review` — slash
  forms. The colon forms (`status:approved`) exist on no remote, and a gate demanding
  them can never pass.

Consequences in the action, both deliberate:

- **The body template resolves from the title, not the label.** Each check owns its
  own failure, so a pull request missing both a label and a section hears about
  both. When the title's type is not allowed, `pr-body-structure` reports `skip`
  and names `pr-title-conventional` as the owner.
- The `type-label` error message reads its example from the configured set rather
  than claiming labels are "all bare".

**A fix in the action only takes effect when a tag moves.** Workflows write
`uses: ailuracollective/actions/pull-request@v2`, which resolves the tag, not
`main`, and moving it changes every repository at once. Check before assuming:

```sh
gh api /repos/ailuracollective/actions/git/refs/tags/v2 --jq '.object.sha'
gh api /repos/ailuracollective/actions/commits/main --jq .sha   # equal means the tag is current
```

## Sync model

The rule is in the organisation conventions: the standard is copied by hand, and
nothing propagates. What follows is this repository's detail behind that rule.

Three layers drift independently:

| Layer                    | What it is                      | How it goes stale                        |
| ------------------------ | ------------------------------- | ---------------------------------------- |
| The remote label set     | what GitHub actually has        | a label renamed or deleted by hand       |
| The manifest file        | the reviewed record             | edited here, never copied out            |
| The gate's `type-labels` | what the check compares against | a rename, or a scheme replaced wholesale |

All three must agree for a gate to be satisfiable. The first two drift silently; the
third turns any disagreement into a gate nobody can pass, which looks like the
contributor's mistake. Reconcile all three in one change, against the remote rather
than another copy of the manifest.

Divergences to know before copying in either direction:

- **Manifest shape.** This `labels.yml` is a bare top-level sequence; another may
  nest under `labels:`. Both parse, so a mechanical copy changes the schema without
  failing. Copying this file over another is an upgrade in content and a regression
  in form: port the target's header and reconciliation recipe instead.
- **Quote every color.** Unquoted hex resolves differently per tool: `yq`
  (`yaml.v3`) turns `000000` into `0`, `008672` into `8672` and `5319E7` into
  `53190000000`; PyYAML converts only the all-digit ones. Either way
  `gh label create` receives a number, silently.
- **Field id casing.** Kebab-case here (`non-goals`), possibly snake_case
  elsewhere. Only the id string differs, but it is a URL fragment.
- **Field types.** Only `textarea` here. `checkboxes`,
  `render: shell`, `type: input` and explicit `required: false` are legitimate
  style choices elsewhere.
- **`blank_issues_enabled`.** `false` here; a per-repository policy choice.
- **Default pull request form.** Here it is inside the directory; others keep it at
  `.github/PULL_REQUEST_TEMPLATE.md`, or have none. The action's default is the
  beside-the-directory path, so the inside layout must set `default-template`.
  Copying only the directory omits the default silently.

## Recipes

### Adding an issue type

1. Add it to CONTRACT.yml under `issue.types`, with its `title_prefix`, `label`,
   and `extra` sections.
2. Add a template in `.github/ISSUE_TEMPLATE/` with `title: "<type>: "`. The filename
   need not be the token, but should be guessable.
3. Give it the common sections from CONTRACT.yml, plus any type-specific sections.
4. Choose its label from `type/*` before writing the file; never invent an
   undeclared one.
5. Update the invariant table above.
6. Run `uv run python scripts/validate_contract.py` to verify.

### Adding a pull request type

1. Add it to CONTRACT.yml under `pr.types`, with its `extra` sections.
2. Add `<type>.md`, named exactly for the Conventional Commit type — the filename is
   the key the gate resolves.
3. Copy the common headings verbatim, adjusting only the type-specific sections.
4. Name one `type/*` label (`type/task` is the catch-all).
5. If it is also a branch type, add it to `branch-types` in every consuming
   `policy.yml`.
6. Run `uv run python scripts/validate_contract.py` to verify.

### Adding or changing a label

1. Edit `.github/labels.yml`, keeping the three-key shape and family order.
2. Reuse a family color where the meaning matches (`type/feature` and
   `type/documentation` share `0075CA`).
3. For a `type/*` label, also update every adopting repository's manifest and its
   `type-labels`. A gate naming a label the remote lacks is unsatisfiable.
4. Removing an entry does not remove the remote label. The apply recipe is in the
   header of `labels.yml`; read the target's own copy before overwriting it.
5. A change for **one** repository is not an edit here: declare it in that
   repository's `standards.local.yml` under `extensions`.

### `labels.yml`

- Each entry has exactly `name`, `color`, `description`, in that order. Colors are
  quoted six-digit hex without `#` (`"D73A4A"`), the form `gh label create` expects.
  Descriptions are quoted and end with a period.
- One blank line between entries. Families in the order `type`, `status`, `scope`,
  `meta`, `github_actions`, `release`; within `type`: bug, feature, improvement,
  task, documentation. Neither is alphabetical — match the file, do not re-sort.

### Issue templates

- Top-level keys in order: `name`, `description`, `title`, `labels`, `body`.
- `title` is the bare prefix with a trailing space: `title: "feat: "`.
- Body order: the common sections from CONTRACT.yml, then the type-specific
  sections. The common sections are Context, Goal, Scope, Acceptance criteria,
  Non-goals, Constraints, References.
- Field `id`s are kebab-case and unique per file. They are URL fragments: renaming
  one breaks bookmarked and prefilled links.
- `description` says what to write, `placeholder` shows an example, `value`
  pre-fills. Most templates pre-fill acceptance criteria as a `- [ ]` checklist.
- `config.yml` has no `contact_links` key: the schema rejects an empty list.

### Pull request templates

`.github/PULL_REQUEST_TEMPLATE/` holds 12 templates plus a default:
`breaking-change`, `build`, `chore`, `ci`, `docs`, `feat`, `fix`, `perf`,
`refactor`, `revert`, `style`, `test` — the eleven branch types `policy.yml` accepts,
plus `breaking-change`.

With `enable-body-structure`, the gate requires **every `##` heading of the template
matching the title's type to appear in the body**, resolving that template from the
repository under review. These files are what make the gate mean the same thing
everywhere; a repository without them has nothing to be checked against.

- **Structure is universal; commands are not.** The `## Verification` block asks
  for evidence, not commands. Each adopting repository replaces it in the pull
  request that changes its CI. Never fill it in here: `cargo test` in a TypeScript
  repository is worse than a TODO.
- **Common headings appear in all files**: `## Linked issue`, `## Summary`,
  `## Changes`, `## Verification`, `## Risk / compatibility`, `## Migration`.
  They are identical across all files. Change one, change all — divergence here is
  divergence in what the gate demands.
- **Each of the twelve names at most one `type/*` label.** Eight of the twelve map
  to `type/task`; `feat`, `fix` and `docs` map to their own label. `breaking-change`
  names none; the template says to apply the underlying change's label. `labels.yml`
  wins over any `type-labels`: the check compares exact names, so a mismatch is
  always the gate's misconfiguration, never the contributor's mistake.

Reconciling with a repository's own templates:

- Merge near-duplicate headings; demote the second one's real content to guidance
  inside the merged one.
- Adopt a unique section when it describes a *type* ("behaviour is unchanged",
  "packaging and version changes"), not a project.
- Leave out anything describing one project's strategy (frozen test vectors, a
  benchmark rig).
- Keep the common headings identical.

Two decisions worth keeping: `## Verification` rather than `## Test plan`, because
"test plan" invites a list of commands CI already runs; and perf's
`## Measurements` carries the qualifier in the heading so an unmeasured
perf change looks incomplete at a glance.
