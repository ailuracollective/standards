# Revert

Use for undoing a previously merged change. Prefer fixing forward when the original intent was
correct.

A revert removes shipped behavior. State what is being lost, not only what is being restored.

## Linked issue (required)

<!-- The issue must carry `status/ready`. Use a closing keyword on its own line; `Refs #N` does not close it. -->

Closes #

## Type (required)

<!-- Check one. The title type and the label differ: twelve title types, five `type/*` labels. -->

- [ ] `revert`

<!-- `type/task` is the catch-all label for this type. -->

## What is being reverted

<!-- Link the pull request or commit being reverted, and its version. -->

## Why revert rather than fix forward

<!-- Why the original change should not stand, and why a fix forward is not better. -->

## Reason the original was wrong

<!-- The defect in the original change, with evidence. -->

## Impact of reverting

<!-- What is being taken away and who is affected. -->

## Version impact

<!-- Whether this is a patch, minor, or major release, and why. -->

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
