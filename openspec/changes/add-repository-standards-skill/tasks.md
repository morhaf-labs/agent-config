## 1. The skill

Coordinated as tasks 3.1-3.2 of `vps-infra-v2`'s
`standardize-morhaf-labs-project-repositories`.

- [x] 1.1 Add `morhaf-labs-project-standards` with an intent-first description covering
  repository creation, adoption, dependency, GitHub Actions, security and release work,
  and a workflow that classifies before it changes anything.
- [x] 1.2 Add bounded references for repository classification, dependency policy,
  Blacksmith CI, workflow security, project-shape routing, solo-to-team governance and
  the public-repository exception, naming owners rather than restating configuration.

## 2. Producer tests

Coordinated as tasks 3.3-3.4.

- [x] 2.1 Add fixtures for the private SaaS, VPS service, hybrid application,
  infrastructure, library, public producer, unknown owner and superseded repository
  shapes.
- [x] 2.2 Add producer tests rejecting native runners, mutable action pins, widened
  permissions, unsafe fork workflows, weakened dependency policy, invented deployment
  targets and maintenance on an unconfirmed legacy repository.

## 3. Package and release

Coordinated as tasks 3.5-3.6 and 6.6.

- [x] 3.1 Update package validation and release verification for both skills, proving
  locked Codex, Copilot and Claude installation, package-owned drift detection and
  preservation of unrelated local guidance.
- [x] 3.2 Move validation and release jobs to Blacksmith, keeping the local workflow and
  community health exception a public repository cannot inherit.
- [x] 3.3 Bump the manifest to 0.2.0 and run the full local validation the workflow runs.
- [x] 3.4 👤 **CHECKPOINT** Review and merge, then tag `v0.2.0` and verify the published
  artifact, its checksum and the absence of private content. Operator delegated this on
  2026-08-14; merged as `e8e43e60`, released `v0.2.0`. See `evidence.md`.
