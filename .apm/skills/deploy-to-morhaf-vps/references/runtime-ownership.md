# Runtime ownership

Classify the changed component, not the repository as a whole.

| Evidence | Owner | Action |
| --- | --- | --- |
| A long-running service, scheduler or worker is declared in the `vps-infra-v2` applications map | VPS platform | Use its application declaration and pinned reusable release caller. |
| The component is declared for Cloudflare and has no VPS application declaration | Repository Cloudflare path | Keep the change on Cloudflare and add no VPS surface. |
| A repository has both kinds | Each declared owner | Apply each contract only to its bounded component paths. |
| No declaration identifies an owner | Unknown | Stop and propose ownership at the natural repository. |

For a hybrid repository, shared files do not make both runtimes interchangeable. Use
the path filters and declarations already reviewed for each component. A change outside
the VPS component's bounded paths must not acquire a VPS release path.

Fail closed when evidence conflicts. Do not resolve ambiguity by adding both deployment
paths or by granting broader credentials.
