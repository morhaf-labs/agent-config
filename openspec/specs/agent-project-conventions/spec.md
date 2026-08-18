# agent-project-conventions Specification

## Purpose

What the published agent guidance must do: select itself from intent, classify a
repository before changing its automation, and name the owner of a mechanism rather than
copying that owner's configuration. The package carries guidance and fixtures only. It
grants no authority, ships no credential, and is public.

The requirements here govern the guidance package. The policies it points at are owned
elsewhere, and a change to one of those is not a change to this spec.

## Requirements
### Requirement: Repository standards guidance is selected automatically

The package SHALL provide one skill whose description selects it without manual
invocation for Morhaf Labs repository creation, adoption, dependency, GitHub Actions,
security and release work, and for starting a new product from a described idea before any
repository exists. It SHALL remain separate from the deployment skill, and the
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

#### Scenario: An operator describes an idea rather than a repository

- **WHEN** the request is to build a new product and names no repository, automation or
  runtime
- **THEN** the repository-standards skill is still selected from its description alone
- **AND** classification precedes any template or runtime choice

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

### Requirement: Guidance covers creating a request-driven SaaS from the declared template

The package SHALL provide guidance for creating a request-driven SaaS from the declared
template that states the supported initialization path, that a successful initialization is
one-shot and refuses to run again, that the profile choice binds who owns product data,
metered usage and billing and becomes a product migration once applied, and that the
authoritative profile and module sets live in the template. It SHALL NOT restate those sets.

#### Scenario: An agent is asked to build a new SaaS product

- **WHEN** an operator describes a product idea that is a request-driven web application
- **THEN** the guidance routes it to the declared template and supplies the initialization
  path rather than a template name alone
- **AND** it directs the agent to read the template's own catalog for the current profile and
  module sets

#### Scenario: The template adds a module

- **WHEN** a module is added to or removed from the template's catalog
- **THEN** this package requires no edit
- **AND** an agent following the guidance still reads the template for the current set

#### Scenario: An agent proposes an integration outside the catalog

- **WHEN** the requested capability has no module in the template's catalog
- **THEN** the guidance requires either the nearest catalog module or a proposed change in the
  template
- **AND** it refuses to satisfy the request by hand-writing the integration into a project
  being created

#### Scenario: An agent is tempted to bypass the generator

- **WHEN** initialization is inconvenient, unavailable or already complete
- **THEN** the guidance refuses hand-scaffolded application structure as a substitute
- **AND** it refuses rerunning a completed initialization, naming later work as normal product
  evolution

### Requirement: Producer tests reject the failures the standard exists to prevent

The package SHALL carry fixtures for the private SaaS, VPS service, hybrid application,
infrastructure, library, public producer, unknown owner and superseded repository
shapes, and for creating a new request-driven SaaS, and SHALL fail its own validation when a
declaration uses a native
GitHub-hosted runner, a mutable action reference, widened workflow permissions, an
unsafe fork-triggered workflow, a weakened dependency policy, an invented deployment
target, maintenance work on an unconfirmed legacy repository, an integration invented outside
the declared catalog, hand-scaffolded application structure in place of the generator, or a
rerun of a completed initialization.

#### Scenario: A declaration weakens the organization dependency policy

- **WHEN** it shortens the normal release age, disables the check gate, or automerges a
  non-security major
- **THEN** validation fails naming the weakened property
- **AND** a stricter local exception continues to pass

#### Scenario: A workflow declaration exposes a secret to fork code

- **WHEN** a fork-triggered workflow declares a secret or a privileged trigger
- **THEN** validation fails
- **AND** a fork-safe declaration without secrets passes

#### Scenario: A creation declaration invents an integration

- **WHEN** a project-creation declaration selects a capability absent from the declared
  catalog
- **THEN** validation fails naming the unsupported selection
- **AND** a declaration selecting only catalog capabilities passes

#### Scenario: A creation declaration bypasses or repeats initialization

- **WHEN** a declaration describes hand-authored application structure instead of a generated
  one, or a second initialization of an already initialized project
- **THEN** validation fails naming which of the two it is

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

### Requirement: The package declares its own capabilities and the declaration is verified

The package SHALL document, in one place, every capability it provides and the value each
delivers, so an operator installing it can see what it now covers. Package validation SHALL
verify that documentation against the primitives actually present and SHALL fail when the
documentation claims a primitive the package does not carry or omits one it does.

#### Scenario: An operator installs the package

- **WHEN** the package is installed and its documentation is read
- **THEN** every capability it provides is named with the value it delivers
- **AND** the skill descriptions an agent selects from cover the same capabilities

#### Scenario: A primitive is added without documenting it

- **WHEN** a skill is added to or removed from the package and the capability documentation is
  not updated
- **THEN** package validation fails naming the undocumented or missing capability

#### Scenario: Documentation claims more than the package carries

- **WHEN** the documentation names a capability the package does not provide
- **THEN** package validation fails rather than shipping a claim an agent would act on
