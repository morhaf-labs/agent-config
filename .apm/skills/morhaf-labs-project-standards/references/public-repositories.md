# Public repositories

Making a repository public is a deliberate operator decision, taken after auditing both
the current tree **and the history**. A secret removed in a later commit is still in the
history, and publishing the repository publishes the history.

## The visibility boundary

`morhaf-labs/.github` is private. A public repository **cannot call a private reusable
workflow at all**, so a public repository keeps its own local validation workflow instead
of the shared caller.

This is worth recognising by its failure, because the failure is almost undiagnosable: a
run of **zero seconds with no job**, reporting only that the run "likely failed because
of a workflow file issue", with no mention of access. If a shared caller behaves that
way, the cause is visibility or the Actions access setting, not the workflow body.

For the same reason, a public repository keeps local `LICENSE`, `SECURITY.md` and
contribution guidance rather than inheriting organization community health files. Do not
propose replacing them with the shared ones.

## The public baseline

- An explicit license.
- A security reporting path.
- Contribution guidance.
- Fork-safe CI: no secret reachable from fork-triggered code, and no
  `pull_request_target` without a separately reviewed untrusted-code boundary.
- Secret scanning and push protection enabled.
- Immutable release tags.
- A published checksum for every artifact a release produces.
- Trusted publishing through OIDC wherever the registry supports it, rather than a
  long-lived publication token.

## Content

Public means public. Guidance in a public repository may name a private repository and
say what it decides; it may not restate that repository's configuration, its
infrastructure detail, its hostnames, its operational evidence or anything that reads as
a credential.

The test is mechanical: if a change to the private owner would make a sentence here
wrong, the sentence is too specific to be here.
