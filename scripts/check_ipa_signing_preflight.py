#!/usr/bin/env python3
"""Read-only IPA signing preflight for LilaShift.

This tool does NOT sign an IPA, validate executable code signatures, authenticate
certificates, install an app, use Apple IDs or process P12 private keys.
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
import plistlib
import re
import subprocess
import sys
import zipfile
from pathlib import Path

APP_INFO = re.compile(r"^(Payload/[^/]+\.app)/Info\.plist$")
EXT_INFO = re.compile(r"^(Payload/[^/]+\.app/PlugIns/[^/]+\.appex)/Info\.plist$")
GROUP_KEY = "com.apple.security.application-groups"


def issue(issues, severity, code, message):
    issues.append({"severity": severity, "code": code, "message": message})


def read_profile(raw):
    """Decode metadata. This is NOT proof of an Apple-issued/valid signature."""
    try:
        data = plistlib.loads(raw)
        if isinstance(data, dict):
            return data
    except (ValueError, TypeError, plistlib.InvalidFileException):
        pass
    try:
        proc = subprocess.run(
            ["openssl", "cms", "-verify", "-inform", "DER", "-noverify"],
            input=raw, capture_output=True, timeout=8, check=False,
        )
        if proc.returncode == 0:
            data = plistlib.loads(proc.stdout)
            if isinstance(data, dict):
                return data
    except (OSError, subprocess.TimeoutExpired, ValueError, plistlib.InvalidFileException):
        pass
    return None


def app_id_allows(profile_id, bundle_id):
    suffix = profile_id.split(".", 1)[-1]
    return bundle_id.startswith(suffix[:-1]) if suffix.endswith("*") else suffix == bundle_id


def profile_info(zf, names, root, bundle_id, issues):
    path = root + "/embedded.mobileprovision"
    empty = {"status": "unknown", "team": None, "groups": [], "expires_at": None}
    if path not in names:
        issue(issues, "warning", "PROFILE_ABSENT",
              f"{root}: embedded profile absent (IPA may be prepared for later re-signing)")
        return empty
    if zf.getinfo(path).file_size > 3_000_000:
        issue(issues, "error", "PROFILE_TOO_LARGE", f"{root}: unusually large profile")
        return empty
    profile = read_profile(zf.read(path))
    if profile is None:
        issue(issues, "warning", "PROFILE_UNREADABLE",
              f"{root}: cannot inspect provisioning profile entitlements")
        return empty
    ent = profile.get("Entitlements", {})
    if not isinstance(ent, dict):
        ent = {}
    teams = profile.get("TeamIdentifier", [])
    team = str(teams[0]) if isinstance(teams, list) and teams else None
    aid = ent.get("application-identifier") or ent.get("com.apple.application-identifier")
    if isinstance(aid, str) and not app_id_allows(aid, bundle_id):
        issue(issues, "error", "BUNDLE_ID_MISMATCH",
              f"{root}: provisioning App ID does not allow {bundle_id}")
    elif not isinstance(aid, str):
        issue(issues, "warning", "APP_ID_UNKNOWN", f"{root}: no application-identifier")
    groups = ent.get(GROUP_KEY, [])
    groups = sorted(set(g for g in groups if isinstance(g, str))) if isinstance(groups, list) else []
    expires_at = None
    expiry = profile.get("ExpirationDate")
    if isinstance(expiry, dt.datetime):
        expiry = expiry.replace(tzinfo=expiry.tzinfo or dt.timezone.utc)
        expires_at = expiry.isoformat()
        if expiry < dt.datetime.now(dt.timezone.utc):
            issue(issues, "error", "PROFILE_EXPIRED", f"{root}: profile expired")
    else:
        issue(issues, "warning", "EXPIRY_UNKNOWN", f"{root}: expiry not available")
    return {"status": "decoded_not_verified", "team": team, "groups": groups, "expires_at": expires_at}


def inspect_ipa(path, *, require_share_extension=True):
    """Examine an IPA without extracting or modifying its files."""
    result = {
        "ipa": str(path), "conclusion": "unknown", "main": None,
        "extensions": [], "issues": [],
        "limitations": "Structural metadata only. Does not verify executable signatures, certificates, runtime App Group access or installation.",
    }
    issues = result["issues"]
    try:
        with zipfile.ZipFile(path) as zf:
            names = set(zf.namelist())
            mains = [m.group(1) for p in names if (m := APP_INFO.fullmatch(p))]
            if len(mains) != 1:
                issue(issues, "error", "MAIN_APP_COUNT",
                      f"expected one Payload/*.app/Info.plist, found {len(mains)}")
                result["conclusion"] = "needs_attention"
                return result
            root = mains[0]
            exts = sorted(m.group(1) for p in names
                          if (m := EXT_INFO.fullmatch(p)) and p.startswith(root + "/"))
            if require_share_extension and not exts:
                issue(issues, "error", "EXTENSION_MISSING",
                      "LilaShift share extension not found")
            bundles = []
            for item_root in [root, *exts]:
                info_path = item_root + "/Info.plist"
                try:
                    if zf.getinfo(info_path).file_size > 5_000_000:
                        raise ValueError("Info.plist too large")
                    info = plistlib.loads(zf.read(info_path))
                    bundle_id = info.get("CFBundleIdentifier")
                    if not isinstance(bundle_id, str) or not bundle_id:
                        raise ValueError("CFBundleIdentifier missing")
                except (KeyError, ValueError, TypeError, plistlib.InvalidFileException) as exc:
                    issue(issues, "error", "INFO_INVALID", f"{item_root}: {exc}")
                    continue
                bundles.append({
                    "path": item_root, "bundle_id": bundle_id,
                    "profile": profile_info(zf, names, item_root, bundle_id, issues),
                })
            if not bundles or bundles[0]["path"] != root:
                issue(issues, "error", "MAIN_INVALID", "Cannot inspect main app Info.plist")
            else:
                result["main"], result["extensions"] = bundles[0], bundles[1:]
                mp = bundles[0]["profile"]
                if not mp["groups"]:
                    issue(issues, "warning", "MAIN_GROUP_UNKNOWN",
                          "Main profile does not identify an App Group authorization")
                for extension in bundles[1:]:
                    ep = extension["profile"]
                    if mp["team"] and ep["team"] and mp["team"] != ep["team"]:
                        issue(issues, "error", "TEAM_MISMATCH",
                              f"{extension['bundle_id']}: different main/extension Team IDs")
                    if mp["status"] == "decoded_not_verified" and ep["status"] == "decoded_not_verified":
                        if not set(mp["groups"]) & set(ep["groups"]):
                            issue(issues, "error", "NO_SHARED_APP_GROUP",
                                  f"{extension['bundle_id']}: no common App Group in profiles")
                    else:
                        issue(issues, "warning", "SHARED_GROUP_UNVERIFIED",
                              f"{extension['bundle_id']}: unable to prove shared group from profiles")
    except (OSError, zipfile.BadZipFile, zipfile.LargeZipFile) as exc:
        issue(issues, "error", "IPA_UNREADABLE", str(exc))
    result["conclusion"] = ("needs_attention" if any(x["severity"] == "error" for x in issues)
                            else "incomplete_evidence" if issues else "structural_preflight_only")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ipa", help="local IPA path; IPA is not uploaded")
    parser.add_argument("--no-require-share-extension", action="store_true")
    args = parser.parse_args()
    result = inspect_ipa(Path(args.ipa),
                         require_share_extension=not args.no_require_share_extension)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result["conclusion"] == "needs_attention" else 0


if __name__ == "__main__":
    sys.exit(main())
