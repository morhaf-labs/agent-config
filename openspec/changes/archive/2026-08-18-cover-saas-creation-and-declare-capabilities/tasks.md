## 1. SaaS creation reference

- [x] 1.1 Write `.apm/skills/morhaf-labs-project-standards/references/founder-stack-v2.md`
  covering the supported initialization path, that a successful initialization is one-shot and
  refuses to run again, and what the profile choice binds
- [x] 1.2 State in that reference that the profile and module sets live in the template's catalog
  and must be read from it, without naming their current values
- [x] 1.3 State the creation refusals: no integration invented outside the catalog, no
  hand-scaffolded application structure in place of the generator, no rerun of a completed
  initialization, no template chosen before the repository is classified
- [x] 1.4 Link the reference from the routing and classification tables, keeping each table row
  as it is
- [x] 1.5 Confirm the reference adds no copy of a Renovate preset, workflow body, runner label
  list, dependency version or environment key

## 2. Selection from product-idea intent

- [x] 2.1 Extend the `morhaf-labs-project-standards` description to select on starting a new
  Morhaf Labs project from a described idea, keeping it anchored to project creation rather than
  product or feature work generally
- [x] 2.2 Add the reference to the skill's workflow so creation reaches it only after
  classification
- [x] 2.3 Confirm the deployment skill's description is unchanged and stays dormant for a
  creation request that declares no long-running component
- [x] 2.4 Review the widened description against phrasings actually used to start a project, and
  record that selection is reviewed rather than asserted

## 3. Capability declaration

- [x] 3.1 Replace the stale single-primitive claim in `README.md` with a section naming every
  capability the package provides and the value each delivers
- [x] 3.2 Extend `tests/test_package.py` to assert set equality between the capabilities
  documented in `README.md` and the skills present under `.apm/skills/`
- [x] 3.3 Assert that each documented capability carries a value statement, without asserting on
  sentences
- [x] 3.4 Verify the test fails when a skill is added without documentation, and when the
  documentation names a capability the package does not carry

## 4. Creation fixtures and model

- [x] 4.1 Add a creation fixture under `tests/fixtures/` using the existing declaration shape
  with `proposed_work: "create"` and a `creation` block naming the template, profile, selected
  capabilities, whether structure is generated or hand-authored, and whether initialization
  already completed
- [x] 4.2 Add `check_creation` to `tests/test_repository_standards.py` beside `check_lifecycle`
  and `check_renovate`, returning the routed owner and action
- [x] 4.3 Add negative tests mutating one field each: capability outside the catalog,
  hand-authored structure, already-initialized project, unclassified shape
- [x] 4.4 Confirm the positive creation fixture still routes to the Cloudflare owner and that the
  existing eight shape fixtures are unaffected

## 5. Release

- [x] 5.1 Run `mise install`, `npm ci`, `npm test`, `npm run validate:renovate`
- [x] 5.2 Run `agentskills validate` for both skills, `apm audit --ci --no-policy`, and
  `apm pack --dry-run --marketplace none --verbose`
- [x] 5.3 Bump the package version in `apm.yml`, `plugin.json` and `.claude-plugin/`, and confirm
  the tag-to-manifest version test passes
- [x] 5.4 Confirm the packed artifact carries no secret, private operational detail or executable
  step, and installs into clean Codex, Copilot and Claude targets
- [x] 5.5 Open the pull request, then tag the release once the companion `founder-stack-v2` change
  has landed so the reference describes a path that exists
