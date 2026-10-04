# Build

Use for build system, bundler, compiler, or packaging changes. A dependency bump that only
changes a lockfile is a `chore`.

Build changes are invisible in review and visible everywhere. State what the output now is, and
prove it is what you intended.

## Linked issue (required)

<!-- The linked issue MUST carry the `status/ready` label. Apply exactly one of these
closing keywords on its own line. `Refs #N` does NOT close the issue and does not satisfy
this requirement. Bot pull requests are exempt; see `skip-actors` in `policy.yml`. -->

Closes #

## Type (required)

<!-- Check exactly ONE. This is the Conventional Commit type for your TITLE; the LABEL
is separate and coarser: there are twelve title types and only five `type/*` labels.
Apply exactly one `type/*` label. -->

- [ ] `build`

<!-- `type/task` is the catch-all. The label family has five members and
     none describes this work, so this is the intended home. The label is
     deliberately coarser than the title type. -->

## What changed in the build

<!--
The configuration, plugin, or pipeline step that changed, and why.
-->

## Why

<!--
What was wrong or missing before this change.
-->

## Before / after output

<!--
Bundle size, emitted files, or timings, before and after. For a packaging change, the difference
in what ships.
-->

## Output equivalence

<!--
How you established the produced artifact is still correct. For a toolchain bump, what was
verified beyond "it built".
-->

## Downstream impact

<!--
Who is affected by this: consumers of the package, the publish pipeline, or only this
repository's CI.
-->

## Packaging and version changes

<!--
If this repository publishes a package: what is now in the artifact, and does the version bump.
A build change that silently alters what ships is a release, not a refactor. Write "not
published" when the repository does not publish.
-->

## Test plan

<!-- REPO OWNER: replace every line below with the checks CI actually runs in THIS
     repository. The gate only requires that this heading exists, but a contributor
     cannot verify a change from a template that lists commands this repository does
     not have — a TypeScript repository cannot run `cargo test`. Keep this block in
     sync with CI in the same pull request that changes CI. -->

- [ ] `TODO: lint and formatting`
- [ ] `TODO: unit tests`
- [ ] `TODO: build`
- [ ] `TODO: type check, if the repository has one`
- [ ] Manually exercised the change end to end

## Contributor checklist

- [ ] Linked an approved issue with `Closes #N`, `Fixes #N` or `Resolves #N`
- [ ] The linked issue carries the `status/ready` label
- [ ] Branch is named `<github-username>/<type>/<description>`, all lowercase
- [ ] Applied exactly one `type/*` label
- [ ] Commit messages follow Conventional Commits
- [ ] No `Co-Authored-By` trailers
- [ ] Documentation updated where public behavior or configuration changed
- [ ] All CI checks pass
