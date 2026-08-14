"""Producer tests for the repository-standards skill.

These test a *model* of the standard against declarative fixtures, in the same shape as
`test_package.py`: one router, eight repository shapes, and negative tests that mutate a
fixture and assert the specific refusal.

They deliberately do not grep SKILL.md for sentences. A test that asserts on wording
passes forever and proves nothing about the decision the wording describes - and the
wording is the part most likely to be rewritten for clarity without any decision
changing.
"""

import copy
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"
SKILL = ROOT / ".apm" / "skills" / "morhaf-labs-project-standards"

FULL_SHA = re.compile(r"^[0-9a-f]{40}$")
EXPRESSION = re.compile(r"^\$\{\{.*\}\}$")

# Refused by prefix rather than by an exhaustive list, so a label GitHub ships tomorrow
# is caught and a Blacksmith size shipped tomorrow is not.
NATIVE_RUNNER = re.compile(r"^(ubuntu|windows|macos)(-|$)")

# The organization release age for normal patch and minor updates. Held here only so a
# fixture can express "shorter than the baseline"; the value itself lives in the
# owning preset.
BASELINE_RELEASE_AGE_DAYS = 5

ACTIVE_LIFECYCLES = {"active", "template", "rehearsal"}
DORMANT_LIFECYCLES = {"legacy", "archived"}

SHAPES_WITHOUT_DEPLOYMENT = {"infrastructure", "library", "public-producer"}

VPS_WORKFLOW_PREFIX = "morhaf-labs/vps-infra-v2/.github/workflows/deploy-to-platform.yml@"


def load(name):
    return json.loads((FIXTURES / name).read_text())


def check_lifecycle(repo):
    lifecycle = repo["lifecycle"]
    if lifecycle not in ACTIVE_LIFECYCLES | DORMANT_LIFECYCLES:
        raise ValueError("unrecognized lifecycle")

    unconfirmed = not repo["lifecycle_confirmed"] or lifecycle in DORMANT_LIFECYCLES
    if unconfirmed and repo["proposed_work"] != "none":
        raise ValueError("maintenance on an unconfirmed or superseded repository")
    return "stop" if unconfirmed else "adopt"


def check_renovate(repo):
    policy = repo["renovate"]
    if not policy["extends_organization_baseline"]:
        raise ValueError("dependency policy does not extend the organization baseline")
    if policy["second_update_producer"]:
        raise ValueError("second dependency-update producer beside Renovate")
    if policy["ignore_tests"]:
        raise ValueError("dependency policy disables the check gate")
    if policy["automerge_non_security_major"]:
        raise ValueError("dependency policy automerges a non-security major")

    age = policy["local_minimum_release_age_days"]
    if age is not None and age < BASELINE_RELEASE_AGE_DAYS:
        raise ValueError("dependency policy shortens the organization release age")

    for exception in policy["stricter_exceptions"]:
        local_age = exception.get("minimum_release_age_days")
        if local_age is not None and local_age < BASELINE_RELEASE_AGE_DAYS:
            raise ValueError("dependency policy shortens the organization release age")
        if exception.get("automerge") not in (None, False):
            raise ValueError("local exception loosens the organization lane")


def check_workflow(workflow, visibility):
    runs_on = workflow["runs_on"]
    if not EXPRESSION.fullmatch(runs_on) and NATIVE_RUNNER.match(runs_on):
        raise ValueError("native GitHub-hosted runner")

    for ref in workflow["action_refs"]:
        _, _, revision = ref.partition("@")
        if not FULL_SHA.fullmatch(revision):
            raise ValueError("mutable action reference")

    permissions = workflow["permissions"]
    if not permissions or permissions == "write-all":
        raise ValueError("widened workflow permissions")

    if workflow["timeout_minutes"] is None:
        raise ValueError("unbounded job")

    triggers = workflow["triggers"]
    if "pull_request_target" in triggers:
        raise ValueError("privileged fork trigger")
    if visibility == "public" and "pull_request" in triggers and workflow["secrets"]:
        raise ValueError("secret exposed to fork code")

    # A public repository cannot call a private reusable workflow at all, so proposing
    # the shared caller there produces a zero-second run with no job and no explanation.
    shared = workflow.get("shared_workflow_security")
    if shared:
        if visibility == "public":
            raise ValueError("public repository cannot call the private shared workflow")
        _, _, revision = shared.partition("@")
        if not FULL_SHA.fullmatch(revision):
            raise ValueError("mutable action reference")


def route_component(component, shape):
    runtime = component["runtime"]

    if shape in SHAPES_WITHOUT_DEPLOYMENT:
        raise ValueError("invented deployment target")

    if runtime == "cloudflare":
        if component["vps_workflow"]:
            raise ValueError("invented deployment target")
        return "cloudflare-founder-stack-v2"

    if runtime == "vps":
        workflow = component["vps_workflow"] or ""
        if not workflow.startswith(VPS_WORKFLOW_PREFIX):
            raise ValueError("VPS component without the owning platform workflow")
        if not FULL_SHA.fullmatch(workflow.removeprefix(VPS_WORKFLOW_PREFIX)):
            raise ValueError("mutable action reference")
        return "vps-infra-v2"

    if runtime == "unknown":
        if component["vps_workflow"]:
            raise ValueError("invented deployment target")
        return "stop"

    raise ValueError("unrecognized runtime")


def validate_repository(repo):
    """Route a repository declaration, or raise the specific refusal."""
    action = check_lifecycle(repo)
    if action == "stop":
        return {"owners": [route_component(c, repo["shape"]) for c in repo["components"]],
                "action": "stop"}

    check_renovate(repo)
    for workflow in repo["workflows"]:
        check_workflow(workflow, repo["visibility"])

    owners = [route_component(c, repo["shape"]) for c in repo["components"]]
    if "stop" in owners:
        action = "stop"

    if repo["visibility"] == "public":
        health = repo.get("community_health") or {}
        missing = [key for key, present in health.items() if not present]
        if not health or missing:
            raise ValueError("public repository missing its local baseline")

    return {"owners": owners, "action": action}


def validate_fixture(repo):
    result = validate_repository(repo)
    if result != repo["expected"]:
        raise ValueError(f"routing does not match the fixture expectation: {result}")
    return result


SHAPE_FIXTURES = (
    "repo-private-saas.json",
    "repo-vps-service.json",
    "repo-hybrid-application.json",
    "repo-infrastructure.json",
    "repo-library.json",
    "repo-public-producer.json",
    "repo-unknown-owner.json",
    "repo-superseded.json",
)


class ShapeCoverageTests(unittest.TestCase):
    def test_every_declared_shape_has_a_fixture_and_routes(self):
        shapes = set()
        for name in SHAPE_FIXTURES:
            with self.subTest(fixture=name):
                repo = load(name)
                validate_fixture(repo)
                shapes.add(repo["shape"])
        self.assertEqual(
            shapes,
            {"saas", "vps-service", "hybrid", "infrastructure", "library",
             "public-producer", "unknown"},
        )

    def test_hybrid_keeps_each_component_with_its_own_owner(self):
        result = validate_repository(load("repo-hybrid-application.json"))
        self.assertEqual(result["owners"], ["cloudflare-founder-stack-v2", "vps-infra-v2"])


class RunnerTests(unittest.TestCase):
    def test_rejects_native_runner(self):
        for label in ("ubuntu-latest", "ubuntu-24.04", "macos-15", "windows-2022"):
            with self.subTest(label=label):
                repo = load("repo-vps-service.json")
                repo["workflows"][0]["runs_on"] = label
                with self.assertRaisesRegex(ValueError, "native GitHub-hosted runner"):
                    validate_repository(repo)

    def test_accepts_blacksmith_self_hosted_and_caller_expressions(self):
        for label in ("blacksmith-2vcpu-ubuntu-2404", "blacksmith-8vcpu-ubuntu-2404",
                      "self-hosted", "${{ inputs.runner }}"):
            with self.subTest(label=label):
                repo = load("repo-vps-service.json")
                repo["workflows"][0]["runs_on"] = label
                validate_repository(repo)


class WorkflowSecurityTests(unittest.TestCase):
    def test_rejects_mutable_action_reference(self):
        repo = load("repo-vps-service.json")
        repo["workflows"][0]["action_refs"] = ["actions/checkout@v4"]
        with self.assertRaisesRegex(ValueError, "mutable action reference"):
            validate_repository(repo)

    def test_rejects_mutable_shared_workflow_reference(self):
        repo = load("repo-vps-service.json")
        repo["workflows"][0]["shared_workflow_security"] = (
            "morhaf-labs/.github/.github/workflows/workflow-security.yml@main"
        )
        with self.assertRaisesRegex(ValueError, "mutable action reference"):
            validate_repository(repo)

    def test_rejects_widened_permissions(self):
        for permissions in ("write-all", {}, None):
            with self.subTest(permissions=permissions):
                repo = load("repo-vps-service.json")
                repo["workflows"][0]["permissions"] = permissions
                with self.assertRaisesRegex(ValueError, "widened workflow permissions"):
                    validate_repository(repo)

    def test_rejects_unbounded_job(self):
        repo = load("repo-vps-service.json")
        repo["workflows"][0]["timeout_minutes"] = None
        with self.assertRaisesRegex(ValueError, "unbounded job"):
            validate_repository(repo)

    def test_rejects_privileged_fork_trigger(self):
        repo = load("repo-public-producer.json")
        repo["workflows"][0]["triggers"] = ["pull_request_target"]
        with self.assertRaisesRegex(ValueError, "privileged fork trigger"):
            validate_repository(repo)

    def test_rejects_secret_reachable_from_fork_code(self):
        repo = load("repo-public-producer.json")
        repo["workflows"][0]["secrets"] = ["NPM_TOKEN"]
        with self.assertRaisesRegex(ValueError, "secret exposed to fork code"):
            validate_repository(repo)

    # The release job carries a token on a push trigger, which fork code cannot reach.
    # Asserted so the rule above cannot be tightened into refusing every secret.
    def test_allows_a_secret_on_a_trigger_fork_code_cannot_reach(self):
        validate_repository(load("repo-public-producer.json"))


class DependencyPolicyTests(unittest.TestCase):
    def test_rejects_repository_that_does_not_extend_the_baseline(self):
        repo = load("repo-vps-service.json")
        repo["renovate"]["extends_organization_baseline"] = False
        with self.assertRaisesRegex(ValueError, "does not extend the organization baseline"):
            validate_repository(repo)

    def test_rejects_shortened_release_age(self):
        repo = load("repo-vps-service.json")
        repo["renovate"]["local_minimum_release_age_days"] = 1
        with self.assertRaisesRegex(ValueError, "shortens the organization release age"):
            validate_repository(repo)

    def test_rejects_shortened_release_age_hidden_in_a_package_exception(self):
        repo = load("repo-hybrid-application.json")
        repo["renovate"]["stricter_exceptions"][0]["minimum_release_age_days"] = 2
        with self.assertRaisesRegex(ValueError, "shortens the organization release age"):
            validate_repository(repo)

    def test_rejects_disabled_check_gate(self):
        repo = load("repo-vps-service.json")
        repo["renovate"]["ignore_tests"] = True
        with self.assertRaisesRegex(ValueError, "disables the check gate"):
            validate_repository(repo)

    def test_rejects_automerged_non_security_major(self):
        repo = load("repo-vps-service.json")
        repo["renovate"]["automerge_non_security_major"] = True
        with self.assertRaisesRegex(ValueError, "automerges a non-security major"):
            validate_repository(repo)

    def test_rejects_a_second_update_producer(self):
        repo = load("repo-vps-service.json")
        repo["renovate"]["second_update_producer"] = True
        with self.assertRaisesRegex(ValueError, "second dependency-update producer"):
            validate_repository(repo)

    # Stricter is always allowed, and the infrastructure fixture is the reason: merging
    # there applies the platform, so automerge is refused for anything that can change
    # what is running.
    def test_allows_stricter_local_exceptions(self):
        result = validate_repository(load("repo-infrastructure.json"))
        self.assertEqual(result["action"], "adopt")


class DeploymentTargetTests(unittest.TestCase):
    def test_rejects_invented_target_on_a_shape_that_deploys_nothing(self):
        repo = load("repo-library.json")
        repo["components"] = [{"name": "web", "runtime": "cloudflare", "vps_workflow": None}]
        with self.assertRaisesRegex(ValueError, "invented deployment target"):
            validate_repository(repo)

    def test_rejects_target_assigned_to_an_unknown_component(self):
        repo = load("repo-unknown-owner.json")
        repo["components"][0]["vps_workflow"] = (
            f"{VPS_WORKFLOW_PREFIX}{'a' * 40}"
        )
        with self.assertRaisesRegex(ValueError, "invented deployment target"):
            validate_repository(repo)

    def test_rejects_cloudflare_component_given_the_vps_workflow(self):
        repo = load("repo-hybrid-application.json")
        repo["components"][0]["vps_workflow"] = repo["components"][1]["vps_workflow"]
        with self.assertRaisesRegex(ValueError, "invented deployment target"):
            validate_repository(repo)

    def test_rejects_vps_component_without_the_owning_workflow(self):
        repo = load("repo-vps-service.json")
        repo["components"][0]["vps_workflow"] = None
        with self.assertRaisesRegex(ValueError, "without the owning platform workflow"):
            validate_repository(repo)


class LifecycleTests(unittest.TestCase):
    def test_superseded_repository_stops_rather_than_adopting(self):
        result = validate_repository(load("repo-superseded.json"))
        self.assertEqual(result["action"], "stop")

    def test_rejects_maintenance_on_an_unconfirmed_repository(self):
        repo = load("repo-superseded.json")
        repo["proposed_work"] = "adopt-standards"
        with self.assertRaisesRegex(ValueError, "unconfirmed or superseded repository"):
            validate_repository(repo)

    # An active repository whose lifecycle nobody has confirmed is the same refusal.
    # This is the case that looks safe and is not: it has recent commits and green CI.
    def test_rejects_maintenance_on_an_unconfirmed_active_repository(self):
        repo = load("repo-vps-service.json")
        repo["lifecycle_confirmed"] = False
        with self.assertRaisesRegex(ValueError, "unconfirmed or superseded repository"):
            validate_repository(repo)


class PublicRepositoryTests(unittest.TestCase):
    def test_rejects_public_repository_calling_the_private_shared_workflow(self):
        repo = load("repo-public-producer.json")
        repo["workflows"][0]["shared_workflow_security"] = (
            "morhaf-labs/.github/.github/workflows/workflow-security.yml@" + "b" * 40
        )
        with self.assertRaisesRegex(ValueError, "cannot call the private shared workflow"):
            validate_repository(repo)

    def test_rejects_public_repository_missing_its_local_baseline(self):
        for key in ("license", "security_policy", "contributing", "secret_scanning",
                    "push_protection", "release_checksums"):
            with self.subTest(missing=key):
                repo = load("repo-public-producer.json")
                repo["community_health"][key] = False
                with self.assertRaisesRegex(ValueError, "missing its local baseline"):
                    validate_repository(repo)

    # This repository is the fixture, so the claim is checked against the real tree
    # rather than only against JSON.
    def test_this_repository_carries_the_files_the_fixture_claims(self):
        for name in ("LICENSE", "SECURITY.md"):
            self.assertTrue((ROOT / name).is_file(), name)


class SkillContentTests(unittest.TestCase):
    """The few structural claims worth asserting on the skill itself."""

    def test_intent_first_description_covers_repository_work(self):
        text = (SKILL / "SKILL.md").read_text()
        self.assertTrue(text.startswith("---\nname: morhaf-labs-project-standards\n"))
        description = text.split("description:", 1)[1].split("\n", 1)[0].lower()
        for intent in ("creating", "adopting", "auditing", "repository automation"):
            self.assertIn(intent, description)

    def test_every_reference_the_workflow_names_exists(self):
        text = (SKILL / "SKILL.md").read_text()
        referenced = set(re.findall(r"\(references/([a-z-]+\.md)\)", text))
        present = {path.name for path in (SKILL / "references").iterdir()}
        self.assertEqual(referenced, present)

    # The public-content boundary, checked mechanically rather than by reading. A
    # private hostname, stack name or tailnet tag is the failure this catches.
    #
    # Note what is deliberately *not* forbidden: "kubeconfig", "Doppler token" and the
    # like. Naming a credential type an agent must never add is the guidance doing its
    # job - the first version of this test refused those and would have deleted the
    # authority boundary to satisfy itself.
    def test_guidance_carries_no_private_operational_detail(self):
        forbidden = re.compile(
            r"(morhaf\.dev|\bcpu555\b|\btag:(ci|vps|k8s)\b"
            r"|\b\d{1,3}(\.\d{1,3}){3}\b|[A-Z_]{4,}_TOKEN\s*[:=])",
            re.IGNORECASE,
        )
        for path in sorted(SKILL.rglob("*.md")):
            with self.subTest(path=path.name):
                self.assertIsNone(forbidden.search(path.read_text()))


if __name__ == "__main__":
    unittest.main()
