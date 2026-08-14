import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
SKILL_PATH = Path("skills/deploy-to-morhaf-vps/SKILL.md")
TARGET_SKILL_PATHS = (
    Path(".agents/skills/deploy-to-morhaf-vps/SKILL.md"),
    Path(".claude/skills/deploy-to-morhaf-vps/SKILL.md"),
)
LOCAL_SKILL_PATHS = (
    Path(".agents/skills/local-only/SKILL.md"),
    Path(".claude/skills/local-only/SKILL.md"),
)
LOCAL_SKILL = b"""---
name: local-only
description: Unrelated local skill preserved during package audits.
---

# Local only

This file is not owned by the package.
"""
CONSUMER_MANIFEST = """name: integrity-fixture
version: 0.0.0
description: Synthetic consumer for APM integrity verification
targets:
  - codex
  - copilot
  - claude
dependencies:
  apm: []
  mcp: []
includes: []
scripts: {}
"""


def run_apm(*args, cwd, check=True):
    result = subprocess.run(
        ("apm", *args),
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )
    if check and result.returncode != 0:
        raise AssertionError(f"apm {' '.join(args)} failed:\n{result.stdout}\n{result.stderr}")
    return result


class APMIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tempdir = tempfile.TemporaryDirectory()
        cls.temp_root = Path(cls.tempdir.name)
        pack_dir = cls.temp_root / "pack"
        run_apm(
            "pack",
            "--archive",
            "--marketplace",
            "none",
            "--output",
            str(pack_dir),
            cwd=ROOT,
        )
        bundles = list(pack_dir.glob("agent-config-*.zip"))
        if len(bundles) != 1:
            raise AssertionError(f"expected one package archive, found {bundles}")
        cls.bundle = bundles[0]

    @classmethod
    def tearDownClass(cls):
        cls.tempdir.cleanup()

    def install_bundle(self, consumer):
        run_apm(
            "install",
            str(self.bundle),
            "--target",
            "codex,copilot,claude",
            "--no-policy",
            cwd=consumer,
        )

    def test_integrity_mismatch_fails_before_replacing_installed_guidance(self):
        consumer = self.temp_root / "integrity-consumer"
        consumer.mkdir()
        self.install_bundle(consumer)
        installed_before = {path: (consumer / path).read_bytes() for path in TARGET_SKILL_PATHS}

        tampered = self.temp_root / "tampered"
        with ZipFile(self.bundle) as archive:
            archive.extractall(tampered)
            bundle_root = tampered / archive.namelist()[0].split("/", 1)[0]
        skill = bundle_root / SKILL_PATH
        skill.write_bytes(skill.read_bytes() + b"\ntampered package content\n")

        result = run_apm(
            "install",
            str(bundle_root),
            "--target",
            "codex,copilot,claude",
            "--no-policy",
            cwd=consumer,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        output = result.stdout + result.stderr
        self.assertIn("Bundle integrity check failed", output)
        self.assertIn(str(SKILL_PATH), output)
        self.assertEqual(
            installed_before,
            {path: (consumer / path).read_bytes() for path in TARGET_SKILL_PATHS},
        )

    def test_drift_reports_only_owned_paths_and_preserves_local_skills(self):
        consumer = self.temp_root / "drift-consumer"
        consumer.mkdir()
        (consumer / "apm.yml").write_text(CONSUMER_MANIFEST)
        for path in LOCAL_SKILL_PATHS:
            target = consumer / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(LOCAL_SKILL)

        self.install_bundle(consumer)
        owned = consumer / TARGET_SKILL_PATHS[0]
        owned.write_bytes(owned.read_bytes() + b"\ntampered installed content\n")

        result = run_apm(
            "audit",
            "--ci",
            "--no-policy",
            "--no-fail-fast",
            "--format",
            "json",
            cwd=consumer,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        report = json.loads(result.stdout)
        details = [
            detail
            for check in report["checks"]
            if not check["passed"]
            for detail in check["details"]
        ]
        self.assertEqual(len(details), 1)
        self.assertIn(str(TARGET_SKILL_PATHS[0]), details[0])
        self.assertNotIn("local-only", result.stdout + result.stderr)
        for path in LOCAL_SKILL_PATHS:
            self.assertEqual((consumer / path).read_bytes(), LOCAL_SKILL)


if __name__ == "__main__":
    unittest.main()
