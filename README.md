# Morhaf Labs agent config

Versioned, non-secret agent guidance for Morhaf Labs projects.

This repository is an APM package. It contains guidance and test fixtures only: it deploys
nothing, runs nothing, and grants no authority. Every primitive it carries is a skill.

## Capabilities

What installing this package provides. Package validation asserts this list against the
skills actually present, so a capability cannot be claimed here without shipping and cannot
ship without being named here.

| Capability | Value |
| --- | --- |
| `morhaf-labs-project-standards` | Classifies a repository before anything about it is changed, routes a new project to the declared source for its shape - including the initialization path for a request-driven SaaS - and refuses the automation failures the organization has already paid for once: a GitHub-hosted runner, a mutable action reference, a widened workflow permission, a weakened dependency policy, an invented deployment target, and maintenance on a repository nobody has confirmed is still live. |
| `deploy-to-morhaf-vps` | Identifies the runtime owner of a changed component and reuses the existing Morhaf Labs VPS deployment contract rather than writing a second one, and refuses direct infrastructure or cluster mutation. Stays dormant for a component whose runtime owner is Cloudflare. |

## Public content boundary

This repository is intentionally public. It may contain stable project conventions,
public repository names, workflow interfaces, synthetic fixtures and generated package
artifacts. It must never contain credentials, secret values, private host details,
incident data, customer data or private operational evidence.

Application repositories retain their existing review and permission boundaries. The
package never provides a kubeconfig, VPS SSH key, Tailscale credential, Pulumi token,
platform Doppler token or direct cluster mutation path.

Report a suspected exposure through GitHub's private vulnerability reporting rather
than a public issue.

## Package layout

```text
apm.yml
plugin.json
.apm/skills/deploy-to-morhaf-vps/
.apm/skills/morhaf-labs-project-standards/
tests/
```

Each skill keeps its detail in references rather than in one long instruction: runtime
ownership, the VPS application contract, release caller review and post-release verification
for the deployment skill; classification, project-shape routing, SaaS creation, dependency
policy, Blacksmith CI, workflow security, governance and public-repository baselines for the
standards skill. APM owns installation, target routing, locking, content integrity and
package-owned drift detection.

## Toolchain and checks

The supported toolchain is pinned in `mise.toml`:

- Python 3.14.7
- Microsoft APM CLI 0.28.0
- Agent Skills reference validator 0.1.1

Run:

```sh
mise install
python -m unittest discover -s tests -v
agentskills validate .apm/skills/deploy-to-morhaf-vps
agentskills validate .apm/skills/morhaf-labs-project-standards
apm audit --ci --no-policy
apm pack --dry-run --marketplace none --verbose
```

`apm compile` is intentionally absent. It validates instruction and agent compilation,
while this package contains only skills. CI packs them into an integrity-locked archive,
audits that artifact, and installs it into clean Codex, Copilot and Claude targets.

Releases are reviewed pull requests followed by immutable `v*` tags. CI builds and
audits the release artifact; release notes are generated from the reviewed artifact.
There is no manually maintained changelog.
