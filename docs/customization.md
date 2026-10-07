# Customizing the standard

How an adopting repository records that it deviates from the core
standard, and what each level of deviation costs.

## The problem

Nothing records which differences between copies are intentional, so
these four cases look identical:

| What a repository did    | What it must also remember         | What goes wrong                              |
| ------------------------ | ---------------------------------- | -------------------------------------------- |
| added `area/auth`        | nothing                            | looks like drift forever                     |
| added `type/chore`       | edit `type-labels` in `policy.yml` | the second record is in no file anyone reads |
| recolored a core label   | the reason                         | invisible, and reverted by the next copy     |
| dropped `scope/security` | whether that was a decision        | cannot be told from an incomplete copy       |

## The answer: an opt-in delta file

`.github/standards.local.yml`, whose schema ships as
`.github/standards.local.example.yml`. It records what a repository
changed and why.

**It declares; it does not configure. No workflow reads it, including
the gate.** A value written there changes nothing; the gate reads the
repository's own `policy.yml`. Keep this sentence through every future
edit — the failure it prevents is silent.

## The four levels

| Level | Deviation                                                                     | Process                                      |
| ----- | ----------------------------------------------------------------------------- | -------------------------------------------- |
| 0     | none — an exact copy                                                          | nothing to declare                           |
| 1     | a label in a family the core does not use                                     | no approval                                  |
| 2     | a core label's `color`/`description`, or a gate input's value                 | declare it with a reason                     |
| 3     | dropping a core label, changing an input's set, changing the manifest's shape | issue here first; `issue:` records which one |

- Level 1 needs no approval because level 2 does not either; a policy
  with an approval step at the bottom is one nobody follows.
- Reserved are the core families — `type/`, `status/`, `scope/`,
  `meta/`, `release/`, `github_actions` — not a closed list of new
  ones.
- `type/` is frozen at five. A project-specific type is an existing
  `type/*` label plus an entry in `extensions`.
- `reason` is **required** wherever a deviation is recorded. It is what
  separates a decision from rot.

## What a checker must be able to answer

The checker belongs to another project; the schema is its public
interface. It must answer:

- Does every label named in a field resolve against the manifest?
- Is every difference from the core declared in this file?
- Is a remote label missing from the manifest, or a manifest label
  missing from the remote?
- Does every level-3 deviation carry the issue that approved it?

And it must **not** report a missing file, or a missing optional
field, as a defect. Absence means "no deviations" by assumption. A
checker that flags absence trains every repository to create an empty
file, which is indistinguishable from a customized one at a glance.
