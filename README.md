# GitHub standards

The origin for how issues and pull requests are written across `ailuracollective`.
Five artifacts, copied by hand into each repository:

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

**It does not propagate.** There is no sync mechanism of any kind: no workflow, no
submodule, no bot. Editing a file here changes nothing anywhere. Each adopting
repository holds its own copy, copies are manual, and drift is the default state
rather than an exception.

The consequence worth stating plainly: **this repository cannot tell you whether a
given repository has adopted it, or has adopted it correctly.** Copies are
untracked. `AGENTS.md` describes the rules and how to check any one repository; it
does not, and deliberately does not, hold a list of who has copied what. That list
would be stale the moment a repository is created or deleted, and a stale list is
worse than none — it reads as authoritative. To find out about a specific
repository, read that repository.

**It cannot require its own gate to pass.** `.github/workflows/policy.yml` runs
the standard against itself, but `main` also requires a code-owner review and one
account holds all the write access, so making the policy job a required status
check would deadlock the repository. See *Ownership and enforcement* in
`AGENTS.md`.

## Adopting it

Copy the five artifacts into the repository's own `.github/`. Three things are not
optional.

**Replace the `## Test plan` block in all 12 pull request templates.** Here they
are `TODO` placeholders, because the commands are per repository and structure is
universal. `vp check` and `cargo clippy` have nothing to do with each other; a
shared test plan would be a shared lie. Do it in the same pull request that wires
up CI, so the form never names a command the repository cannot run.

**Reconcile the label vocabulary.** Do not copy `labels.yml` over a manifest that
has a reconciliation recipe without porting the recipe across — see *Sync model* in
`AGENTS.md`. And if the repository runs `pull-request@v2`, fix `type-labels` in the
same change, or the type-label check will reject the very labels the templates tell
contributors to apply.

**Create the labels.** A manifest is a record, not a mechanism: GitHub does not
read it, and nothing applies it. Until the labels exist on the remote, every
template that names one has that label silently discarded, and the issue arrives
unlabelled with nothing in any log to say so.

**Check where the default pull request form goes.** Its location is not fixed, and
copying only the directory omits it. This repository keeps it inside the
directory, at `.github/PULL_REQUEST_TEMPLATE/PULL_REQUEST_TEMPLATE.md`; a
repository may instead keep it beside the directory at
`.github/PULL_REQUEST_TEMPLATE.md`. Either is valid, so tell the gate which one you
chose with `default-template` — its own default is the second, and inheriting it
while your file is the first makes the body-structure check resolve to nothing.

## Verifying an adoption

Nothing here runs against an adopting repository, so the checks are manual and
per-repository. Two are worth doing first, because both catch the same class of
defect — a configuration that names something that does not exist, which fails
silently rather than loudly.

```sh
# 1. does every label a template or a workflow names actually exist on the remote?
gh label list --limit 100 --json name --jq '.[].name' | sort

# 2. do the gate's inputs name labels that repository has, rather than labels it once had?
grep -A3 'type-labels:\|approved-label:\|auto-label-name:' .github/workflows/policy.yml
```

A gate that names a label the repository does not have is not a strict gate, it is
an **unsatisfiable** one: the check matches by exact name, so no pull request can
pass it, and the failure reads as though the contributor did something wrong.

Then check that the gate is enforced at all, which is a different question from
whether it is configured correctly. `AGENTS.md` has the commands and the trap
involved.

## Changing the standard

Read `CONTRIBUTING.md` first. The short version: open an issue before a pull
request, and a change to `labels.yml` or to a template is not finished when it
lands here — it also has to be mirrored into every repository that adopted it, which
is manual and is the part that is easy to forget.

## Licence

MIT. See [LICENSE](LICENSE). The standard is MIT for the same reason everything
that adopts it should be: these files get copied into other projects, and the
point is that copying them is unencumbered.