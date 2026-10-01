import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import profile_manager


class ProfileManagerTests(unittest.TestCase):
    def test_valid_aliases(self):
        for alias in ("thm", "offsec", "my-vpn", "vpn_01"):
            self.assertTrue(profile_manager.valid_alias(alias))

    def test_invalid_aliases(self):
        for alias in ("", "my vpn", "vpn/path", "vpn$", "../vpn"):
            self.assertFalse(profile_manager.valid_alias(alias))

    def test_profile_is_saved(self):
        with tempfile.TemporaryDirectory() as tmp:
            config_root = Path(tmp)
            ovpn = config_root / "test.ovpn"
            ovpn.write_text("# test\n", encoding="utf-8")

            with patch.object(profile_manager, "config_dir", return_value=config_root), \
                 patch("builtins.input", side_effect=[
                     "Test VPN",
                     "test",
                     str(ovpn),
                     "Y",
                 ]):
                self.assertEqual(profile_manager.main(), 0)

            profile = config_root / "profiles" / "test"
            self.assertEqual((profile / "name").read_text(), "Test VPN\n")
            self.assertEqual((profile / "config").read_text(), str(ovpn.resolve()) + "\n")


if __name__ == "__main__":
    unittest.main()
