# Creating a request-driven SaaS

The declared source for a request-driven SaaS is Founder Stack v2, a private GitHub template
that composes one application and then stops having a say in it. Classify the project first:
this reference applies once the shape is known to be a request-driven web application, and
choosing a template before that is the failure the classification step exists to prevent.

Nothing here is the source of truth for what the template offers. The template is.

## The supported path

```sh
gh repo create <name> --template morhaf-labs/founder-stack-v2 --private --clone
cd <name>
bun install
bun run init --name "<application name>" --profile <profile-id> --modules <ids or none>
```

The initializer also runs with no flags and prompts for every choice. Supplying any one of
`--name`, `--profile` or `--modules` supplies the whole selection, and every one of the three
is then required - an omitted flag is refused rather than defaulted, and `--modules none`
is how nothing is selected. `--yes` skips the confirmation and is for unattended runs only.

Propose the command and let the operator approve it. The resolved configuration appears in
the transcript before anything is applied, and that is the approval step - not a formality to
route around with `--yes` because a prompt is inconvenient.

Initialization needs the APM CLI on `PATH` and network access: it installs this package into
the generated project and commits the lockfile it resolves. It composes and validates in a
staging directory first, so a failure leaves the repository untouched. A successful run
replaces the template sources; committing the result is the operator's step, not the
initializer's.

## Read the catalog, do not recall it

The profile and module sets are declared in the template and change there without a release
here. Read them at the moment of use:

- `bun run init --help` prints the supported profiles and the module ids it accepts.
- `template/manifests/catalog.ts` in `morhaf-labs/founder-stack-v2` is where they are declared.

A module list quoted from memory is how a project acquires a capability that no longer exists
or misses one that does. This reference deliberately names neither set.

## The profile is the one irreversible choice

The profile binds who owns product data, metered usage and billing in the generated schema:
either the individual user, or a tenant with memberships and roles. Every table, query and
billing decision after initialization follows from it.

Choose it from how the product is sold and used, not from which option looks more capable.
Changing it afterwards is a product migration with its own change and its own data
migration - it is never an initializer rerun, and treating it as one is how a working project
gets replaced by a fresh one.

Module selections are cheaper to revisit: a module can be added later as ordinary product
work. The profile cannot.

## Refuse

- **A capability with no module in the catalog.** Offer the nearest module the catalog does
  declare, or propose a change in the template that adds one. Hand-writing the integration
  into a project being created spends the template's guarantee - the composition validation
  and the exclusion proofs - on the first day of the project's life.
- **Hand-scaffolded application structure in place of the generator.** If initialization is
  inconvenient, unavailable, or already complete, that is a reason to stop and say so. An
  application assembled by hand looks like a generated one and carries none of the same
  proofs.
- **A second initialization.** A successful initialization is recorded in the generated
  project and the initializer refuses to run again. Later work is normal product evolution,
  in the project's own repository, by its own changes.
- **A template chosen before the shape is classified.** Resemblance to another repository is
  not a classification.

## What the generated project already has

Do not propose these as new work:

- Its own CI on the organization runner, calling the shared workflow-security workflow, and
  an audit of the agent guidance installed during generation.
- This package, installed and pinned, with its lockfile committed.
- A `renovate.json` extending the organization baseline.
- Cloudflare Workers as its only production runtime, and guidance in its own `AGENTS.md`
  saying so. Adopting the VPS platform is a separate declared decision, never implicit.

Provider accounts, OAuth clients, verified domains and secret values are not created by the
initializer. The generated `SETUP.md` lists the ones the selection actually needs.
