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


def documented_capabilities():
    """Capability name -> value, read from the README capability table."""
    document = (ROOT / "README.md").read_text().split("\n## Capabilities\n", 1)
    if len(document) == 1:
        return {}
    section = document[1].split("\n## ", 1)[0]
    rows = {}
    for line in section.splitlines():
        cells = [cell.strip() for cell in line.split("|")[1:-1]]
        if len(cells) != 2 or cells[0] in ("Capability", "---"):
            continue
        rows[cells[0].strip("`")] = cells[1]
    return rows


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
    # An exact set rather than a length check, so a third skill stays a deliberate
    # decision instead of arriving because a test only counted.
    def test_package_contains_the_declared_skills_and_no_stronger_primitive(self):
        skill_root = ROOT / ".apm" / "skills"
        self.assertEqual(
            sorted(path.name for path in skill_root.iterdir()),
            ["deploy-to-morhaf-vps", "morhaf-labs-project-standards"],
        )
        for prohibited in ("agents", "prompts", "hooks", "bin", "mcp"):
            self.assertFalse((ROOT / ".apm" / prohibited).exists())

    def test_skill_frontmatter_and_references(self):
        expected = {
            "deploy-to-morhaf-vps": (
                "runtime-ownership.md",
                "vps-application-contract.md",
                "release-caller-review.md",
                "post-release-verification.md",
            ),
            "morhaf-labs-project-standards": (
                "repository-classification.md",
                "dependency-policy.md",
                "blacksmith-ci.md",
                "workflow-security.md",
                "project-shape-routing.md",
                "founder-stack-v2.md",
                "governance.md",
                "public-repositories.md",
            ),
        }
        for skill_name, references in expected.items():
            with self.subTest(skill=skill_name):
                skill_dir = ROOT / ".apm" / "skills" / skill_name
                skill = (skill_dir / "SKILL.md").read_text()
                self.assertTrue(
                    skill.startswith(f"---\nname: {skill_name}\ndescription: Use when")
                )
                for name in references:
                    self.assertTrue((skill_dir / "references" / name).is_file(), name)

    # Set equality against the installed skills, never an assertion on sentences: a claim
    # about what the package provides must not outlive the primitive it describes, and the
    # stale "first and only primitive" line this replaced is the evidence that one place is
    # already hard enough to keep true.
    def test_documented_capabilities_match_the_installed_skills(self):
        self.assertEqual(
            set(documented_capabilities()),
            {path.name for path in (ROOT / ".apm" / "skills").iterdir()},
        )

    def test_every_documented_capability_carries_a_value(self):
        for capability, value in documented_capabilities().items():
            with self.subTest(capability=capability):
                self.assertTrue(value.strip())

    def test_manifest_has_no_marketplace_or_executable_dependency(self):
        manifest = (ROOT / "apm.yml").read_text()
        self.assertNotIn("marketplace:", manifest)
        self.assertIn("type: skill", manifest)
        self.assertIn("mcp: []", manifest)
        self.assertIn("scripts: {}", manifest)


class ReleaseWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.workflow = (ROOT / ".github" / "workflows" / "release.yml").read_text()

    def test_tag_must_match_manifest_version(self):
        self.assertIn('expected_tag="v${package_version}"', self.workflow)
        self.assertIn('test "$GITHUB_REF_NAME" = "$expected_tag"', self.workflow)

    def test_sidecar_verifies_in_downloaded_layout(self):
        self.assertIn(
            '(cd dist && sha256sum "$bundle_name" > "$bundle_name.sha256")',
            self.workflow,
        )
        self.assertIn(
            '(cd "$verify_dir" && sha256sum -c "$bundle_name.sha256")',
            self.workflow,
        )

    def test_token_is_exposed_only_to_publish_step(self):
        pack, publish = self.workflow.split("      - name: Publish verified release\n", 1)
        self.assertNotIn("GH_TOKEN:", pack)
        self.assertIn("GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}", publish)


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
