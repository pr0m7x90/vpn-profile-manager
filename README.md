# VPN Profile Manager

Lightweight OpenVPN Profile Manager for Linux.

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Shell](https://img.shields.io/badge/Shell-Bash-green.svg)](https://www.gnu.org/software/bash/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Description

VPN Profile Manager is a lightweight command-line tool for managing OpenVPN profiles on Linux systems.

It allows users to register existing `.ovpn` configuration files under simple profile aliases and provides dedicated commands to connect, check, and disconnect VPN connections.

The project is designed to keep the workflow simple while allowing multiple VPN configurations to be managed from the same system.

## Features

- Interactive VPN profile creation
- Custom VPN names and profile aliases
- Supports existing OpenVPN `.ovpn` configuration files
- Runs OpenVPN in the background
- Displays VPN connection status
- Displays VPN interface and assigned IP address
- Displays VPN routing information
- Checks internet connectivity
- Profile-based OpenVPN disconnect
- PID-based process management
- Prevents disconnecting unrelated OpenVPN processes
- Keeps VPN configuration files outside the repository
- Lightweight Bash and Python implementation

## Requirements

- Linux
- Python 3
- OpenVPN
- sudo privileges

## Installation

Clone the repository:

    git clone https://github.com/pr0m7x90/vpn-profile-manager.git
    cd vpn-profile-manager

Make the installer executable:

    chmod +x install.sh

Run the installer:

    sudo ./install.sh

The installer provides the following commands:

    vpn-profile-manager
    connect
    check
    disconnect

## Creating a VPN Profile

Start the profile manager:

    sudo vpn-profile-manager

The manager will ask for:

    VPN Name:
    Profile Alias:
    OVPN Configuration File Path:

Example:

    VPN Name: Example VPN
    Profile Alias: example-vpn
    OVPN Configuration File Path: /home/user/Downloads/example.ovpn

The manager then displays the commands associated with the profile:

    sudo connect example-vpn
    check example-vpn
    sudo disconnect example-vpn

## Usage

### Connect

Connect to a saved VPN profile:

    sudo connect <alias>

Example:

    sudo connect example-vpn

OpenVPN runs in the background and the script waits for the VPN tunnel interface to become available.

### Check

Check the current VPN status:

    check <alias>

Example:

    check example-vpn

The status command displays:

- OpenVPN process status
- VPN interface status
- VPN IP address
- VPN routes
- Internet connectivity

### Disconnect

Disconnect a saved VPN profile:

    sudo disconnect <alias>

Example:

    sudo disconnect example-vpn

The disconnect command uses the profile's PID file to terminate the OpenVPN process associated with that profile.

If no profile-specific PID file exists, the script refuses to terminate an unrelated OpenVPN process.

## Profile Storage

Profiles are stored under:

    /etc/vpn-profile-manager/profiles/

The `name` file stores the VPN display name.

The `config` file stores the path to the existing `.ovpn` configuration file.

The actual `.ovpn` file is not copied into the project.

## Notes

The current implementation expects OpenVPN to create a `tun0` tunnel interface.

If an OpenVPN configuration uses a different interface name, the connection-status logic may need to be adjusted.

OpenVPN warnings or compatibility messages depend on the installed OpenVPN version and the supplied `.ovpn` configuration.

## License

VPN Profile Manager is released under the MIT License.

See [LICENSE](LICENSE) for details.
