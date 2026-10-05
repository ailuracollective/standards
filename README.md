# GitHub standards

The origin for how issues and pull requests are written across
`ailuracollective`. Four artifacts, copied by hand into each repository:

| Artifact                          | What it decides                                             |
| --------------------------------- | ----------------------------------------------------------- |
| `.github/ISSUE_STANDARD.md`       | how an issue is written — prose, not data                   |
| `.github/ISSUE_TEMPLATE/*.yml`    | the 7 forms in the issue chooser, plus `config.yml`         |
| `.github/PULL_REQUEST_TEMPLATE/`  | 12 forms, one per Conventional Commit type, plus a default  |
| `.github/labels.yml`              | the 30-label set                                            |
| `.github/CODEOWNERS`              | who reviews a change, per file                              |

`AGENTS.md` is the working reference: the invariants, the conventions, the known
gaps, and the commands to check a change by hand. Read it before editing anything
here — most of it exists because something went wrong the obvious way at least
once.

## What this repository does not do

**It does not enforce its own standard.** There is no CI in this repository: no
workflows, no validation job, nothing that fails a pull request for violating an
invariant. Every invariant in `AGENTS.md` is checked by hand, by whoever remembers
to run the block at the end of it. If you want that changed, it is a real piece of
work — see *Adding CI* in `AGENTS.md`'s follow-ups — not a toggle.

**It does not propagate.** There is no sync mechanism of any kind: no workflow, no
submodule, no bot. Editing a file here changes nothing anywhere. Each consumer
holds its own copy, copies are manual, and drift is the default state rather than
an exception. See *Sync model* in `AGENTS.md` for the measured drift.

**The gates in `ailuracollective/actions` are advisory in both current
consumers.** `pull-request@v1` runs five checks — linked issue, type label, title
length, Conventional Commit title, body structure — and neither `alpinejs-toolkit`
nor `colander` requires its job as a status check. `alpinejs-toolkit`'s `master`
has no branch protection at all. The gates annotate a pull request and are then
ignored, which is why pull requests carrying no type label have been merged. The
templates in this repository are read by the gate; the headings they declare are
requirements that nothing currently checks.

There is also a live disagreement about label naming that the gates would expose
the moment they were enforced. This repository's manifest and both remotes use
prefixed slash names (`type/bug`). Both `policy.yml` files fill `type-labels`
with bare names (`feat`, `fix`), and the check compares by exact name, so a pull
request labelled `type/bug` is reported as carrying no type label at all. Both
cannot be right. The manifest wins, because it is what exists on the remotes,
which makes `type-labels` the half that needs fixing.

## Adopting it

Copy the four artifacts into the consumer's own `.github/`. Two things are not
optional.

**Replace the `## Test plan` block in all 12 pull request templates.** Here they
are `TODO` placeholders, because the commands are per repository and structure is
universal. `vp check` and `cargo clippy` have nothing to do with each other; a
shared test plan would be a shared lie. Do it in the same pull request that wires
up CI, so the form never names a command the repository cannot run.

**Reconcile the label vocabulary.** Do not copy `labels.yml` over a manifest that
has a reconciliation recipe without porting the recipe across — see *Sync model*
in `AGENTS.md`. And if the repository runs `pull-request@v1`, fix `type-labels` in
the same change, or the type-label check will reject the very labels the templates
tell contributors to apply.

Copying only the directory also silently omits the default pull request form,
whose location differs across the organisation: this repository keeps it at
`.github/PULL_REQUEST_TEMPLATE/PULL_REQUEST_TEMPLATE.md`, `alpinejs-toolkit` and
`ailuracollective/actions` at `.github/PULL_REQUEST_TEMPLATE.md`, and `colander`
has none at all.

## Current consumers

Measured, not aspirational. `type/*` labels here means labels matching this
repository's manifest.

| Repository             | Remote labels | Its own manifest | Issue forms | PR forms | Gates block merges |
| ---------------------- | ------------- | ---------------- | ----------- | -------- | ------------------ |
| `alpinejs-toolkit`     | 30 of 30, colors identical | 14 names, none of them the 30 | 2 | 7 of 12 | no — no branch protection |
| `colander`             | 29 of 30, plus a stray `type:feature` | 12 names, none of them the 30 | 4 | 10 of 12 | no — two other checks required |

Neither consumer has adopted the 7-type issue standard, and both apply issue
template labels that exist on no remote, so issues arrive with no type label at
all. `colander` additionally lacks `github_actions` and has drifted two release
label colors.

## Changing the standard

Read `CONTRIBUTING.md` first. The short version: open an issue before a pull
request, and a change to `labels.yml` or to a template is not finished when it
lands here — it also has to be mirrored into every consumer, which is manual and
is the part that is easy to forget.

## Licence

MIT. See [LICENSE](LICENSE). The other three public repositories in the
organisation are MIT for the same reason: these files get copied into other
projects, and the point is that copying them is unencumbered.
