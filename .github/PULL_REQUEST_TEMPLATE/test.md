# Tests

Use when the primary purpose is test coverage. If the pull request also changes runtime code to
make a test pass, it is a `fix` or a `feat`.

Say what the suite now guarantees that it did not before. Coverage that does not change a
guarantee is not worth the maintenance cost.

## Linked issue (required)

<!-- The issue must carry `status/ready`. Use a closing keyword on its own line; `Refs #N` does not close it. -->

Closes #

## Type (required)

<!-- Check one. The title type and the label differ: twelve title types, five `type/*` labels. -->

- [ ] `test`

<!-- `type/task` is the catch-all label for this type. -->

## Scope of this change

<!-- Which behavior is under test here, and why it is separated from the change that introduced it. -->

## Now covered

<!-- The scenarios that are covered and were not before. Name the cases, not the files. -->

## Existing coverage that moved

<!-- Tests renamed, moved, merged or deleted, and where their coverage went. -->

## Deliberately uncovered

<!-- What you chose not to test, and why. -->

## Fixtures and mocks

<!-- How the test isolates its subject (fixtures, doubles, clock); note any ordering or shared state. -->

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
