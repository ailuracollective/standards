# Tests

Use when the primary purpose is test coverage. If the pull request also changes runtime code to
make a test pass, it is a `fix` or a `feat`.

Say what the suite now guarantees that it did not before. Coverage that does not change a
guarantee is not worth the maintenance cost.

## Linked issue (required)

<!-- The linked issue MUST carry the `status/ready` label. Apply exactly one of these
closing keywords on its own line. `Refs #N` does NOT close the issue and does not satisfy
this requirement. Bot pull requests are exempt; see `skip-actors` in `policy.yml`. -->

Closes #

## Type (required)

<!-- Check exactly ONE. This is the Conventional Commit type for your TITLE; the LABEL
is separate and coarser: there are twelve title types and only five `type/*` labels.
Apply exactly one `type/*` label. -->

- [ ] `test`

<!-- `type/task` is the catch-all. The label family has five members and
     none describes this work, so this is the intended home. The label is
     deliberately coarser than the title type. -->

## Scope of this change

<!--
Which behavior is under test here, and why it is separated from the change that introduced it.
-->

## Now covered

<!--
The scenarios that are covered and were not before. Name the cases, not the files.
-->

## Existing coverage that moved

<!--
Any test you renamed, moved, merged, or deleted, and what happened to the coverage it carried.
Silent deletion of a test is indistinguishable from silent loss of coverage.
-->

## Deliberately uncovered

<!--
What you chose not to test, and why. This is the section that stops the next contributor from
re-litigating it.
-->

## Fixtures and mocks

<!--
How the test isolates its subject: fixtures, doubles, sandboxing, clock control. If a test
depends on ordering or shared state, say so here.
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
