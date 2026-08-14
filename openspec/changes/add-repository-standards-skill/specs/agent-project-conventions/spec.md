## ADDED Requirements

### Requirement: Repository standards guidance is selected automatically

The package SHALL provide one skill whose description selects it without manual
invocation for Morhaf Labs repository creation, adoption, dependency, GitHub Actions,
security and release work. It SHALL remain separate from the deployment skill, and the
package SHALL NOT add an agent, prompt, hook, MCP server or executable step to achieve
selection.

#### Scenario: An agent is asked to set up CI for a new repository

- **WHEN** the work concerns runners, dependency updates, workflow permissions or
  release automation in a `morhaf-labs` repository
- **THEN** the repository-standards skill is selected from its description alone
- **AND** the deployment skill stays dormant because the work declares no runtime
  component

#### Scenario: The package is inspected for stronger primitives

- **WHEN** the package contents are validated
- **THEN** it contains only skills
- **AND** it declares no marketplace, executable script or MCP dependency

### Requirement: Guidance names owners rather than restating their configuration

Each reference SHALL name the decision and the repository that implements it, and SHALL
NOT copy a Renovate preset, a workflow body, a runner label list or a schema. Guidance
SHALL remain correct when an owner changes its implementation.

#### Scenario: The organization changes a dependency policy value

- **WHEN** the owning preset changes a release age, a lane or a package rule
- **THEN** the package requires no edit
- **AND** an agent following it still reads the owner for the current value

#### Scenario: An agent needs the default runner label

- **WHEN** the agent adds a Linux job
- **THEN** the guidance supplies the declared default label directly
- **AND** it directs the agent to measured evidence before selecting another size

### Requirement: Classification precedes any repository automation change

The skill SHALL require an agent to classify the repository's lifecycle and project
shape before proposing automation, dependency or release changes. An unknown shape or
an unconfirmed legacy repository SHALL stop the work and produce a question, not a
default.

#### Scenario: An agent finds a repository that appears active but is superseded

- **WHEN** its lifecycle is not confirmed and a replacement may exist
- **THEN** the agent stops and asks the operator to confirm or archive
- **AND** it does not spend maintenance effort adopting current standards there

#### Scenario: A project shape cannot be determined

- **WHEN** the repository declares no runtime owner and matches no known shape
- **THEN** the agent proposes a change in the repository that owns the contract
- **AND** it does not invent a deployment target or select a template by resemblance

### Requirement: Producer tests reject the failures the standard exists to prevent

The package SHALL carry fixtures for the private SaaS, VPS service, hybrid application,
infrastructure, library, public producer, unknown owner and superseded repository
shapes, and SHALL fail its own validation when a declaration uses a native
GitHub-hosted runner, a mutable action reference, widened workflow permissions, an
unsafe fork-triggered workflow, a weakened dependency policy, an invented deployment
target, or maintenance work on an unconfirmed legacy repository.

#### Scenario: A declaration weakens the organization dependency policy

- **WHEN** it shortens the normal release age, disables the check gate, or automerges a
  non-security major
- **THEN** validation fails naming the weakened property
- **AND** a stricter local exception continues to pass

#### Scenario: A workflow declaration exposes a secret to fork code

- **WHEN** a fork-triggered workflow declares a secret or a privileged trigger
- **THEN** validation fails
- **AND** a fork-safe declaration without secrets passes

### Requirement: The package proves locked installation across supported targets

Package validation SHALL prove a frozen Codex, Copilot and Claude installation of every
skill, package-owned drift detection, and that unrelated local agent guidance survives
installation. Release verification SHALL cover every skill, publish a checksum for the
artifact, and confirm the artifact carries no secret, private operational detail or
executable deployment authority.

#### Scenario: A release artifact is verified

- **WHEN** the package is packed and installed from the artifact
- **THEN** every declared skill installs identically for all supported targets
- **AND** the working tree is unchanged and the checksum verifies in the downloaded
  layout

#### Scenario: Installation meets existing local guidance

- **WHEN** the target repository already holds unrelated agent instructions
- **THEN** installation replaces only package-owned files
- **AND** the unrelated guidance is preserved
