# Bug fix

Use for correcting incorrect behavior. If the behavior was never correct and is being newly
defined, that is a `feat`.

Show the defect with evidence. The root cause is what stops it recurring, so do not stop at the
symptom.

## Linked issue (required)

<!-- The linked issue MUST carry the `status/ready` label. Apply exactly one of these
closing keywords on its own line. `Refs #N` does NOT close the issue and does not satisfy
this requirement. Bot pull requests are exempt; see `skip-actors` in `policy.yml`. -->

Closes #

## Type (required)

<!-- Check exactly ONE. This is the Conventional Commit type for your TITLE; the LABEL
is separate and coarser: there are twelve title types and only five `type/*` labels.
Apply exactly one `type/*` label. -->

- [ ] `fix`

<!-- Label to apply: `type/bug`. -->

## Symptom

<!--
What is wrong, and what does the user see as a result?
-->

## Root cause

<!--
Why it happens. A fix that does not name the cause is a patch, not a fix.
-->

## Minimal reproduction

<!--
The smallest reliable reproduction, starting from a clean checkout. If it is not reliably
reproducible, say what makes it flaky.
-->

1. ...
2. ...
3. ...

## Expected vs actual

<!--
What you expected, and what happened instead.
-->

Expected: ...
Actual: ...

## Regression test

<!--
The test that fails before this change and passes after it. This is what proves the fix holds.
Also state how to verify the fix by hand if the automated check does not cover it.
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
