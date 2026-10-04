# AGENTS.md

Guidance for AI agents and contributors working in this repository.

## What this repository is

The source of truth for GitHub issue standards shared across an organisation's
repositories. There is no application code here, no build, no test suite, and no
CI. The entire repository is **9 YAML files and 1 Markdown file** under
`.github/`, plus this `AGENTS.md`.

Three artifacts, each with exactly one owner:

| File                                                   | Owns                                     | Read by                                     |
| ------------------------------------------------------ | ---------------------------------------- | ------------------------------------------- |
| `.github/ISSUE_STANDARD.md`                            | how an issue is written                  | humans and agents drafting issues           |
| `.github/labels.yml`                                   | the label set (30 labels)                | anything that reads or applies labels       |
| `.github/ISSUE_TEMPLATE/*.yml` (7 templates + config)  | the forms in the issue chooser           | GitHub                                      |

`ISSUE_STANDARD.md` is **prose and is not machine-readable**. It was
`ISSUE_STANDARD.yml` and did not parse as YAML — the numbered list under Purpose
reads as mapping keys, so the file failed to load from its first numbered line
onward. It was renamed rather than repaired. Nothing should parse it, and no
validator should be pointed at it.

Nothing in this repository executes. `labels.yml` is a reviewed manifest, not
workflow input: GitHub does not read it and no CI parses it. Editing it changes
the *record* of the label set, not the labels on any remote.

## Inventory

- **7** issue types, declared once in `ISSUE_STANDARD.md` § Issue Types.
- **7** templates — one per type — plus `config.yml`, which is not a template.
- **30** labels: six prefixed families (`type` 5, `priority` 4, `status` 5,
  `scope` 8, `meta` 5, `release` 2) plus one unprefixed, `github_actions`.
- **11** files total: the 9 YAML files and 1 Markdown file above, plus this one.
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

## Known gap: no template applies a label that exists

This is the one real inconsistency in the repository, and it is deliberate that
it is documented rather than quietly patched. **None of the seven `labels:`
values in the templates is a member of `labels.yml`.**

| Template            | `labels:` today | In the manifest? | Intended `type/*`                     |
| ------------------- | --------------- | --------------- | ------------------------------------- |
| `feature.yml`       | `enhancement`   | no              | `type/feature`                        |
| `improvement.yml`   | `enhancement`   | no              | `type/improvement`                    |
| `bug.yml`           | `bug`           | no              | `type/bug`                            |
| `docs.yml`          | `documentation` | no              | `type/documentation`                  |
| `maintenance.yml`   | `maintenance`   | no              | `type/task` (no `chore` exists)       |
| `test.yml`          | `testing`       | no              | none fits — `scope/testing` is a scope |
| `investigation.yml` | `investigation` | no              | none                                  |

GitHub drops a label a template names but the repository does not have, without
an error, so an issue opened through any of these forms currently arrives with
**no type label at all**. `enhancement` is doubly wrong: it is undeclared, and
`feature.yml` and `improvement.yml` both apply it, so even if it existed it could
not tell the two apart.

Four of the seven have an unambiguous fix. Three do not, and that is what makes
this a decision rather than a mechanical change:

- `type/task` is declared in the manifest and applied by no template, which is
  the strongest signal that it is `chore`'s home.
- `test:` has no type label. It either maps to `type/task` alongside `chore`, or
  the family gains a sixth member.
- `spike:` has no type label and no candidate. `type/task` is the only
  defensible stretch.

Adding `type/chore`, `type/test`, and `type/spike` would grow the family from 5
to 8 and break a gate that consuming repositories already enforce — see
`alpinejs-toolkit`'s `policy.yml`, which lists its five `type-labels` as an
input. Fixing this properly is a cross-repository change: amend the seven
templates, then mirror the decision into every consumer's manifest and into the
`type-labels` input of its `policy.yml`. Nothing here should be changed in
isolation.

## Sync model

`labels.yml` opens with "Keep this file synchronized across projects."
Concretely: this repository is the origin, each consuming repository holds its
own copy under its own `.github/`, and **edits here do not propagate**. There
is no workflow, submodule, or sync bot in this repository. Synchronization is a
manual copy, which means drift is expected and has to be checked for by hand.

State of the one comparable consumer, `alpinejs-toolkit`:

- Its `.github/labels.yml` declares the **same 30 labels with identical names and
  colors** — verified, zero divergence.
- Its file is structurally different, and richer: a top-level `labels:` mapping
  key rather than a bare sequence; entries alphabetised within each family;
  `# --- family ---` comments; a long header; and a `gh label create --force`
  reconciliation recipe with a prune procedure at the bottom. The file here is a
  bare top-level sequence, grouped `type`, `priority`, `status`, `scope`, `meta`,
  `github_actions`, `release`, with a three-line header and no recipe.
- Its header corrects a claim this file's line 3 leaves open: the labels *are*
  applied on the remote, so the manifest records a set, not a plan to create one.
- Its two templates already fix the gap above. They use
  `labels: ["type/bug", "status/needs-review"]` — inline array form, manifest
  members only, and the auto-applied triage label alongside the type.
- It has **not** adopted the seven-type standard: only `bug_report.yml` and
  `feature_request.yml` exist, and its `config.yml` sets
  `blank_issues_enabled: true` where this repository sets `false`.

So the label set has converged and the template set has not. Copying this
repository's `labels.yml` over a consumer's manifest would be a downgrade. Prefer
porting the consumer's header and reconciliation recipe back here, and treat the
bare list as the portable subset.

Other divergences worth knowing before you copy anything either direction:

- **Label form.** This repository uses a block sequence under a bare top level;
  the consumer nests under `labels:`. Both parse as YAML; they are not the same
  schema, so a mechanical copy between them changes the document shape.
- **Field id casing.** This repository uses kebab-case (`out-of-scope`,
  `acceptance-criteria`); the consumer uses snake_case (`proposed_outcome`,
  `additional_context`).
- **Field types.** This repository uses only `textarea` and one `markdown`. The
  consumer also uses `checkboxes` with per-option `required: true` for a
  preflight block, `render: shell` for a log field, `type: input` for a version
  string, and explicit `validations: required: false` on optional fields.
- **`blank_issues_enabled`.** `false` here, `true` there. Treat this as a
  per-repository policy choice, not drift.

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
- `labels.yml` is the only file in the repository with no trailing newline. Do
  not fix that incidentally in an unrelated change, and do not propagate it into
  a consumer.

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

# one template per type, prefixes matching the standard
sed -n '/^## Issue Types/,/^## Title/p' .github/ISSUE_STANDARD.md | grep -c '^- `'
ls .github/ISSUE_TEMPLATE/*.yml | grep -vc config       # 7 templates
grep -h '^title: ' .github/ISSUE_TEMPLATE/*.yml | sort   # 7 prefixes
```

The first check needs `pyyaml`, which is not vendored. It globs `*.yml`, so it
never touches `ISSUE_STANDARD.md` — there is nothing to parse there.

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
- Do not grow the `type/*` family in this repository alone. It is enforced
  downstream at exactly five members.
- Do not overwrite a consuming repository's `labels.yml` with this bare list
  without porting its header and reconciliation recipe back here first.