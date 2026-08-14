# Workflow security

Every private repository with GitHub Actions calls the shared workflow-security workflow
from `morhaf-labs/.github`, pinned by full commit SHA and given a runner:

```yaml
jobs:
  workflow-security:
    uses: morhaf-labs/.github/.github/workflows/workflow-security.yml@<full-commit-sha>
    with:
      runner: blacksmith-2vcpu-ubuntu-2404
```

It runs actionlint, an offline zizmor scan and the runner-label check. Read the owner
for the current release SHA. A public repository cannot call it at all - see
[public repositories](public-repositories.md).

## What every workflow declares

- **Immutable references.** Full commit SHA for every action and reusable workflow. A
  tag moves; a major tag moves silently.
- **Least privilege.** An explicit `permissions` block, narrowed at the job rather than
  granted at the workflow when jobs differ.
- **Checkout without persisted credentials.** `persist-credentials: false` unless the
  job pushes.
- **A timeout.** Every job. A hung job otherwise runs to the platform maximum.
- **Frozen installs.** The lockfile decides the versions, not the resolver.
- **Safe concurrency.** Pull-request validation cancels superseded runs; anything that
  deploys, migrates or applies serialises and does **not** cancel in progress. An
  interrupted mutation is worse than a queue.

## Forks

A fork-triggered workflow receives no secret. `pull_request_target` runs with the base
repository's token and is refused unless a separate reviewed design proves untrusted
code cannot reach authority - and the review has to cover the checkout ref, because
checking out the pull request head under that trigger is the whole vulnerability.

## Reading a zizmor result

Two findings look like gaps and are not:

- Workflow-level broad permissions are only reported when the workflow has more than one
  job. With a single job there is no wider scope to report.
- A finding on a line a change did not touch is pre-existing. Compare against the
  baseline before attributing it to the change; the honest way is to run the scan on
  both trees rather than to reason about it.

## What this is not

A general policy engine. Syntax, known hazards and runner labels. A new rule needs a
requirement that already exists in a specification, not a preference.
