# Pull Request

<!--
Catch-all for any type that has no dedicated template. If a template exists for your
type under `.github/PULL_REQUEST_TEMPLATE/`, use that one instead — the body-structure
gate reads the headings from the template that matches your title's type, so using the
wrong template means writing the wrong headings.

Types without a dedicated template here: see the directory listing. `style` and
`revert` are covered; `build`, `chore`, and `ci` are covered. If your type is not in
this directory, no per-type structure is enforced for it.
-->

<!-- REPO OWNER: replace the Test plan block below with this repository's checks. -->

## Linked issue (required)

<!-- The linked issue MUST carry the `status/ready` label. Apply exactly one of these
closing keywords on its own line. `Refs #N` does NOT close the issue and does not satisfy
this requirement. Bot pull requests are exempt; see `skip-actors` in `policy.yml`. -->

Closes #

## Type (required)

<!-- Check exactly ONE. This is the Conventional Commit type for your TITLE; the LABEL
is separate and coarser: there are twelve title types and only five `type/*` labels.
Apply exactly one `type/*` label. -->

- [ ] `<type>`
<!-- Check exactly ONE. The twelve allowed types are `breaking-change`, `build`, `chore`, `ci`,
`docs`, `feat`, `fix`, `perf`, `refactor`, `revert`, `style`, and `test`. The LABEL is separate
and coarser: five `type/*` labels exist. Apply exactly one. -->

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
