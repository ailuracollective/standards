# Releases

How release-please cuts releases in this repository, and why the
release pull request is exempt from the policy gate.

## The flow

`release-please` runs on every push to `main`. When there is
anything releasable it opens **a pull request** with the version
bump and a generated changelog; merging it creates the tag and the
release. Nothing is published directly, so a release is a reviewed
change like any other.

`release.yml` sets `cancel-in-progress: false` on purpose: a new
push must wait for a release in flight, not interrupt it halfway.

## The configuration, key by key

`release-please-config.json`:

- **`release-type: simple`** — there is no package; the version lives
  only in `.release-please-manifest.json`.
- **`initial-version: 0.1.0`** — without it the first release is
  `1.0.0`, a compatibility claim nobody made.
- **`packages: { ".": … }`** — looks redundant, is not. The schema
  requires it, and `parseConfig` builds `repositoryConfig` from it,
  which `manifest.ts` dereferences on exactly this repository's path.
  Omitting it crashes on the first push, not at configuration time.
- **`label: release/pending`** and **`release-label: release/tagged`** —
  override release-please's defaults (`autorelease: pending`,
  `autorelease: tagged`). Those defaults are not in
  `.github/labels.yml`, and GitHub drops an unknown label silently; the
  release pull request and the tagged release carry the manifest's
  `release/*` labels instead.

## The release pull request is exempt by head ref

Its head ref is `release-please--branches--<branch>` — hardcoded in
`src/util/branch-name.ts`, not configurable — and it has no type
segment, no linked issue, no template body and no `type/*` label. It
cannot pass the gates, so `policy.yml` skips both pull request jobs
with:

```yaml
!startsWith(github.event.pull_request.head.ref, 'release-please--branches--')
```

Not `skip-actors`, which matches the login: the release account is the
one both tokens belong to, and it also posts every status comment — it
is not exclusively a machine identity. Exempting it would exempt
everything it ever opens. A head ref says what a pull request *is*; a
human's branch has a type segment by choice.

The cost: an exempt pull request has **no check and no status
comment**, so nothing records that the exemption was deliberate.

Making release-please satisfy the checks (`extra-label`, a static
`pull-request-footer` with a closing keyword and the headings) was
rejected: it would name the same issue in every release and carry
headings that exist only to be grepped — a green board without a
review.

## The automation tokens

Two secrets run the workflows, one per function. No secret value
lives in the repository; this file names them only.

| Secret                       | Where                         | Function                                                    |
| ---------------------------- | ----------------------------- | ----------------------------------------------------------- |
| `AILURA_PR_COMPLIANCE_TOKEN` | `policy.yml`, `comment-token` | posts and edits the status comment on every pull request    |
| `AILURA_RELEASE_TOKEN`       | `release.yml`, `token`        | opens the release PR; on merge, creates the tag and release |

### `AILURA_PR_COMPLIANCE_TOKEN` — the status comment

- **What it does:** posts and edits the sticky status comment that
  `ailuracollective/actions` keeps up to date on every pull request
  that is not a draft.
- **Where:** the `branch-validation` and `pull-request-policy` jobs of
  `.github/workflows/policy.yml`, as their `comment-token` input.
- **Who issues it:** a PAT of the **AiluraKitty** account. `comment-author:
  AiluraKitty` did not change, and the action verifies the identity with
  `gh api user` before writing; a token from any other account posts
  nothing.
- **Scope:** `pull-requests: write` on the token. The job permissions stay
  read-only — `pull-requests: read` on `pull-request-policy`, none on
  `branch-validation` — because the comment is written with the token, not
  with the job's grant.
- **If revoked or leaked:** status comments stop being updated. Releases
  keep working.

### `AILURA_RELEASE_TOKEN` — the releases

- **What it does:** release-please's `token`. Opens the release pull
  request; merging it creates the tag and the release.
- **Where:** `.github/workflows/release.yml`, as the action's `token`
  input.
- **Who issues it:** the account that signs the release commits.
  release-please has no author setting — GitHub attributes API commits to
  the calling token — so **the token is the author setting**; with
  `GITHUB_TOKEN` every release commit is `github-actions[bot]`'s.
- **Scope:** `contents: write`, `issues: write` and `pull-requests: write`
  (already declared in the job's `permissions`), plus write access to the
  repository to create tags.
- **If revoked or leaked:** releases stop: the pull request opens but
  fails at merge.

### `GITHUB_TOKEN` — the automatic one

Deliberately **not** used here for comments or releases: a
`github-actions[bot]` comment cannot be edited or deleted by anyone, and
release commits would be attributed to the bot. It is used for reads (the
action's default `github-token`) and by the `triage` job to apply
`status/needs-review` (`issues: write`).

### Why two, not one

With a single token, a leak or a revocation hit both functions at once:
revoking it stopped releases *and* silenced the comments. Separated, each
blast radius stays its own: the compliance token cannot create tags, and
the release token posts no comments.

### Rules that must not break

- Do not widen the job `permissions` to `pull-requests: write` to "make
  the comment work": that hands write access to the checking scripts,
  which only read.
- Do not go back to `GITHUB_TOKEN` for simplicity, or merge the two
  secrets into one: the split is what limits the damage.
- If `AILURA_PR_COMPLIANCE_TOKEN` changes account, `comment-author` must
  change with it; otherwise the action refuses to write.
- The names must exist in *Settings → Secrets and variables → Actions*;
  a missing secret fails the job without creating anything.
