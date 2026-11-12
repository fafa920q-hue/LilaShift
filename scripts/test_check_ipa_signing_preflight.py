"""Fixture-only IPA tests: no Apple credentials, devices, or real certs used."""
import datetime as dt
import importlib.util
import plistlib
import tempfile
import unittest
import zipfile
from pathlib import Path

MODULE = Path(__file__).with_name("check_ipa_signing_preflight.py")
spec = importlib.util.spec_from_file_location("ipa_preflight", MODULE)
preflight = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preflight)

MAIN = "Payload/LilaShift.app"
EXT = MAIN + "/PlugIns/ShareExtension.appex"
GROUP = "group.lilashift.example"


def make_profile(bundle, team="TEAM12345", groups=(GROUP,), expired=False):
    return plistlib.dumps({
        "TeamIdentifier": [team],
        "ExpirationDate": dt.datetime(2020 if expired else 2099, 1, 1),
        "Entitlements": {
            "application-identifier": team + "." + bundle,
            "com.apple.security.application-groups": list(groups),
        },
    })


def make_ipa(path, include_extension=True, include_profiles=True,
             main_groups=(GROUP,), ext_groups=(GROUP,), ext_team="TEAM12345",
             expired=False):
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr(MAIN + "/Info.plist",
                    plistlib.dumps({"CFBundleIdentifier": "dev.lilashift.test"}))
        if include_profiles:
            zf.writestr(MAIN + "/embedded.mobileprovision",
                        make_profile("dev.lilashift.test", groups=main_groups, expired=expired))
        if include_extension:
            zf.writestr(EXT + "/Info.plist",
                        plistlib.dumps({"CFBundleIdentifier": "dev.lilashift.test.share"}))
            if include_profiles:
                zf.writestr(EXT + "/embedded.mobileprovision",
                            make_profile("dev.lilashift.test.share",
                                         team=ext_team, groups=ext_groups))


class TestIPAReadiness(unittest.TestCase):
    def inspect_fixture(self, **kwargs):
        with tempfile.TemporaryDirectory() as folder:
            filename = Path(folder) / "sample.ipa"
            make_ipa(filename, **kwargs)
            return preflight.inspect_ipa(filename)

    def test_metadata_only_not_signature_claim(self):
        result = self.inspect_fixture()
        self.assertEqual(result["conclusion"], "structural_preflight_only")
        self.assertIn("Does not verify", result["limitations"])

    def test_missing_share_extension_is_error(self):
        result = self.inspect_fixture(include_extension=False)
        self.assertIn("EXTENSION_MISSING", {x["code"] for x in result["issues"]})
        self.assertEqual(result["conclusion"], "needs_attention")

    def test_different_app_group_is_error(self):
        result = self.inspect_fixture(ext_groups=("group.other",))
        self.assertIn("NO_SHARED_APP_GROUP", {x["code"] for x in result["issues"]})

    def test_different_team_is_error(self):
        result = self.inspect_fixture(ext_team="OTHER1234")
        self.assertIn("TEAM_MISMATCH", {x["code"] for x in result["issues"]})

    def test_expired_provisioning_is_error(self):
        result = self.inspect_fixture(expired=True)
        self.assertIn("PROFILE_EXPIRED", {x["code"] for x in result["issues"]})

    def test_missing_provisioning_is_unknown_not_success(self):
        result = self.inspect_fixture(include_profiles=False)
        self.assertEqual(result["conclusion"], "incomplete_evidence")
        self.assertIn("PROFILE_ABSENT", {x["code"] for x in result["issues"]})

    def test_unreadable_ipa(self):
        with tempfile.TemporaryDirectory() as folder:
            filename = Path(folder) / "broken.ipa"
            filename.write_text("not a zip", encoding="utf-8")
            result = preflight.inspect_ipa(filename)
            self.assertEqual(result["conclusion"], "needs_attention")


if __name__ == "__main__":
    unittest.main()
