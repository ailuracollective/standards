# AGENTS.md

Guidance for AI agents and contributors working in this repository.

## What this repository is

The source of truth for GitHub issue standards shared across an organisation's
repositories. There is no application code here, no build and no test suite.
`README.md` is the entry point for a human; this file is the working reference.
Under `.github/` there are **11 YAML files, 14 Markdown files, and 1 CODEOWNERS
file**; four more files sit in the repository root.

Seven artifacts, each with exactly one owner:

| File                                                   | Owns                                     | Read by                                     |
| ------------------------------------------------------ | ---------------------------------------- | ------------------------------------------- |
| `.github/ISSUE_STANDARD.md`                            | how an issue is written                  | humans and agents drafting issues           |
| `.github/labels.yml`                                   | the label set (30 labels)                | anything that reads or applies labels       |
| `.github/ISSUE_TEMPLATE/*.yml` (7 templates + config)  | the forms in the issue chooser           | GitHub                                      |
| `.github/PULL_REQUEST_TEMPLATE/*.md` (12 + default)    | the form per pull request type           | GitHub                                      |
| `.github/CODEOWNERS`                                   | who reviews a change                     | GitHub, via branch protection               |
| `.github/workflows/policy.yml`                         | the projection of all of the above      | GitHub Actions, on every pull request       |
| `.github/standards.local.example.yml`                  | the shape of a customization record      | a reader — or a checker, once one exists    |

The last one is opt-in and is the only artifact nobody is required to copy; see
§ Customizing the standard for what it is and, more importantly, what it is not.

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

### What is named here, and what is not

This file names `ailuracollective/actions`, because the gate is implemented
there and every input it discusses — `type-labels`, `title-types`,
`approved-label`, `auto-label-name`, `enable-body-structure`, `default-template`,
and the `v1` tag workflows resolve — belongs to that action rather than to this
standard. Stripping the name would leave the configuration unwriteable.

It names **no adopting repository**, on purpose. § Sync model explains why, and
§ Enforcement carries the method for checking any one of them instead.

Where this file says "here", it means this repository: the origin manifest, these
seven issue templates, these twelve pull request templates, these conventions.
Where it says "an adopting repository", it means any repository that copied them,
of which there may be none, one, or many.

## Inventory

- **7** issue types, declared once in `ISSUE_STANDARD.md` § Issue Types.
- **7** templates — one per type — plus `config.yml`, which is not a template.
- **12** pull request templates — one per Conventional Commit type — plus a
  default `PULL_REQUEST_TEMPLATE.md`.
- **30** labels: six prefixed families (`type` 5, `priority` 4, `status` 5,
  `scope` 8, `meta` 5, `release` 2) plus one unprefixed, `github_actions`.
- **30** files total: 4 in `.github/` (`labels.yml`, `ISSUE_STANDARD.md`,
  `standards.local.example.yml`, `CODEOWNERS`), 1 in `.github/workflows/`, 8 in `ISSUE_TEMPLATE/`, 13 in
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
`type/breaking-change`: adopting repositories enforce "exactly one of five
`type/*` labels"
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
it is *not*: no repository enforces this family's size. Each adopting
repository declares its own `type-labels`, and that list names `type/*` labels
because those are the names its remote has. Widening this repository's family
would break nothing — but it would be a change to every adopting repository
regardless, because their manifests are copies that nothing syncs
automatically.

## Sync model

`labels.yml` opens with "Keep this file synchronized across projects."
Concretely: this repository is the origin, each adopting repository holds its
own copy under its own `.github/`, and **edits here do not propagate**. There
is no workflow, submodule, or sync bot in this repository. Synchronization is
a manual copy, which means drift is expected and has to be checked for by hand.

**This file deliberately does not record who has adopted it.** A list of adopting
repositories, their label counts and their gate configuration is the kind of fact
that is true when written and wrong a week later, and a stale list is worse than
none because it reads as authoritative. Someone checking a specific repository
reads that repository. What belongs here is the rule and the command.

Three layers drift apart independently, and conflating them is how a
reconciliation goes wrong:

| Layer | What it is | How it goes stale |
| --- | --- | --- |
| The remote label set | what GitHub actually has | a label renamed or deleted by hand |
| The manifest file | a reviewed record of the intended set | edited here, never copied out |
| The gate's `type-labels` | what the check compares against | a rename, or a scheme replaced wholesale |

All three must agree for a gate to be satisfiable, and they fail differently. The
first two drift silently. The third turns any disagreement into a gate no pull
request can pass, which reads as though the contributor did something wrong.
Reconcile all three in the same change, against the remote rather than against
another copy of the manifest.

Two traps in the copy itself:

- **Copying a manifest over another manifest is an upgrade in content and a
  regression in form.** This repository's `labels.yml` is a block sequence under a
  bare top level; an adopting repository may nest under `labels:`. Both parse as
  YAML, so a mechanical copy changes the document shape without failing anywhere.
  Port the target's header and reconciliation recipe across instead of
  overwriting it.
- **Quote every color.** An unquoted six-digit hex string is not always a string:
  `5319E7` parses as the integer `53190000000`, `008672` as `8672`, and `000000`
  as `0`. It fails silently, and the recipe that reads the file then hands
  `gh label create` a number rather than a hex value.

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
`type-labels`, so a repository that uses one vocabulary for both declares nothing
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

An adopting repository must declare both lists: `type-labels` names the five
`type/*` labels, `title-types` names the Conventional Commit types. And because
the status family is slash-named everywhere, `approved-label` is `status/ready`
and `auto-label-name` is `status/needs-review` — never the colon forms
`status:approved` and `status:needs-review`, which no remote carries and which a
gate demanding them can never see satisfied.

**This was a fix in the gate's own repository, and it could not have been made
in an adopting repository.** Editing `type-labels` alone would have replaced one
broken check with two. **Nothing worked until a tag moved.** A tag points at a
commit; a workflow writes `uses: ailuracollective/actions/pull-request@v2`,
which resolves the tag, not `main`. Moving it is a separate, deliberate step
from merging the pull request, and it changes every repository that resolves
that tag at once. Verify before assuming:

```sh
# which commit does the tag a workflow writes actually resolve to?
gh api /repos/ailuracollective/actions/git/refs/tags/v2 --jq '.object.sha'
gh api /repos/ailuracollective/actions/commits/main --jq .sha   # equal means the tag is current
```

**Two majors exist, and picking one is a decision rather than a search.** `v2`
adds the sticky status comment, which publishes into the pull request
conversation and therefore needs a token that can write there. Note *which*
token: `comment-token` is separate from `github-token` and carries its own
scope, so a job can publish a comment while its own grant stays read-only —
or, in the branch-name job here, stays empty. Widening `permissions` to
`pull-requests: write` is the third way to make it work and the worst one:
it hands a write grant on the pull request to the five check scripts, which
only ever read. Three outcomes:

| Choice | Cost |
| --- | --- |
| `enable-status-comment: false` | nothing; the job summary carries the same table |
| `comment-token` for an organisation account | a secret, but the comment can be edited by a person, and the job's grant stays read-only |
| `comment-author` naming the identity your token actually has | no secret, but a `github-actions[bot]` comment can be edited or deleted by nobody |

The third is the tempting one and it is a trap worth naming: it works, the
comment appears, and the reason the action refuses to post under an unheld
identity by default is precisely that a bot comment outlives whoever would have
fixed a wrong one. Prefer the second. The first is the honest answer for a
repository with no opinion.

**A comment is authored by the token that wrote it, so the identity is chosen
by which token is passed, not by a field.** `comment-author` only says which
identity the comment is *required* to have, and the action checks it against
`gh api user` before writing anything. Setting it to match whatever token you
already have is not configuring an author; it is agreeing to publish under that
account. The default exists so the two cannot drift apart unnoticed.

### Enforcement: how to tell, for any repository

A gate being **configured** and a gate being **enforced** are different questions,
and the second one is per-repository, per-branch, and changes without anyone
editing a file. So this section carries the method rather than a result. A result
recorded here would be true when written and wrong later, in a document whose whole
purpose is to be relied on.

Both mechanisms exist and they do not answer the same request:

```sh
# classic branch protection — 404 means no protection, NOT "unprotected"
gh api /repos/OWNER/REPO/branches/BRANCH/protection --jq '.required_status_checks'

# rulesets — a separate API, and this is the one people forget
gh api /repos/OWNER/REPO/rulesets --jq '.[] | "\(.id) \(.name) \(.enforcement)"'
for id in $(gh api /repos/OWNER/REPO/rulesets --jq '.[].id'); do
  gh api /repos/OWNER/REPO/rulesets/$id --jq \
    '.rules[] | select(.type=="required_status_checks") | .parameters.required_status_checks[].context'
done
```

**The trap is reading a 404 from the first as "this branch is unprotected" when it
has moved to a ruleset.** That mistake has already been made once here, and it
produced a confident, wrong claim that the gates enforced nothing anywhere. Check
both APIs before concluding anything about enforcement.

Then read the required contexts against what the workflows actually report:

```sh
gh pr view N --repo OWNER/REPO --json statusCheckRollup \
  --jq '.statusCheckRollup[].name' | sort -u
```

Three failure shapes to recognise, all of which look like a contributor's mistake
and none of which are:

| What the required context says | What it means |
| --- | --- |
| the policy job is **not** among them | it annotates and is ignored; a fix to it changes nothing about what merges |
| it is there, under a **different name** | the branch is unmergeable for anyone who cannot bypass protection |
| a required context **no workflow reports** | the same, and it is invisible until someone without admin rights tries |

The second and third rows are the same defect wearing two hats: a required context
is a literal string, so `Branch name and PR title` and a job actually named
`Branch name` do not match, and neither does a required context that is one name
containing commas where five were meant. Bypass permission is what keeps such a
repository mergeable, and it hides the problem until bypass is removed.

Do not describe a rule as binding without having read one of these for that
repository and that branch. The same organisation will have one repository where
the gate blocks and another where it does not.

Structural divergences worth knowing before you copy anything either direction:

- **Label form.** This repository uses a block sequence under a bare top level;
  another repository may nest under `labels:`. Both parse as YAML; they are not
  the same schema, so a mechanical copy between them changes the document shape.
- **Manifest content.** Copying this repository's `labels.yml` over a repository's
  current file would be an upgrade in content and a regression in form: it names
  the labels the remote actually has, but drops the header and the reconciliation
  recipe. Port the recipe across instead, and reconcile the target's file against
  its remote in the same change.
- **Field id casing.** This repository uses kebab-case (`out-of-scope`,
  `acceptance-criteria`). An adopting repository may use snake_case
  (`proposed_outcome`). Either parses; only the id string differs, and it becomes
  a URL fragment.
- **Field types.** This repository uses only `textarea` and one `markdown`. Others
  are available and legitimate — `checkboxes` with per-option `required: true` for
  a preflight block, `render: shell` for a log field, `type: input` for a version
  string, and explicit `validations: required: false` on optional fields. The set is
  a style choice, not a rule.
- **`blank_issues_enabled`.** `false` here. Treat it as a per-repository policy
  choice, not drift.
- **Default pull request form location.** Two conventions are in use: inside the
  directory, as here, or beside it at `.github/PULL_REQUEST_TEMPLATE.md`. A
  repository may also have none, in which case every type falls back to whatever
  the gate is told. Copying only the directory omits the fallback silently, and the
  action's own default is the beside-the-directory path — so a repository using the
  inside-the-directory layout must say so with `default-template`.

## Customizing the standard

The structural divergences above are an observation taxonomy: they name what two
copies may disagree about. They are not a policy, and nothing records which
divergences an adopting repository actually has. So the question "is this difference
intentional, or did the copy rot?" has no answer today, and four situations that need
different responses are indistinguishable in the result:

| What a repository did | What it must also remember | What goes wrong |
| --- | --- | --- |
| added `area/auth` | nothing | looks like drift forever |
| added `type/chore` | edit `type-labels` in its `policy.yml` | the second record is in no file anyone reads |
| recolored a core label | the reason | invisible, and reverted by the next copy |
| dropped `scope/security` | whether that was a decision | cannot be told from an incomplete copy |

The answer is an **opt-in delta file**, `.github/standards.local.yml`, whose schema
ships as `.github/standards.local.example.yml`. It records what the repository
changed and why. It is not a sixth artifact anyone is required to copy.

**It declares; it does not configure.** No workflow reads it, including the gate. The
gate reads the repository's own `policy.yml`, because a workflow cannot read a file —
the reason every input in `policy.yml` is duplicated rather than loaded. Writing a
value here changes nothing at all. That sentence has to survive every future edit of
this section, because the failure it prevents is silent: a repository that assumes
the file configures the gate sees no error and no effect.

Deviations are costed in four levels, and the level decides the process, not the data
shape:

| Level | Deviation | Process |
| --- | --- | --- |
| 0 | none — an exact copy | nothing to declare |
| 1 | a label in a family the core does not use | no approval |
| 2 | a core label's `color`/`description`, or a gate input's value | declare it with a reason |
| 3 | dropping a core label, changing an input's set, changing the manifest's shape | issue here first; `issue:` records which one |

Level 1 needs no approval **because level 2 does not need approval either, and a
tiered policy with an approval step at the bottom is a policy nobody follows.** What
is reserved is the list of core families — `type/`, `priority/`, `status/`, `scope/`,
`meta/`, `github_actions`, `release/` — not a closed set of new ones. An open
extension set costs little: two repositories inventing `area/ownership`
independently is a smaller problem than one repository inventing `type/chore` and
having to edit a second record in a second file to make it pass.

`type/` is frozen at five members. It is the family the gate reads, and a sixth
member is a change to every adopting repository's `policy.yml` and manifest — all
copies that nothing synchronizes. A need for a sixth type is a `type/*` label plus an
entry in `extensions`.

`reason` is **required** wherever a deviation is recorded. That is the whole
mechanism: an override with a reason is a decision someone can review and a verifier
can recognise, and an override without one is precisely the thing the file exists to
distinguish from rot.

### What a checker must be able to answer

The schema is a public interface. The consistency checker belongs to another project,
and it is the only thing that can turn this file from a note into a guarantee. Four
questions it has to answer, and one it must not invent:

- Does every label named in a field resolve against the manifest? (Already a manual
  check here; the defect it caught was seven templates applying six undeclared
  names.)
- Is a difference from the core declared in this file?
- Is a label on the remote missing from the manifest, or in the manifest missing from
  the remote?
- Does a level-3 deviation carry the issue that approved it?
- **Absence of the file means "no deviations" by assumption, not by declaration.** It
  must not report a missing file as a defect, and it must not report the absence of a
  field it did not expect as one either.

The last one is the failure mode of this whole design. Opt-in means the common case is
an absent file; a checker that treats absence as an error trains every repository to
create an empty one, and an empty file is indistinguishable from a customized one to
anyone skimming.

## Conventions when editing

YAML style as observed across all eleven files:

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
  propagate it into another repository. Everything else, `LICENSE` included, ends
  with one.

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
`pull-request@v2` requires that **every `## ` heading in the template matching the
pull request's title type appears in its body**, and it resolves that template from
the repository under review, not from here. A repository that ships no template for
a type falls back to whatever `default-template` names, so the twelve here are what
makes that gate mean the same thing everywhere — and a repository that has not
copied them has no headings to be checked against at all.

### Structure is universal; commands are not

Every template splits into two kinds of content, and the split is the whole
design:

- **Structure** — which headings a type must have. Universal. Lives here.
- **Commands** — the checks CI actually runs. Per repository. Does not.

The `## Test plan` block is therefore a `TODO` placeholder, never a real command.
A TypeScript repository and a Rust repository cannot share a test plan:
`vp check` / `pnpm run size` and `cargo clippy` / `cargo test` have nothing to do
with each other. **Each adopting repository replaces that block**, in the same
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

That mapping follows `labels.yml`, and it is the manifest that wins, because the
manifest is a record of what the remote has while `type-labels` is only what some
workflow claims to check. When they disagree, the gate is the misconfigured half:
the check compares by exact name, so a pull request labelled `type/feature`
against a `type-labels` of bare names is reported as carrying no type label at all,
correctly labelled ones included. There is no failure mode in which the
contributor was wrong.

### Reconciling a divergent template set

An adopting repository may arrive with its own templates whose headings share
nothing beyond the first two. Reconciling them is a design decision, and the rule
that settles almost all of it:

- **Merge near-duplicates; do not carry both.** Two headings that ask the same
  question are one heading. A second required section restating the first is a
  form contributors fill in twice and reviewers read once. Where a second heading
  carries real content, demote it to guidance *inside* the merged one — that is
  where "how to verify" belongs once "regression test" exists.
- **Adopt a section unique to one repository when it generalises.** "Behaviour is
  unchanged", "existing coverage that moved", "packaging and version changes",
  "why the previous text was wrong" each describe a *type*, not a project.
- **Leave out anything that describes a project's strategy.** A heading about
  frozen test vectors, a specific benchmark rig, or a particular fixture set
  belongs to that repository and would be a lie in every other one.
- **Keep the four common headings byte-identical.** If the guidance in one drifts,
  the gate demands different things in different repositories, which is the exact
  failure this directory exists to prevent.

Two judgement calls worth keeping, because the reasoning is not recoverable from
the files: the test-plan heading is `## Test plan` rather than `## Checks run`,
because "test plan" is what a contributor looks for and "checks" invites a list of
everything CI does; and perf carries `## Measurements (required)` with the
qualifier in the heading, so an unmeasured perf change is visibly incomplete
without anyone having to read the section to find out.

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
with write access. Because all eight rules resolve to that same account, the
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
2. If the name is a `type/*` label, mirror it into every adopting repository's
   manifest **and** into the `type-labels` input of that repository's
   `policy.yml`. A gate that names a label the remote does not have is
   unsatisfiable, not merely strict.
3. Reuse an existing family color where the meaning matches — `type/feature` and
   `type/documentation` already share `0075CA`.
4. Removing an entry does not remove the remote label, and a remote label absent
   from this manifest is drift in the other direction. The reconciliation recipe
   travels with the manifest rather than with this repository, so read the target's
   copy before overwriting it; this repository has one of its own at the bottom of
   `labels.yml`.
5. If the change is for **one** repository rather than the standard, it is not an
   edit here at all: declare it in that repository's `.github/standards.local.yml`
   under `extensions`, per § Customizing the standard.

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
- Do not treat `.github/standards.local.yml` as configuration either. Nothing
  reads it, not even the gate; it records a deviation so that a human or a checker
  can recognise one. The failure is silent — a repository that believes it
  configures something sees no error and no effect.
- Do not record a deviation without a `reason`. That is the one field the whole
  file exists for: an unexplained difference from the core is exactly what the
  record was supposed to make recognisable.
- Do not express a repository's own concern as a new `type/*` member. Use the
  existing five plus an `extensions` entry; `type/` is frozen for the reason in
  § Customizing the standard, which is not "the gate forbids it".
- Do not grow the `type/*` family in this repository alone. It is not enforced
  downstream at five members or any other number — see the sync model section for
  why the two vocabularies have to be declared separately.
- Do not write "the gate requires" about **this** repository. Its policy job is
  not a required status check and cannot become one while one person holds all the
  write access. Enforcement is a per-repository fact, and the same organisation
  will have repositories on both sides of it — check, per § Enforcement, before
  describing a rule as binding.
- Do not overwrite an adopting repository's `labels.yml` with this bare list
  without porting its header and reconciliation recipe across first.
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