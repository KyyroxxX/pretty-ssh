# PrettySSH

A zero-dependency Python utility designed to configure and standardize SSH terminal environments on remote Linux hosts (Ubuntu, Debian, Arch, RHEL, CentOS).

PrettySSH solves common terminal emulation issues (`TERM` mismatches, broken `Ctrl+L` screen clearing, cursor desynchronization in `nano`/`vim`), enforces dynamic host and IPv4 visibility in a clean two-line prompt, and configures history search and productivity shortcuts.

---

## Terminal Preview

```text
┌──[ubuntu@wr-wazuh (10.0.31.10)]-[/var/ossec]
└─$ ports
State    Recv-Q   Send-Q   Local Address:Port   Peer Address:Port   Process
LISTEN   0        128            0.0.0.0:22          0.0.0.0:*      sshd
LISTEN   0        4096           0.0.0.0:1514        0.0.0.0:*      wazuh-remoted
LISTEN   0        4096           0.0.0.0:1515        0.0.0.0:*      wazuh-authd
LISTEN   0        128          127.0.0.1:55000       0.0.0.0:*      wazuh-apid
```

---

## Technical Specifications

- **Terminal Environment Standardization:** Exports `TERM=xterm-256color`, fixing terminal capability detection, `clear` commands, `Ctrl+L`, and full-screen text editor rendering (`nano`, `vim`, `htop`).
- **Network-Aware Two-Line Prompt:** Dynamically resolves the primary IPv4 address and current hostname directly into the shell prompt (`\u@\h ($IP_LOCAL)`), preventing operational errors across multi-node or segmented network topologies.
- **Enhanced History Navigation:** Binds up/down arrow keys to incremental prefix search (`history-search-backward` and `history-search-forward`).
- **Session History Persistence:** Appends shell history concurrently across multiple active SSH sessions using `shopt -s histappend` and synchronized `PROMPT_COMMAND` execution.
- **Built-in Aliases:** Preconfigures standard diagnostic shortcuts:
  - `ll`: Extended listing sorted by directories first (`ls -lah --color=auto --group-directories-first`).
  - `ports`: Active listening sockets (`sudo ss -tulpn`).
  - `myip`: Compact network interface status (`ip -br a`).
  - `cls`: Clear terminal buffer (`clear`).
- **Zero External Dependencies:** Built strictly using Python 3 standard library modules (`os`, `sys`, `shutil`, `subprocess`, `argparse`). Compatible with fresh cloud instances without requiring `pip` or virtual environments.
- **Idempotent and Reversible:** Backs up `~/.bashrc` prior to execution, isolates additions using explicit delimiter blocks, and supports clean rollbacks via `--uninstall`.

---

## Installation and Usage

### Direct Execution via curl

Execute remotely without manual cloning:

```bash
curl -sSL https://raw.githubusercontent.com/KyyroxxX/pretty-ssh/main/pretty_ssh.py | python3
```

Specify a corporate hostname during deployment:

```bash
curl -sSL https://raw.githubusercontent.com/KyyroxxX/pretty-ssh/main/pretty_ssh.py | python3 - -n wr-wazuh
```

---

### Local Execution

1. Clone or download the script:
   ```bash
   wget -O pretty_ssh.py https://raw.githubusercontent.com/KyyroxxX/pretty-ssh/main/pretty_ssh.py
   chmod +x pretty_ssh.py
   ```

2. Run the interactive installer:
   ```bash
   python3 pretty_ssh.py
   ```

3. Reload the shell environment:
   ```bash
   source ~/.bashrc
   ```

---

## Available Themes

| Theme | Flag | Description |
|---|---|---|
| **Cyber (Default)** | `-t cyber` | Cyan frame, orange host identifier, green working directory. |
| **Dracula** | `-t dracula` | Purple frame, pink user identifier, cyan working directory. |
| **Matrix** | `-t matrix` | Forest green frame, emerald user identifier, lime working directory. |
| **Nord** | `-t nord` | Frost blue frame, ice white user identifier, sage working directory. |

---

## Command-Line Arguments

```text
usage: pretty_ssh.py [-h] [-n HOSTNAME] [-t {cyber,dracula,matrix,nord}] [-u] [-q]

PrettySSH - Cloud & DevSecOps SSH Terminal Enhancer

options:
  -h, --help            Show this help message and exit.
  -n HOSTNAME, --hostname HOSTNAME
                        Set system hostname via hostnamectl and /etc/hosts.
  -t {cyber,dracula,matrix,nord}, --theme {cyber,dracula,matrix,nord}
                        Select ANSI color palette (default: cyber).
  -u, --uninstall       Remove configuration block and restore original ~/.bashrc.
  -q, --quiet           Suppress console banner output.
```

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
