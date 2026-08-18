## Context

See proposal.md for motivation. Four existing properties of this package constrain the
approach:

- `morhaf-labs-project-standards` already claims new repository setup and project-shape
  selection in its description, and its workflow makes classification step 2. Creation cannot
  legitimately skip that step.
- The published requirements forbid restating an owner's configuration, and forbid adding an
  agent, prompt, hook, MCP server or executable step to achieve selection.
- `test_repository_standards.py` tests a *model* of the standard against declarative JSON
  fixtures and deliberately does not assert on SKILL.md wording, on the stated grounds that a
  wording assertion passes forever and proves nothing.
- `tests/fixtures/repo-private-saas.json` already routes a Cloudflare component to
  `cloudflare-founder-stack-v2`, so routing has a tested model. What has no model is creation.

## Goals / Non-Goals

**Goals:**

- Creation guidance that survives a change to the template's catalog without a release here.
- One place a person reads to recall what installing this package provides, that cannot go
  stale silently.
- Creation-specific refusals held by the same fixture-and-model pattern as every other refusal
  in this package.

**Non-Goals:**

- Any executable step, orchestrator, wrapper CLI or MCP server. Explicitly forbidden by the
  published requirements and not revisited here.
- Documenting the template's profiles, modules, dependency versions or environment keys.
- Changing the deployment skill, or introducing a Cloudflare deployment contract. The absent
  Cloudflare release path is a real gap and it belongs to the template, not to this package.

## Decisions

### A reference in the existing skill, not a second skill

`references/founder-stack-v2.md` joins the seven references already in
`morhaf-labs-project-standards`, and the routing and classification tables link to it.

A separate `create-morhaf-labs-saas` skill was the alternative and is rejected. Creation must
run classification first, which is step 2 of the standards skill; a separate skill would either
duplicate that step or cross-reference it, and both readings compete for the same "new project"
trigger. Two skills that can both answer "I am starting something new" is how an operator loses
track of which guidance the agent actually followed, and this package's stated priority is that
the guidance stay maintainable rather than maximally discoverable.

### Selection is widened by description, and that widening is not testable here

The description gains product-idea intent so the skill is selected before a repository exists.
This is wording, which by this package's own testing philosophy is not something to assert on.
The fixtures therefore cover what happens *after* selection - the creation decision and its
refusals - and the description is reviewed rather than tested. Naming that boundary is better
than adding a wording assertion that would appear to cover it.

### The capability declaration lives in README and is verified as a set, not as prose

One section of `README.md` names every capability the package provides and the value each
delivers. `test_package.py` asserts set equality between the capabilities documented there and
the skills actually present under `.apm/skills/`, and that each documented capability carries a
value statement.

A separate `CAPABILITIES.md` was rejected: it becomes a second place to drift from, and the
current stale README line is evidence that one place is already hard enough to keep true. An
installed agent-facing capability index was also rejected - the skill descriptions *are* the
index an agent sees at install time, and a document competing with them for attention is a
new primitive in a package whose value is that it has only skills.

The test asserts on the capability set and the presence of a value statement, never on
sentences, for the reason the existing suite already documents.

### Creation fixtures extend the existing declarative shape

A creation fixture is an existing repository declaration with `proposed_work: "create"` and a
`creation` block naming the template, the profile, the selected capabilities, whether the
application structure is generated or hand-authored, and whether initialization already
completed. The model gains a `check_creation` function beside `check_lifecycle` and
`check_renovate`, and negative tests mutate one field and assert the specific refusal.

This keeps the suite one pattern. A second testing style for creation would double the cost of
every future change to it.

### The catalog is named, never copied

The reference names the template and its catalog file as the owner of the profile and module
sets and instructs the agent to read it. The spec scenario "the template adds a module → this
package requires no edit" is the standing check on that decision, and it is the difference
between guidance that ages and guidance that does not.

## Risks / Trade-offs

- **The widened description fires on unrelated application work.** → Keep the trigger anchored
  to starting a Morhaf Labs project rather than to product or feature work generally, and review
  it against phrasings actually used. An over-broad guidance skill is noise, not a wrong answer,
  but noise erodes trust in selection.
- **The reference drifts toward restating the catalog as modules are added.** → The published
  "names owners" requirement plus the no-edit scenario are the guard. Review any addition to the
  reference against them.
- **The README verification becomes a wording test over time.** → It asserts set equality and
  presence, and this design is the record of why it must stay that shape.
- **Guidance describes an initialization path the template does not yet expose.** → The
  companion change in `founder-stack-v2` lands first. Writing this reference against the current
  interactive-only initializer would document an aspiration.

## Migration Plan

Additive. The package version and tag advance by a minor release; existing skills keep their
behavior, and consumers pick the pin up through Renovate with no action. Rollback is reverting
the reference, the description and the tests, which returns the package to routing by table row.
