# Style

Use for formatting-only changes produced by a formatter. If a human chose the formatting, it is
a `refactor`.

Formatting changes are unreviewable line by line once the diff is large. State how the change
was produced and how it was verified.

## Linked issue (required)

<!-- The linked issue MUST carry the `status/ready` label. Apply exactly one of these
closing keywords on its own line. `Refs #N` does NOT close the issue and does not satisfy
this requirement. Bot pull requests are exempt; see `skip-actors` in `policy.yml`. -->

Closes #

## Type (required)

<!-- Check exactly ONE. This is the Conventional Commit type for your TITLE; the LABEL
is separate and coarser: there are twelve title types and only five `type/*` labels.
Apply exactly one `type/*` label. -->

- [ ] `style`

<!-- `type/task` is the catch-all. The label family has five members and
     none describes this work, so this is the intended home. The label is
     deliberately coarser than the title type. -->

## Scope of reformatting

<!--
Which files or directories were reformatted, and the approximate size of the diff.
-->

## Tool and configuration

<!--
The formatter, its version, and the configuration that produced this. A formatting change with
no recorded tool cannot be reproduced.
-->

## Proof of no behavior change

<!--
How you established the reformatting is inert. For most languages this is the type checker plus
the test suite; name them.
-->

## Diff size and review strategy

<!--
The line count, and how a reviewer should read it — by config change or by trusting the
formatter.
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
