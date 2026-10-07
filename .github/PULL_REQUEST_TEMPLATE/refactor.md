# Refactor

Use for restructuring that leaves observable behavior identical. If behavior changes, this is a
`feat`, a `fix`, or a `breaking-change`.

The burden of proof is on equivalence. State what is equivalent, and how that was established.

## Linked issue (required)

<!-- The issue must carry `status/ready`. Use a closing keyword on its own line; `Refs #N` does not close it. -->

Closes #

## Type (required)

<!-- Check one. The title type and the label differ: twelve title types, five `type/*` labels. -->

- [ ] `refactor`

<!-- `type/task` is the catch-all label for this type. -->

## Structure: before and after

<!-- The shape of the code before and after. A diagram or an outline is enough. -->

```text
// before

// after
```

## Behavioral equivalence

<!-- How you know behavior is unchanged: tests passing before and after, or why none are needed. -->

## Public API and observable behavior

<!-- State explicitly whether any exported signature changes. If none does, say "no public API change". -->

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
