# Feature

Use for new user-facing capability. A change that alters or removes existing behavior is NOT a
feature — use `breaking-change` instead.

Describe the problem and the outcome. A request that already specifies a solution tends to be
closed faster than one that states the need clearly.

## Linked issue (required)

<!-- The linked issue MUST carry the `status/ready` label. Apply exactly one of these
closing keywords on its own line. `Refs #N` does NOT close the issue and does not satisfy
this requirement. Bot pull requests are exempt; see `skip-actors` in `policy.yml`. -->

Closes #

## Type (required)

<!-- Check exactly ONE. This is the Conventional Commit type for your TITLE; the LABEL
is separate and coarser: there are twelve title types and only five `type/*` labels.
Apply exactly one `type/*` label. -->

- [ ] `feat`

<!-- Label to apply: `type/feature`. -->

## User-facing outcome

<!--
What can a user do now that they could not do before? State it as a capability, not as an
implementation.
-->

## What is new

<!--
The new surface: exports, components, directives, CLI flags, configuration keys, or endpoints.
Link the files that define them.
-->

| Surface | Location | Purpose |
| --- | --- | --- |
| `path/to/file` | exported symbol, component, flag | What it is for |

## How to try it

<!--
Give the reviewer a runnable path. Prefer a snippet they can paste and run. If no snippet is
possible, spell out the exact manual steps, including the command to run and what they should
observe.
-->

```
// Runnable snippet, or the concrete manual path below
```

## Compatibility impact

<!--
State explicitly whether existing code keeps working unchanged. Name any new opt-in flag,
default, or deprecation. If existing behavior changes, this belongs in `breaking-change`
instead.
-->

- Backward compatible: yes / no
- New opt-in behavior: <!-- describe the flag or config key, or "none" -->
- Deprecations introduced: <!-- describe, or "none" -->

## Screenshots or demo

<!--
Required when the change is visual — components, styling, rendered output. Paste before and
after, or link a recording. Write "Not visual" when it is not.
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
