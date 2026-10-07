# AGENTS.md — instructions for agents working in this repository

> ## This file is a template. It is not valid as an instruction set.
>
> Every `TODO` below must be replaced with something true of the repository that
> adopts this file. **An incomplete `AGENTS.md` must not be treated as the
> complete source of repository instructions** — an agent that finds one has to
> assume the gaps are the whole truth.
>
> Delete this banner and every `TODO:` marker together, or do not copy the file.
> Everything outside them is a contract and survives completion unchanged:
> § Organization standards and § Completion requirements are true of every
> adopting repository and are not yours to rewrite.

TODO: one line saying what this repository is and who reads this file.

---

## Organization standards

**Mandatory. Read it before anything else in this file.**

The organisation's conventions are not in this file. They live in
[.agents/organization-conventions.md](.agents/organization-conventions.md),
which is mandatory, and they apply to every repository in the organisation.

They are a link rather than a copy on purpose. A copy is N repositories to fix
when the organisation decides something, and nothing detects the N; a link is one
line to change. Do not paste organisation conventions into this file, and do not
restate them from memory — if a rule is not in that file, it is not an
organisation rule.

### Locating it

The path above is **relative to the repository root**, not to wherever you happen
to be working.

1. Read `.agents/organization-conventions.md`.
2. **If it is not there, search the whole repository.** Do not conclude it is
   absent because the directory you are standing in does not contain it. An agent
   scoped to `packages/api/` still has to find a file that lives at
   `docs/organization-conventions.md`.

   ```sh
   # from any directory inside the repository; --full-name makes the paths
   # root-relative, which is the entire point
   git ls-files --full-name | grep -E '(^|/)organization-conventions\.md$'

   # same, and it also finds the file if it is untracked
   find "$(git rev-parse --show-toplevel)" -name 'organization-conventions.md' \
     -not -path '*/.git/*'
   ```

   `find .` and a bare `cat .agents/...` are both wrong here for the same
   reason: they resolve against the current working directory. An agent that has
   drifted into a subdirectory reports "this repository has no organisation
   standards" about a repository that has them, and that is the report that
   leads to the mistake below.
3. **If you find it somewhere else, use it**, and record the path you found in
   § Additional references so the next agent does not repeat the search.
4. **If it is not in the repository at all, stop and say so.** Do not infer it,
   do not reconstruct it, do not proceed on a plausible guess, and do not create
   the file.

   A reconstructed organisation standard is worse than a missing one. It is
   indistinguishable from a real one, every later agent treats it as
   authoritative, and nothing will ever correct it — the failure is silent and
   permanent. Reporting the missing reference is a short conversation and it is
   the honest answer; inventing the file is a quiet lie that outlives the session.

### Exceptions

Organisation standards apply here unless this repository documents a specific
exception, in § Repository-specific conventions, carrying the reason it was
taken.

An exception nobody wrote down is not an exception. If you are about to work
against an organisation standard and this file says nothing permitting it, you
are working against the standard.

---

## Repository scope

TODO: what this file covers. Name the directories an agent should treat as part
of the repository and any it must not touch — vendored trees, generated output,
fixtures, submodules.

Agents read the nearest `AGENTS.md` above the file they are editing, so a
subdirectory may carry its own. Say so if it does, and say which one wins where
they overlap: the deeper file, for the paths it covers.

TODO: —

## Repository context

TODO: what this project is for, in a paragraph. Then its shape: the language and
framework, the entry points, which directory holds which part, and anything an
agent would otherwise have to infer by reading the tree.

TODO: —

## Repository-specific conventions

TODO: the house rules for this repository — naming, file layout, error handling,
style — where they differ from the organisation standards. A rule that matches
the organisation standards does not belong in this file; it is already in the
linked file, and repeating it here is the copy this template exists to prevent.

**Every departure from the organisation standards is recorded in this section**,
in this shape:

> - `<the rule>` — we do `<what we do instead>` because `<reason>`.

An exception without a reason is indistinguishable from drift, and recognising
the difference is the only reason this section exists. If you cannot write the
reason, that is the answer.

TODO: —

## Development instructions

TODO: how to get from a fresh clone to a running project. Install, generate,
build, run. Name the commands exactly, including the package manager and the
runtime version, and say what has to be running before anything else works.

TODO: —

## Testing and validation

TODO: the checks this repository actually runs, as copy-pasteable commands, and
what a failure looks like.

These must be this repository's real commands. A `TODO` here is not a harmless
placeholder: it is the section an agent trusts most, and a plausible command
that does not exist is how an agent reports a verification it never ran.

TODO: —

## Git and pull requests

TODO: branch naming, the commit-message convention, and what a pull request must
carry before it merges — title format, required sections, the label to apply,
and who reviews.

TODO: —

## Documentation

TODO: where the documentation lives, which parts are expected to change with the
code, and what "documented" means here: a comment, a docstring, a page, a
changelog entry.

TODO: —

## Additional references

TODO: files an agent should read before working, and why each one matters.

The organisation conventions are linked from § Organization standards. If you
found that file somewhere other than `.agents/`, record the real path here, and
correct the link above to match — the link must resolve.

TODO: —

## Completion requirements

A repository's `AGENTS.md` is **valid** when every line below holds. This is
the baseline contract, not a placeholder: it is not deleted when the file is
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
python3 - <<'PY'
import os, re, sys
missing = [t for t in re.findall(r'\]\(([^)#\s]+)', open('AGENTS.md').read())
           if '://' not in t and not os.path.exists(t.split('#')[0])]
print('\n'.join(f'MISSING: {m}' for m in missing) or 'every referenced file exists')
sys.exit(1 if missing else 0)
PY
```

TODO: add this repository's own definition of done here, if it has one that
belongs in this file.
