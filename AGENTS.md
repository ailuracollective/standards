# AGENTS.md

Working reference for agents and contributors. `README.md` is the entry point for a
human; this file holds the invariants, the conventions, and the checks. Most rules
here exist because something went wrong the obvious way at least once.

## What this repository is

The origin of the GitHub issue and pull request standards shared across
`ailuracollective`. There is no application code, no build and no test suite.

| File                                                           | Owns                                      | Read by                                                   |
| -------------------------------------------------------------- | ----------------------------------------- | --------------------------------------------------------- |
| `.github/ISSUE_STANDARD.md`                                    | how an issue is written                   | humans and agents drafting issues                         |
| `.github/labels.yml`                                           | the label set (26 labels)                 | anything that reads or applies labels                     |
| `.github/ISSUE_TEMPLATE/*.yml` (7 templates + config)          | the forms in the issue chooser            | GitHub                                                    |
| `.github/PULL_REQUEST_TEMPLATE/*.md` (12 + default)            | the form per pull request type            | GitHub                                                    |
| `.github/CODEOWNERS`                                           | who reviews a change                      | GitHub, via branch protection                             |
| `.github/standards.local.example.yml`                          | the shape of a customization record       | a reader — or a checker, once one exists                  |
| `.github/workflows/policy.yml`                                 | the standard applied to this repository   | GitHub Actions, on every pull request that is not a draft |
| `.github/workflows/ci.yml`                                     | lint and format checks                    | GitHub Actions, on every pull request that is not a draft |
| `.github/workflows/release.yml`                                | when a release is cut                     | GitHub Actions, on every push to `main`                   |
| `release-please-config.json` + `.release-please-manifest.json` | the release type, and the current version | release-please                                            |

The first five rows are **the standard**: what an adopting repository copies. The
example file is opt-in (§ Customizing the standard). The last four serve this
repository only and are not copied.

Facts that are easy to get wrong:

- **`ISSUE_STANDARD.md` is prose, not data.** It was `ISSUE_STANDARD.yml` and did not
  parse — the numbered list under Purpose reads as mapping keys. Nothing should parse
  it and no validator should be pointed at it.
- **`labels.yml` is a reviewed record, not configuration.** GitHub does not read it
  and no CI parses it. Editing it changes no remote.
- **`policy.yml` never runs code under review.** It checks out the base branch, so
  nothing from the head reaches a runner holding a token.
- **`release.yml` is the only workflow that writes**, and the release files are the
  only ones a machine rewrites without a human-authored pull request (§ Releases).

### What is named here, and what is not

This file names `ailuracollective/actions`, because the gate lives there and every
input discussed below (`type-labels`, `title-types`, `approved-label`,
`auto-label-name`, `enable-body-structure`, `default-template`, the `v2` tag)
belongs to that action.

It names **no adopting repository**, on purpose: such a list is true when written
and wrong a week later, and a stale list reads as authoritative. § Enforcement
carries the method for checking any one repository instead.

"Here" means this repository. "An adopting repository" means any repository that
copied these files — there may be none, one, or many.

## Inventory

- **7** issue types, declared once in `ISSUE_STANDARD.md` § Issue Types.
- **7** issue templates — one per type — plus `config.yml`, which is not a template.
- **12** pull request templates — one per Conventional Commit type — plus a default
  `PULL_REQUEST_TEMPLATE.md`.
- **26** labels: five prefixed families (`type` 5, `status` 5, `scope` 8, `meta` 5,
  `release` 2) plus one unprefixed, `github_actions`.
- **38** files total:
  - 4 in `.github/`: `labels.yml`, `ISSUE_STANDARD.md`,
    `standards.local.example.yml`, `CODEOWNERS`;
  - 3 in `.github/workflows/`, 8 in `ISSUE_TEMPLATE/`, 13 in
    `PULL_REQUEST_TEMPLATE/` — so 13 YAML and 14 Markdown files under `.github/`;
  - 10 in the root: `AGENTS.md`, `CHANGELOG.md`, `README.md`, `CONTRIBUTING.md`,
    `LICENSE`, `release-please-config.json`, `.release-please-manifest.json`, and
    the lint configuration `.yamllint`, `pyproject.toml`, `uv.lock`.

`.gitignore` is not counted: it is local-only (listed in `.git/info/exclude`) and not
part of anything copied. `CHANGELOG.md` is written by release-please. The lint files
sit outside `.github/` so that nothing an adopting repository copies carries this
repository's lint settings.

Do not quote these numbers loosely; if you change one, update this section.

## The invariant: one type, one template, one title prefix

Every type in `ISSUE_STANDARD.md` has exactly one template, whose `title:` is the
type token plus a colon and one space.

| Type          | Template            | `title:`          | `labels:` (+ `status/needs-review`) | Opening pair           |
| ------------- | ------------------- | ----------------- | ----------------------------------- | ---------------------- |
| `feat`        | `feature.yml`       | `"feat: "`        | `type/feature`                      | Context, Objective     |
| `fix`         | `bug.yml`           | `"fix: "`         | `type/bug`                          | What happens, Expected |
| `improvement` | `improvement.yml`   | `"improvement: "` | `type/improvement`                  | Context, Objective     |
| `chore`       | `maintenance.yml`   | `"chore: "`       | `type/task`                         | Context, Objective     |
| `test`        | `test.yml`          | `"test: "`        | `type/task`                         | Context, Objective     |
| `docs`        | `docs.yml`          | `"docs: "`        | `type/documentation`                | Context, Objective     |
| `spike`       | `investigation.yml` | `"spike: "`       | `type/task`                         | Context, Question      |

- **Only 3 of 7 filenames match their type token.** The filename only drives chooser
  ordering. Do not derive a type from it, and do not "fix" it by renaming.
- `bug.yml` and `investigation.yml` replace Context/Objective with a pair that fits
  them; `investigation.yml` also carries an Expected outcome block. Everything from
  Scope onward is common to all seven.
- Every template applies `status/needs-review` itself, so an issue is never briefly
  unlabelled while waiting for the triage job.

### Why three templates map to `type/task`

Every `labels:` value must be a member of `labels.yml`: GitHub drops an unknown label
**without an error**. That used to be the case for every template — they applied
`enhancement`, `bug`, `documentation`, `maintenance`, `testing` and `investigation`,
none of which were declared, so every issue arrived with no type label.
(`enhancement` was also shared by `feature.yml` and `improvement.yml`.)

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
- `type/` is **frozen at five** (§ Customizing the standard). Growing it is not
  forbidden by any gate — each repository declares its own `type-labels` — but it is
  a change to every adopting repository's manifest and `policy.yml`, all copies that
  nothing synchronizes.

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
  forms. The colon forms (`status:approved`) exist on no remote, and a gate
  demanding them can never pass.

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

### The status comment

`v2` adds a sticky status comment, which needs a token that can write to the pull
request conversation. `comment-token` is separate from `github-token`, so the job's
own grant can stay read-only. Never widen `permissions` to `pull-requests: write`
instead — that hands a write grant to five scripts that only read.

| Choice                                      | Cost                                                                      |
| ------------------------------------------- | ------------------------------------------------------------------------- |
| `enable-status-comment: false`              | nothing; the job summary carries the same table                           |
| `comment-token` for an organisation account | a secret, but a person can edit the comment and the grant stays read-only |
| `comment-author` matching your own token    | no secret, but a `github-actions[bot]` comment can be edited by nobody    |

Prefer the second; this repository uses it (`AiluraKitty`). The third is a trap: it
works, but a bot comment outlives whoever would have fixed a wrong one. The token
decides the author; `comment-author` only states which identity is *required*, and
the action checks it against `gh api user` before writing.

## Sync model

This repository is the origin; each adopting repository holds its own copy under its
own `.github/`. **Edits here do not propagate.** There is no workflow, submodule or
bot. Copies are manual and drift is expected.

Three layers drift independently:

| Layer                    | What it is                      | How it goes stale                        |
| ------------------------ | ------------------------------- | ---------------------------------------- |
| The remote label set     | what GitHub actually has        | a label renamed or deleted by hand       |
| The manifest file        | the reviewed record             | edited here, never copied out            |
| The gate's `type-labels` | what the check compares against | a rename, or a scheme replaced wholesale |

All three must agree for a gate to be satisfiable. The first two drift silently;
the third turns any disagreement into a gate nobody can pass, which looks like the
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
- **Field id casing.** Kebab-case here (`out-of-scope`), possibly snake_case
  elsewhere. Only the id string differs, but it is a URL fragment.
- **Field types.** Only `textarea` and one `markdown` here. `checkboxes`,
  `render: shell`, `type: input` and explicit `required: false` are legitimate
  style choices elsewhere.
- **`blank_issues_enabled`.** `false` here; a per-repository policy choice.
- **Default pull request form.** Here it is inside the directory; others keep it at
  `.github/PULL_REQUEST_TEMPLATE.md`, or have none. The action's default is the
  beside-the-directory path, so the inside layout must set `default-template`.
  Copying only the directory omits the default silently.

### Enforcement: how to tell, for any repository

Configured and enforced are different questions, and the second is per repository,
per branch, and changes without a file being edited. So this section carries the
method, never a result. Check **both** APIs:

```sh
# classic branch protection — 404 means "no classic protection", NOT "unprotected"
gh api /repos/OWNER/REPO/branches/BRANCH/protection --jq '.required_status_checks'

# rulesets — a separate API, and the one people forget
gh api /repos/OWNER/REPO/rulesets --jq '.[] | "\(.id) \(.name) \(.enforcement)"'
for id in $(gh api /repos/OWNER/REPO/rulesets --jq '.[].id'); do
  gh api /repos/OWNER/REPO/rulesets/$id --jq \
    '.rules[] | select(.type=="required_status_checks") | .parameters.required_status_checks[].context'
done

# what the workflows actually report
gh pr view N --repo OWNER/REPO --json statusCheckRollup \
  --jq '.statusCheckRollup[].name' | sort -u
```

Reading a 404 from the first as "unprotected" when the branch moved to a ruleset has
already produced one confident, wrong claim here. Then compare required contexts
with reported ones:

| Required contexts                      | Meaning                                                          |
| -------------------------------------- | ---------------------------------------------------------------- |
| the policy job is **not** among them   | it annotates and is ignored                                      |
| it is there under a **different name** | unmergeable for anyone who cannot bypass protection              |
| a context **no workflow reports**      | the same, and invisible until someone without admin rights tries |

A required context is a literal string: `Branch name and PR title` does not match a
job named `Branch name`. Bypass permission hides both failures until it is removed.
Never describe a rule as binding without having read these for that repository and
branch.

## Releases

`release-please` runs on every push to `main`. When there is anything releasable it
opens **a pull request** with the version bump and a generated changelog; merging it
creates the tag and the release. Nothing is published directly, so a release is a
reviewed change like any other.

`release-please-config.json`, and why each key is there:

- **`release-type: simple`** — there is no package; the version lives only in
  `.release-please-manifest.json`.
- **`initial-version: 0.1.0`** — without it the first release is `1.0.0`, a
  compatibility claim nobody made.
- **`packages: { ".": … }`** — looks redundant, is not. The schema requires it, and
  `parseConfig` builds `repositoryConfig` from it, which `manifest.ts` dereferences
  on exactly this repository's path. Omitting it crashes on the first push, not at
  configuration time.

### The release pull request is exempt by head ref

Its head ref is `release-please--branches--<branch>` — hardcoded in
`src/util/branch-name.ts`, not configurable — and it has no type segment, no linked
issue, no template body and no `type/*` label. It cannot pass the gates, so
`policy.yml` skips both pull request jobs with:

```yaml
!startsWith(github.event.pull_request.head.ref, 'release-please--branches--')
```

Not `skip-actors`, which matches the login: the release account is the one behind
`AILURA_KITTY_TOKEN`, which also posts every status comment and is not exclusively a
machine identity. Exempting it would exempt everything it ever opens. A head ref
says what a pull request *is*; a human's branch has a type segment by choice.

The cost: an exempt pull request has **no check and no status comment**, so nothing
records that the exemption was deliberate.

Making release-please satisfy the checks (`extra-label`, a static
`pull-request-footer` with a closing keyword and the headings) was rejected: it
would name the same issue in every release and carry headings that exist only to be
grepped — a green board without a review.

### One token, two jobs

`release.yml` uses `AILURA_KITTY_TOKEN`, the same token `policy.yml` passes as
`comment-token`. release-please has no author setting and GitHub attributes API
commits to the calling token, so **the token is the author setting**; with
`GITHUB_TOKEN` every release commit is `github-actions[bot]`'s.

The trade, accepted deliberately: one credential posts comments **and** creates tags
and releases. Revoking it stops releases; a leak reaches further. A separate token
would carry the same scopes on the same account, so it would not be narrower.

Two prerequisites live outside this repository: `AiluraKitty` needs write access to
create tags, and the token needs `contents: write` and `issues: write` besides
`pull-requests: write`. Without both, the release pull request opens and then fails
at merge.

## Customizing the standard

Nothing records which differences between copies are intentional, so these four
cases look identical:

| What a repository did    | What it must also remember         | What goes wrong                              |
| ------------------------ | ---------------------------------- | -------------------------------------------- |
| added `area/auth`        | nothing                            | looks like drift forever                     |
| added `type/chore`       | edit `type-labels` in `policy.yml` | the second record is in no file anyone reads |
| recolored a core label   | the reason                         | invisible, and reverted by the next copy     |
| dropped `scope/security` | whether that was a decision        | cannot be told from an incomplete copy       |

The answer is an **opt-in** delta file, `.github/standards.local.yml`, whose schema
ships as `.github/standards.local.example.yml`. It records what a repository changed
and why.

**It declares; it does not configure. No workflow reads it, including the gate.** A
value written there changes nothing; the gate reads the repository's own
`policy.yml`. Keep this sentence through every future edit — the failure it prevents
is silent.

| Level | Deviation                                                                     | Process                                      |
| ----- | ----------------------------------------------------------------------------- | -------------------------------------------- |
| 0     | none — an exact copy                                                          | nothing to declare                           |
| 1     | a label in a family the core does not use                                     | no approval                                  |
| 2     | a core label's `color`/`description`, or a gate input's value                 | declare it with a reason                     |
| 3     | dropping a core label, changing an input's set, changing the manifest's shape | issue here first; `issue:` records which one |

- Level 1 needs no approval because level 2 does not either; a policy with an
  approval step at the bottom is one nobody follows.
- Reserved are the core families — `type/`, `status/`, `scope/`, `meta/`,
  `release/`, `github_actions` — not a closed list of new ones.
- `type/` is frozen at five. A project-specific type is an existing `type/*` label
  plus an entry in `extensions`.
- `reason` is **required** wherever a deviation is recorded. It is what separates a
  decision from rot.

### What a checker must be able to answer

The checker belongs to another project; the schema is its public interface. It must
answer:

- Does every label named in a field resolve against the manifest?
- Is every difference from the core declared in this file?
- Is a remote label missing from the manifest, or a manifest label missing from the
  remote?
- Does every level-3 deviation carry the issue that approved it?

And it must **not** report a missing file, or a missing optional field, as a defect.
Absence means "no deviations" by assumption. A checker that flags absence trains
every repository to create an empty file, which is indistinguishable from a
customized one at a glance.

## Conventions when editing

YAML (all thirteen files):

- 2-space indent; no tabs, no CRLF anywhere.
- Every file opens with `---`; the workflow trigger key is quoted as `"on":`. This
  keeps `.yamllint` on the `default` profile, changed only to a 120-column
  `line-length`.
- **Every** tracked text file ends with exactly one newline. There used to be a list
  of exceptions; it grew unnoticed and was closed, so `.yamllint` and `mdlint`
  (`MD047`) both enforce it.
- `config.yml` has no `contact_links` key: the schema rejects an empty list.
- Every workflow job sets `timeout-minutes: 10`, and `ci.yml` checks out with
  `persist-credentials: false`. The release-please schema URL is pinned to a tag in
  `ci.yml` and here; bump both together, because `main` changes without this
  repository changing.

`labels.yml`:

- Each entry has exactly `name`, `color`, `description`, in that order. Colors are
  quoted six-digit hex without `#` (`"D73A4A"`), the form `gh label create` expects.
  Descriptions are quoted and end with a period.
- One blank line between entries. Families in the order `type`,
  `status`, `scope`, `meta`, `github_actions`, `release`; within `type`: bug,
  feature, improvement, task, documentation. Neither is alphabetical — match the
  file, do not re-sort.

Issue templates:

- Top-level keys in order: `name`, `description`, `title`, `labels`, `body`.
- `title` is the bare prefix with a trailing space: `title: "feat: "`.
- Body order: Context → Objective → Scope → Constraints → Scenarios → Out of scope →
  Acceptance criteria → Dependencies → Notes, minus what a type does not need, with
  the two opening-pair exceptions above.
- Field `id`s are kebab-case and unique per file. They are URL fragments: renaming
  one breaks bookmarked and prefilled links.
- Required fields carry `validations: required: true`; optional fields carry only
  `label`, plus `description` when the label is not self-explanatory.
- `description` says what to write, `placeholder` shows an example, `value`
  pre-fills. Six of seven templates pre-fill acceptance criteria as a `- [ ]`
  checklist; `improvement.yml` does not, because "complete" is type-specific there.
- Only **26 of 55** fields have a `description`. Always described: the opening pair.
  `dependencies` and `notes` are bare everywhere but `feature.yml`, which describes
  all its fields and is the best model for a new template.
- Only `feature.yml` uses a `type: markdown` block. Use one only for guidance that
  must be read before filling a field, never to restate a field's description.

## Pull request templates

`.github/PULL_REQUEST_TEMPLATE/` holds 12 templates plus a default: `breaking-change`,
`build`, `chore`, `ci`, `docs`, `feat`, `fix`, `perf`, `refactor`, `revert`, `style`,
`test` — the eleven branch types `policy.yml` accepts, plus `breaking-change`.

With `enable-body-structure`, the gate requires **every `##` heading of the template
matching the title's type to appear in the body**, resolving that template from the
repository under review. These files are what make the gate mean the same thing
everywhere; a repository without them has nothing to be checked against.

- **Structure is universal; commands are not.** The `## Test plan` block is a `TODO`
  placeholder. Each adopting repository replaces it in the pull request that changes
  its CI. Never fill it in here: `cargo test` in a TypeScript repository is worse
  than a `TODO`.
- **Four headings appear in all thirteen files**: `## Linked issue (required)`,
  `## Type (required)`, `## Test plan`, `## Contributor checklist`. They are
  byte-identical except, inside `## Type (required)`, the `- [ ] \`type\`` checkbox
  and the label note under it. Change one, change all thirteen — divergence here is
  divergence in what the gate demands.
- **Each template names one `type/*` label.** Nine of twelve map to `type/task`.
  `breaking-change` has no label; the template says to apply the underlying change's
  label. `labels.yml` wins over any `type-labels`: the check compares exact names, so
  a mismatch is always the gate's misconfiguration, never the contributor's mistake.

Reconciling with a repository's own templates:

- Merge near-duplicate headings; demote the second one's real content to guidance
  inside the merged one.
- Adopt a unique section when it describes a *type* ("behaviour is unchanged",
  "packaging and version changes"), not a project.
- Leave out anything describing one project's strategy (frozen test vectors, a
  benchmark rig).
- Keep the four common headings byte-identical.

Two decisions worth keeping: `## Test plan` rather than `## Checks run`, because
"checks" invites a list of everything CI does; and perf's
`## Measurements (required)` carries the qualifier in the heading so an unmeasured
perf change looks incomplete at a glance.

## Ownership and enforcement

`.github/CODEOWNERS` assigns every path to `@SiddharthaGF`, the only collaborator
with write access. The eleven rules all resolve to that account, so the grouping
changes no outcome today; it is written so a second owner is a one-line change per
group. The **last** matching pattern wins and replaces earlier owners — rules are
not cumulative.

CODEOWNERS only binds through branch protection. `main` carries:

| Setting                                    | Value     |
| ------------------------------------------ | --------- |
| `require_code_owner_reviews`               | true      |
| `required_approving_review_count`          | 1         |
| `dismiss_stale_reviews`                    | true      |
| `require_last_push_approval`               | true      |
| `required_conversation_resolution`         | true      |
| `allow_force_pushes` / `allow_deletions`   | false     |
| `enforce_admins`                           | **false** |

**`enforce_admins: false` governs every other row**: protection does not apply to
admins, so the single admin can bypass all of it, force-push protection included.
It is off because of a deadlock, not a preference — the only code owner is the only
writer, and GitHub forbids approving your own pull request, so enforcing it would
freeze the repository. For the same reason the policy job is not a required status
check.

API traps, both silent: the field is `require_code_owner_reviews` (**plural**; the
singular returns 200 and does nothing), and the `PUT` must send
`required_status_checks` and `restrictions` explicitly as `null` or nothing applies.
Always read back:

```sh
gh api /repos/ailuracollective/standards/branches/main/protection \
  --jq '.required_pull_request_reviews.require_code_owner_reviews'   # must be true
```

**Enforcement is configured, not proven.** A test pull request shows
`REVIEW_REQUIRED`/`BLOCKED`, which a plain one-approval rule would also show. Proving
it, and making it a guarantee, takes one step: grant write access to a second person,
then set `enforce_admins` to true.

Until then: CODEOWNERS owns itself, so a pull request cannot remove the review it
needs; and nobody pushes straight to `main` even though they could — the review is
the point.

## Recipes

### Adding an issue type

1. Add it to `## Issue Types` in `ISSUE_STANDARD.md`, with an example under
   `## Title Convention`.
2. Add a template in `.github/ISSUE_TEMPLATE/` with `title: "<type>: "`. The filename
   need not be the token, but should be guessable.
3. Give it Context, Objective, Scope, Out of scope, Acceptance criteria,
   Dependencies, Notes, plus any field it can justify.
4. Choose its label from `type/*` before writing the file; never invent an
   undeclared one.
5. Update § Inventory and the invariant table.

### Adding a pull request type

1. Add `<type>.md`, named exactly for the Conventional Commit type — the filename is
   the key the gate resolves.
2. Copy the four common headings verbatim, adjusting only the checkbox and label note
   in `## Type (required)`.
3. Name one `type/*` label (`type/task` is the catch-all).
4. Keep `## Test plan` as `TODO`.
5. If it is also a branch type, add it to `branch-types` in every consuming
   `policy.yml`.

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

## Validation

`yamllint`, `check-jsonschema`, `mdlint`, `actionlint` (with `shellcheck` and `pyflakes`,
which it runs on the embedded scripts) and `yamlfix` are pinned in the `lint` and
`format` groups of `pyproject.toml`. There is no wrapper script: `uv` has no task
runner, and each tool already reads its own configuration, so the commands are the
tools themselves.

`.github/workflows/ci.yml` runs the lint and format commands below on every pull request
that is ready for review, as a single job: one runner, one checkout and one `uv sync`.
Every lint and format step carries `if: ${{ !cancelled() }}`, so a failure does not hide
the steps after it and one run reports everything. A draft is skipped
(`github.event.pull_request.draft == false`), and the `ready_for_review` event starts
the run when it stops being one; the pull request jobs
of `policy.yml` follow the same rule. `release.yml` and the issue triage job do not.
**The cross-file checks further down are not in CI yet**,
nor are the two `gh api` checks, which need a token. The workflow holds `contents: read`
and no secrets, so it is safe on a pull request from a fork. Like the policy job, it is
**not a required status check**: that is a branch-protection setting, not a file.

```sh
# lint — each exits non-zero on any finding
uv run yamllint .
uv run mdlint check . .github
uv run check-jsonschema --builtin-schema vendor.github-workflows .github/workflows/*.yml
find .github/ISSUE_TEMPLATE -name '*.yml' ! -name config.yml \
  -exec uv run check-jsonschema --builtin-schema vendor.github-issue-forms {} +
uv run check-jsonschema --builtin-schema vendor.github-issue-config .github/ISSUE_TEMPLATE/config.yml
uv run check-jsonschema --schemafile \
  https://raw.githubusercontent.com/googleapis/release-please/v17.11.2/schemas/config.json \
  release-please-config.json
uv run actionlint .github/workflows/*.yml

# format — add --check to change nothing
uv run yamlfix -i '*.yml' -e '.cache/**' -e '.github/standards.local.example.yml' .
uv run mdlint check --fix --select MD060 . .github
```

Where the strictness lives:

- **`yamllint`** reads `.yamllint`: the `default` profile with its four warning-level
  rules (`comments`, `comments-indentation`, `document-start`, `truthy`) raised to
  errors, so a plain run fails on them and `--strict` is not needed. It also ignores
  the tool caches, listed there because `.gitignore` is local-only.
- **`mdlint`** reads `[tool.mdlint]`. **It skips hidden directories** unless named:
  a bare `mdlint check` lints three files and silently misses all of `.github/`,
  which is why `.github` is on every command above.
- **`yamlfix`** reads `[tool.yamlfix]`, which keeps this repository's style; its
  defaults turn `"on":` back into `on:` and expand every flow list. Its `--include`
  defaults to `*.yaml`, so `-i '*.yml'` is required, and the exclude glob must be
  `.cache/**` (`.cache/*` matches nothing). It skips `standards.local.example.yml`,
  whose commented examples it would delete.
- **`mdformat` is not used:** without a GFM plugin it flattens tables, escapes
  `<type>`, breaks code spans containing a backtick, and renumbers ordered lists.

**A green lint is not verification**: linters see
one file at a time, while the checks below cover relationships *between* files —
the defect they were written for (templates applying labels the manifest never
declared) is invisible to every linter.

There is no test suite. Before proposing a change, run (needs `pyyaml`):

```sh
# every file must parse as YAML
python3 -c "import yaml,glob;[yaml.safe_load(open(f)) for f in glob.glob('.github/**/*.yml',recursive=True)]"

# label names unique, colors well-formed, count as documented
python3 - <<'PY'
import re
txt = open('.github/labels.yml').read()
names = re.findall(r'- name: "([^"]+)"', txt)
assert len(names) == len(set(names)), 'duplicate label name'
assert len(names) == 26, f'expected 26 labels, found {len(names)}'
assert all(re.fullmatch(r'[0-9A-Fa-f]{6}', c) for c in re.findall(r'color: "([0-9A-Fa-f]{6})"', txt))
print(len(names), 'labels ok')
PY

# every label NAMED IN A FIELD resolves against the manifest. Reads fields, not raw
# text, so the comment saying there is no `type/breaking-change` is not reported.
python3 - <<'PY'
import glob, sys, yaml
have = {e['name'] for e in yaml.safe_load(open('.github/labels.yml'))}
bad = []
for f in sorted(glob.glob('.github/**/*.yml', recursive=True)):
    doc = yaml.safe_load(open(f))
    if not isinstance(doc, dict):
        continue
    for l in (doc.get('labels') or []):
        if l not in have:
            bad.append(f'{f}: labels: {l}')
    for job in (doc.get('jobs') or {}).values():
        for step in (job or {}).get('steps') or []:
            w = step.get('with') or {}
            for key in ('type-labels', 'approved-label', 'auto-label-name'):
                for l in (w.get(key) or '').split(','):
                    l = l.strip()
                    if l and l not in have:
                        bad.append(f'{f}: {key}: {l}')
for b in bad:
    print('DANGLING', b)
print('no dangling label references' if not bad else f'{len(bad)} dangling')
sys.exit(1 if bad else 0)
PY

# the workflow's two vocabularies are as documented, and disjoint
python3 - <<'PY'
import re
txt = open('.github/workflows/policy.yml').read()
labels = re.search(r'type-labels: (\S+)', txt).group(1).split(',')
titles = re.search(r'title-types: (\S+)', txt).group(1).split(',')
assert labels == ['type/feature','type/bug','type/documentation','type/improvement','type/task'], labels
assert len(titles) == 12, titles
assert not set(labels) & set(titles), 'the two sets must not overlap'
print(len(labels), 'labels,', len(titles), 'title types, disjoint')
PY

# one issue template per type (scope the grep to the section: the whole file gives 14)
sed -n '/^## Issue Types/,/^## Title/p' .github/ISSUE_STANDARD.md | grep -c '^- `'   # 7
ls .github/ISSUE_TEMPLATE/*.yml | grep -vc config                                    # 7
grep -h '^title: ' .github/ISSUE_TEMPLATE/*.yml | sort                               # 7 prefixes

# pull request templates and their common headings
find .github/PULL_REQUEST_TEMPLATE -name '*.md' ! -name 'PULL_REQUEST_TEMPLATE.md' | wc -l  # 12
find .github/PULL_REQUEST_TEMPLATE -name '*.md' | wc -l                                   # 13
for h in 'Linked issue (required)' 'Type (required)' 'Test plan' 'Contributor checklist'; do
  printf '%-24s %s/13\n' "$h" "$(grep -lF "## $h" .github/PULL_REQUEST_TEMPLATE/*.md | wc -l)"
done
grep -rn 'vp check\|pnpm run\|cargo ' .github/PULL_REQUEST_TEMPLATE/ \
  | grep -v 'cannot run' || echo 'no hardcoded CI commands'

# CODEOWNERS parses (GitHub skips bad lines silently) and every owner can push
gh api repos/ailuracollective/standards/codeowners/errors --jq '.errors'   # expect []
gh api repos/ailuracollective/standards/collaborators \
  --jq '.[] | select(.permissions.push) | .login'                          # owners must appear

# release files validate, and `packages` keys match the manifest paths
curl -sSL -o /tmp/rp-schema.json \
  https://raw.githubusercontent.com/googleapis/release-please/v17.11.2/schemas/config.json
python3 -m venv /tmp/yamlenv && /tmp/yamlenv/bin/pip -q install pyyaml jsonschema
/tmp/yamlenv/bin/python - <<'PY'
import json, jsonschema
cfg = json.load(open('release-please-config.json'))
man = json.load(open('.release-please-manifest.json'))
jsonschema.validate(cfg, json.load(open('/tmp/rp-schema.json')))
assert set(cfg['packages']) == set(man), f"packages vs manifest: {set(cfg['packages']) ^ set(man)}"
assert cfg['initial-version'] == '0.1.0', 'the first release must not claim 1.0.0'
print(len(man), 'release path(s), config and manifest agree')
PY

# the head-ref exemption covers release branches and nothing else
python3 - <<'PY'
PREFIX = 'release-please--branches--'
exempt = ['release-please--branches--main',
          'release-please--branches--master',
          'release-please--branches--master--components--core']
runs   = ['siddharthagf/feat/customization-policy', 'dependabot/npm_and_yarn/core-1.2.3']
assert all(r.startswith(PREFIX) for r in exempt), 'a release PR would hit the gate'
assert not any(r.startswith(PREFIX) for r in runs),   'a human PR would be exempted'
print(f'{len(exempt)} release refs exempt, {len(runs)} human refs still checked')
PY
```

Notes on the block:

- Count typed templates with `! -name 'PULL_REQUEST_TEMPLATE.md'`, not
  `grep -v PULL_REQUEST_TEMPLATE` — every path contains the directory name, so that
  returns zero.
- The issue-type count is a text check on prose: a declaration has the colon outside
  the backticks (`feat`:), an example inside (`feat: ...`).
- The hardcoded-command grep matters most: a repository-specific command in these
  files makes the gate demand a check other repositories cannot run.

Functional verification is manual: on a test repository with these files, confirm
the seven forms render, the blank option is hidden, and the expected labels apply. A
label the repository lacks is dropped without an error, so "no label appeared"
usually means a missing remote label, not a broken change.

## Do not

Standard and templates:

- Do not add an issue template without adding its type to `ISSUE_STANDARD.md`.
- Do not convert `ISSUE_STANDARD.md` back to YAML, point a parser or `.yamllint` at
  it, or add a `*.md` file to a YAML glob.
- Do not rename a template file without checking references, and never change or
  remove a body field `id`.
- Do not introduce a second title vocabulary; `breaking-change` is not an issue type.
- Do not fill in `## Test plan` commands, and do not let the four common pull
  request headings drift.

Labels and customization:

- Do not treat `labels.yml` or `standards.local.yml` as configuration. Neither is
  read by anything; the failure is silent.
- Do not record a deviation without a `reason`.
- Do not grow `type/*`, here or for one repository's concern. Use the five plus an
  `extensions` entry.
- Do not overwrite an adopting repository's `labels.yml` without porting its header
  and reconciliation recipe.

Releases:

- Do not exempt the release pull request with `skip-actors`, and do not make
  release-please fake its way through the gates with a static footer.
- Do not drop `initial-version`, raise it above `0.1.0` without a release that earns
  it, or omit `packages`.

Verification and ownership:

- Do not treat a green lint as verification.
- Do not write "the gate requires" about this repository, or call a rule binding
  anywhere without checking per § Enforcement.
- Do not drop the `*` catch-all from `CODEOWNERS`. It is the only owner of
  `README.md`, `CONTRIBUTING.md`, `LICENSE`, `CHANGELOG.md`, `policy.yml`
  and the lint files; an unowned file skips the code-owner gate.
- Do not add an owner to one rule expecting it to be additive:
  `.github/labels.yml @alice` *replaces* @SiddharthaGF on that path.
