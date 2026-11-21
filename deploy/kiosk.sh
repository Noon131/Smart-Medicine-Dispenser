#!/usr/bin/env bash
# Opens the Smart Medicine UI full-screen in Chromium (kiosk). Started automatically after login,
# or by double-tapping the "Smart Medicine" desktop icon.
URL="http://127.0.0.1:5000"
PROFILE="$HOME/.config/smart-medicine-chromium"   # fixed profile: users, stock and schedule (localStorage) are kept after reboot

# wait up to 60 s for the backend
for _ in $(seq 1 60); do
  curl -fs "$URL/api/health" >/dev/null 2>&1 && break
  sleep 1
done

# the screen must never go blank on a medicine dispenser
command -v xset >/dev/null 2>&1 && { xset s off; xset -dpms; xset s noblank; } 2>/dev/null || true

BROWSER="$(command -v chromium-browser || command -v chromium || true)"
[ -z "$BROWSER" ] && { echo "Chromium not found: sudo apt install -y chromium-browser"; exit 1; }

# a crash / power cut must not show the "restore pages" bubble
if [ -f "$PROFILE/Default/Preferences" ]; then
  sed -i 's/"exited_cleanly":false/"exited_cleanly":true/; s/"exit_type":"Crashed"/"exit_type":"Normal"/' "$PROFILE/Default/Preferences" 2>/dev/null || true
fi

exec "$BROWSER" --kiosk --noerrdialogs --disable-infobars --disable-session-crashed-bubble \
  --disable-pinch --overscroll-history-navigation=0 --check-for-update-interval=31536000 \
  --autoplay-policy=no-user-gesture-required --user-data-dir="$PROFILE" \
  --no-first-run --password-store=basic "$URL"
