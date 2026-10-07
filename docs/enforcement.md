# Enforcement

CODEOWNERS, branch protection, and how to tell whether a rule is
actually enforced — for this repository or any other. Configured
and enforced are different questions, and the second is per
repository, per branch, and changes without a file being edited.

## CODEOWNERS

`.github/CODEOWNERS` assigns every path to `@SiddharthaGF`, the only
collaborator with write access. The rules all resolve to that account
today; the file is written so a second owner is a one-line change per
group. The **last** matching pattern wins and replaces earlier owners —
rules are not cumulative.

The catch-all (`*`) is load-bearing: it is the only owner of
`README.md`, `CONTRIBUTING.md`, `LICENSE`, `CHANGELOG.md`, `policy.yml`
and the lint files; an unowned file skips the code-owner gate. Do not
remove it, and do not add an owner to one rule expecting it to be
additive: `.github/labels.yml @alice` *replaces* `@SiddharthaGF` on
that path.

GitHub silently skips any line it cannot parse and any owner without
write access. CODEOWNERS only binds through branch protection or
rulesets.

## This repository's protection

`main` carries:

| Setting                                    | Value     |
| ------------------------------------------ | --------- |
| `require_code_owner_reviews`               | true      |
| `required_approving_review_count`          | 1         |
| `dismiss_stale_reviews`                    | true      |
| `require_last_push_approval`               | true      |
| `required_conversation_resolution`         | true      |
| `allow_force_pushes` / `allow_deletions`   | false     |
| `enforce_admins`                           | **false** |

**`enforce_admins: false` governs every other row**: protection does
not apply to admins, so the single admin can bypass all of it,
force-push protection included. It is off because of a deadlock, not a
preference — the only code owner is the only writer, and GitHub
forbids approving your own pull request, so enforcing it would freeze
the repository. For the same reason the policy job is not a required
status check.

API traps, both silent: the field is `require_code_owner_reviews`
(**plural**; the singular returns 200 and does nothing), and the `PUT`
must send `required_status_checks` and `restrictions` explicitly as
`null` or nothing applies. Always read back:

```sh
gh api /repos/ailuracollective/standards/branches/main/protection \
  --jq '.required_pull_request_reviews.require_code_owner_reviews'   # must be true
```

**Enforcement is configured, not proven.** A test pull request shows
`REVIEW_REQUIRED`/`BLOCKED`, which a plain one-approval rule would also
show. Proving it, and making it a guarantee, takes one step: grant
write access to a second person, then set `enforce_admins` to true.

Until then: CODEOWNERS owns itself, so a pull request cannot remove
the review it needs; and nobody pushes straight to `main` even though
they could — the review is the point.

## How to tell, for any repository

Check **both** APIs:

```sh
# classic branch protection — 404 means "no classic protection", NOT "unprotected"
gh api /repos/OWNER/REPO/branches/BRANCH/protection --jq '.required_status_checks'

# rulesets — a separate API, and the one people forget
gh api /repos/OWNER/REPO/rulesets --jq '.[] | "\(.id) \(.name) \(.enforcement)"'
for id in $(gh api /repos/OWNER/REPO/rulesets --jq '.[].id'); do
  gh api /repos/OWNER/REPO/rulesets/$id --jq \
    '.rules[] | select(.type=="required_status_checks") | .parameters.required_status_checks[].context'
done

# what the workflows actually report
gh pr view N --repo OWNER/REPO --json statusCheckRollup \
  --jq '.statusCheckRollup[].name' | sort -u
```

Reading a 404 from the first as "unprotected" when the branch moved to
a ruleset has already produced one confident, wrong claim here. Then
compare required contexts with reported ones:

| Required contexts                      | Meaning                                                          |
| -------------------------------------- | ---------------------------------------------------------------- |
| the policy job is **not** among them   | it annotates and is ignored                                      |
| it is there under a **different name** | unmergeable for anyone who cannot bypass protection              |
| a context **no workflow reports**      | the same, and invisible until someone without admin rights tries |

A required context is a literal string: `Branch name and PR title` does
not match a job named `Branch name`. Bypass permission hides both
failures until it is removed. Never describe a rule as binding without
having read these for that repository and branch.
