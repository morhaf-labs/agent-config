# Project shape routing

A new repository starts from the declared source for its shape. Do not start from
whichever existing repository looks closest - that is how a SaaS project acquires a VPS
workflow it never needed, and how a worker ends up on a runtime that cannot keep it
running.

| Shape | Start from | Runtime | Deployment guidance |
| --- | --- | --- | --- |
| Request-driven SaaS | Founder Stack v2 | Cloudflare | The generated Cloudflare path |
| Long-running service, scheduler, worker | VPS App Template | `vps-infra-v2` | `deploy-to-morhaf-vps` |
| Hybrid | Both, per declared component | Each component's own | Bounded to that component's paths |
| Infrastructure | Itself | Itself | Not an application |
| Library | Nothing to deploy | None | Do not add a deployment workflow |
| Public producer | Its own release path | None | See [public repositories](public-repositories.md) |

The request-driven SaaS row has its own path: read
[creating a request-driven SaaS](founder-stack-v2.md) before proposing any command, and
read it from the template rather than from memory.

## The two refusals

**Do not adopt the VPS path implicitly.** A SaaS repository gets a VPS workflow only when
it declares a separate long-running component that needs one. Being in the organization
is not a reason.

**Do not invent a target.** If the shape is unclear or the runtime owner is undeclared,
propose a change in the repository that owns the contract and stop. A guessed target is
worse than no target, because it looks decided.

A hybrid repository keeps each contract bounded to its own component paths. Two contracts
in one repository is fine; two contracts over the same component is not.

## Production readiness, whatever the shape

The runtime owner implements these. The standard's contribution is that they are
*decided* rather than discovered later:

- Failures are observable, and someone owns the alert.
- Anything that accumulates - logs, sessions, artifacts, rows - has a declared bound.
  Prefer the upstream retention, TTL or pruning setting to a cleanup job.
- Data retention and deletion are stated.
- Backup and restore have an owner, and restore has been exercised rather than assumed.
- A schema migration is backward compatible with the version still running during the
  rollout, or the change documents a reviewed expand-and-contract sequence.
- Rollback is possible without a rebuild.
