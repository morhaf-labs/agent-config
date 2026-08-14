# Release caller review

The application repository owns only its trigger and a narrow call to
`morhaf-labs/vps-infra-v2/.github/workflows/deploy-to-platform.yml`.

Review the caller against the workflow at its referenced revision:

- pin `uses:` to a full 40-character commit SHA, never a branch or mutable tag;
- pass only inputs declared by the owning workflow;
- keep `contents: read` and grant `packages: write` only to the image-publishing job;
- use only the existing platform App private-key secret expected by the workflow;
- preserve a CI-qualified `ref` when the repository deploys the exact commit approved
  by another workflow;
- keep path filters bounded to the VPS-owned component in a hybrid repository.

Do not copy build, dispatch, preview, apply or rollout steps from the reusable workflow.
Do not add a second deployer or a direct host or cluster credential.
