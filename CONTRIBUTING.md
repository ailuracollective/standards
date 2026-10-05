# Contributing

## Open an issue first

Every change to the standard starts as an issue. This is the one repository in the
organisation where that matters most rather than least, because the artifacts here
are copied into other repositories by hand: a change lands here, then sits
unmirrored everywhere until somebody remembers. An issue is where the
cross-repository impact gets written down, before the change exists.

Say what has to happen outside this repository, without naming which repository
that is until you are sure. A change to `.github/labels.yml` that adds one label is
not one change: it is the manifest here, the manifest in each adopting repository,
the `type-labels` input of each `policy.yml`, and the label on each remote. All of
it is manual and none of it is enforced by anything.

Issues are filed with the forms in `.github/ISSUE_TEMPLATE/`, which is this
repository consuming its own standard. Use them. If one of the seven does not fit
what you need, that is a finding about the template: open it as a `docs:` or
`improvement:` issue rather than falling back to a blank issue, which
`config.yml` disables anyway.

## Branches

- `main` is the record. It is the only branch, and it is protected.
- Branch names are `<github-username>/<type>/<description>`, lowercased, where
  `<type>` is a Conventional Commit type. The twelve are `breaking-change`,
  `build`, `chore`, `ci`, `docs`, `feat`, `fix`, `perf`, `refactor`, `revert`,
  `style`, `test`.

  ```bash
  OWNER=$(gh api user -q .login | tr '[:upper:]' '[:lower:]')
  git checkout -b "$OWNER/fix/template-label-gap" main
  ```

The gate **does** check the shape of a branch name, in
`.github/workflows/policy.yml`. Keep it right for a second reason anyway: the
templates are keyed on the type segment, and GitHub selects the pull request form
from the branch name. A branch named `fix/thing` renders `fix.md`; one named
`wip/thing` renders the default, which asks for almost nothing.

## Commits

Conventional Commits. The type in the subject is not decoration: the title grammar
and the pull request template are both selected from it.

- `fix: name the label each issue template actually applies`
- `docs: state that a manifest is a record, not a mechanism`

Squash-merge, and take the squash commit message from the pull request title.

## Before opening a pull request

`.github/workflows/policy.yml` checks the five things that are cheap to check
mechanically: the branch name, the linked issue, the type label, the title, and the
body's sections. It cannot check the rest, so the block at the end of `AGENTS.md`
is still the whole verification story — it is the same block that has caught real
mistakes, and the only thing standing between a claim and a fact here. At minimum:

```sh
# every YAML file parses
python3 -c "import yaml,glob;[yaml.safe_load(open(f)) for f in glob.glob('.github/**/*.yml',recursive=True)]"

# CODEOWNERS parses and every owner it names can be asked to review
gh api repos/ailuracollective/standards/codeowners/errors --jq '.errors'   # expect []
gh api /repos/ailuracollective/standards/collaborators --jq '.[] | select(.permissions.push) | .login'
```

The second pair matters because both failure modes are silent. GitHub skips a
CODEOWNERS line it cannot parse, and drops an owner without explicit write access,
without warning either. An empty `errors` array is the only evidence the file is
doing anything.

If your change touches a pull request template, state in the pull request which of
the twelve you edited and that the four common headings are unchanged. They are
identical across all thirteen files on purpose; a divergence means a different
repository is being asked for a different body.

## What a finished change looks like

Merging here is the midpoint, not the end. A change is finished when:

1. Every adopting repository has the same content. Check it; do not assume:
   `gh api /repos/ailuracollective/REPO/contents/.github/labels.yml`
2. Every `policy.yml` agrees, if the change touched labels or types.
3. Any remote label that changed has actually been applied with `gh label create
   --force`. Editing `labels.yml` here changes no remote anywhere.
4. The `AGENTS.md` counts still match. They are quoted as exact numbers, so adding
   a file means updating the inventory rather than letting it rot.

Steps 1 to 3 cannot be verified from here. This repository does not track who
adopted it — see *Sync model* in `AGENTS.md` — so finishing a change means asking,
not looking something up.

## Review

`main` requires one approving review from a code owner, and
`.github/CODEOWNERS` gives every path to `@SiddharthaGF`. That is the only account
with write access, so `enforce_admins` is off and that one person can merge their
own work. Treat the review as the point anyway: open a pull request even though you
could push, because the review is the thing that makes this repository worth
trusting.

Turning the requirement real takes one step that is not a code change — grant write
access to a second person, then turn `enforce_admins` on.