#!/usr/bin/env python3
"""Read-only static gate for LilaShift patch source inputs.

This does not test iOS write safety, provide legal certification, or build an IPA.
Safe to run on PRs; it never modifies release assets or system/device files.
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATCH = ROOT / "china-unlock-v107.patch"
REQUIRED = (
    "GestaltX/DevicePlistWriter.swift",
    "GestaltX/AIReadinessCheckup.swift",
    "GestaltX/LiveGestaltProbe.swift",
    "GestaltX/DeviceAIEligibility.swift",
    "GestaltX/USRegulatoryModelMapping.swift",
    "tests/DevicePlistWriterTests.swift",
    "tests/SystemVaultTests.swift",
    "tests/AIReadinessTests.swift",
)
ATTRIBUTION = (
    ("GestaltX", "huamidev", "GPL"),
    ("Erosion-CN", "Kianuni", "GPL"),
    ("MGKeys", "PoomSmart", "MIT"),
    ("Nugget", "AGPL", "AGPL"),
)
SAFE_OUTPUTS = (
    "docs/LILASHIFT_SOURCE_AUDIT.md",
    "docs/LILASHIFT_IMPLEMENTATION_PLAN.md",
    "docs/LILASHIFT_PROVENANCE.md",
    "THIRD_PARTY_NOTICES.md",
)

def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    if not PATCH.is_file():
        print("FAIL: missing patch", file=sys.stderr)
        return 1
    data = PATCH.read_bytes()
    text = data.decode("utf-8", errors="replace")
    sha = hashlib.sha256(data).hexdigest()
    files = set(re.findall(r"^diff --git a/(.+?) b/(.+)$", text, flags=re.M))
    paths = {path for _, path in files}
    print(f"Patch: {len(data):,} bytes; SHA-256={sha}; {len(paths)} changed paths")
    if not text.startswith("diff --git "):
        errors.append("Patch must start with git diff metadata")
    for filename in REQUIRED:
        if filename not in paths:
            errors.append(f"Expected development patch path missing: {filename}")
    for filename in SAFE_OUTPUTS:
        if not (ROOT / filename).is_file():
            errors.append(f"Missing audit/provenance document: {filename}")
    lic = ROOT / "LICENSE"
    if not lic.is_file() or "GNU GENERAL PUBLIC LICENSE" not in lic.read_text(errors="replace"):
        errors.append("Missing original GPL license text")
    notices = (ROOT / "THIRD_PARTY_NOTICES.md").read_text(errors="replace") if (ROOT / "THIRD_PARTY_NOTICES.md").exists() else ""
    source = (ROOT / "docs/LILASHIFT_PROVENANCE.md").read_text(errors="replace") if (ROOT / "docs/LILASHIFT_PROVENANCE.md").exists() else ""
    for project, author, license_hint in ATTRIBUTION:
        combined = notices + source
        if not all(token in combined for token in (project, author, license_hint)):
            errors.append(f"Attribution incomplete for {project}: {author}/{license_hint}")
    if "UNRESOLVED CONFLICT (#178)" in text:
        warnings.append("Audio Intelligence #178 conflict remains unresolved; no claim of validated compatibility")
    if "productType.hasPrefix(\"iPhone19,\")" in text:
        warnings.append("Broad iPhone19 prefix detected; verify exact allowlist before shipping")
    if "if opened >= 0 { return opened }" in text and "O_NOFOLLOW" in text:
        warnings.append("Examine DevicePlistWriter's O_NOFOLLOW fallback and fd identity checks")
    if "GIT binary patch" in text:
        warnings.append("Binary patch assets detected; manually verify original licenses and asset provenance")

    for item in errors:
        print("ERROR: " + item, file=sys.stderr)
    for item in warnings:
        print("REVIEW REQUIRED: " + item)
    print("Result:", "FAIL" if errors else "PASS (static metadata only)")
    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
