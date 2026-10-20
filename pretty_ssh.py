#!/usr/bin/env python3
"""
===============================================================================
 PrettySSH - Cloud & DevSecOps Terminal Enhancer
 Author: k1r0x (Weather Report Solutions S.L. / Open Source Tool)
 Description: Configura y embellece al instante consolas SSH en Linux (Ubuntu,
              Debian, Arch, RHEL). Corrige TERM para Ctrl+L y editores,
              aplica un prompt en 2 líneas con IP y añade historial inteligente.
 License: MIT
===============================================================================
"""

import sys
import os
import shutil
import subprocess
import argparse
from datetime import datetime

MARKER_BEGIN = "# === BEGIN PRETTY-SSH CONFIG ==="
MARKER_END = "# === END PRETTY-SSH CONFIG ==="

THEMES = {
    "cyber": {
        "name": "Cyber Blue / Neon Orange (Default)",
        "frame": r"\[\033[38;5;39m\]",     # Neon Blue
        "user": r"\[\033[38;5;81m\]",      # Light Cyan
        "at": r"\[\033[38;5;250m\]",       # Grey
        "host": r"\[\033[38;5;214m\]",     # Orange
        "ip": r"\[\033[38;5;244m\]",       # Dim Grey
        "path": r"\[\033[38;5;48m\]",      # Spring Green
        "prompt": r"\[\033[38;5;196m\]",   # Red
    },
    "dracula": {
        "name": "Dracula Vampire (Purple / Pink)",
        "frame": r"\[\033[38;5;141m\]",    # Purple
        "user": r"\[\033[38;5;212m\]",     # Pink
        "at": r"\[\033[38;5;250m\]",
        "host": r"\[\033[38;5;84m\]",      # Green
        "ip": r"\[\033[38;5;244m\]",
        "path": r"\[\033[38;5;117m\]",     # Cyan
        "prompt": r"\[\033[38;5;212m\]",
    },
    "matrix": {
        "name": "Matrix Terminal (Emerald / Bright Green)",
        "frame": r"\[\033[38;5;34m\]",     # Forest Green
        "user": r"\[\033[38;5;46m\]",      # Matrix Green
        "at": r"\[\033[38;5;250m\]",
        "host": r"\[\033[38;5;82m\]",      # Lime
        "ip": r"\[\033[38;5;244m\]",
        "path": r"\[\033[38;5;118m\]",     # Light Green
        "prompt": r"\[\033[38;5;46m\]",
    },
    "nord": {
        "name": "Nordic Frost (Ice Blue / Snow)",
        "frame": r"\[\033[38;5;110m\]",    # Frost Blue
        "user": r"\[\033[38;5;153m\]",     # Ice White
        "at": r"\[\033[38;5;250m\]",
        "host": r"\[\033[38;5;179m\]",     # Nord Yellow
        "ip": r"\[\033[38;5;244m\]",
        "path": r"\[\033[38;5;143m\]",     # Nord Sage
        "prompt": r"\[\033[38;5;110m\]",
    }
}

BANNER = r"""
  ____           _   _         ____ ____  _   _ 
 |  _ \ _ __ ___| |_| |_ _   _/ ___/ ___|| | | |
 | |_) | '__/ _ \ __| __| | | \___ \___ \| |_| |
 |  __/| | |  __/ |_| |_| |_| |___) |__) |  _  |
 |_|   |_|  \___|\__|\__|\__, |____/____/|_| |_|
                         |___/  by k1r0x
 [ Cloud & DevSecOps Automated SSH Terminal Setup ]
"""

def print_banner():
    # ANSI Cyan banner
    print(f"\033[38;5;39m{BANNER}\033[0m")

def run_cmd(cmd, check=True):
    try:
        res = subprocess.run(cmd, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return res.returncode == 0, res.stdout.strip(), res.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def set_system_hostname(new_hostname):
    if not new_hostname:
        return True
    print(f"[*] Configurando hostname a: \033[1;33m{new_hostname}\033[0m...")
    ok, _, err = run_cmd(f"sudo hostnamectl set-hostname {new_hostname}")
    if not ok:
        print(f"    [!] Advertencia: No se pudo cambiar el hostname con hostnamectl ({err})")
    
    # Añadir a /etc/hosts si no está presente
    hosts_path = "/etc/hosts"
    if os.path.exists(hosts_path):
        try:
            with open(hosts_path, "r", encoding="utf-8") as f:
                content = f.read()
            if new_hostname not in content:
                run_cmd(f"echo '127.0.0.1 {new_hostname}' | sudo tee -a /etc/hosts")
                print(f"    [+] Añadido '127.0.0.1 {new_hostname}' a /etc/hosts.")
        except Exception as e:
            print(f"    [!] No se pudo editar /etc/hosts: {e}")
    return True

def generate_bashrc_block(theme_key="cyber"):
    t = THEMES.get(theme_key, THEMES["cyber"])
    
    block = f"""{MARKER_BEGIN}
# ==========================================================
# PrettySSH - Cloud & DevSecOps Enhanced Terminal
# Configured on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
# Theme: {t['name']}
# ==========================================================
export TERM=xterm-256color
export CLICOLOR=1
export LSCOLORS=ExFxBxDxCxegedabagacad

# Aliases de alta productividad y visibilidad
alias ll='ls -lah --color=auto --group-directories-first'
alias l='ls -CF --color=auto'
alias grep='grep --color=auto'
alias ports='sudo ss -tulpn'
alias cls='clear'
alias myip='ip -br a'

# Navegacion y busqueda en historial con teclas Flecha Arriba/Abajo
bind '"\\e[A": history-search-backward' 2>/dev/null
bind '"\\e[B": history-search-forward' 2>/dev/null
shopt -s histappend 2>/dev/null
PROMPT_COMMAND="history -a; history -c; history -r; ${{PROMPT_COMMAND:-}}"

# Prompt estilizado en dos lineas con IP de interfaz principal visible
IP_LOCAL=$(hostname -I 2>/dev/null | awk '{{print $1}}')
export PS1="{t['frame']}┌──[{t['user']}\\u{t['at']}@{t['host']}\\h{t['ip']} ($IP_LOCAL){t['frame']}]-[{t['path']}\\w{t['frame']}]\\n{t['frame']}└─{t['prompt']}\\${{\\033[0m\}} "
{MARKER_END}
"""
    return block

def install_enhancement(theme_key="cyber", hostname=None):
    bashrc_path = os.path.expanduser("~/.bashrc")
    if not os.path.exists(bashrc_path):
        open(bashrc_path, "w").close()
    
    # 1. Crear copia de seguridad
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{bashrc_path}.bak_prettyssh_{timestamp}"
    shutil.copy2(bashrc_path, backup_path)
    print(f"[+] Copia de seguridad creada en: \033[38;5;244m{backup_path}\033[0m")
    
    # 2. Configurar hostname si se especificó
    if hostname:
        set_system_hostname(hostname)
        
    # 3. Leer y limpiar configuración anterior si ya existía
    with open(bashrc_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    if MARKER_BEGIN in content and MARKER_END in content:
        print("[*] Actualizando bloque PrettySSH existente en ~/.bashrc...")
        before = content.split(MARKER_BEGIN)[0]
        after = content.split(MARKER_END)[1]
        content = before.rstrip() + "\n" + after.lstrip()
    else:
        print("[+] Inyectando configuración en ~/.bashrc...")

    # 4. Inyectar nuevo bloque
    new_block = generate_bashrc_block(theme_key)
    new_content = content.rstrip() + "\n\n" + new_block + "\n"
    
    with open(bashrc_path, "w", encoding="utf-8") as f:
        f.write(new_content)
        
    print(f"[+] ¡Instalación completada con éxito! (Tema: \033[1;32m{theme_key}\033[0m)")
    print("\n\033[1;36mPara ver los cambios reflejados de inmediato ejecuta:\033[0m")
    print("    \033[1;32msource ~/.bashrc\033[0m   (o ejecuta: \033[1;32mexec bash\033[0m)\n")

def uninstall_enhancement():
    bashrc_path = os.path.expanduser("~/.bashrc")
    if not os.path.exists(bashrc_path):
        print("[-] ~/.bashrc no encontrado.")
        return
        
    with open(bashrc_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    if MARKER_BEGIN not in content or MARKER_END not in content:
        print("[-] No se encontró ninguna instalación de PrettySSH en ~/.bashrc.")
        return
        
    print("[*] Desinstalando PrettySSH de ~/.bashrc...")
    before = content.split(MARKER_BEGIN)[0]
    after = content.split(MARKER_END)[1]
    new_content = before.rstrip() + "\n" + after.lstrip()
    
    with open(bashrc_path, "w", encoding="utf-8") as f:
        f.write(new_content)
        
    print("[+] PrettySSH ha sido desinstalado. Ejecuta 'source ~/.bashrc' para restablecer tu terminal.")

def main():
    parser = argparse.ArgumentParser(
        description="PrettySSH — Cloud & DevSecOps SSH Terminal Enhancer",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-n", "--hostname", help="Nombre corporativo a fijar para el servidor (ej: wr-wazuh, wr-nginx)")
    parser.add_argument("-t", "--theme", choices=list(THEMES.keys()), default="cyber", help="Tema de color para el prompt (cyber, dracula, matrix, nord)")
    parser.add_argument("-u", "--uninstall", action="store_true", help="Desinstala PrettySSH y restaura ~/.bashrc original")
    parser.add_argument("-q", "--quiet", action="store_true", help="Modo silencioso (sin banner)")
    
    args = parser.parse_args()

    if not args.quiet:
        print_banner()

    if args.uninstall:
        uninstall_enhancement()
        return

    # Si no se pasó hostname ni parámetros por CLI y es sesión interactiva, preguntar
    hostname = args.hostname
    theme = args.theme

    if not hostname and sys.stdin.isatty() and len(sys.argv) == 1:
        print("Modo interactivo rápido (pulsa ENTER para valores por defecto):\n")
        try:
            current_host = os.uname().nodename
        except Exception:
            current_host = "servidor"
            
        custom_h = input(f"¿Deseas cambiar el nombre del servidor? [Actual: {current_host}] (deja vacío para no cambiar): ").strip()
        if custom_h:
            hostname = custom_h
            
        print("\nTemas disponibles:")
        for k, v in THEMES.items():
            print(f"  [{k}] - {v['name']}")
        custom_t = input("Elige tema [cyber]: ").strip().lower()
        if custom_t in THEMES:
            theme = custom_t

    install_enhancement(theme_key=theme, hostname=hostname)

if __name__ == "__main__":
    main()
