# 🚀 PrettySSH — Cloud & DevSecOps SSH Terminal Enhancer

[![Python](https://img.shields.io/badge/Python-3.6+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)](https://www.kernel.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Zero-Dependencies](https://img.shields.io/badge/Dependencies-Zero%20(Pure%20Stdlib)-blueviolet?style=for-the-badge)]()

**PrettySSH** es una herramienta ligera y automatizada en Python diseñada para transformar cualquier terminal SSH recién desplegada (en AWS, Azure, GCP o VPS local) en un entorno de trabajo profesional, cómodo y visualmente impecable estilo **DevSecOps / Arch Linux**.

---

## 📸 Vista Previa del Terminal

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

## ✨ Características Principales

* 🎯 **Solución nativa para `Ctrl + L` y editores:** Exporta `TERM=xterm-256color`, resolviendo los habituales fallos de desalineación de cursor, cortes al limpiar pantalla (`Ctrl+L`) o visualización defectuosa en `nano`, `vim` y `htop`.
* 🌐 **Prompt en 2 líneas con IP dinámica:** Muestra siempre el usuario, nombre de máquina y la **IP privada del servidor entre paréntesis** `($IP_LOCAL)`, evitando confusiones al administrar múltiples servidores en arquitecturas segmentadas.
* 🔍 **Búsqueda inteligente en el historial con flechas:** Permite teclear el comienzo de un comando (ej. `sudo`, `ping` o `docker`) y pulsar `↑` / `↓` para autocompletar únicamente los comandos coincidentes del historial.
* ⚡ **Aliases de alta productividad preconfigurados:**
  * `ll` → Lista directorios primero, con tamaños legibles (`-h`) y colores.
  * `ports` → Muestra todos los sockets TCP/UDP escuchando en el sistema (`sudo ss -tulpn`).
  * `myip` → Resumen claro de interfaces de red e IPs asignadas (`ip -br a`).
  * `cls` → Limpieza rápida de terminal.
* 🛡️ **Seguro, Idempotente y Reversible:**
  * Genera automáticamente una copia de seguridad timestamped de tu `~/.bashrc` antes de tocar nada.
  * Se puede ejecutar múltiples veces sin duplicar bloques gracias a delimitadores de configuración.
  * Incluye desinstalador completo con `--uninstall`.
* 📦 **Cero dependencias externas:** Funciona únicamente con la biblioteca estándar de Python 3. No requiere `pip`, no instala paquetes pesados y corre en servidores mínimos.

---

## ⚡ Instalación Rápida (1 solo comando)

### Opción A: Ejecución Directa con `curl` (Sin clonar repositorio)
Puedes ejecutar el asistente directamente en cualquier servidor Linux remoto:

```bash
curl -sSL https://raw.githubusercontent.com/k1r0x/pretty-ssh/main/pretty_ssh.py | python3
```

O especificando el nombre del host directamente:
```bash
curl -sSL https://raw.githubusercontent.com/k1r0x/pretty-ssh/main/pretty_ssh.py | python3 - -n wr-wazuh
```

---

### Opción B: Ejecución Local en el Servidor

1. **Descarga el script:**
   ```bash
   wget -O pretty_ssh.py https://raw.githubusercontent.com/k1r0x/pretty-ssh/main/pretty_ssh.py
   chmod +x pretty_ssh.py
   ```

2. **Ejecuta el asistente interactivo:**
   ```bash
   python3 pretty_ssh.py
   ```

3. **Aplica los cambios en tu sesión actual:**
   ```bash
   source ~/.bashrc
   ```
   *(O ejecuta `exec bash`)*.

---

## 🎨 Opciones y Temas Disponibles

Puedes elegir entre varios esquemas de color optimizados para pantallas oscuras:

| Tema | Flag | Descripción |
|---|---|---|
| **Cyber (Default)** | `-t cyber` | Azul cian vibrante, naranja corporativo y verde primavera. |
| **Dracula** | `-t dracula` | Púrpura pastel, rosa vampiro y verde esmeralda. |
| **Matrix** | `-t matrix` | Verde bosque, verde terminal clásico y lima brillante. |
| **Nord** | `-t nord` | Azul ártico, blanco hielo y tonos nórdicos relajantes. |

### Ejemplos de uso CLI:

```bash
# Cambiar el nombre del servidor a wr-nginx y usar tema Matrix:
python3 pretty_ssh.py -n wr-nginx -t matrix

# Usar tema Dracula en wr-data:
python3 pretty_ssh.py -n wr-data -t dracula

# Desinstalar y restaurar ~/.bashrc original:
python3 pretty_ssh.py --uninstall

# Modo silencioso para scripts de automatización / cloud-init:
python3 pretty_ssh.py -n wr-app -q
```

---

## 🛠️ Opciones de Línea de Comandos

```text
usage: pretty_ssh.py [-h] [-n HOSTNAME] [-t {cyber,dracula,matrix,nord}] [-u] [-q]

PrettySSH — Cloud & DevSecOps SSH Terminal Enhancer

options:
  -h, --help            Muestra este mensaje de ayuda y sale.
  -n HOSTNAME, --hostname HOSTNAME
                        Nombre corporativo a fijar para el servidor (ej: wr-wazuh, wr-nginx).
  -t {cyber,dracula,matrix,nord}, --theme {cyber,dracula,matrix,nord}
                        Tema de color para el prompt (por defecto: cyber).
  -u, --uninstall       Desinstala PrettySSH y restaura ~/.bashrc al estado previo.
  -q, --quiet           Modo silencioso (sin banner ASCII).
```

---

## 📄 Licencia

Este proyecto está distribuido bajo la licencia **MIT**. Eres libre de usarlo, modificarlo y distribuirlo libremente en proyectos personales, académicos y comerciales.

Desarrollado con ❤️ por **k1r0x**.
