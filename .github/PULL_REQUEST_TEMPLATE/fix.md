# Bug fix

Use for correcting incorrect behavior. If the behavior was never correct and is being newly
defined, that is a `feat`.

Show the defect with evidence. The root cause is what stops it recurring, so do not stop at the
symptom.

## Linked issue (required)

<!-- The issue must carry `status/ready`. Use a closing keyword on its own line; `Refs #N` does not close it. -->

Closes #

## Type (required)

<!-- Check one. The title type and the label differ: twelve title types, five `type/*` labels. -->

- [ ] `fix`

<!-- Label to apply: `type/bug`. -->

## Symptom

<!-- What is wrong, and what does the user see as a result? -->

## Root cause

<!-- Why it happens. A fix that does not name the cause is a patch, not a fix. -->

## Minimal reproduction

<!-- Smallest reliable reproduction from a clean checkout; if flaky, say why. -->

1. ...
2. ...
3. ...

## Expected vs actual

<!-- What you expected, and what happened instead. -->

Expected: ...
Actual: ...

## Regression test

<!-- The test that fails before and passes after. Add manual steps if it does not cover the fix. -->

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
