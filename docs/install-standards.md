# Installing the GitHub standards

This guide is for AI agents adopting the shared GitHub standards from
`ailuracollective/standards` into another repository. Read the target
repository's own `AGENTS.md` and any nearer agent instructions first.
Do not treat the source repository's instructions as a replacement for
the target repository's local rules.

The [source README](../README.md) describes the adoption model;
[architecture](architecture.md) explains which artifacts are canonical and
which are templates. These files are the source of truth when this guide
and the repository disagree.

## Preconditions

- Identify the target repository, its default branch, maintainers, and
  current `.github/` contents. Work on a separate branch and use a pull
  request; do not edit its default branch directly.
- Obtain permission to change the target repository and, separately, to
  create or update labels and configure secrets or branch protection.
- Read the source [contract](../.github/CONTRACT.yml), the target
  repository's `AGENTS.md`, and any target-specific conventions.
- Inspect the target's `.github/labels.yml`, issue and PR templates,
  workflows, `CODEOWNERS`, remote labels, and existing customization
  record before copying anything. Missing files are different from
  intentionally customized files.
- Select a specific source revision or release. Use the same revision for
  every copied file and record it in the adoption pull request. Do not
  assemble a mixed-version standard.

## Apply the standard

Work in the target repository. Paths below refer to the source repository
unless otherwise stated. Preserve relative paths in the target.

### 1. Compare and copy the canonical artifacts

Copy these from one source revision into the corresponding target paths,
after comparing each destination with its existing contents:

| Source path | Target path |
| --- | --- |
| `.github/CONTRACT.yml` | `.github/CONTRACT.yml` |
| `.github/ISSUE_STANDARD.md` | `.github/ISSUE_STANDARD.md` |
| `.github/ISSUE_TEMPLATE/` | `.github/ISSUE_TEMPLATE/` |
| `.github/PULL_REQUEST_TEMPLATE/` | `.github/PULL_REQUEST_TEMPLATE/` |
| `.github/labels.yml` | `.github/labels.yml` |
| `.github/CODEOWNERS` | `.github/CODEOWNERS` |
| `.github/workflows/policy.yml` | `.github/workflows/policy.yml` |
| `scripts/validate_contract.py` | `scripts/validate_contract.py` |

Copy the organization's
[conventions](../.agents/organization-conventions.md) to
`.agents/organization-conventions.md` if the target does not already
have the authoritative conventions at that path. Reconcile an existing
copy rather than blindly replacing it.

The source's `.github/standards.local.example.yml` is an **optional**
schema example, not an active configuration file. If intentional
deviations are needed, record them in the target's
`.github/standards.local.yml` as described in
[customization](customization.md). This file documents decisions; it
does not change workflow behavior.

If the target already has standards files, compare their content,
structure, and local changes with the selected source revision. Preserve
approved deviations and seek a maintainer's decision for unresolved
conflicts. Do not overwrite files or remove remote labels by default.

### 2. Complete repository-specific skeletons

Use `templates/AGENTS.md`, `templates/.github/workflows/ci.yml`,
and `templates/.github/workflows/release.yml` as **starting points**,
not ready-to-run files. Inspect the actual paths and contents before use.

- Complete every `TODO` in the target's `AGENTS.md`; preserve its
  repository-specific instructions and mandatory organization links.
  Do not replace an existing valid `AGENTS.md` wholesale.
- Adapt CI to the target's real stack and commands. Include contract
  validation in CI after copying the validator.
- Configure release automation for the target only if applicable;
  placeholder release steps and source-repository release settings
  are not usable as-is.
- Replace the generic `## Verification` section in **every** PR
  template with evidence prompts and commands that actually apply to
  the target repository when wiring up CI.

### 3. Reconcile labels and policy

Treat the target's remote GitHub labels, manifest, and policy inputs as
three separate records that must agree.

1. Inspect remote label names in the target repository:

   ```sh
   gh label list --limit 100 --json name --jq '.[].name' | sort
   ```

2. Compare them with `.github/labels.yml` and every label referenced
   by issue templates and workflows. Reconcile the target's manifest
   shape and any label-management recipe before replacing it. Do not
   assume copying the manifest creates GitHub labels.
3. With authorization, create or update missing or mismatched remote
   labels using the target's reviewed manifest and a documented
   reconciliation procedure. Verify the result against the remote API.
   Do not delete unrelated labels.
4. Check the target `.github/workflows/policy.yml`:
   `type-labels` must name the actual `type/*` labels,
   `title-types` must name PR title types, and
   `approved-label` / `auto-label-name` must resolve to real
   status labels. Do not conflate the type and title vocabularies.
5. Check where the default PR template is stored. If it lives in
   `.github/PULL_REQUEST_TEMPLATE/PULL_REQUEST_TEMPLATE.md`,
   configure the policy's `default-template` input accordingly;
   the action otherwise assumes `.github/PULL_REQUEST_TEMPLATE.md`.

See [architecture](architecture.md) for the label sync model and
[customization](customization.md) for permitted deviations.

### 4. Wire up validation and repository permissions

Run the copied contract validator in the target with PyYAML available:

```sh
uv run --with PyYAML python scripts/validate_contract.py
```

Add the same check to the target's CI workflow. Ensure CI runs the
target's real lint, build, and test commands rather than placeholders.
Confirm that `CODEOWNERS` refers to accounts with the appropriate
repository permissions and that branch rules and required checks
actually exist; a committed `CODEOWNERS` file does not enforce reviews
on its own.

Inspect the target's policy and release workflows before supplying
secrets or permissions. Never copy token values from another repository,
print them in logs, or assume source-repository credentials are valid
for the target.

## Verify the adoption

In the target repository, check and record the results of all of these:

1. Every relative link in the completed `AGENTS.md` resolves; there
   are no `TODO` markers or unused template placeholders.
2. `uv run --with PyYAML python scripts/validate_contract.py`
   succeeds against the copied contract, templates, and labels.
3. All labels used by forms and policy inputs exist on the target's
   GitHub remote, with the expected names.
4. The policy points at the actual default PR template and has
   consistent `type-labels`, `title-types`, and status labels.
5. Target-specific CI and release workflows contain real, reviewed
   configuration; required checks, reviewers, and permissions are
   validated against the target repository rather than assumed.
6. The adoption pull request lists the source revision, files copied,
   intentional deviations, commands run, observed output, and any
   approvals or follow-up work still required.

If a check cannot be completed because permissions, credentials, or
repository context are missing, report it as **not verified**. Do not
claim installation success based solely on a passing linter.

## Conflicts and recovery

Stop before any destructive change. For each conflict, document the
source version, current target content, proposed resolution, and owner
approval. Preserve unrelated work and do not force-push or delete
target files to make adoption appear clean.

Keep changes in a dedicated branch so maintainers can review the diff
and abandon or revert the adoption commit if necessary. Remote label,
secret, and repository-setting changes need their own recorded rollback
plan: reverting a commit alone does not undo them.

This is a manual, one-repository-at-a-time process. The source
repository does not automatically propagate updates and does not track
all adopting repositories.
