"""Smart Medicine Dispenser backend for Raspberry Pi.

BCM GPIO pins are configured in config.json. The browser UI syncs the active profile's
six-compartment schedule to /api/schedule. A physical box opening NEVER confirms medicine
was taken; the user must still confirm that in the UI.
"""
from __future__ import annotations
import json, subprocess, threading, time
from datetime import datetime
from pathlib import Path
from flask import Flask, jsonify, request, send_file

BASE_DIR = Path(__file__).resolve().parent
CONFIG = json.loads((BASE_DIR / "config.json").read_text(encoding="utf-8"))
app = Flask(__name__)
lock = threading.RLock()
box_status = {str(i): {"is_open": False, "state": "unknown"} for i in range(1, 7)}
events = []
next_event_id = 1
current_warning = None
last_opened_box = None
hardware_status = "mock mode" if CONFIG.get("mock_mode") else "starting"
runtime_schedule = None
runtime_person = {"id": None, "name": ""}


def now_iso():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def minute_value(value):
    try:
        h, m = map(int, str(value).split(":", 1))
        if not (0 <= h <= 23 and 0 <= m <= 59): return None
        return h * 60 + m
    except (ValueError, TypeError):
        return None


def due_box_at(now=None):
    now = now or datetime.now()
    minute = now.hour * 60 + now.minute
    schedule = runtime_schedule if runtime_schedule is not None else CONFIG["boxes"]
    for box_id, cfg in schedule.items():
        if not cfg.get("has_meds", True):
            continue
        start, end = minute_value(cfg.get("time")), minute_value(cfg.get("end_time"))
        if start is None or end is None: continue
        # Handle a schedule that crosses midnight as well as ordinary windows.
        in_window = start <= minute <= end if start <= end else (minute >= start or minute <= end)
        if in_window: return str(box_id)
    return None


def record_event(box_id, action):
    global next_event_id, current_warning, last_opened_box
    box_id = str(box_id)
    timestamp = now_iso()
    expected = due_box_at()
    event = {"id": next_event_id, "box_id": box_id, "action": action,
             "timestamp": timestamp, "expected_box_id": expected, "message": ""}
    next_event_id += 1
    if action == "BOX_OPENED":
        last_opened_box = box_id
        if expected is not None and box_id != expected:
            event["message"] = f"Wrong box opened! Box {expected} is scheduled now, but Box {box_id} was opened."
            current_warning = {"box_id": box_id, "expected_box_id": expected,
                              "message": event["message"], "timestamp": timestamp}
        elif expected is not None:
            event["message"] = f"Correct box opened: Box {box_id}. Confirm separately whether medicine was taken."
        else:
            event["message"] = f"Box {box_id} opened. No medicine is scheduled for this time."
    else:
        event["message"] = f"Box {box_id} closed."
    with lock:
        events.append(event)
        del events[:-200]
        if action in ("BOX_OPENED", "BOX_CLOSED"):
            box_status[box_id] = {"is_open": action == "BOX_OPENED",
                                  "state": "open" if action == "BOX_OPENED" else "closed",
                                  "changed_at": timestamp}
    app.logger.info("Sensor event: %s", event)
    return event


def monitor_gpio():
    """Poll configured Hall sensors with debounce. Requires RPi.GPIO on Raspberry Pi OS."""
    global hardware_status
    try:
        import RPi.GPIO as GPIO
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        for cfg in CONFIG["boxes"].values():
            GPIO.setup(int(cfg["bcm_pin"]), GPIO.IN, pull_up_down=GPIO.PUD_UP)
        closed_level = int(CONFIG.get("closed_level", 1))
        pins = {str(k): int(v["bcm_pin"]) for k, v in CONFIG["boxes"].items()}
        stable, candidate, candidate_since = {}, {}, {}
        for box_id, pin in pins.items():
            is_closed = GPIO.input(pin) == closed_level
            stable[box_id] = candidate[box_id] = is_closed
            candidate_since[box_id] = time.monotonic()
            with lock:
                box_status[box_id] = {"is_open": not is_closed,
                                      "state": "closed" if is_closed else "open",
                                      "changed_at": now_iso()}
        with lock: hardware_status = "connected"
        debounce = max(0.01, float(CONFIG.get("debounce_seconds", 0.08)))
        poll = max(0.01, float(CONFIG.get("poll_interval_seconds", 0.05)))
        while True:
            tick = time.monotonic()
            for box_id, pin in pins.items():
                is_closed = GPIO.input(pin) == closed_level
                if is_closed != candidate[box_id]:
                    candidate[box_id] = is_closed
                    candidate_since[box_id] = tick
                elif is_closed != stable[box_id] and tick - candidate_since[box_id] >= debounce:
                    stable[box_id] = is_closed
                    record_event(box_id, "BOX_CLOSED" if is_closed else "BOX_OPENED")
            time.sleep(poll)
    except Exception as exc:
        with lock: hardware_status = f"error: {type(exc).__name__}: {exc}"
        app.logger.exception("Hall sensor monitor failed")


# Box voices are static MP3 files in static/audio/ (served by Flask's /static route) and played by the UI.


@app.get("/")
def home():
    return send_file(BASE_DIR / "Smart_medicine_dispenser_V75.html")


@app.get("/api/health")
def health():
    with lock:
        return jsonify({"ok": True, "hardware_status": hardware_status,
                        "server_time": now_iso(), "schedule_synced": runtime_schedule is not None})


@app.get("/api/status")
def status():
    with lock:
        return jsonify({"hardware_status": hardware_status, "server_time": now_iso(),
                        "expected_box_id": due_box_at(), "boxes": dict(box_status),
                        "current_warning": current_warning,
                        "latest_event": events[-1] if events else None,
                        "schedule_synced": runtime_schedule is not None,
                        "person_name": runtime_person.get("name", "")})


@app.post("/api/schedule")
def update_schedule():
    """Accept the current profile's six UI compartments and use them for wrong-box checks."""
    global runtime_schedule, runtime_person
    payload = request.get_json(silent=True) or {}
    incoming = payload.get("boxes")
    if not isinstance(incoming, list) or len(incoming) != 6:
        return jsonify({"ok": False, "error": "boxes must contain exactly six compartments"}), 400
    clean = {}
    for item in incoming:
        if not isinstance(item, dict): continue
        box_id = str(item.get("id", ""))
        if box_id not in {str(i) for i in range(1, 7)}:
            return jsonify({"ok": False, "error": f"invalid box id: {box_id}"}), 400
        if minute_value(item.get("time")) is None or minute_value(item.get("end_time")) is None:
            return jsonify({"ok": False, "error": f"invalid time for box {box_id}"}), 400
        clean[box_id] = {"time": str(item["time"]), "end_time": str(item["end_time"]),
                         "has_meds": bool(item.get("has_meds", True))}
    if set(clean) != {str(i) for i in range(1, 7)}:
        return jsonify({"ok": False, "error": "all six box IDs 1–6 are required"}), 400
    with lock:
        runtime_schedule = clean
        runtime_person = {"id": payload.get("person_id"), "name": str(payload.get("person_name", ""))[:100]}
    return jsonify({"ok": True, "schedule_synced": True, "active_person": runtime_person,
                    "expected_box_id": due_box_at()})


@app.get("/api/events")
def get_events():
    with lock: return jsonify({"events": list(events)})


@app.post("/api/warning/clear")
def clear_warning():
    global current_warning
    with lock: current_warning = None
    return jsonify({"ok": True})


@app.post("/api/mock/event")
def mock_event():
    """Optional bench test only. Must set mock_mode=true in config.json; never used by real sensors."""
    if not CONFIG.get("mock_mode"):
        return jsonify({"ok": False, "error": "mock mode disabled"}), 403
    payload = request.get_json(silent=True) or {}
    box_id = str(payload.get("box_id", ""))
    action = str(payload.get("action", "BOX_OPENED"))
    if box_id not in {str(i) for i in range(1, 7)} or action not in {"BOX_OPENED", "BOX_CLOSED"}:
        return jsonify({"ok": False, "error": "box_id must be 1–6 and action BOX_OPENED/BOX_CLOSED"}), 400
    return jsonify({"ok": True, "event": record_event(box_id, action)})


@app.post("/api/kiosk/exit")
def kiosk_exit():
    """Touch-only exit: closes the full-screen Chromium so the Pi desktop shows. Local screen only; the backend keeps running."""
    if request.remote_addr not in ("127.0.0.1", "::1"):
        return jsonify({"ok": False, "error": "local screen only"}), 403
    subprocess.Popen(["pkill", "-f", "smart-medicine-chromium"])
    return jsonify({"ok": True})


if __name__ == "__main__":
    if CONFIG.get("mock_mode"):
        hardware_status = "mock mode (no GPIO polling)"
    else:
        threading.Thread(target=monitor_gpio, name="hall-sensor-monitor", daemon=True).start()
    app.run(host=CONFIG.get("host", "0.0.0.0"), port=int(CONFIG.get("port", 5000)),
            debug=False, use_reloader=False, threaded=True)
