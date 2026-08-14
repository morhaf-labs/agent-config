# Morhaf Labs agent config

Versioned, non-secret agent guidance for Morhaf Labs projects.

This repository is an APM package. Its first and only primitive is
`deploy-to-morhaf-vps`, a skill that helps an agent identify the runtime owner of a
changed component and reuse the existing Morhaf Labs deployment contract. It contains
guidance and test fixtures only. It does not deploy anything and grants no authority.

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
tests/
```

The skill uses references for detailed runtime ownership, the VPS application
contract, release caller review and post-release verification. APM owns installation,
target routing, locking, content integrity and package-owned drift detection.

## Toolchain and checks

The supported toolchain is pinned in `mise.toml`:

- Python 3.14.7
- Microsoft APM CLI 0.28.0

Run:

```sh
mise install
python -m unittest discover -s tests -v
apm compile --validate --local-only
apm install --dry-run --target codex,copilot,claude
apm audit --ci --no-policy
apm pack --dry-run --marketplace none
```

Releases are reviewed pull requests followed by immutable `v*` tags. CI builds and
audits the release artifact; release notes are generated from the reviewed artifact.
There is no manually maintained changelog.
