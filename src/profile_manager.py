#!/usr/bin/env python3
"""Interactive VPN Profile Manager."""
from pathlib import Path
import os
import re
import sys

ALIAS_RE = re.compile(r"^[A-Za-z0-9_-]+$")
DEFAULT_CONFIG_DIR = Path(__file__).resolve().parent.parent


def config_dir():
    return Path(os.environ.get("VPNPM_CONFIG_DIR", DEFAULT_CONFIG_DIR)).expanduser()


def valid_alias(alias):
    return bool(ALIAS_RE.fullmatch(alias))


def prompt(label):
    while True:
        value = input(label).strip()
        if value:
            return value
        print("[!] This field cannot be empty.")


def main():
    print("VPN Profile Manager")
    print()

    vpn_name = prompt("VPN Name: ")
    alias = prompt("Profile Alias: ")

    if not valid_alias(alias):
        print("[!] Invalid profile alias. Use only letters, numbers, '-' and '_'.")
        return 1

    raw_path = prompt("OVPN Configuration File Path: ")
    ovpn_path = Path(raw_path.strip('"').strip("'")).expanduser()

    print()
    print("Commands that will be available:")
    print()
    print(f"  sudo connect {alias}")
    print(f"  check {alias}")
    print(f"  sudo disconnect {alias}")
    print()

    if not ovpn_path.is_file():
        print("[!] OVPN configuration file not found:")
        print(f"    {ovpn_path}")
        return 1

    target = config_dir() / "profiles" / alias
    if target.exists():
        print(f"[!] A profile named '{alias}' already exists.")
        return 1

    print("Profile:")
    print(f"  VPN Name        : {vpn_name}")
    print(f"  Profile Alias   : {alias}")
    print(f"  OVPN File       : {ovpn_path}")
    print()

    if input("Save profile? [Y/n]: ").strip().lower() == "n":
        print("[*] Profile not saved.")
        return 0

    try:
        target.mkdir(parents=True)
        (target / "name").write_text(vpn_name + "\n", encoding="utf-8")
        (target / "config").write_text(str(ovpn_path.resolve()) + "\n", encoding="utf-8")
        os.chmod(target, 0o700)
        os.chmod(target / "name", 0o600)
        os.chmod(target / "config", 0o600)
    except OSError as exc:
        print(f"[!] Could not save profile: {exc}")
        return 1

    print(f"[+] Profile '{alias}' saved.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
