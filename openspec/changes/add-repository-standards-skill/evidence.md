## Release

| What | Value |
| --- | --- |
| Release | `v0.2.0` |
| Merge commit | `e8e43e60dac8b55bdab5ebda7152373a0a4d8c58` |
| Package version | 0.2.0, in `apm.yml` and all three `plugin.json` manifests |
| Assets | `agent-config-0.2.0.zip`, `agent-config-0.2.0.zip.sha256` |
| Bundle SHA-256 | `32f007a580d83624a10607deed246790123f540054466314e38a191ba7fdc07c` |

Merged and released on 2026-08-14 with the operator's explicit delegation of the
checkpoint. Squash merging is retained here: this repository publishes a *package*, not
commit SHAs for others to pin, so the rule that disabled squash on `morhaf-labs/.github`
does not apply.

## Checks

| Check | Result |
| --- | --- |
| `python -m unittest discover -s tests` | 45 tests, 0 failures. |
| `apm audit --ci` | 10 of 10 checks pass. |
| `agentskills validate` | Valid, both skills. |
| `actionlint` | Exit 0, with the new `.github/actionlint.yaml`. |
| `zizmor --offline --persona=regular .github` | No findings, 3 suppressed. |
| Organization runner check, from `.github@v1.3.0` | Passes. Run against this repository with the released script. |
| `Validate` on Blacksmith | Green on the pull request, 27s. |
| `Release` on Blacksmith | Green on the tag. |

## The published artifact, verified after publication

Downloaded from the release rather than trusted from the build:

- `sha256sum -c` verifies in the downloaded layout.
- 15 files, exactly the declared set, checked by `tests/verify_release.py` against the
  reviewed `plugin.json`.
- Both skills are byte-identical to the reviewed source tree.
- No credential-like content, and no private hostname, stack name or tailnet tag.

**It is not byte-reproducible, and the reason is worth stating rather than leaving as a
surprise.** Repacking the tagged tree produces a different zip digest. The only content
difference is `packed_at` in the bundled `apm.lock.yaml`, a timestamp APM writes at pack
time; `diff -r -I packed_at` between the published artifact and a fresh repack reports
nothing. So the guarantee this release offers is content verification against reviewed
source, not bit-for-bit reproducibility.

## What the tests caught while being written

**The public-content boundary test refused the word `kubeconfig`.** The first version
scanned for credential-shaped strings and flagged the authority boundary in both skills -
the lines that tell an agent never to add a kubeconfig or a platform token to an
application repository. Satisfying that test would have deleted the guidance. Naming a
credential type an agent must not add is the guidance working; the rule now targets
hostnames, stack names, tailnet tags and IP addresses, and the reason is recorded beside
it so the narrower rule is not read as an oversight.

**Package validation asserted exactly one skill.** It now asserts an exact *set*, so a
third skill remains a deliberate decision rather than something a loosened length check
waves through.

## What is proved and what is not

Proved: both skills install identically for Codex, Copilot and Claude from the published
artifact; package-owned drift is detected, by introducing drift and requiring the audit
to fail rather than by observing that it passed; unrelated local guidance survives
installation, written before the install so there was something to preserve.

Not proved: that this package agrees with `morhaf-labs/.github`. The producer tests check
a model of the standard against fixtures, not the private owner's live configuration. The
reference-level answer is the boundary rule - say nothing specific enough to diverge -
rather than a test that would need private access to run.
