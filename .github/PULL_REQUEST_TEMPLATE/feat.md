# Feature

Use for new user-facing capability. A change that alters or removes existing behavior is NOT a
feature — use `breaking-change` instead.

Describe the problem and the outcome. A request that already specifies a solution tends to be
closed faster than one that states the need clearly.

## Linked issue (required)

<!-- The issue must carry `status/ready`. Use a closing keyword on its own line; `Refs #N` does not close it. -->

Closes #

## Type (required)

<!-- Check one. The title type and the label differ: twelve title types, five `type/*` labels. -->

- [ ] `feat`

<!-- Label to apply: `type/feature`. -->

## User-facing outcome

<!-- What a user can do now that they could not before, as a capability. -->

## What is new

<!-- The new surface (exports, flags, config keys, endpoints), linking its definitions. -->

| Surface | Location | Purpose |
| --- | --- | --- |
| `path/to/file` | exported symbol, component, flag | What it is for |

## How to try it

<!-- A runnable path for the reviewer: a snippet, or exact commands and expected output. -->

```text
// Runnable snippet, or the concrete manual path below
```

## Compatibility impact

<!-- Whether existing code keeps working, and any new flag, default or deprecation. -->

- Backward compatible: yes / no
- New opt-in behavior: <!-- describe the flag or config key, or "none" -->
- Deprecations introduced: <!-- describe, or "none" -->

## Screenshots or demo

<!-- Required for visual changes: before and after, or a recording. Otherwise "Not visual". -->

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
