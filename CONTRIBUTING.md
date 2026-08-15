# Contributing

This repository publishes one public APM package of non-secret Morhaf Labs conventions
for coding agents. It carries no credential, no deployment authority and no executable
step, and it should stay that way.

## Reporting something

Open an issue. If it is a security problem, follow [SECURITY.md](SECURITY.md) instead and
do not open a public issue.

## Making a change

```
mise install                  # python, apm, agentskills
npm ci
npm test                      # producer tests
npm run validate:renovate
```

CI runs the same checks plus `apm audit`, `agentskills validate`, and a full pack,
install and drift verification. All of it runs on a pull request from a fork with no
secret, so you can watch it pass before a maintainer looks at anything.

## What the guidance may say

The package describes private repositories. Naming one and saying what it decides is
fine. **Restating its configuration is not** - not a Renovate preset, a workflow body, a
runner label list or a schema.

The test is mechanical: if a change to the private repository would make a sentence here
wrong, the sentence is too specific to be here. `tests/test_repository_standards.py`
enforces the narrower half of that by refusing hostnames, stack names, tailnet tags and
IP addresses.

Note what it deliberately permits: naming a credential *type* an agent must never add - a
kubeconfig, a platform token - is the guidance doing its job, not a leak.

## How guidance is tested

Against fixtures, through a router, never by asserting on wording. A test that greps a
skill for a sentence passes forever and proves nothing about the decision that sentence
describes - and the wording is the part most likely to be rewritten for clarity without
any decision changing.

New guidance that makes a claim about repository shape should come with a fixture and the
negative case that would catch it being wrong.

## Releases

Maintainers only. The manifest version and the tag must match, and a release publishes the
archive with a SHA-256 sidecar. Published releases are never moved or deleted.
