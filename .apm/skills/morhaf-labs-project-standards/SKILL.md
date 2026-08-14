---
name: morhaf-labs-project-standards
description: Use when creating, adopting, auditing or changing repository automation for a Morhaf Labs project, including new repository setup, GitHub Actions runners and permissions, dependency update policy, branch and release protection, project-shape selection, public-repository baselines, and deciding whether a repository is still maintained. Classify the repository before changing anything, and reuse the owning automation rather than restating it.
---

# Morhaf Labs project standards

Classify the repository first. Every other decision here depends on what it is, and the
common failure is not choosing wrongly but never choosing - applying current standards
to a repository that has been replaced, or picking a template because another repository
resembles it.

The organization owns these decisions in specific places. Read the owner for the current
value; nothing in this package is the source of truth for one.

## Workflow

1. Read the repository's own instructions first. They win over this skill wherever they
   are more specific.
2. Read [repository classification](references/repository-classification.md) and
   determine the lifecycle and the project shape. If either is unknown, or the
   repository may be superseded, stop and ask. Do not adopt standards into a repository
   whose lifecycle nobody has confirmed.
3. For a new project, read [project shape routing](references/project-shape-routing.md)
   and start from the declared source for that shape. Membership in the organization
   implies no deployment target.
4. For dependency work, read [dependency policy](references/dependency-policy.md).
5. For GitHub Actions work, read [Blacksmith CI](references/blacksmith-ci.md) and
   [workflow security](references/workflow-security.md).
6. For repository settings, protection or a maintainer change, read
   [governance](references/governance.md).
7. If the repository is public, read
   [public repositories](references/public-repositories.md) before proposing any shared
   workflow or inherited community health file.

## Refuse

- A native GitHub-hosted runner label. There is no fallback: an unavailable Blacksmith
  runner fails the job rather than moving the work back onto GitHub-hosted compute.
- A mutable action or reusable-workflow reference. Full commit SHA, always.
- Widening workflow permissions, or a fork-triggered workflow that can reach a secret.
- Shortening the organization release age, bypassing the check gate, or automerging a
  non-security major. A repository may only be stricter.
- A second dependency-update producer beside Renovate.
- Inventing a deployment target, or copying one from a repository that resembles this
  one.
- Maintenance work on a repository whose lifecycle is unconfirmed.

## Authority boundary

- Propose repository changes as a pull request. Do not change organization or repository
  settings as a side effect of another task.
- Do not add a kubeconfig, VPS SSH key, Tailscale credential, Pulumi token, platform
  Doppler token or broader GitHub authority to an application repository.
- Do not build a substitute for a GitHub capability the current plan does not include.
  Record the gap and leave it.
- Do not restate an owner's configuration in a repository that does not own it.
