# Governance

The organization has one authorized writer and is on a GitHub plan that does not include
branch protection or required status checks for private repositories, nor
organization-wide Actions secrets.

**Do not build a substitute for a missing plan capability.** A repository file, a bot
reviewer or a custom approval step that cannot actually block a push is worse than the
documented gap, because it reads as enforcement to whoever looks next. Record the gap
and leave it.

## What gates work today

Automated evidence. Every repository with Actions runs its own checks and the shared
workflow-security workflow, so something always reports, and Renovate waits for observed
green status before merging on its own. Direct-push prevention is not claimed, and
guidance must not claim it either.

Note the interaction: Renovate reads a branch with no status checks as green. The
requirement that every repository with Actions has a reporting check is what keeps an
unchecked repository from automerging - not a gate anyone wrote.

## What does not depend on the plan

- Immutable release tags, never moved or deleted.
- Full-SHA consumer pins, never a branch or a moving major tag.
- Secret scanning and push protection where the plan offers them.

## A repository that publishes its own SHAs must not squash

If a repository publishes commit SHAs for others to pin - a shared workflow or action -
then squash and rebase merging must be disabled on it. A squash replaces the branch
commits with a new one and discards exactly the SHAs that were published, including the
pin a reusable workflow holds on its own repository's action. Enforce it with GitHub's
merge-method setting rather than a convention, because it only matters on the day nobody
is thinking about it.

Renovate needs no configuration for this: it derives its merge method from the
repository's allowed methods.

Repositories that publish nothing keep squashing.

## When a second maintainer arrives

An operator checkpoint, not an automatic change. Review repository access, secret access
and ownership boundaries, then raise high-risk repositories to one non-author approving
review. Requiring a review while one person holds write access either blocks all work or
is satisfied by the author, and neither is a control.

## Repository settings are not a side effect

Changing a repository or organization setting is its own reviewed decision. Do not change
one while doing something else, and record what changed and why.
