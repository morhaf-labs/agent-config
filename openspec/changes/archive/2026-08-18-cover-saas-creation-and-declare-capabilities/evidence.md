## Selection review

The widened description is wording, and this package's testing philosophy is that a wording
assertion passes forever and proves nothing. Selection is therefore reviewed here rather than
asserted in a test, and this is the record of that review.

Description under review:

> Use when creating, adopting, auditing or changing repository automation for a Morhaf Labs
> project, including starting a new Morhaf Labs project from a described product idea before
> any repository exists, new repository setup, ...

| Phrasing | Should select | Why |
| --- | --- | --- |
| "I want to build a SaaS that does X" | yes | A described product idea, no repository yet. |
| "let's start a new project for X" | yes | Starting a project is the anchor phrase. |
| "turn this idea into a product I can charge for" | yes | Idea intent, and the profile decision is exactly what billing ownership turns on. |
| "create a repo for my idea" | yes | Already covered before this change, and still covered. |
| "set up CI for this repository" | yes | Unchanged from the original description. |
| "add a settings page to the dashboard" | no | Product work inside an existing project, not starting one. |
| "fix the failing test in checkout" | no | Neither creation nor automation. |
| "deploy the scheduler component" | no | Runtime work; `deploy-to-morhaf-vps` owns it, and its description is unchanged. |

The trigger is anchored to *starting* a project rather than to product or feature work, which
is the boundary the design names as the risk. The four required intents from the existing
structural test - creating, adopting, auditing, repository automation - are all still present,
so the widening added a case rather than displacing one.

`deploy-to-morhaf-vps` is untouched by this change: `git diff` reports no change under
`.apm/skills/deploy-to-morhaf-vps/`, and the creation fixture routes to the Cloudflare owner
with no VPS owner in the result, which is the dormancy claim held as a test rather than a
sentence.

## Release

| What | Value |
| --- | --- |
| Release | `v0.3.0` |
| Merge commit | `c5fc8a2` (squash of pull request #9) |
| Package version | 0.3.0, in `apm.yml` and all three `plugin.json` manifests |
| Assets | `agent-config-0.3.0.zip`, `agent-config-0.3.0.zip.sha256` |
| Bundle SHA-256 | `76e9a6982a430d7c160272e72e0d12179805bf1229378331b862c5c8c0ca4434` |
| `Release` on Blacksmith | Green on the tag, 23s. |

Tagged after the companion `founder-stack-v2` change landed on its main branch, which is the
ordering the plan required: the reference describes an initialization path, and tagging first
would have published a description of something that did not exist yet.

Squash merging is retained, for the reason the previous release recorded: this repository
publishes a *package*, not commit SHAs for others to pin.

### Verified after publication

Downloaded from the release rather than trusted from the build:

- The `.sha256` sidecar matches the downloaded bundle.
- `tests/verify_release.py` verifies 16 declared files, one more than v0.2.0 - the new
  reference.
- All 14 guidance files are byte-identical to the reviewed source tree.
- The published `plugin.json` carries 0.3.0.

Worth noting for the next reader: the archive is rooted at `agent-config-0.3.0/`, not at the
skill tree. A first pass at this verification compared paths without that prefix and reported
the new reference absent while simultaneously reporting every guidance file identical - two
results that cannot both be true, which is how the mistake surfaced. A check that can pass
vacuously is worth distrusting until it has been made to fail.

## Checks

Run locally on the branch, at package version 0.3.0.

| Check | Result |
| --- | --- |
| `python -m unittest discover -s tests` | 55 tests, 0 failures. Was 45 before this change. |
| `agentskills validate` | Valid, both skills. |
| `apm audit --ci --no-policy --no-fail-fast` | 10 of 10 checks pass. |
| `apm audit --file` over every guidance file | 14 files, 0 findings. |
| `apm pack --dry-run --marketplace none --verbose` | Exit 0. |
| `apm pack --archive` then `tests/verify_release.py` | `agent-config-0.3.0.zip`, 16 declared files verified. Was 15. |
| Clean-target install, `--target codex,copilot,claude` | Both skills byte-identical in `.agents/skills/` and `.claude/skills/`. |
| Unrelated local guidance | Untouched: a local skill and a local `AGENTS.md` written before the install both survive it. |
| Package-owned drift detection | A byte appended to an installed skill fails `apm audit --ci`, so the detector is proven to run. |

The change's own plan named `npm ci`, `npm test` and `npm run validate:renovate` in task 5.1.
Those belong to `morhaf-labs/.github`, which carries a `package.json` and the Renovate policy
tests; this repository has neither and its declared checks are the ones above, which
`.github/workflows/validate.yml` runs. The plan's step was followed by running this
repository's actual check set rather than by inventing a Node project to satisfy the wording.

## What the tests caught while being written

**The reference-existence test could not see the new reference.** `test_every_reference_the_workflow_names_exists`
extracted `(references/[a-z-]+\.md)` from `SKILL.md`, and `founder-stack-v2.md` carries a digit.
The link was present and the test reported it missing from the workflow, which is the failure
mode that would have been "fixed" by renaming the reference to suit the regex. The pattern now
accepts a digit.

**The capability parser raised instead of failing.** Removing the README section entirely made
`documented_capabilities()` raise `IndexError` rather than report a mismatch. It now returns an
empty mapping for a missing section, so deleting the declaration fails as "the package carries
two skills this documentation does not name" - which is the sentence a reader needs.

Both directions of the declaration check were exercised by mutation: a skill added without
documentation, documentation naming a capability the package does not carry, a documented
capability with an empty value, and the section deleted outright. All four fail; the tree was
restored from a copy and the suite is green.

## What is proved and what is not

Proved: the package declares what it provides and cannot drift from it silently; a creation
declaration that invents a capability, hand-authors structure, repeats initialization or skips
classification is refused by the model; the artifact packs, verifies and installs cleanly at
0.3.0.

Not proved: that an agent selects the standards skill from a product-idea phrasing. That is a
property of a model reading a description, reviewed above and deliberately not asserted. Also
not proved by this repository: that the initialization path in the new reference works - that is
`founder-stack-v2`'s own test suite and CI, and the reference was written against the landed
change rather than an intended one.
