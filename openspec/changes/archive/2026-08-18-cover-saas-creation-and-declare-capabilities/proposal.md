## Why

The package routes a request-driven SaaS to Founder Stack v2 in a single table cell and
stops there. An agent learns which template to use and nothing about how to use it: not that
initialization is one-shot and refuses to run again, not that the profile choice is a product
migration once made, not that the module list is a closed set to read rather than infer. The
gap is filled by guessing, and guessing at project creation is the most expensive place to
guess, because everything after it inherits the result.

The package also does not describe itself. `README.md` still states that
`deploy-to-morhaf-vps` is "its first and only primitive" while a second skill has shipped, so
the one document a person reads to recall what the package provides is already wrong. Nothing
verifies that claim against the primitives actually present, which is why it drifted
silently.

Both gaps have the same consequence at the moment of installation: an operator asks an agent
to install the guidance and neither of them can say what it now covers.

## What Changes

- Repository-standards guidance gains a reference for creating a request-driven SaaS from
  Founder Stack v2: the initialization command path, the one-shot and irreversible nature of
  initialization, the profile decision and what it binds, and where the authoritative module
  catalog lives.
- The reference names the template as the owner of the profile and module sets and does not
  restate them, so adding a module to Founder Stack v2 requires no release here.
- Skill selection covers starting a new product from an idea, not only repository automation
  work, so guidance is selected before a repository exists. This remains description-driven;
  no agent, prompt, hook or executable step is added.
- The package documents the capabilities it provides and the value each one delivers, in one
  place, for a person recalling what installing it buys them.
- A producer test verifies that documentation against the primitives actually present, so a
  claim about what the package provides cannot outlive the primitive it describes.
- Producer fixtures cover project creation and the refusals specific to it: inventing an
  integration outside the catalog, hand-scaffolding an application instead of running the
  generator, rerunning a completed initialization, and creating a project without
  classifying its shape first.

## Capabilities

### New Capabilities

None. Both changes extend what the existing published-guidance capability must do.

### Modified Capabilities

- `agent-project-conventions`: guidance must cover creating a request-driven SaaS from the
  declared template and must be selected from product-idea intent; the package must declare
  its own capabilities and prove that declaration against its installed primitives; producer
  fixtures must reject the creation-specific failures.

## Impact

- `.apm/skills/morhaf-labs-project-standards/references/founder-stack-v2.md` is added; the
  routing and classification references gain a link to it.
- The skill description is extended to select on product-idea intent. Wording only, no new
  primitive.
- `README.md` gains a capability and value section and loses the stale claim about a single
  primitive.
- `tests/test_package.py` gains documentation-to-primitive verification;
  `tests/test_repository_standards.py` and `tests/fixtures/` gain the creation fixtures and
  their negative mutations.
- The package version and tag advance; consumers pick the new pin up through Renovate. No
  consumer is required to act, and no existing skill changes behavior.
- Founder Stack v2 remains the owner of the profile and module sets. This change adds no
  copy of them and no dependency on that repository.
