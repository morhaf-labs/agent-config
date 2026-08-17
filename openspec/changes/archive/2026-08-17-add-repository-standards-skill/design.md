## Context

This package is public and installs into Codex, Copilot and Claude through APM. It is
consumed by private repositories whose automation lives in a private organization
repository. That asymmetry is the whole design constraint: the guidance has to be
useful to an agent working in a private repository without restating anything private,
and without going stale the moment the private owner changes.

`morhaf-labs/.github@v1.3.0` now owns the Renovate lanes, the Blacksmith runner check
and the workflow security gate. `vps-infra-v2` owns the VPS contract, Founder Stack v2
owns the Cloudflare SaaS path. None of those belong here.

## Goals / Non-Goals

**Goals:**

- One skill an agent loads without being asked, for repository work rather than
  deployment work.
- Guidance that names decisions and owners, and stays correct when an owner's
  implementation changes.
- Failure-closed routing: an unknown shape stops rather than guessing.

**Non-Goals:**

- Copying the Renovate preset, a workflow, a runner label list or a schema into this
  package.
- A second agent, hook, MCP server or executable step.
- Replacing repository-local instructions. This skill is read *before* them and never
  over them.

## Decisions

### D1. One skill, two skills in the package, no marketplace

The routing skill is separate from `deploy-to-morhaf-vps` because the two trigger on
different work: one on deployment, one on repository automation. They stay in one
package because skill routing already keeps the irrelevant one dormant, and one
manifest, one lockfile and one audit path is less machinery than a marketplace.

`test_package.py` currently asserts the package holds exactly one skill. That assertion
becomes a set membership check rather than being deleted, so a *third* skill still has
to be a deliberate decision.

### D2. Name the owner, never the value

A reference may say that normal updates wait five days and that
`morhaf-labs/.github:renovate-config` is where that number lives. It may not restate the
JSON. The test for this is mechanical: if a change to the private preset would make a
sentence here wrong, the sentence is too specific.

This is also the public-content boundary. Naming a private repository and what it
decides is not a leak; pasting its configuration would be one, and pasting its
operational detail certainly would.

There is one deliberate exception. `blacksmith-2vcpu-ubuntu-2404` is written out,
because an agent choosing a runner needs the literal string and the alternative is
guidance that says "use the declared default" and leaves the agent to invent one. It is
also already public in every consumer's workflow files.

### D3. Classification comes before any other decision

Every other decision depends on what the repository *is*, and the standard's own first
requirement is that classification happens before automation changes. So the skill's
workflow starts there and refuses to proceed on an unknown or unconfirmed-legacy
repository, the same way the deployment skill refuses an unknown runtime.

The failure this prevents is specific and has already happened in this organization:
an agent finding a repository that looks active, applying current standards to it, and
spending the effort on something whose replacement already exists.

### D4. Fixtures are declarative, and the test is the matcher

The existing `test_package.py` validates JSON fixtures through a small `validate_*`
function rather than asserting on prose. The new tests follow it exactly: eight shape
fixtures, one function that routes a repository declaration to an owner and a set of
required properties, and negative tests that mutate a fixture and assert the specific
refusal.

That keeps the guidance testable without testing the wording, which is the trap - a test
that greps SKILL.md for a sentence passes forever and proves nothing.

### D5. Blacksmith, with the public exception intact

Both workflows move to `blacksmith-2vcpu-ubuntu-2404`. This repository keeps its *local*
`validate.yml` rather than calling the shared `workflow-security` workflow, because a
public repository cannot call a private reusable workflow at all. `LICENSE`,
`SECURITY.md` and contribution guidance stay local for the same reason.

That exception is recorded in the package as guidance, because a public repository is
exactly where an agent would otherwise propose adopting the shared caller and get an
undiagnosable failure.

## Risks / Trade-offs

- **Two skills in one package means the irrelevant one is installed everywhere.**
  Accepted: routing keeps it dormant, and each skill fails closed on its own.
- **Guidance that names an owner can still go stale if the owner is renamed.** Less
  often than guidance that copies values, which goes stale on every edit.
- **Producer tests assert on a model of the standard, not the standard itself.** They
  catch a fixture or router regression, not a divergence between this package and
  `.github`. The reference-level answer to that is D2: say nothing specific enough to
  diverge.

## Migration Plan

1. Add the skill and its references.
2. Add fixtures and producer tests; extend package and release verification to both
   skills.
3. Move both workflows to Blacksmith.
4. Bump the manifest to 0.2.0, release one immutable tag, verify the artifact, its
   checksum and the absence of private content.
5. Consumers adopt the new locked version through their own changes.

Rollback is a consumer pinning the previous package version. Published releases are
never moved or deleted.

## Open Questions

None.
