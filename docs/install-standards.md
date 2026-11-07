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
- Adapt CI to the target's real stack and test commands; do not install the
  source-only contract validator in the target.
- Ask separately whether automated releases and deployment are needed;
  neither is required for standards adoption.
- Replace the generic `## Verification` section in **every** PR
  template with evidence prompts and commands that actually apply to
  the target repository when wiring up CI.

### 3. Choose release and deployment options

Before configuring release or deployment workflows, **ask the owner**:

1. Should the project automatically version packages, generate changelogs,
   create tags or GitHub releases, or publish packages? Which packages?
2. Does it need deployment? If so, to which hosting provider, environment,
   and region, with what approval and rollback requirements? Deployment
   and releases are separate decisions; either, both, or neither may apply.
3. Which languages, frameworks, package managers, and build artifacts
   are in use? Inspect manifests and workflows and confirm assumptions.

Recommend options suited to the detected stack: npm for Node.js/TypeScript
packages, PyPI for Python packages, Maven repositories for JVM libraries,
or container registries for container-based services. Applications may
deploy to Cloud Run, Kubernetes, or an existing approved hosting service.
These are **examples**, not default requirements. Confirm the choice
with the owner before creating any configuration.

For automatic versioning, changelogs, and GitHub releases, normally
propose [Google Release Please](https://github.com/googleapis/release-please).
It is optional and **does not perform deployment**. If selected:

- Configure `.github/workflows/release.yml`,
  `release-please-config.json`, and
  `.release-please-manifest.json` according to the target's package
  type, existing version, paths, and release branch. Do not assume
  the standards repository's `simple` release type is applicable.
- Configure the release labels that the chosen technology actually uses.
  This standards repository overrides Release Please's default
  `autorelease: pending` and `autorelease: tagged` labels with custom
  `release/pending` and `release/tagged` labels via its `label`
  and `release-label` settings. These are **not universal** labels:
  decide which names the target will use, reconcile only those names
  in its manifest and remote GitHub labels, and obtain approval.
- Verify release PR behavior against the target's pull request policy.
  If an exemption is needed, scope it to release branches, not every
  PR authored by a bot account.
- Configure target-specific credentials, permissions, and secrets.
  Do not copy this repository's tokens or assume its token names apply.

If no releases are requested, do not install the placeholder release
workflow, release secrets, or release labels. If there is no deployment,
do not create deployment workflows, environments, or credentials. For
deployments that are requested, document build, delivery, approval, and
rollback independently from Release Please.

See [releases](releases.md) for the source repository's implementation.

### 4. Reconcile labels and policy

Treat the target's remote GitHub labels, manifest, and policy inputs as
three separate records that must agree.

1. Inspect remote label names in the target repository:

   ```sh
   gh api --paginate --slurp 'repos/{owner}/{repo}/labels?per_page=100' \
     --jq '[.[][] | .name] | sort | .[]'
   ```

2. Use the **complete paginated inventory** for both comparison and
   post-installation verification. Compare all remote labels against
   `.github/labels.yml` and names referenced by templates and workflows. Reconcile the target's manifest
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

A target may retain an approved manifest with a top-level `labels:`
mapping rather than the source's top-level list. Preserve its valid
structure and reconcile the actual entries against templates, policy,
and remote labels. **Do not copy or adapt the source-only validator**.

For policy status comments, the source workflow uses
`AILURA_PR_COMPLIANCE_TOKEN` and a fixed `comment-author`. A target
must configure its own suitably scoped `pull-requests: write` token,
set the appropriate `comment-token` and matching `comment-author`
in both relevant policy jobs, and verify that comments appear on a
test PR. Alternatively, disable status comments if supported by the
policy action, record the approved deviation, and check the rest of
the policy independently. Do not widen read-only checker job
permissions just to post comments.

See [architecture](architecture.md) for label reconciliation and
[customization](customization.md) for approved deviations.

### 5. Validate the adopted configuration and permissions

`scripts/validate_contract.py` is **internal to the standards source
repository**. Do not copy it or add it to a target's CI. Instead,
compare the target's copied files against the pinned source revision
and verify that its templates, policy inputs, and remote GitHub
labels are consistent. Adopters do not require Python or `uv`
to validate this documentation-based adoption.

Configure real stack-specific lint, build, and test commands in the
target's CI. Ask its maintainers to confirm **each** `CODEOWNERS`
account before adopting source owners: the standard repository's
`@SiddharthaGF` must not inadvertently own target files. Preserve
the catch-all rule, record approved owner deviations, and check that
the selected owners have appropriate permissions. Verify branch
protection and required checks in the target's actual settings;
`CODEOWNERS` alone cannot enforce reviews.

Inspect policy and optional release/deployment workflows before
supplying secrets. Never copy token values between repositories
or print them in logs.

## Verify the adoption

In the target repository, check and record the results of all of these:

1. Every relative link in the completed `AGENTS.md` resolves; there
   are no `TODO` markers or unused template placeholders.
2. Copied artifacts match the pinned source revision or have
   approved deviations, with the templates, policy configuration,
   and labels checked without a copied validator.
3. All labels used by forms and policy inputs exist on the target's
   GitHub remote, with the expected names.
4. The policy points at the actual default PR template and has
   consistent `type-labels`, `title-types`, and status labels.
5. CI uses real project commands. Optional release and deployment
   workflows exist only if requested, with checked technology-specific
   labels, credentials, destinations, approvals, and rollback plans.
   Required checks, reviewers, and permissions reflect the target.
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
