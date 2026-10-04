# Breaking change

Use for a change that removes or alters existing public behavior in a way a consumer can
observe. A breaking change is not a `feat`: `feat` is new capability that leaves what exists
working.

State the old contract, the new one, and exactly what a consumer has to change. A breaking
change is a permanent obligation on every downstream reader, so the migration path matters more
than the diff.

## Linked issue (required)

<!-- The linked issue MUST carry the `status/ready` label. Apply exactly one of these
closing keywords on its own line. `Refs #N` does NOT close the issue and does not satisfy
this requirement. Bot pull requests are exempt; see `skip-actors` in `policy.yml`. -->

Closes #

## Type (required)

<!-- Check exactly ONE. This is the Conventional Commit type for your TITLE; the LABEL
is separate and coarser: there are twelve title types and only five `type/*` labels.
Apply exactly one `type/*` label. -->

- [ ] `breaking-change`

<!-- A breaking change has no `type/*` label of its own: the family has
     exactly five members and none of them marks a break. Apply the label of the
     underlying change instead — for example `type/bug` when reverting broken
     behavior, or `type/task` when the break is incidental. -->

## What breaks and for whom

<!--
Name the API, option, or behavior that changes, and who is affected. Do not write "the API" —
write the export, flag, or endpoint.
-->

## Before / after

<!--
Show the old contract and the new one side by side, concretely. This is what a consumer compares
against their own code.
-->

## Migration

<!--
The exact steps a consumer takes. Include code. If the migration is mechanical, say so; if it
needs judgement, say that too.
-->

## Codemod feasibility

<!--
Whether this can be automated. If a codemod is viable, link or open the issue for it. "Not
feasible" is a valid answer; silence is not.
-->

## What was decided

<!--
Why this shape and not a compatible alternative. This is the section future maintainers read
when someone asks why the API is shaped this way.
-->

## Affected version range

<!--
Which versions carry the old behavior, and which release removes it.
-->

## Deprecation plan

<!--
If the old behavior is retained behind a flag, give the timeline and the removal version. If it
is removed outright, write "removed outright".
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
