# Dependency policy

Renovate is the only mechanism that opens dependency-update pull requests in this
organization. Do not add a second one, and do not enable Dependabot version updates or
its automated security pull requests beside it. GitHub's dependency graph and alerts
stay on; they report, they do not open pull requests.

## Where the policy lives

`morhaf-labs/.github`, in its `renovate-config` preset. Every maintained repository
extends it:

```json
{ "extends": ["local>morhaf-labs/.github:renovate-config"] }
```

Renovate resolves that from the owner's default branch, so a policy change reaches every
repository with no repository edit. **Read the preset for current values.** Do not copy
them into a repository, and do not restate them in guidance - a number restated in two
places is a number that will disagree with itself.

## The three lanes

Normal patch and minor releases wait a release-age delay, then merge automatically once
the repository's checks pass. A known-vulnerability fix skips the delay and the
dashboard approval regardless of update type, and never skips the checks. A non-security
major waits for a human.

## What a repository may add

Ecosystem groups, custom managers for versions no built-in manager reads, and **stricter**
exceptions for a named package: a longer age, or `automerge: false`.

A repository may not shorten the base age, disable the check gate, or automerge a
non-security major. Those are the three weakenings to refuse.

## When automerge is the wrong default

Automerge assumes merging is cheap to undo. In a repository where merging to the default
branch *applies* something - an infrastructure repository whose CI runs an apply on push
- an automerged pull request is an unattended production change whose preview nobody
read. There, refuse automerge for anything that can alter what is running, and keep it
for updates that only touch CI.

`vps-infra-v2` is the worked example: Pulumi and every container-image and chart
dependency are held for review, while actions and dev tooling automerge.

## Before enabling automerge anywhere

The repository must have a check that actually reports. Renovate reads a branch with no
status checks as green, so automerge on a repository with no CI merges everything
immediately. Add the validation workflow first.
