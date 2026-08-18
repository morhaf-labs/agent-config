# Repository classification

Two axes, both required before any automation change. Neither is inferable from the
repository name or from how recently it was committed to.

## Lifecycle

| Lifecycle | What it means | What may be done |
| --- | --- | --- |
| active | Maintained and in use | Adopt current standards |
| template | A source other repositories are generated from | Change it *before* anything generated from it |
| rehearsal | A generated fixture proving a template works | Regenerate from the source, or reconcile deliberately |
| legacy | Superseded, retained only until responsibilities are proven absent | No standards work |
| archived | Read-only on GitHub | Nothing |

**An unconfirmed lifecycle stops the work.** A repository that has been replaced usually
still looks active: recent commits, green CI, a plausible README. Adopting standards
into it is effort spent on something whose replacement already exists, and it is the
most common way this goes wrong. Ask the operator to confirm or archive.

Signals that a repository may be superseded: a newer repository with a similar name, a
contract or template it no longer implements, deployment history that stops while a
sibling's begins.

## Project shape

| Shape | Recognised by | Runtime owner |
| --- | --- | --- |
| SaaS | Request-driven web application | Cloudflare, via Founder Stack v2 |
| VPS service | Long-running service, scheduler or worker | `vps-infra-v2` |
| hybrid | Both, in separately declared components | Each component's own owner |
| infrastructure | Declares the platform other repositories deploy onto | Itself |
| library | Published or consumed as a dependency, deploys nothing | None |
| public producer | Distributes an artifact publicly | Its own release path |

A SaaS being *created* rather than classified continues to
[creating a request-driven SaaS](founder-stack-v2.md), after the shape above is settled.

Shape is read from what the repository *declares* - a platform declaration, a release
caller, a runtime target - not from what its code looks like. A repository that declares
nothing has no shape yet, and that is a question rather than a default.

## Order

Classification, then shape, then the specific reference for the work at hand. A shape
decision made before the lifecycle is confirmed is a decision that may not be worth
making at all.
