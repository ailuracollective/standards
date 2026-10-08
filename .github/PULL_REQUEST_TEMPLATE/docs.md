# Documentation

Use for changes to documentation only. If code changes too, this is the type of the code change.

Documentation is read by someone who cannot see the implementation. Write for that reader.

## Linked issue (required)

<!-- The issue must carry `status/ready`. Use a closing keyword on its own line; `Refs #N` does not close it. -->

Closes #

## Type (required)

<!-- Check one. The title type and the label differ: twelve title types, five `type/*` labels. -->

- [ ] `docs`

<!-- Label to apply: `type/documentation`. -->

## Documentation changed

<!-- Which documents, and what changed in each. -->

## Preview links

<!-- Link the rendered result, or say it is not rendered. -->

## Why the previous text was wrong

<!-- What was wrong, or "new documentation". -->

## Anything else that referenced the old text

<!-- Links, indexes or READMEs that pointed at what you changed. -->

## Read-through check

<!-- Confirm the result reads correctly end to end, not only in the diff. -->

## Link and anchor verification

<!-- Check that every link and anchor you touched resolves. -->

## Runtime code untouched

<!-- Confirm no runtime code changed. -->

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
