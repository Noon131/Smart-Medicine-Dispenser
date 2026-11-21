#!/usr/bin/env bash
# Removes the auto-start service and launchers (your data and files are NOT deleted).
set -u
RUN_USER="${SUDO_USER:-$(id -un)}"; RUN_HOME="$(getent passwd "$RUN_USER" | cut -d: -f6)"
S=""; [ "$(id -u)" = 0 ] || S="sudo"
$S systemctl disable --now smart-medicine.service 2>/dev/null
$S rm -f /etc/systemd/system/smart-medicine.service; $S systemctl daemon-reload
rm -f "$RUN_HOME/Desktop/smart-medicine.desktop" "$RUN_HOME/.local/share/applications/smart-medicine.desktop" "$RUN_HOME/.config/autostart/smart-medicine.desktop"
[ -f "$RUN_HOME/.config/labwc/autostart" ] && sed -i '/smart_medicine_kiosk/d' "$RUN_HOME/.config/labwc/autostart"
echo "Removed."
