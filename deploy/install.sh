#!/usr/bin/env bash
# One-time setup on the Raspberry Pi:  ./deploy/install.sh   then   sudo reboot
set -euo pipefail
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUN_USER="${SUDO_USER:-$(id -un)}"
RUN_HOME="$(getent passwd "$RUN_USER" | cut -d: -f6)"
DRY="${DRY_RUN:-0}"
run(){ if [ "$DRY" = 1 ]; then echo "[dry-run] $*"; else "$@"; fi; }
sudo_(){ if [ "$(id -u)" = 0 ] || [ "$DRY" = 1 ]; then run "$@"; else run sudo "$@"; fi; }

echo ">> App folder: $APP_DIR   user: $RUN_USER"
chmod +x "$APP_DIR/deploy/"*.sh "$APP_DIR/run.sh" 2>/dev/null || true

echo ">> Python environment"
if [ "$DRY" != 1 ]; then
  [ -d "$APP_DIR/.venv" ] || python3 -m venv "$APP_DIR/.venv" --system-site-packages
  "$APP_DIR/.venv/bin/pip" install -q -r "$APP_DIR/requirements.txt"
fi

echo ">> Backend service (starts at power-on, restarts if it crashes)"
UNIT=/etc/systemd/system/smart-medicine.service
UNIT_TXT="[Unit]
Description=Smart Medicine Dispenser backend
After=network.target

[Service]
User=$RUN_USER
Group=$RUN_USER
SupplementaryGroups=gpio
WorkingDirectory=$APP_DIR
ExecStart=$APP_DIR/.venv/bin/python $APP_DIR/app.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target"
if [ "$DRY" = 1 ]; then echo "[dry-run] write $UNIT:"; echo "$UNIT_TXT"; else
  echo "$UNIT_TXT" | sudo_ tee "$UNIT" >/dev/null
fi
sudo_ systemctl daemon-reload
sudo_ systemctl enable --now smart-medicine.service

echo ">> Launcher, desktop icon and auto-start of the full-screen screen"
ICON="$APP_DIR/static/icon.svg"
DESKTOP_TXT="[Desktop Entry]
Type=Application
Name=Smart Medicine
Comment=Smart Medicine Dispenser
Exec=$APP_DIR/deploy/kiosk.sh
Icon=$ICON
Terminal=false
Categories=Utility;"
mk(){ # mk <path> [executable]
  if [ "$DRY" = 1 ]; then echo "[dry-run] write $1"; return; fi
  mkdir -p "$(dirname "$1")"; printf '%s\n' "$DESKTOP_TXT" > "$1"; chmod +x "$1"
  [ "$(id -u)" = 0 ] && chown "$RUN_USER":"$RUN_USER" "$1" || true
}
mk "$RUN_HOME/Desktop/smart-medicine.desktop"
mk "$RUN_HOME/.local/share/applications/smart-medicine.desktop"
mk "$RUN_HOME/.config/autostart/smart-medicine.desktop"           # X11 / LXDE / wayfire (XDG autostart)
LAB="$RUN_HOME/.config/labwc/autostart"                            # labwc (newer Raspberry Pi OS)
if [ -d "$RUN_HOME/.config/labwc" ] || command -v labwc >/dev/null 2>&1; then
  if [ "$DRY" = 1 ]; then echo "[dry-run] add to $LAB"; else
    mkdir -p "$(dirname "$LAB")"; touch "$LAB"
    grep -q "smart_medicine_kiosk" "$LAB" || echo "$APP_DIR/deploy/kiosk.sh & # smart_medicine_kiosk" >> "$LAB"
    [ "$(id -u)" = 0 ] && chown -R "$RUN_USER":"$RUN_USER" "$RUN_HOME/.config/labwc" || true
  fi
fi
command -v chromium-browser >/dev/null 2>&1 || command -v chromium >/dev/null 2>&1 || echo "!! Chromium not found:  sudo apt install -y chromium-browser"
echo
echo "Done.  Reboot now:  sudo reboot     (backend + full-screen app start by themselves)"
echo "Backend status:     systemctl status smart-medicine        Logs: journalctl -u smart-medicine -f"
echo "Leave kiosk mode:   Alt+F4  (or Ctrl+W);  start again from the 'Smart Medicine' desktop icon"
