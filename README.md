# fw-lid-fprint-daemon

A lightweight, always-on systemd daemon for Framework 13 laptops running Fedora. Every 15 seconds, it checks whether your lid is open or closed and if any external displays are connected. When docked with the lid closed, it automatically disables fingerprint authentication (`fprintd`) and falls back to password login; when you open the lid, it re-enables fingerprint authentication.

---

## Problem

On Framework 13 machines under Fedora, the system often asks for a fingerprint when the lid is closed and docked, but the scanner is not accessible with the lid down. In GNOME, there’s no built-in fallback, so users must reopen the lid or cancel commands. This daemon solves that by toggling `fprintd` off when closed and docked (forcing a password prompt) and turning it back on when the lid opens.

## Design

This daemon avoids using the legacy ACPI daemon (acpid) because on Fedora, systemd-logind intercepts lid events directly, preventing acpid from reliably firing scripts. We are not using inotify on /proc/acpi/button/lid/LID0/state because that file does not emit filesystem change events under the virtual /proc filesystem. Instead, we use a simple, polling-based systemd daemon that checks lid state and display connections every 15 seconds, ensuring consistent behavior across suspends and hardware configurations.

---

## Table of Contents

- [Installation](#installation)  
- [Usage](#usage)  
- [Configuration](#configuration)  
- [Development](#development)  
- [Contributing](#contributing)  
- [License](#license)

---

## Installation

### RPM (Recommended)

1. Place the source and spec in your RPM build tree:  
   ```bash
   mkdir -p ~/rpmbuild/{SPECS,SOURCES}
   cp fw-lid-fprint-daemon-1.0.tar.gz ~/rpmbuild/SOURCES/
   cp fw-lid-fprint-daemon.spec ~/rpmbuild/SPECS/
   ```
2. Build the package:  
   ```bash
   rpmbuild -ba ~/rpmbuild/SPECS/fw-lid-fprint-daemon.spec
   ```
3. Install the resulting RPM:  
   ```bash
   sudo dnf install ~/rpmbuild/RPMS/noarch/fw-lid-fprint-daemon-1.0-1.noarch.rpm
   ```

### Manual

1. Copy `laptop-lid-daemon.sh` to `/usr/local/bin/` and make it executable:  
   ```bash
   sudo install -m 755 laptop-lid-daemon.sh /usr/local/bin/
   ```
2. Copy `laptop-lid-daemon.service` to `/etc/systemd/system/`:  
   ```bash
   sudo install -m 644 laptop-lid-daemon.service /etc/systemd/system/
   ```
3. Reload and start the daemon:  
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable --now laptop-lid-daemon.service
   ```

---

## Usage

Once installed, the daemon runs continuously. It logs only when the lid or docking state changes:

```bash
journalctl -f -t lid-daemon
```

- **Closed & docked:** “LID CLOSED + DOCKED → mask & stop fprintd”  
- **Closed & undocked:** “LID CLOSED + UNDOCKED → leave fprintd alone”  
- **Open:** “LID OPEN → unmask & start fprintd”

To check the service status:

```bash
systemctl status laptop-lid-daemon.service
```

---

## Configuration

- **Poll Interval:** Modify the `sleep 15` line in `/usr/local/bin/laptop-lid-daemon.sh` for faster or slower checks.  
- **Connector Paths:** By default, the script inspects `/sys/class/drm/*-DP-*/status` and `/sys/class/drm/*-HDMI-A-*/status`. Update these patterns if your setup uses different interfaces.

---

## Development

1. Clone the repository:  
   ```bash
   git clone https://github.com/andypiper/fw-lid-fprint-daemon.git
   cd fw-lid-fprint-daemon
   ```
2. Build and install the RPM for testing:  
   ```bash
   rpmbuild -ba fw-lid-fprint-daemon.spec
   sudo dnf install ~/rpmbuild/RPMS/noarch/fw-lid-fprint-daemon-1.0-1.noarch.rpm
   journalctl -f -t lid-daemon
   ```

---

## Contributing

Contributions and bug reports are welcome:

1. Fork the repo and create a feature branch.  
2. Commit your changes with clear messages.  
3. Submit a pull request for review.

Please open an issue first for major features or breaking changes.

---

## License

This project is MIT licensed. See [LICENSE](LICENSE) for details.

---

**Author:** Andy Piper  
GitHub: [@andypiper](https://github.com/andypiper)  
Email: [andypiper@omg.lol](mailto:andypiper@omg.lol)


