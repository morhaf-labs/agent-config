---
name: deploy-to-morhaf-vps
description: Use when creating, reviewing, or repairing deployment for a Morhaf Labs project, including deciding whether a changed component belongs on the shared VPS, Cloudflare, or neither; preparing or reviewing a VPS application declaration or reusable workflow caller; and checking post-release evidence. Preserve the declared runtime owner and refuse direct infrastructure or cluster mutation.
---

# Deploy to Morhaf VPS

Select the declared runtime owner before proposing deployment work. Reuse the owning
workflow and application contract without copying their implementation or granting new
authority.

## Workflow

1. Read the repository's instructions and identify the changed component and paths.
2. Read [runtime ownership](references/runtime-ownership.md). Find an existing platform
   declaration and release caller; repository membership alone proves nothing.
3. If the component is VPS-owned, read the
   [VPS application contract](references/vps-application-contract.md) and
   [release caller review](references/release-caller-review.md). Make only the minimal
   application-repository and reviewed platform-declaration changes.
4. If the component is Cloudflare-owned, follow its repository-native Cloudflare path.
   Do not add VPS workflow inputs, credentials or declarations.
5. If ownership is unknown or undeclared, stop and propose a change in the repository
   that owns the runtime. Do not invent a target.
6. Before reporting success, read
   [post-release verification](references/post-release-verification.md). Do not trigger
   production solely to prove agent guidance.

## Authority boundary

- Never run or propose direct cluster mutation, VPS provisioning, SSH deployment or a
  Pulumi apply as an application deployment action.
- Never add a kubeconfig, VPS SSH key, Tailscale credential, Pulumi token, platform
  Doppler token or undeclared secret to an application repository.
- Keep image publication, version recording, preview, apply, migration, declared tasks
  and rollout verification in `vps-infra-v2`.
- Use a full commit SHA for every reusable workflow reference. Preserve existing
  human-review and repository-permission boundaries.
