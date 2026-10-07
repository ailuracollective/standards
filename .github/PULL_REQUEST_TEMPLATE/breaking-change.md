# Breaking change

Use for a change that removes or alters existing public behavior in a way a consumer can
observe. A breaking change is not a `feat`: `feat` is new capability that leaves what exists
working.

State the old contract, the new one, and exactly what a consumer has to change. A breaking
change is a permanent obligation on every downstream reader, so the migration path matters more
than the diff.

## Linked issue (required)

<!-- The issue must carry `status/ready`. Use a closing keyword on its own line; `Refs #N` does not close it. -->

Closes #

## Type (required)

<!-- Check one. The title type and the label differ: twelve title types, five `type/*` labels. -->

- [ ] `breaking-change`

<!-- No `type/*` label marks a break. Apply the label of the underlying change. -->

## What breaks and for whom

<!-- The API, option or behavior that changes, and who is affected. -->

## Before / after

<!-- The old and new contract side by side. -->

## Migration

<!-- Exact steps a consumer takes, with code. -->

## Codemod feasibility

<!-- Whether a codemod is viable. "Not feasible" is a valid answer. -->

## What was decided

<!-- Why this shape and not a compatible alternative. -->

## Affected version range

<!-- Which versions carry the old behavior, and which release removes it. -->

## Deprecation plan

<!-- Timeline and removal version, or "removed outright". -->

## Test plan

<!-- REPO OWNER: replace with the checks this repository's CI runs. -->

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
