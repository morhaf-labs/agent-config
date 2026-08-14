import copy
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"
FULL_SHA = re.compile(r"^[0-9a-f]{40}$")
ALLOWED_CREDENTIALS = {"PLATFORM_APP_PRIVATE_KEY"}
ALLOWED_INPUTS = {"app", "dockerfile", "context", "image", "runner", "environment", "ref"}
REQUIRED_APPLICATION_FIELDS = {"tier", "memory", "cpu", "port", "health", "user"}
PROHIBITED_ACTIONS = ("kubectl", "pulumi up", "ssh ", "helm upgrade", "k3s")


def load_fixture(name):
    return json.loads((FIXTURES / name).read_text())


def validate_component(component):
    runtime = component["runtime"]
    actions = [action.lower() for action in component.get("direct_actions", [])]
    if any(token in action for action in actions for token in PROHIBITED_ACTIONS):
        raise ValueError("direct infrastructure or cluster mutation")

    if runtime == "vps":
        workflow = component.get("workflow")
        application = component.get("application")
        if not workflow or not application:
            raise ValueError("VPS components require the owning contracts")
        prefix = "morhaf-labs/vps-infra-v2/.github/workflows/deploy-to-platform.yml@"
        uses = workflow.get("uses", "")
        if not uses.startswith(prefix) or not FULL_SHA.fullmatch(uses.removeprefix(prefix)):
            raise ValueError("mutable or foreign workflow reference")
        credentials = set(workflow.get("credentials", []))
        if not credentials <= ALLOWED_CREDENTIALS:
            raise ValueError("undeclared credential")
        if not set(workflow.get("inputs", [])) <= ALLOWED_INPUTS:
            raise ValueError("undeclared workflow input")
        missing = REQUIRED_APPLICATION_FIELDS - application.keys()
        if application.get("tier") == "burstable":
            missing |= {"memoryRequest", "cpuRequest"} - application.keys()
        if missing:
            raise ValueError(f"missing resource bounds or runtime fields: {sorted(missing)}")
        return "vps-infra-v2"

    if runtime == "cloudflare":
        if component.get("workflow") or component.get("application"):
            raise ValueError("Cloudflare-owned component assigned to VPS")
        return "repository-cloudflare"

    if runtime == "unknown":
        if component.get("workflow") or component.get("application"):
            raise ValueError("unknown component assigned a deployment target")
        return "stop"

    raise ValueError("unrecognized runtime")


def validate_fixture(fixture):
    owners = [validate_component(component) for component in fixture["components"]]
    if owners != fixture["expected_owners"]:
        raise ValueError("fixture ownership expectation does not match declarations")
    return owners


class PackageStructureTests(unittest.TestCase):
    def test_package_contains_one_skill_and_no_stronger_primitive(self):
        skill_root = ROOT / ".apm" / "skills"
        self.assertEqual([path.name for path in skill_root.iterdir()], ["deploy-to-morhaf-vps"])
        for prohibited in ("agents", "prompts", "hooks", "bin", "mcp"):
            self.assertFalse((ROOT / ".apm" / prohibited).exists())

    def test_skill_frontmatter_and_references(self):
        skill = (ROOT / ".apm" / "skills" / "deploy-to-morhaf-vps" / "SKILL.md").read_text()
        self.assertTrue(skill.startswith("---\nname: deploy-to-morhaf-vps\ndescription: Use when"))
        for name in (
            "runtime-ownership.md",
            "vps-application-contract.md",
            "release-caller-review.md",
            "post-release-verification.md",
        ):
            self.assertTrue((ROOT / ".apm" / "skills" / "deploy-to-morhaf-vps" / "references" / name).is_file())

    def test_manifest_has_no_marketplace_or_executable_dependency(self):
        manifest = (ROOT / "apm.yml").read_text()
        self.assertNotIn("marketplace:", manifest)
        self.assertIn("type: skill", manifest)
        self.assertIn("mcp: []", manifest)
        self.assertIn("scripts: {}", manifest)


class FixturePolicyTests(unittest.TestCase):
    def test_reference_shapes(self):
        for name in (
            "simple-vps-service.json",
            "full-vps-application.json",
            "hybrid-cloudflare-runner.json",
            "unknown-component.json",
        ):
            with self.subTest(name=name):
                validate_fixture(load_fixture(name))

    def test_rejects_direct_cluster_mutation(self):
        fixture = load_fixture("simple-vps-service.json")
        fixture["components"][0]["direct_actions"] = ["kubectl apply -f rendered.yaml"]
        with self.assertRaisesRegex(ValueError, "direct infrastructure or cluster mutation"):
            validate_fixture(fixture)

    def test_rejects_undeclared_credentials(self):
        fixture = load_fixture("simple-vps-service.json")
        fixture["components"][0]["workflow"]["credentials"].append("KUBECONFIG")
        with self.assertRaisesRegex(ValueError, "undeclared credential"):
            validate_fixture(fixture)

    def test_rejects_mutable_workflow_reference(self):
        fixture = load_fixture("simple-vps-service.json")
        fixture["components"][0]["workflow"]["uses"] = (
            "morhaf-labs/vps-infra-v2/.github/workflows/deploy-to-platform.yml@main"
        )
        with self.assertRaisesRegex(ValueError, "mutable or foreign workflow reference"):
            validate_fixture(fixture)

    def test_rejects_missing_resource_bounds(self):
        fixture = load_fixture("simple-vps-service.json")
        del fixture["components"][0]["application"]["memory"]
        with self.assertRaisesRegex(ValueError, "missing resource bounds"):
            validate_fixture(fixture)

    def test_rejects_cloudflare_component_assigned_to_vps(self):
        fixture = load_fixture("hybrid-cloudflare-runner.json")
        cloudflare = fixture["components"][1]
        cloudflare["workflow"] = copy.deepcopy(fixture["components"][0]["workflow"])
        with self.assertRaisesRegex(ValueError, "Cloudflare-owned component assigned to VPS"):
            validate_fixture(fixture)


if __name__ == "__main__":
    unittest.main()
