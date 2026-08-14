import json
import re
import sys
from pathlib import Path, PurePosixPath
from zipfile import ZipFile


EXPECTED_FILES = {
    "apm.lock.yaml",
    "plugin.json",
    "skills/deploy-to-morhaf-vps/SKILL.md",
    "skills/deploy-to-morhaf-vps/references/post-release-verification.md",
    "skills/deploy-to-morhaf-vps/references/release-caller-review.md",
    "skills/deploy-to-morhaf-vps/references/runtime-ownership.md",
    "skills/deploy-to-morhaf-vps/references/vps-application-contract.md",
    "skills/morhaf-labs-project-standards/SKILL.md",
    "skills/morhaf-labs-project-standards/references/blacksmith-ci.md",
    "skills/morhaf-labs-project-standards/references/dependency-policy.md",
    "skills/morhaf-labs-project-standards/references/governance.md",
    "skills/morhaf-labs-project-standards/references/project-shape-routing.md",
    "skills/morhaf-labs-project-standards/references/public-repositories.md",
    "skills/morhaf-labs-project-standards/references/repository-classification.md",
    "skills/morhaf-labs-project-standards/references/workflow-security.md",
}
FORBIDDEN_CONTENT = (
    re.compile(rb"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(rb"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(rb"(?i)\b(password|private[_-]?key|secret|token)\s*[:=]\s*['\"][^'\"]+['\"]"),
    # The package is public and describes private repositories. Naming an owner is
    # intended; carrying its hostnames, stack names or tailnet tags is not.
    re.compile(rb"(?i)(morhaf\.dev|\bcpu555\b|\btag:(ci|vps|k8s)\b)"),
)


def main():
    bundle = Path(sys.argv[1])
    if not bundle.is_file():
        raise SystemExit(f"release bundle not found: {bundle}")

    with ZipFile(bundle) as archive:
        members = [PurePosixPath(name) for name in archive.namelist() if not name.endswith("/")]
        roots = {member.parts[0] for member in members}
        if len(roots) != 1:
            raise SystemExit(f"release bundle must have one root directory: {sorted(roots)}")

        root = roots.pop()
        metadata = json.loads(archive.read(f"{root}/plugin.json"))
        expected_root = f"{metadata['name']}-{metadata['version']}"
        if root != expected_root:
            raise SystemExit(f"release root mismatch: expected {expected_root}, found {root}")
        if metadata != json.loads(Path("plugin.json").read_text()):
            raise SystemExit("release plugin metadata differs from the reviewed source")

        actual = {str(member.relative_to(root)) for member in members}
        if actual != EXPECTED_FILES:
            missing = sorted(EXPECTED_FILES - actual)
            unexpected = sorted(actual - EXPECTED_FILES)
            raise SystemExit(f"release content mismatch; missing={missing}, unexpected={unexpected}")

        for member in members:
            content = archive.read(str(member))
            for pattern in FORBIDDEN_CONTENT:
                if pattern.search(content):
                    raise SystemExit(f"forbidden credential-like content in {member}")

    print(f"verified {len(EXPECTED_FILES)} release files in {bundle.name}")


if __name__ == "__main__":
    main()
