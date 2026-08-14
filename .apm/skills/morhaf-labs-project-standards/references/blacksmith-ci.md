# Blacksmith CI

Blacksmith runs every Linux job in this organization. This is one of the few literal
values in this package, because an agent adding a job needs the string and the
alternative is guidance that says "use the declared default" and leaves it to invent one:

```yaml
runs-on: blacksmith-2vcpu-ubuntu-2404
```

Another Blacksmith size or architecture needs **measured** evidence - a recorded run
duration or cache result showing the smaller runner is the constraint. "It feels slow"
is not evidence, and a larger runner chosen without it is a recurring cost nobody
revisits.

## There is no fallback

A native GitHub-hosted label is refused by the shared workflow-security check, not
merely discouraged. An unavailable Blacksmith runner fails the job rather than moving
the work, and the spend, onto GitHub-hosted compute. Failing closed is the intended
behaviour.

The check refuses by prefix - `ubuntu-`, `windows-`, `macos-` - so it catches labels
that do not exist yet. It accepts Blacksmith labels, `self-hosted`, a repository's own
labels, and `${{ }}` expressions, because a reusable workflow's runner is caller-owned
and gets checked in the caller's file. It reads matrix values too, so moving a native
label into a matrix does not hide it.

Each repository keeps a `.github/actionlint.yaml` declaring the Blacksmith labels it
uses. Without it, actionlint reports every job as an unknown runner and the real
finding - a typo, or a size nobody justified - is lost in the noise.

## Caches

Prefer the **upstream** language setup and cache actions. Blacksmith redirects them to
its colocated cache automatically, so a hand-rolled cache layer buys nothing and has to
be maintained.

## Docker

Use Blacksmith's current setup and build actions, pinned by full SHA. The current setup
action requires a `cache-key`, and that requirement is the useful part: it forces the
scoping decision to be explicit.

Scope the key to what genuinely shares layers:

- One key per Dockerfile when a job builds several unrelated images, or they evict each
  other's layers on every build.
- In a **shared reusable workflow**, include the caller's repository in the key.
  `github.repository` resolves to the caller there, so a key naming only the Dockerfile
  puts every consuming repository into one cache where each release evicts the last.

Push directly from the builder when the workflow publishes, and record the digest the
build reports rather than re-resolving the tag afterwards.
