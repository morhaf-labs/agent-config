# VPS application contract

The source of truth is `docs/apps.md`, the application parser and rendered-resource
policy in `morhaf-labs/vps-infra-v2`. Inspect them at the workflow revision being
proposed. Do not copy their schema or validation implementation into an application
repository or this package.

Before proposing a VPS declaration, confirm the component supplies the contract's
current required evidence, including:

- immutable image version and correct Docker build context;
- explicit workload tier, memory and CPU ceilings, and every request required by that
  tier;
- declared port, meaningful readiness path and numeric non-root uid when required;
- only the environment names, secret names, data, tasks, migration and exposure the
  component actually uses;
- a bound for every accumulating store or persistent volume.

Unknown fields and missing load-bearing fields must fail closed at the owning platform.
Submit declaration changes to `vps-infra-v2` through review. Do not place platform
credentials or rendered Kubernetes resources in the application repository.
