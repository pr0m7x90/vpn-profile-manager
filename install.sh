#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="/usr/local/lib/vpn-profile-manager"
CONFIG_DIR="/etc/vpn-profile-manager"
PROFILE_DIR="$CONFIG_DIR/profiles"

if [[ $EUID -ne 0 ]]; then
    echo "[!] Run with sudo:"
    echo "    sudo ./install.sh"
    exit 1
fi

echo "VPN Profile Manager"
echo

if ! command -v openvpn >/dev/null 2>&1; then
    echo "[*] OpenVPN is not installed."
    if command -v apt-get >/dev/null 2>&1; then
        apt-get update
        apt-get install -y openvpn
    else
        echo "[!] apt-get is unavailable. Install OpenVPN manually."
        exit 1
    fi
fi

command -v python3 >/dev/null 2>&1 || {
    echo "[!] Python 3 is required."
    exit 1
}

mkdir -p "$INSTALL_DIR" "$PROFILE_DIR"
chmod 700 "$CONFIG_DIR" "$PROFILE_DIR"

cp "$PROJECT_DIR/src/profile_manager.py" "$INSTALL_DIR/profile_manager.py"
cp "$PROJECT_DIR/src/connect" "$INSTALL_DIR/connect"
cp "$PROJECT_DIR/src/check" "$INSTALL_DIR/check"
cp "$PROJECT_DIR/src/disconnect" "$INSTALL_DIR/disconnect"
chmod 755 "$INSTALL_DIR/"*

cat > /usr/bin/vpn-profile-manager <<EOF
#!/usr/bin/env bash
export VPNPM_CONFIG_DIR="$CONFIG_DIR"
exec python3 "$INSTALL_DIR/profile_manager.py" "\$@"
EOF

cat > /usr/bin/connect <<EOF
#!/usr/bin/env bash
export VPNPM_CONFIG_DIR="$CONFIG_DIR"
exec "$INSTALL_DIR/connect" "\$@"
EOF

cat > /usr/bin/check <<EOF
#!/usr/bin/env bash
export VPNPM_CONFIG_DIR="$CONFIG_DIR"
exec "$INSTALL_DIR/check" "\$@"
EOF

cat > /usr/bin/disconnect <<EOF
#!/usr/bin/env bash
export VPNPM_CONFIG_DIR="$CONFIG_DIR"
exec "$INSTALL_DIR/disconnect" "\$@"
EOF

chmod 755 /usr/bin/vpn-profile-manager /usr/bin/connect /usr/bin/check /usr/bin/disconnect

# Remove wrappers from older versions so only /usr/bin is canonical.
rm -f /usr/local/bin/vpn-profile-manager \
      /usr/local/bin/connect \
      /usr/local/bin/check \
      /usr/local/bin/disconnect

echo
echo "[+] Installation complete."
echo
echo "Add a profile:"
echo "  sudo vpn-profile-manager"
echo
echo "Use:"
echo "  sudo connect <alias>"
echo "  check <alias>"
echo "  sudo disconnect <alias>"
