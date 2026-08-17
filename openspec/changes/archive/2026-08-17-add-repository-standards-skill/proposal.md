## Why

This package already tells an agent how to deploy a Morhaf Labs component, and it is
loaded automatically when deployment work appears. Nothing tells an agent how to
*create or maintain the repository around that component* - which runner a job uses,
how a dependency update is allowed to merge, which shape a new project is, whether a
repository is still maintained at all.

The organization now has one answer to each of those, released in
`morhaf-labs/.github` at `v1.3.0`. Without a routing skill, an agent finds it only by
reading a private repository it may not think to open, so the standard is followed when
someone remembers and not otherwise. That is the same failure the deployment skill was
written to fix, one layer out.

## What Changes

- Add one intent-first `morhaf-labs-project-standards` skill whose description selects
  it automatically for repository creation, adoption, dependency, GitHub Actions,
  security and release work in a `morhaf-labs` remote.
- Add bounded references for repository classification, dependency policy, Blacksmith
  CI, workflow security, project-shape routing, solo-to-team governance and the
  public-repository exception. Each names the decision and the owner that implements it;
  none copies a preset, workflow or schema.
- Add fixtures for the eight repository shapes the standard has to distinguish, and
  producer tests that reject native runners, mutable pins, widened permissions, unsafe
  fork workflows, weakened dependency policy, invented deployment targets and
  maintenance work on an unconfirmed legacy repository.
- Extend package validation and release verification to cover both skills, proving
  locked Codex, Copilot and Claude installation and package-owned drift detection.
- Move validation and release onto Blacksmith, keeping this repository's local workflow
  and community health files, which a public repository cannot inherit from the private
  organization repository.

## Capabilities

### Modified Capabilities

- `agent-project-conventions`: Expands the package from deployment-only guidance to
  automatic repository-standard selection, while keeping repository-local authority and
  the existing runtime boundaries unchanged.

## Impact

- Files: a second skill under `.apm/skills/`, new fixtures and tests, `apm.yml` version,
  and both workflows.
- Consumers: repositories installing this package at the new locked version gain the
  routing skill. The deployment skill is unchanged, so nothing that depends on it moves.
- Runtime: none. This package holds no credential, no deployment authority and no
  executable step.
- Boundary: the package stays public and stays non-secret. It names the private owner
  and tells an agent to read it; it never restates its contents.
