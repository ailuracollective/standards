# Style

Use for formatting-only changes produced by a formatter. If a human chose the formatting, it is
a `refactor`.

Formatting changes are unreviewable line by line once the diff is large. State how the change
was produced and how it was verified.

## Linked issue (required)

<!-- The issue must carry `status/ready`. Use a closing keyword on its own line; `Refs #N` does not close it. -->

Closes #

## Type (required)

<!-- Check one. The title type and the label differ: twelve title types, five `type/*` labels. -->

- [ ] `style`

<!-- `type/task` is the catch-all label for this type. -->

## Scope of reformatting

<!-- Which files or directories were reformatted, and the approximate size of the diff. -->

## Tool and configuration

<!-- The formatter, its version and its configuration. -->

## Proof of no behavior change

<!-- How you know the reformatting is inert, e.g. type checker and tests. -->

## Diff size and review strategy

<!-- The line count, and how a reviewer should read it — by config change or by trusting the formatter. -->

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
