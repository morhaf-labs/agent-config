# Post-release verification

The platform-owned reusable workflow waits for version recording, preview, apply and
rollout verification. A failed platform run must fail the caller. Do not replace that
contract with an application-side cluster check.

After a release triggered by the repository's normal lifecycle:

1. Confirm the caller built the intended immutable commit and reported the platform run.
2. Confirm the platform run succeeded and recorded the same version and digest.
3. Confirm any declared migration, task dependency and in-cluster serving check behaved
   as the application contract requires.
4. Report the evidence and any failure without starting a second production release.

For agent-only or documentation-only changes, reuse current successful deployment
evidence when runtime behavior did not change. A technical deployment success does not
enable payment or satisfy legal, provider, first-user or launch-evidence gates.
