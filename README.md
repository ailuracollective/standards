# GitHub standards

The origin for how issues and pull requests are written across `ailuracollective`.
The canonical contract is [CONTRACT.yml](.github/CONTRACT.yml), and each repository
copies the artifacts by hand:

| Artifact                         | What it decides                                            |
| -------------------------------- | ---------------------------------------------------------- |
| `.github/CONTRACT.yml`           | the canonical issue and PR contract — the source of truth  |
| `.github/ISSUE_STANDARD.md`      | how an issue is written — documentation of the contract    |
| `.github/ISSUE_TEMPLATE/*.yml`   | the 7 forms in the issue chooser, plus `config.yml`        |
| `.github/PULL_REQUEST_TEMPLATE/` | 12 forms, one per Conventional Commit type, plus a default |
| `.github/labels.yml`             | the 26-label set                                           |
| `.github/CODEOWNERS`             | who reviews a change, per file                             |

A sixth file, `.github/standards.local.example.yml`, is opt-in: it is the shape of a
customization record (see [below](#if-the-repository-deviates-from-the-standard)).

[`AGENTS.md`](AGENTS.md) is the working reference: invariants, conventions, known
gaps, and the commands to check a change. Read it before editing anything here.

## What this repository does not do

**It does not propagate.** There is no sync mechanism — no workflow, submodule or
bot. Editing a file here changes nothing anywhere else. Copies are manual, and drift
is the default state.

**It does not track who adopted it.** Such a list would be stale the moment a
repository is created or deleted, and a stale list reads as authoritative. To learn
about a specific repository, read that repository.

**It cannot require its own gate to pass.** `.github/workflows/policy.yml` runs the
standard against this repository, but one account holds all write access and `main`
requires a code-owner review, so making the policy job a required check would
deadlock the repository. See docs/enforcement.md.

## Adopting it

Copy the artifacts and `policy.yml` verbatim into the repository's own
`.github/`; the skeletons it completes itself live in [`templates/`](templates/).
Five steps are not optional:

1. **Replace the `## Verification` block in all pull request templates.** Here they
   are generic evidence prompts: structure is universal, commands are not. Do it in
   the pull request that wires up CI, so the form never names a command the
   repository cannot run.
2. **Reconcile the label vocabulary.** Do not copy `labels.yml` over an existing
   manifest without porting its reconciliation recipe — see *Sync model* in
   docs/architecture.md. If the repository runs `pull-request@v2`, fix `type-labels` in the
   same change, or the gate rejects the labels the templates ask for.
3. **Create the labels on the remote.** GitHub does not read the manifest. Until a
   label exists, any template naming it has it silently discarded.
4. **Tell the gate where the default pull request form is.** Here it lives inside
   the directory (`.github/PULL_REQUEST_TEMPLATE/PULL_REQUEST_TEMPLATE.md`); others
   keep it at `.github/PULL_REQUEST_TEMPLATE.md`. The gate defaults to the second, so
   set `default-template` if you use the first — otherwise the body-structure check
   resolves to nothing.
5. **Wire the contract validator into CI.** Copy `scripts/validate_contract.py` into
   the repository and run it with PyYAML available:
   `uv run --with PyYAML python scripts/validate_contract.py`. The check fails when
   templates drift from `.github/CONTRACT.yml` — see *Contract validation* in
   docs/architecture.md.

## If the repository deviates from the standard

A repository that changes nothing copies the artifacts and is done.

Once you add a label, change a color, or tune a gate input, nothing records whether
that difference was decided. Copy `.github/standards.local.example.yml` to
`.github/standards.local.yml` and declare what you changed and why.

It declares, it does not configure: **nothing reads it, not even the gate**. A value
there changes nothing until you also edit your own `policy.yml`. docs/customization.md
has the four deviation levels and what each costs.

A label in a new family such as `area/` needs no approval. A new `type/*` label
does: it is the family the gate reads, and it is frozen at five.

## Verifying an adoption

Nothing here runs against an adopting repository, so checks are manual. Start with
the defect that fails silently — configuration naming something that does not exist:

```sh
# 1. which labels exist on the remote? Every label a template or workflow names must be here.
gh label list --limit 100 --json name --jq '.[].name' | sort

# 2. which labels do the gate's inputs name?
grep -A3 'type-labels:\|approved-label:\|auto-label-name:' .github/workflows/policy.yml

# 3. if it customizes, which labels did it declare? (no file means no deviations — not a defect)
yq -r '.extensions[]?.name' .github/standards.local.yml 2>/dev/null
```

A gate that names a label the repository lacks is **unsatisfiable**, not strict: no
pull request can pass it, and the failure looks like the contributor's mistake.

Whether the gate is *enforced* is a separate question; docs/enforcement.md has
the commands and the trap.

## Changing the standard

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) first. In short: open an issue before a
pull request. A change to `labels.yml` or a template is not finished when it lands
here — it must also be mirrored, by hand, into every adopting repository.

## Drift prevention

The canonical contract ([CONTRACT.yml](.github/CONTRACT.yml)) is the source of
truth. CI validates that templates match the contract:

```sh
uv run python scripts/validate_contract.py
```

This checks that issue templates have the correct sections, PR templates have the
correct headings, and labels are consistent. A change that makes the contract and
templates drift fails the build.

## Secrets

Two tokens run this repository's automation. Only their names live here —
the values are repository secrets:

| Secret                         | Used by                       | For                                                    |
| ------------------------------ | ----------------------------- | ------------------------------------------------------ |
| `AILURA_PR_COMPLIANCE_TOKEN`   | `policy.yml`, `comment-token` | the status comment on every pull request               |
| `AILURA_RELEASE_TOKEN`         | `release.yml`, `token`        | release-please: the release pull request, tag, release |

The compliance token must be a PAT of `AiluraKitty`, because
`comment-author: AiluraKitty` is verified before the action writes. The
release token's holder becomes the author of release commits —
release-please has no author setting — so it is issued to the same account.
Splitting the two functions keeps a leak or a revocation to one function
each. [`docs/releases.md`](docs/releases.md) carries the full reasoning
and the operational detail.

## Licence

MIT — see [LICENSE](LICENSE). These files are meant to be copied into other
projects, and copying them should be unencumbered.
