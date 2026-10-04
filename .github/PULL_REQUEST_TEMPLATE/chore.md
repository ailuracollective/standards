# Chore

Use for technical maintenance with no intended functional change. If the change is user-visible
it is not a chore.

State the preservation guarantees explicitly. "No functional change" is a claim that has to be
defended, not asserted.

## Linked issue (required)

<!-- The linked issue MUST carry the `status/ready` label. Apply exactly one of these
closing keywords on its own line. `Refs #N` does NOT close the issue and does not satisfy
this requirement. Bot pull requests are exempt; see `skip-actors` in `policy.yml`. -->

Closes #

## Type (required)

<!-- Check exactly ONE. This is the Conventional Commit type for your TITLE; the LABEL
is separate and coarser: there are twelve title types and only five `type/*` labels.
Apply exactly one `type/*` label. -->

- [ ] `chore`

<!-- `type/task` is the catch-all. The label family has five members and
     none describes this work, so this is the intended home. The label is
     deliberately coarser than the title type. -->

## What is being changed

<!--
The cleanup: what is removed, simplified, or maintained.
-->

## Why now

<!--
What makes this worth doing now rather than later.
-->

## Behavior preserved

<!--
State explicitly that observable behavior is unchanged, and how you know. If any behavior does
change, this is not a chore.
-->

## Public API preserved

<!--
State explicitly whether exported signatures change. If none do, say "no public API change".
-->

## Risk and rollback

<!--
What could go wrong, and how to revert it if it does.
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
