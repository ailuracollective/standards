# AGENTS.md — instructions for agents working in this repository

> **This file is a template. It is not valid as an instruction set.**
>
> Replace every `TODO` below with something true of the repository that adopts
> this file. **An incomplete `AGENTS.md` must not be treated as the complete
> source of repository instructions** — an agent that finds one has to assume the
> gaps are the whole truth.
>
> Delete this banner and every `TODO:` marker together, or do not copy the file.
> Everything outside them is a contract and survives completion unchanged:
> § Organization standards and § Completion requirements are true of every
> adopting repository and are not yours to rewrite.

TODO: one line saying what this repository is and who reads this file.

---

## Organization standards

**Mandatory. Read it before anything else in this file.**

The organisation's conventions live in
[.agents/organization-conventions.md](.agents/organization-conventions.md), not
in this file. The link is mandatory and applies to every repository in the
organisation. Do not paste them here or restate them from memory — if a rule is
not in that file, it is not an organisation rule.

If it is not there, search the whole repository before concluding it is absent;
use it where you find it and record the path in § Additional references. If it
is not in the repository at all, stop and say so — do not reconstruct it.

Organisation standards apply here unless this repository documents a specific
exception, in § Repository-specific conventions, carrying the reason it was
taken. An exception nobody wrote down is not an exception.

---

## Defaults

The repository ships with the standard and its gate. Link them, do not restate
them:

- [.agents/organization-conventions.md](.agents/organization-conventions.md) — mandatory.
- [.github/workflows/policy.yml](.github/workflows/policy.yml) — the gate; complete and intact.
- [.github/workflows/ci.yml](.github/workflows/ci.yml) — skeleton; no checks until the stack fills it.
- [.github/workflows/release.yml](.github/workflows/release.yml) — skeleton; a placeholder step until replaced.
- [.github/ISSUE_STANDARD.md](.github/ISSUE_STANDARD.md),
  [.github/ISSUE_TEMPLATE/](.github/ISSUE_TEMPLATE/),
  [.github/PULL_REQUEST_TEMPLATE/](.github/PULL_REQUEST_TEMPLATE/),
  [.github/labels.yml](.github/labels.yml),
  [.github/CODEOWNERS](.github/CODEOWNERS) — the standard artifacts.

No language or toolchain is fixed; the stack that completes `ci.yml` and
`release.yml` is this repository's choice.

## Repository scope

TODO: what this file covers — the directories that are part of the repository and
any an agent must not touch. Agents read the nearest `AGENTS.md` above the file
they are editing; say so if a subdirectory has one.

## Repository context

TODO: what this project is for, in a paragraph. Then its shape: the stack it
chose (or that none is fixed), the entry points, which directory holds which
part, and anything else an agent would otherwise have to infer from the tree.

## Repository-specific conventions

TODO: the house rules for this repository, where they differ from the organisation
standards. Record every departure as `<the rule>` — we do `<what we do instead>`
because `<reason>`; a rule that matches the organisation standards does not belong
here.

## Development instructions

TODO: how to get from a fresh clone to a running project — install, generate,
build, run, with the exact commands. Until a stack is chosen there is nothing to
install or run.

## Testing and validation

TODO: the checks this repository actually runs, as copy-pasteable commands, and
what a failure looks like. They must be this repository's real commands.

## Git and pull requests

TODO: branch naming, the commit-message convention, and what a pull request must
carry before it merges — title format, required sections, the label to apply, and
who reviews.

## Documentation

TODO: where the documentation lives, which parts are expected to change with the
code, and what "documented" means here.

## Additional references

TODO: files an agent should read before working, and why each one matters. If the
organisation conventions were found somewhere other than `.agents/`, record the
path here and correct the link in § Organization standards.

## Completion requirements

A repository's `AGENTS.md` is **valid** when every line below holds. This is the
baseline contract, not a placeholder: it is not deleted when the file is
completed.

- [ ] No `TODO` marker remains anywhere in the file.
- [ ] The organisation conventions reference resolves — either
      `.agents/organization-conventions.md` exists, or the path it was found at
      is recorded in § Additional references.
- [ ] Every file this document links to exists in this repository, at the path
      given.
- [ ] Every section above says something true of this repository, and nothing
      still says something that was only true of the template.
- [ ] Every departure from the organisation standards appears in
      § Repository-specific conventions with a reason.
- [ ] The commands in § Development instructions and § Testing and validation
      run in this repository exactly as written.

Check them by hand:

```sh
# 1. no unresolved placeholders
grep -n 'TODO' AGENTS.md                                    # expect no output

# 2. the organisation reference resolves, from any directory
git ls-files --full-name | grep -E '(^|/)organization-conventions\.md$'

# 3. every linked path exists
grep -oE '\]\([^)]+\)' AGENTS.md | tr -d ']()' | while read -r p; do
  [ -e "${p%%#*}" ] || echo "MISSING: $p"
done
```

TODO: add this repository's own definition of done here, if it has one that
belongs in this file.
