# Contributing

## Open an issue first

Every change to the standard starts as an issue. The files here are copied by hand
into other repositories, so a change that lands here stays unmirrored everywhere else
until someone remembers it. The issue is where that cross-repository impact gets
written down, before the change exists.

Say what has to happen outside this repository. Adding one label to
`.github/labels.yml` is four changes, none of them automatic: the manifest here, the
manifest in each adopting repository, the `type-labels` input of each `policy.yml`,
and the label on each remote.

File issues with the forms in `.github/ISSUE_TEMPLATE/` (blank issues are disabled).
If none of the seven fits, that is a finding about the templates: open it as a
`docs:` or `improvement:` issue.

**A need that belongs to one repository is not a change to the standard.** An extra
label, a house colour, a stricter title length or a dropped scope goes in that
repository's own `standards.local.yml`. Promoting it into the core is a separate
decision, taken in an issue once several repositories want the same thing. See
docs/customization.md.

## Branches

`main` is the only branch, and it is protected. Name branches
`<github-username>/<type>/<description>`, lowercased, where `<type>` is one of the
eleven types `policy.yml` accepts: `build`, `chore`, `ci`, `docs`, `feat`, `fix`,
`perf`, `refactor`, `revert`, `style`, `test`. `breaking-change` is not a branch
type; use the type of the underlying change.

```bash
OWNER=$(gh api user -q .login | tr '[:upper:]' '[:lower:]')
git checkout -b "$OWNER/fix/template-label-gap" main
```

## Commits and pull request titles

Use Conventional Commits. The type is not decoration: the title check reads it, and
the body check compares the body against the template named for it — `fix:` is
checked against `.github/PULL_REQUEST_TEMPLATE/fix.md`.

- `fix: name the label each issue template actually applies`
- `docs: state that a manifest is a record, not a mechanism`

To start from the right form, open the pull request with `?template=<type>.md` in the
URL. Squash-merge, and use the pull request title as the commit message.

## Before opening a pull request

`policy.yml` checks five things: the branch name, the linked issue, the type label,
the title, and the body's sections. Nothing else is checked for you. Run the linters. Linters only look at one file at a
time, so passing them does not mean the change is verified.

At minimum, confirm `CODEOWNERS` still works. GitHub skips any line it cannot parse,
and silently drops any owner without write access:

```sh
gh api repos/ailuracollective/standards/codeowners/errors --jq '.errors'   # expect []
gh api /repos/ailuracollective/standards/collaborators --jq '.[] | select(.permissions.push) | .login'
```

If you edit a pull request template, say which ones in the pull request, and confirm
the four common headings are unchanged. They are identical across all thirteen files,
so any difference makes the gate demand different bodies in different repositories.

## What a finished change looks like

Merging here is the midpoint. A change is finished when:

1. Every adopting repository has the same content. Check, do not assume:
   `gh api /repos/ailuracollective/REPO/contents/.github/labels.yml`
2. Every `policy.yml` agrees, if labels or types changed.
3. Every changed label has been applied to each remote with
   `gh label create --force`. Editing `labels.yml` changes no remote.

Steps 1–3 cannot be verified from here, because this repository does not track who
adopted it (see *Sync model* in docs/architecture.md). Finishing a change means
asking.

## Review

`main` requires one approving review from a code owner, and `.github/CODEOWNERS`
gives every path to `@SiddharthaGF` — the only account with write access. So
`enforce_admins` is off and that person can merge their own work. Open a pull request
anyway: the review is what makes this repository worth trusting.

Making the requirement binding takes one step outside the code: grant write access to
a second person, then turn `enforce_admins` on.
