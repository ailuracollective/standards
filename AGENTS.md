# AGENTS.md

Guidance for AI agents and contributors working in this repository.

## What this repository is

The source of truth for GitHub issue standards shared across an organisation's
repositories. There is no application code here, no build and no test suite.
`README.md` is the entry point for a human; this file is the working reference.
Under `.github/` there are **10 YAML files, 14 Markdown files, and 1 CODEOWNERS
file**; four more files sit in the repository root.

Six artifacts, each with exactly one owner:

| File                                                   | Owns                                     | Read by                                     |
| ------------------------------------------------------ | ---------------------------------------- | ------------------------------------------- |
| `.github/ISSUE_STANDARD.md`                            | how an issue is written                  | humans and agents drafting issues           |
| `.github/labels.yml`                                   | the label set (30 labels)                | anything that reads or applies labels       |
| `.github/ISSUE_TEMPLATE/*.yml` (7 templates + config)  | the forms in the issue chooser           | GitHub                                      |
| `.github/PULL_REQUEST_TEMPLATE/*.md` (12 + default)    | the form per pull request type           | GitHub                                      |
| `.github/CODEOWNERS`                                   | who reviews a change                     | GitHub, via branch protection               |
| `.github/workflows/policy.yml`                         | the projection of all of the above      | GitHub Actions, on every pull request       |

`ISSUE_STANDARD.md` is **prose and is not machine-readable**. It was
`ISSUE_STANDARD.yml` and did not parse as YAML — the numbered list under Purpose
reads as mapping keys, so the file failed to load from its first numbered line
onward. It was renamed rather than repaired. Nothing should parse it, and no
validator should be pointed at it.

Nothing in this repository is application code. `labels.yml` is a reviewed
manifest, not workflow input: GitHub does not read it and no CI parses it.
Editing it changes the *record* of the label set, not the labels on any remote.

`.github/workflows/policy.yml` is the exception to "nothing here runs", and it
runs nothing of this repository either. It checks out the base branch, never the
head, so no code under review reaches a runner holding a token. It is the
standard projected onto its own repository, and it is what makes this repository's
templates and labels load-bearing rather than decorative — see § Enforcement.

## Inventory

- **7** issue types, declared once in `ISSUE_STANDARD.md` § Issue Types.
- **7** templates — one per type — plus `config.yml`, which is not a template.
- **12** pull request templates — one per Conventional Commit type — plus a
  default `PULL_REQUEST_TEMPLATE.md`.
- **30** labels: six prefixed families (`type` 5, `priority` 4, `status` 5,
  `scope` 8, `meta` 5, `release` 2) plus one unprefixed, `github_actions`.
- **29** files total: 3 in `.github/` (`labels.yml`, `ISSUE_STANDARD.md`,
  `CODEOWNERS`), 1 in `.github/workflows/`, 8 in `ISSUE_TEMPLATE/`, 13 in
  `PULL_REQUEST_TEMPLATE/`, and 4 in the repository root (`AGENTS.md`,
  `README.md`, `CONTRIBUTING.md`, `LICENSE`).
  Do not quote these numbers loosely; if you change one of them, update this
  section.

## The invariant: one type, one template, one title prefix

Every type in `ISSUE_STANDARD.md` has exactly one template, and that template's
`title:` is exactly the type token plus a colon and one space. Seven types, seven
templates, no gaps in either direction.

| Type         | Template               | `title:`          | Body's opening pair          |
| ------------ | ---------------------- | ----------------- | ---------------------------- |
| `feat`       | `feature.yml`          | `"feat: "`        | Context, Objective           |
| `fix`        | `bug.yml`              | `"fix: "`         | What happens, Expected       |
| `improvement`| `improvement.yml`      | `"improvement: "` | Context, Objective           |
| `chore`      | `maintenance.yml`      | `"chore: "`       | Context, Objective           |
| `test`       | `test.yml`             | `"test: "`        | Context, Objective           |
| `docs`       | `docs.yml`             | `"docs: "`        | Context, Objective           |
| `spike`      | `investigation.yml`    | `"spike: "`       | Context, Question            |

**Only 3 of the 7 filenames match their type token.** `feat`→`feature`,
`fix`→`bug`, `chore`→`maintenance`, `spike`→`investigation`. The filename is not
load-bearing for anything except the chooser's ordering, so do not assume you can
derive a type from a filename, and do not "fix" the mismatch by renaming —
`bug.yml` and `maintenance.yml` are understood names.

Two templates substitute their own opening pair for Context/Objective, because
the standard's pair does not fit them: `bug.yml` asks what happens versus what
was expected, and `investigation.yml` asks a Question and carries an Expected
outcome block. Everything from Scope onward is common to all seven.

## Three vocabularies

Three type vocabularies coexist across the repositories this standard feeds.
Keeping them apart is the single most common source of confusion here.

| Vocabulary          | Members                                                                                                  | Where it applies                        |
| ------------------- | -------------------------------------------------------------------------------------------------------- | --------------------------------------- |
| Label family `type/*` | 5: `feature`, `bug`, `improvement`, `task`, `documentation`                                            | PR type-label gate in consuming repos   |
| Issue title types   | 7: `feat`, `fix`, `improvement`, `chore`, `test`, `docs`, `spike`                                         | this standard and the issue chooser     |
| Conventional Commit | 12                                                                                                        | PR titles and release tooling — **absent from this repository** |

The label family is the coarser of the two that matter here: 5 against 7. Two
type tokens have no `type/*` label of their own.

- `chore` has no label. `type/task` is its intended home.
- `spike` has no label, and no member of the family describes it.

`breaking-change` is a Conventional Commit type, not a label and not an issue
type. It does not belong in `ISSUE_STANDARD.md`, and there is deliberately no
`type/breaking-change`: consumers enforce "exactly one of five `type/*` labels"
on a pull request, so growing the family breaks a gate that is already deployed.

## Every template applies a label that exists

This was the one real inconsistency in the repository, and it is closed. It is
recorded here because the reasoning behind the three judgement calls is not
recoverable from the files.

**All seven templates now name labels that are members of `labels.yml`.**

| Template            | `labels:`             | Why                                                     |
| ------------------- | --------------------- | ------------------------------------------------------- |
| `feature.yml`       | `type/feature`        | exact match                                             |
| `improvement.yml`   | `type/improvement`    | exact match                                             |
| `bug.yml`           | `type/bug`            | exact match                                             |
| `docs.yml`          | `type/documentation`  | exact match                                             |
| `maintenance.yml`   | `type/task`           | no `chore` label exists; `type/task` is the catch-all    |
| `test.yml`          | `type/task`           | no `test` label exists — see below                      |
| `investigation.yml` | `type/task`           | no `spike` label exists — see below                     |

Every template also applies `status/needs-review`, which is what the triage
action would otherwise apply automatically on `issues` events. Declaring it
means the label is present from the moment the form is submitted, so an issue is
never briefly unlabelled.

The old values were `enhancement`, `bug`, `documentation`, `maintenance`,
`testing` and `investigation`. **None was a member of the manifest**, so GitHub
dropped every one of them without an error and an issue opened through any of
these forms arrived with no type label at all. `enhancement` was doubly wrong: it
was undeclared, and `feature.yml` and `improvement.yml` both applied it, so even
if it had existed it could not tell those two apart.

Three of the seven were judgement calls rather than mechanical:

- `chore` (`maintenance.yml`) → `type/task`. Unambiguous in substance:
  `type/task` was declared in the manifest and applied by no template at all,
  which is the strongest available signal that it was `chore`'s intended home.
- `test` (`test.yml`) → `type/task`. `scope/testing` exists but is a scope, and
  applying a scope as a type would be a category error. `type/task` is the
  defensible reading: a test-only change is a defined piece of work that is not
  itself a feature or a bug, which is the manifest's own description of
  `type/task`. The alternative is a sixth family member, which is a larger
  decision than this gap required.
- `spike` (`investigation.yml`) → `type/task`. The weakest of the three, and the
  one to revisit first if the family ever grows. A spike is exploratory work, and
  `type/task` is the only label whose description admits that. Nothing in the
  standard claims a spike is a task; this is the least-wrong available answer.

**Adding `type/chore`, `type/test` and `type/spike` would grow the family from 5
to 8.** That remains a real cost and a legitimate future decision, but note what
it is *not*: downstream does not enforce this family's size. Each consumer
declares its own `type-labels`, and after the alignment recorded below those
lists name `type/*` labels. Widening this repository's family would break
nothing — but it would be a cross-repository change regardless, because the
consumers' manifests are copies that nothing syncs automatically.

## Sync model

`labels.yml` opens with "Keep this file synchronized across projects."
Concretely: this repository is the origin, each consuming repository holds its
own copy under its own `.github/`, and **edits here do not propagate**. There
is no workflow, submodule, or sync bot in this repository. Synchronization is a
manual copy, which means drift is expected and has to be checked for by hand.

Two things drift apart here, and confusing them is how this section went wrong
before. The **remote label set** has converged. The **manifest files** do not
describe that remote at all.

Verified state of the two comparable consumers, as reconciled:

| | `alpinejs-toolkit` | `colander` |
| --- | --- | --- |
| Remote labels matching this manifest | 30 of 30, colors identical | 29 of 30, 2 colors differ |
| Extra label on the remote | — | `type:feature`, a leftover |
| Missing from the remote | — | `github_actions` |
| Its own `.github/labels.yml` now declares | the 30, its own schema | the 30, its own schema |
| `policy.yml` `type-labels` | the 5 `type/*` labels | the 5 `type/*` labels |
| `policy.yml` `title-types` | 12, declared separately | 10, declared separately |
| Policy job a required status check | **yes** | no — and see below |

Both consumer *manifest files* were a different, older scheme: bare names
(`feat`, `fix`) and a colon form (`status:approved`) instead of prefixed slash
names. Both carried a `gh label create --force` reconciliation recipe, and running
either today would have tried to create labels that do not exist on the remote.
Both have since been reconciled against their remotes in the same change that
fixed their `policy.yml`.

Each kept its own schema, header and reconciliation recipe rather than taking
this file's shape. A mechanical copy between the two is an upgrade in content and
a regression in form.

### The two vocabularies, and the input that separated them

`type-labels` used to feed three checks at once: the label check, the Conventional
Commit subject grammar, and pull request template resolution. That made it
impossible to configure, because the three want different sets.

The label set is coarse — five `type/*` labels, because that is what a
contributor picks from. The title set is the twelve Conventional Commit types,
because release tooling parses the squashed subject and the template directory
is named for them. One input cannot be both, and neither available value worked:

| Value of `type-labels` | Label check | Title grammar | Template resolution |
| ---------------------- | ----------- | ------------- | ------------------- |
| `feat,fix,…` (bare)    | **unsatisfiable** — no such labels on any remote | works | works |
| `type/feature,…`       | works | **rejects every `feat:`/`fix:` title** | **hard error** — `/` is a path character |

So the fix was not a choice of vocabulary. `ailuracollective/actions` now has a
second input, `title-types`, which feeds the grammar and the resolution, while
`type-labels` feeds the label check alone. `title-types` defaults to
`type-labels`, so a consumer that uses one vocabulary for both declares nothing
extra.

Two consequences in the scripts, both deliberate:

- **The template resolves from the pull request's title, not from its label.**
  This is what lets the two sets differ, and it makes `pr-body-structure`
  independent of `type-label`: each check owns its own failure, so a pull request
  missing both a label and a section is told about both instead of one hiding the
  other. When the title's type is not allowed, the check reports `skip` and
  names `pr-title-conventional` as the owner rather than inventing a second
  diagnosis for the same mistake.
- **The `type-label` error message no longer claims the labels are "all bare,
  with no `type:` prefix".** That was advice about the hub's own vocabulary
  printed as if it were a rule, and it was actively wrong for anyone who had
  moved to a prefixed family. The worked example is now read from the configured
  set.

Both consumers now declare both lists: `type-labels` names the five `type/*`
labels that exist on their remotes, `title-types` names the Conventional Commit
types. `approved-label` became `status/ready` and `auto-label-name` became
`status/needs-review`, replacing the colon forms `status:approved` and
`status:needs-review` that no remote in this organisation carries.

**This was a fix in `ailuracollective/actions`, and it could not have been made
in the consumers.** Editing a consumer's `type-labels` alone would have replaced
one broken check with two. **Nothing worked until the `v1` tag moved.** `v1`
points at a commit; consumers write `uses: ailuracollective/actions/pull-request@v1`,
which resolves the tag, not `main`. Moving that tag is a separate, deliberate
step from merging the pull request, and it changes every repository in the
organisation at once. Verify before assuming:

```sh
gh api /repos/ailuracollective/actions/git/refs/tags/v1 --jq '.object.sha'
gh api /repos/ailuracollective/actions/commits/main --jq .sha   # equal means the tag moved
```

### Enforcement, verified per repository

This is the part that changes most often, so it is recorded as a dated reading
rather than a standing claim. Read it against the API before relying on it.

| Repository | Default branch | Mechanism | Policy job required? |
| --- | --- | --- | --- |
| `ailuracollective/actions` | `main` | ruleset | **yes** — plus `Check suite`, `Static analysis`, `Branch name` |
| `ailuracollective/alpinejs-toolkit` | `master` | ruleset | **yes** — plus `Verify` |
| `ailuracollective/colander` | `master` | classic branch protection | no |
| `ailuracollective/standards` | `main` | classic branch protection | no — and it cannot become one yet |

**The hub enforces its own gate on itself.** `actions`' `Pull request policy` is a
required status check, so the split in this section was verified by a real merge,
not only by the offline harness.

**`alpinejs-toolkit` enforces it too.** Its ruleset requires `Verify` and
`Pull request policy`, which is why the misconfiguration in this section could
not have gone unnoticed for long — and why fixing it changed what blocks a merge
rather than only what an annotation says.

**`colander`'s required checks are all dead.** `master` requires two contexts that
no workflow in the repository produces:

| required context | what the job is actually called |
| --- | --- |
| `Branch name and PR title` | `Branch name` |
| `fmt-check, lint, check, test, build` | `ci` — and that is **one** context name containing commas, not five |

So `colander`'s `master` is unmergeable by anyone without admin rights, and
`enforce_admins: false` is the only reason pull requests there merge at all. The
policy job is not required, so its gates annotate and are ignored. Correcting the
two context names is a branch-protection change, not a policy change, and is a
decision rather than a fix.

**`standards` cannot require the policy job without freezing itself.** `main`
requires a code-owner review and `@SiddharthaGF` is the only account with write
access, so a policy job that must pass before merge would deadlock the
repository. § Ownership and enforcement covers this in full.

In every repository, **the twelve pull request templates in *this* repository are
what the body-structure check reads in the *consuming* repository.** A consumer
that has not copied them has no template to compare against, and the check skips.
So the headings those files declare are requirements only in the repositories
that carry them.

Structural divergences worth knowing before you copy anything either direction:

- **Label form.** This repository uses a block sequence under a bare top level;
  the consumers nest under `labels:`. Both parse as YAML; they are not the same
  schema, so a mechanical copy between them changes the document shape.
- **Manifest content.** Copying this repository's `labels.yml` over a consumer's
  current file would be an upgrade in content and a regression in form: it names
  the labels the remote actually has, but drops the header and the reconciliation
  recipe. Port the recipe back here instead, and reconcile the consumer's file
  against its remote in the same change.
- **Field id casing.** This repository uses kebab-case (`out-of-scope`,
  `acceptance-criteria`); `alpinejs-toolkit` uses snake_case
  (`proposed_outcome`, `additional_context`).
- **Field types.** This repository uses only `textarea` and one `markdown`.
  `alpinejs-toolkit` also uses `checkboxes` with per-option `required: true` for a
  preflight block, `render: shell` for a log field, `type: input` for a version
  string, and explicit `validations: required: false` on optional fields.
- **`blank_issues_enabled`.** `false` here, `true` in `alpinejs-toolkit`. Treat
  this as a per-repository policy choice, not drift.
- **Default pull request form location.** `alpinejs-toolkit` and
  `ailuracollective/actions` keep theirs at `.github/PULL_REQUEST_TEMPLATE.md`,
  beside the directory; `colander` has none at all; this repository keeps it
  inside the directory. Copying only the directory silently omits the fallback.

## Conventions when editing

YAML style as observed across all ten files:

- 2-space indent. No tabs, no CRLF anywhere in the repository.
- Hex colors are quoted six-digit strings with no `#`: `"D73A4A"`. That is the
  form `gh label create --color` expects and the form GitHub returns.
- Every label entry has exactly three keys — `name`, `color`, `description` —
  in that order. Descriptions are quoted and end with a period.
- One blank line between label entries. Families appear in the order `type`,
  `priority`, `status`, `scope`, `meta`, `github_actions`, `release`, which is
  neither alphabetical nor the order the manifest header lists them in. Within
  `type`, the order is bug, feature, improvement, task, documentation — also not
  alphabetical. Match the file, do not re-sort it.
- Three files have no trailing newline: `labels.yml`, `CODEOWNERS`, and this
  `AGENTS.md`. Do not fix that incidentally in an unrelated change, and do not
  propagate it into a consumer. Everything else, `LICENSE` included, ends with one.

Issue templates:

- Every template declares `name`, `description`, `title`, `labels`, `body`, in
  that order.
- `title` is the bare prefix with a trailing space and no description:
  `title: "feat: "`.
- Body field order is Context → Objective → Scope → Constraints → Scenarios →
  Out of scope → Acceptance criteria → Dependencies → Notes, minus the fields a
  type does not need, and with the two opening-pair exceptions noted above.
- Field `id`s are kebab-case and unique within a file. They become URL fragments,
  so renaming one breaks any bookmarked or prefilled link.
- A required field carries `validations: required: true`. Optional fields carry
  only `label`, plus `description` when the label is not self-explanatory.
- `description` tells the reporter what to write, `placeholder` shows one worked
  example, `value` pre-fills content. **Six** of the seven templates pre-fill
  acceptance criteria as a `- [ ]` checklist through `value`;
  `improvement.yml` is the sole exception, carrying only a `description`,
  because "complete" means something different for an improvement than for a
  feature or a fix. Use `value` for a checklist that is genuinely always true of
  the type, and leave it empty where completion is type-specific.
- Only **26 of 55** fields carry a `description`, so a bare `label` is the norm,
  not the exception. Two rules hold across all seven templates: the **opening
  pair is always described** (Context and Objective, or What happens and
  Expected, or Context and Question), and `dependencies` and `notes` are bare in
  **six of seven** — described only in `feature.yml`. Everything between is a
  matter of whether the label speaks for itself, and the split is not even:
  `scope`, `out-of-scope`, and `acceptance-criteria` are each described in
  exactly two templates. `feature.yml` is the only template that describes all
  seven of its fields, and is the best model for a new one; the six others are
  closer to the minimum.
- Only `feature.yml` uses a `type: markdown` block, to tell the reporter when to
  pick that form. Reach for markdown only for guidance that must be read before
  a field is filled, never to restate a field's own description.

## Pull request templates

`.github/PULL_REQUEST_TEMPLATE/` holds **12 templates plus a default**, one per
Conventional Commit type: `breaking-change`, `build`, `chore`, `ci`, `docs`,
`feat`, `fix`, `perf`, `refactor`, `revert`, `style`, `test`. That is the eleven
types `policy.yml` accepts as a branch segment, plus `breaking-change`.

This directory matters more than it looks. The `enable-body-structure` gate in
`ailuracollective/actions/pull-request@v1` requires that **every `## ` heading in
the template matching the pull request's title type appears in its body**, and it
resolves that template from the *consuming* repository. A repository that ships
no template for a type falls back to `PULL_REQUEST_TEMPLATE.md`, so the twelve
here are what makes that gate mean the same thing everywhere.

### Structure is universal; commands are not

Every template splits into two kinds of content, and the split is the whole
design:

- **Structure** — which headings a type must have. Universal. Lives here.
- **Commands** — the checks CI actually runs. Per repository. Does not.

The `## Test plan` block is therefore a `TODO` placeholder, never a real command.
A TypeScript repository and a Rust repository cannot share a test plan:
`vp check` / `pnpm run size` and `cargo clippy` / `cargo test` have nothing to do
with each other. **Each consuming repository replaces that block**, in the same
pull request that changes its CI. Do not "helpfully" fill it in here.

### Four headings are common to all thirteen

`## Linked issue (required)`, `## Type (required)`, `## Test plan`, and
`## Contributor checklist` appear in every file. Three of the four are
**byte-identical** across all thirteen. `## Type (required)` differs in exactly two
lines — the `- [ ] \`type\`` checkbox and the label note beneath it — which is the
point of the heading; the guidance above them is identical.

If you change the guidance in one, change it in all thirteen. A divergence here is
a divergence in what the gate demands per repository, which is precisely the
failure this directory exists to prevent.

### The label a template asks for

Each template names the single `type/*` label to apply, because the two
vocabularies differ and contributors conflate them. Nine of the twelve types map
to `type/task`, the catch-all. **`breaking-change` has no label of its own**: the
family has exactly five members and none marks a break, so the template says to
apply the label of the underlying change instead.

That mapping follows `labels.yml`, which is what both remotes actually carry. It
does **not** follow what the gate checks: every consumer fills `type-labels` with
bare names, and the check compares by exact name, so a pull request labelled
`type/feature` would be reported as carrying no type label at all. Only one of
the two can be right, and the manifest wins because it is what exists on the
remotes — which makes `type-labels` the misconfigured half. Correcting it is a
cross-repository change to each consumer's `policy.yml`, and it is the same change
that has to happen before any of these templates can be enforced.

### Merges against the existing consumers

`alpinejs-toolkit` (7 templates) and `colander` (10) both ran this gate with
templates that shared no headings beyond the first two. Reconciling them was a
design decision, recorded here because the alternatives are recoverable:

| Decision | Chosen | Over |
| --- | --- | --- |
| Test-plan heading | `## Test plan` | `## Checks run` (colander) |
| Fix regression section | `## Regression test` | `## Regression coverage` + `## How to verify the fix` |
| Refactor equivalence | `## Behavioral equivalence` | `## Proof that behavior is unchanged` |
| Perf measurement | `## Measurements (required)` | `## Measurements` |

Near-duplicate headings were merged rather than carried as two required sections;
colander's `## How to verify the fix` survives as guidance inside
`## Regression test`. Sections unique to one repo were adopted where they
generalise — colander's `## Behavior is unchanged` on `perf.md`,
`## Existing coverage that moved` on `test.md`, `## Packaging and version
changes` on `build.md`, `## Why the previous text was wrong` on `docs.md`. Repo-
specific headings such as colander's `## Frozen vectors` were left out: they
describe one repository's test strategy, not the type.

## Adding an issue type

1. Add the type to `## Issue Types` in `.github/ISSUE_STANDARD.md` and give it
   an example line under `## Title Convention`.
2. Add `<type>.yml` in `.github/ISSUE_TEMPLATE/` with `title: "<type>: "`. The
   filename does not have to be the type token — `bug.yml` proves it — but it
   should be a name a human would guess.
3. Give it Context, Objective, Scope, Out of scope, Acceptance criteria,
   Dependencies, Notes, plus any field the type genuinely needs and can justify.
4. Decide its label before writing the file. If it has no home in `type/*`, say
   so rather than inventing an undeclared label — see the known gap above.
5. Update the counts in this file.

## Ownership and enforcement

`.github/CODEOWNERS` gives every path to `@SiddharthaGF`, the only collaborator
with write access. Because all seven rules resolve to that same account, the
grouping currently changes no outcome — but it is not decoration. GitHub
applies the **last** matching pattern, so each group is a real rule that
overrides the catch-all above it, and the file is written as though a second
owner already existed: adding one is a one-line change per group rather than a
redesign.

**CODEOWNERS is advisory on its own.** It requests a review; it does not block
anything. It only binds when the branch is protected, so `main` carries:

| Setting | Value | Why |
| --- | --- | --- |
| `required_pull_request_reviews.require_code_owner_reviews` | true | this is what makes CODEOWNERS binding |
| `required_pull_request_reviews.required_approving_review_count` | 1 | one human read |
| `required_pull_request_reviews.dismiss_stale_reviews` | true | a new push invalidates the approval it was based on |
| `required_pull_request_reviews.require_last_push_approval` | true | nobody may push on top of someone else's approval |
| `required_conversation_resolution` | true | unresolved threads do not merge |
| `enforce_admins` | **false** | see below |
| `allow_force_pushes` | false | this repository is the record; rewriting it loses the trail |
| `allow_deletions` | false | as above |

**Read `enforce_admins` as the setting that governs the other seven.**
GitHub's default is that branch protection restrictions *do not apply* to people
with admin permissions, so `enforce_admins: false` does not merely waive review
— it is the single reason @SiddharthaGF can ignore every row above it, including
the two that read as guarantees. `allow_force_pushes: false` protects the
history of `main` against everyone except its one admin. The `Why` column states
intent; only `enforce_admins` states what is enforced.

Two of those field names are easy to get wrong, and both fail silently rather than
loudly. The API spells it `require_code_owner_reviews`, **plural**; sending the
singular form returns HTTP 200 and quietly leaves the flag `false`. And the `PUT`
rejects a body that omits `required_status_checks` and `restrictions` — send them
explicitly as `null` — so a partial payload never applies anything at all. Always
read the settings back rather than trusting the 200:

```sh
gh api /repos/ailuracollective/standards/branches/main/protection \
  --jq '.required_pull_request_reviews.require_code_owner_reviews'   # must be true
```

`enforce_admins` is deliberately off, and the reason is a deadlock rather than a
preference. @SiddharthaGF is both the only code owner and the only account with
write access. GitHub does not let an author approve their own pull request, so
enforcing admin review would mean **no pull request could ever be merged** — the
repository would be frozen after its first commit. As configured, every other
contributor needs @SiddharthaGF's code-owner review, while @SiddharthaGF keeps a
direct-push escape hatch, which is verified to work both as a plain `git push` and
as `gh pr merge --admin`.

**The enforcement is not fully verified, and cannot be while one person holds all
the access.** A test pull request reports `REVIEW_REQUIRED` and `BLOCKED`, which is
what a binding code-owner rule looks like — but it looks identical to a plain
one-approval rule, because the only account that could supply a second approval is
the author. Distinguishing the two requires granting write access to a second
person. Until then, treat the code-owner rule as configured rather than proven.

That is a bootstrap state, not a finished one. Turning it into a real guarantee
takes one thing: **grant write access to a second person**, then flip
`enforce_admins` to true. Do that before treating this repository as reviewed.

Two rules that must hold while there is a single owner. CODEOWNERS owns itself,
so a pull request cannot delete the rule demanding the review it needs. And
nobody with write access may push straight to `main` — open a pull request even
though you could bypass the review, because the review is the point.

## Adding a pull request type

1. Add `<type>.md` to `.github/PULL_REQUEST_TEMPLATE/`, named for the Conventional
   Commit type exactly — the filename is the key the gate resolves against.
2. Copy the four common headings from an existing template **verbatim**, except
   the `- [ ] \`type\`` checkbox and the label note inside `## Type (required)`,
   which are per-type by design.
3. Name the one `type/*` label to apply. `type/task` is the catch-all; if the type
   genuinely maps to none of the five, say so in the file rather than inventing a
   sixth.
4. Keep the `## Test plan` block as `TODO` placeholders.
5. If the type is also a valid branch segment, mirror it into the `branch-types`
   input of every consuming `policy.yml`.

## Adding or changing a label

1. Edit `.github/labels.yml`. Keep the three-key shape and the family grouping.
2. If the name is a `type/*` label, mirror it into every consuming repository's
   manifest **and** into the `type-labels` input of that repository's
   `policy.yml`. A gate that names a label the remote does not have is
   unsatisfiable, not merely strict.
3. Reuse an existing family color where the meaning matches — `type/feature` and
   `type/documentation` already share `0075CA`.
4. Removing an entry does not remove the remote label, and a remote label absent
   from this manifest is drift in the other direction. The reconciliation recipe
   to re-apply or prune lives at the bottom of `alpinejs-toolkit/.github/labels.yml`;
   port it here if this repository should be self-sufficient.

## Validation

There is no test suite, so check by hand before proposing a change:

```sh
# every file must parse as YAML
python3 -c "import yaml,glob;[yaml.safe_load(open(f)) for f in glob.glob('.github/**/*.yml',recursive=True)]"

# label names unique, colors well-formed, count as documented
python3 - <<'PY'
import re
txt = open('.github/labels.yml').read()
names = re.findall(r'- name: "([^"]+)"', txt)
assert len(names) == len(set(names)), 'duplicate label name'
assert len(names) == 30, f'expected 30 labels, found {len(names)}'
assert all(re.fullmatch(r'[0-9A-Fa-f]{6}', c) for c in re.findall(r'color: "([0-9A-Fa-f]{6})"', txt))
print(len(names), 'labels ok')
PY

# every label NAMED IN A FIELD resolves against the manifest. This is the check that
# caught the original defect: seven templates applying six undeclared names, which
# GitHub discards without an error. It reads fields, not prose -- scanning the raw
# text reports `type/breaking-change`, which appears here only in a comment saying
# there deliberately is no such label.
python3 - <<'PY'
import re, glob, sys, yaml
have = {e['name'] for e in yaml.safe_load(open('.github/labels.yml'))}
bad = []
for f in sorted(glob.glob('.github/**/*.yml', recursive=True)):
    doc = yaml.safe_load(open(f))
    if not isinstance(doc, dict):
        continue
    # issue templates: the `labels:` list a chooser form applies on submit
    for l in (doc.get('labels') or []):
        if l not in have:
            bad.append(f'{f}: labels: {l}')
    # workflows: the gate inputs that name one or more labels
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

# the workflow declares two vocabularies, and they are disjoint sets
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

# one template per type, prefixes matching the standard
sed -n '/^## Issue Types/,/^## Title/p' .github/ISSUE_STANDARD.md | grep -c '^- `'
ls .github/ISSUE_TEMPLATE/*.yml | grep -vc config       # 7 templates
grep -h '^title: ' .github/ISSUE_TEMPLATE/*.yml | sort   # 7 prefixes

# one pull request template per type, common headings intact
find .github/PULL_REQUEST_TEMPLATE -name '*.md' ! -name 'PULL_REQUEST_TEMPLATE.md' | wc -l  # 12
find .github/PULL_REQUEST_TEMPLATE -name '*.md' | wc -l                                   # 13
for h in 'Linked issue (required)' 'Type (required)' 'Test plan' 'Contributor checklist'; do
  printf '%-24s %s/13\n' "$h" "$(grep -lF "## $h" .github/PULL_REQUEST_TEMPLATE/*.md | wc -l)"
done
grep -rn 'vp check\|pnpm run\|cargo ' .github/PULL_REQUEST_TEMPLATE/ \
  | grep -v 'cannot run' || echo 'no hardcoded CI commands'

# CODEOWNERS parses and every owner exists. An empty errors array is the whole
# check: GitHub skips any line it cannot parse, silently, and an owner without
# explicit write access is dropped without a warning either.
gh api repos/ailuracollective/standards/codeowners/errors --jq '.errors'   # expect []
gh api repos/ailuracollective/standards/collaborators \
  --jq '.[] | select(.permissions.push) | .login'                          # owners must appear
```

Count the typed templates with `find … ! -name 'PULL_REQUEST_TEMPLATE.md'`, not
`grep -v PULL_REQUEST_TEMPLATE`: every path contains the *directory's* name, so
that filter matches all thirteen and returns zero.

The last check is the one that matters most: a repository-specific command in
these files makes the gate demand a check that repository cannot run.

The first and third checks need `pyyaml`, which is not vendored. Both glob
`*.yml`, so neither ever touches `ISSUE_STANDARD.md` — there is nothing to parse
there. The label-reference check reads fields rather than raw text on purpose:
grepping the files for label-shaped tokens reports `type/breaking-change`, which
appears only in a comment recording that there deliberately is no such label.

The type count is a **text** check against a prose file, which is a weaker
guarantee than the others: nothing checks that the list is well-formed, only
that it has seven lines shaped a particular way. Scope it to the `## Issue
Types` section with `sed` first. A bare `grep -c '^- \`'` over the whole file
returns **14**, because the seven example titles under `## Title Convention` are
formatted the same way. The distinguishing feature is that a declaration puts the
colon *outside* the backticks (`` `feat`: ``) while an example puts it *inside*
(`` `feat: ...` ``).

Functional verification is manual. Open the issue chooser on a test repository
that has copied these files and confirm each of the seven forms renders, that
`blank_issues_enabled: false` hides the blank option, and that the applied labels
are the ones you expect — remembering that a label the repository lacks is
dropped without an error, so "no label appeared" is the expected symptom of the
gap above rather than a bug in your change.

## Do not

- Do not fill in the `## Test plan` commands here. They are per repository by
  necessity, and a hardcoded `cargo test` in a TypeScript repository is worse
  than a `TODO`.
- Do not let the guidance in one of the four common headings drift. It is
  identical across all thirteen files on purpose; only the checkbox and label
  note inside `## Type (required)` are per-type.
- Do not add a template without adding its type to `ISSUE_STANDARD.md`. The
  standard and the chooser must not disagree about what kinds of issue exist.
- Do not convert `ISSUE_STANDARD.md` back to YAML or point a parser at it. It is
  prose on purpose; as `.yml` it did not parse at all.
- Do not rename a template file without checking that nothing references it.
  Filenames are what GitHub keys on for chooser ordering, and they are not
  required to match the type token.
- Do not change or remove a body field `id` in a template. It breaks existing
  links and prefilled drafts.
- Do not introduce a second title vocabulary. `breaking-change` belongs to
  Conventional Commits and pull request titles; it is not an issue type here.
- Do not treat `labels.yml` as configuration that applies itself. Editing it
  changes no remote and gates no CI.
- Do not grow the `type/*` family in this repository alone. It is not enforced
  downstream at five members or any other number — see the sync model section for
  what the consumers actually declare and why the two vocabularies disagree.
- Do not write "the gate requires" about **this** repository. Its policy job is
  not a required status check and cannot become one while one person holds all
  the write access. The gate is enforced in `actions` and `alpinejs-toolkit`, and
  advisory in `colander` — check which before describing a rule as binding.
- Do not overwrite a consuming repository's `labels.yml` with this bare list
  without porting its header and reconciliation recipe back here first.
- Do not drop the catch-all from `CODEOWNERS`. A pattern with no slash matches at
  every depth, so `*` alone owns every file in the repository, present and future.
  The groups below it document blast radius rather than close a coverage gap, and
  the catch-all is currently the only thing owning the four files in the
  repository root. An unowned file skips the code-owner gate entirely.
- Do not add a second owner to a CODEOWNERS rule expecting it to be reviewed by
  someone it does not already name. Rules are not cumulative: the **last** matching
  pattern replaces the owners of the ones before it, so
  `.github/labels.yml @alice` drops @SiddharthaGF from that path rather than adding
  her alongside him.