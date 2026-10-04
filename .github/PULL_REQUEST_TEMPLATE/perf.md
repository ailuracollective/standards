# Performance

Use for a change whose purpose is measurable performance. A change that is merely cleaner is a
`refactor`, not a `perf`.

A performance claim without a measurement is an opinion. Give the number, the command that
produced it, and the threshold that would make this a regression.

## Linked issue (required)

<!-- The linked issue MUST carry the `status/ready` label. Apply exactly one of these
closing keywords on its own line. `Refs #N` does NOT close the issue and does not satisfy
this requirement. Bot pull requests are exempt; see `skip-actors` in `policy.yml`. -->

Closes #

## Type (required)

<!-- Check exactly ONE. This is the Conventional Commit type for your TITLE; the LABEL
is separate and coarser: there are twelve title types and only five `type/*` labels.
Apply exactly one `type/*` label. -->

- [ ] `perf`

<!-- `type/task` is the catch-all. The label family has five members and
     none describes this work, so this is the intended home. The label is
     deliberately coarser than the title type. -->

## Measurements (required)

<!--
Before and after, with units. Give the benchmark output, not a summary of it. If the improvement
is within noise, say so and close the pull request.
-->

## Measurement command

<!--
The exact command or benchmark that produces the number above, reproducible from a clean
checkout.
-->

```

# exact benchmark or measurement command
```

## Environment

<!--
Hardware, OS, runtime version, and anything else that affects the number. A measurement without
an environment cannot be compared.
-->

## Regression threshold

<!--
What CI should assert, and what the budget is. If no threshold is being enforced, say so.
-->

## What was made cheaper

<!--
Which operation got faster, and why the change achieves it.
-->

## Behavior is unchanged

<!--
State explicitly that observable behavior is identical. A `perf` change that alters behavior is
a `feat` or a `breaking-change`.
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
