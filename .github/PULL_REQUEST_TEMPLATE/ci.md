# Continuous integration

Use for changes to workflows, actions, or automation that runs on pull requests.

CI runs with repository permissions on every pull request, including from forks. Treat a change
here as a security change.

## Linked issue (required)

<!-- The linked issue MUST carry the `status/ready` label. Apply exactly one of these
closing keywords on its own line. `Refs #N` does NOT close the issue and does not satisfy
this requirement. Bot pull requests are exempt; see `skip-actors` in `policy.yml`. -->

Closes #

## Type (required)

<!-- Check exactly ONE. This is the Conventional Commit type for your TITLE; the LABEL
is separate and coarser: there are twelve title types and only five `type/*` labels.
Apply exactly one `type/*` label. -->

- [ ] `ci`

<!-- `type/task` is the catch-all. The label family has five members and
     none describes this work, so this is the intended home. The label is
     deliberately coarser than the title type. -->

## What changes in CI

<!--
Which workflow or action changes, and what it will do differently.
-->

## Why

<!--
What failure this prevents or what capability it adds.
-->

## Effect on pull requests

<!--
Runtime added, checks added or removed, and whether contributors will see new required checks.
-->

## Permissions and secrets

<!--
What `permissions:` and `secrets:` this grants. State the blast radius explicitly — a new
`pull_request_target` or a widened `permissions` block is a security change wearing a CI
change's clothes.
-->

## Failure mode

<!--
What happens when this workflow itself is wrong or unavailable. Does it block merges, or
silently pass?
-->

## How to reproduce locally

<!--
How to exercise the change before it runs on someone else's pull request.
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
