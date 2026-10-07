# Performance

Use for a change whose purpose is measurable performance. A change that is merely cleaner is a
`refactor`, not a `perf`.

A performance claim without a measurement is an opinion. Give the number, the command that
produced it, and the threshold that would make this a regression.

## Linked issue (required)

<!-- The issue must carry `status/ready`. Use a closing keyword on its own line; `Refs #N` does not close it. -->

Closes #

## Type (required)

<!-- Check one. The title type and the label differ: twelve title types, five `type/*` labels. -->

- [ ] `perf`

<!-- `type/task` is the catch-all label for this type. -->

## Measurements (required)

<!-- Before and after, with units. Paste the benchmark output. -->

## Measurement command

<!-- The exact command or benchmark that produces the number above, reproducible from a clean checkout. -->

```text

# exact benchmark or measurement command
```

## Environment

<!-- Hardware, OS, runtime version and anything else affecting the number. -->

## Regression threshold

<!-- What CI should assert, and what the budget is. If no threshold is being enforced, say so. -->

## What was made cheaper

<!-- Which operation got faster, and why the change achieves it. -->

## Behavior is unchanged

<!-- State that observable behavior is identical; otherwise it is a `feat` or `breaking-change`. -->

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
