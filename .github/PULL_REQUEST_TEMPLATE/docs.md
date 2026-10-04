# Documentation

Use for changes to documentation only. If code changes too, this is the type of the code change.

Documentation is read by someone who cannot see the implementation. Write for that reader.

## Linked issue (required)

<!-- The linked issue MUST carry the `status/ready` label. Apply exactly one of these
closing keywords on its own line. `Refs #N` does NOT close the issue and does not satisfy
this requirement. Bot pull requests are exempt; see `skip-actors` in `policy.yml`. -->

Closes #

## Type (required)

<!-- Check exactly ONE. This is the Conventional Commit type for your TITLE; the LABEL
is separate and coarser: there are twelve title types and only five `type/*` labels.
Apply exactly one `type/*` label. -->

- [ ] `docs`

<!-- Label to apply: `type/documentation`. -->

## Documentation changed

<!--
Which documents, and what changed in each.
-->

## Preview links

<!--
If the documentation is rendered somewhere — a docs site, a preview deployment, a notebook —
link the rendered result. If it is not rendered anywhere, say so.
-->

## Why the previous text was wrong

<!--
If this corrects existing documentation, say what was wrong. If it is genuinely new, say "new
documentation".
-->

## Anything else that referenced the old text

<!--
Links, indexes, READMEs, or code comments that pointed at what you changed. Search for them; do
not assume there are none.
-->

## Read-through check

<!--
Confirm the result reads correctly end to end, not only in the diff.
-->

## Link and anchor verification

<!--
Verify every link and heading anchor you touched resolves. Broken anchors are the most common
defect in a documentation-only change.
-->

## Runtime code untouched

<!--
Confirm no runtime code changed. A documentation pull request that ships code cannot be reviewed
as documentation.
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
