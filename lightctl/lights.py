from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
ENV_CONFIG_PATH = "LIGHTCTL_CONFIG"
DEFAULT_CONFIG_BASENAME = "lights.json"
SEARCH_DIRS = [
    Path.home() / ".config" / "lightctl",
    Path.home() / ".lightctl",
    ROOT / "config",
]
VENV_PY = ROOT / ".venv" / "bin" / "python"


class LightsError(RuntimeError):
    pass


class LightsNotConfiguredError(LightsError):
    pass


class LightNetworkError(LightsError):
    pass


def _python_bin() -> str:
    if VENV_PY.exists():
        return str(VENV_PY)
    return sys.executable


def _config_path() -> Path:
    override = os.environ.get(ENV_CONFIG_PATH)
    if override:
        return Path(override).expanduser()
    for directory in SEARCH_DIRS:
        candidate = directory / DEFAULT_CONFIG_BASENAME
        if candidate.exists():
            return candidate
    return SEARCH_DIRS[0] / DEFAULT_CONFIG_BASENAME


def load_lights_config() -> dict[str, Any]:
    path = _config_path()
    if not path.exists():
        raise LightsNotConfiguredError(
            f"lights config not found at {path}. create it from config/lights.example.json or set {ENV_CONFIG_PATH}"
        )
    with path.open() as f:
        return json.load(f)


def configured_devices() -> dict[str, dict[str, Any]]:
    return load_lights_config().get("devices", {})


def device_config(device_id: str) -> dict[str, Any]:
    devices = configured_devices()
    if device_id not in devices:
        raise LightsNotConfiguredError(f"device '{device_id}' not found in lights config")
    device = devices[device_id]
    required = ["host", "device_id"]
    missing = [field for field in required if not device.get(field)]
    if missing:
        raise LightsNotConfiguredError(f"device '{device_id}' missing required fields: {', '.join(missing)}")
    return device


def local_ready(device_id: str) -> tuple[bool, list[str], dict[str, Any]]:
    device = device_config(device_id)
    missing = []
    if not device.get("local_key"):
        missing.append("local_key")
    if not device.get("switch_dp"):
        missing.append("switch_dp")
    return (len(missing) == 0, missing, device)


def reachability(device_id: str, timeout_s: float = 1.5) -> dict[str, Any]:
    device = device_config(device_id)
    host = device["host"]
    port = int(device.get("port", 6668))
    try:
        with socket.create_connection((host, port), timeout=timeout_s):
            return {"ok": True, "host": host, "port": port}
    except OSError as exc:
        return {"ok": False, "host": host, "port": port, "error": str(exc)}


def _normalize_device(device_id: str) -> dict[str, Any]:
    device = dict(device_config(device_id))
    device["config_id"] = device_id
    return device


def _tuya_rpc(device: dict[str, Any], action: str, power: bool | None = None) -> dict[str, Any]:
    script = """
import json
import tinytuya

device = json.loads({device_json!r})
action = {action!r}
power = {power!r}

outlet = tinytuya.OutletDevice(device['device_id'], device['host'], device['local_key'])
outlet.set_version(float(device.get('protocol_version', '3.3')))

if action == 'status':
    result = outlet.status()
elif action == 'set':
    result = outlet.set_status(bool(power), int(str(device['switch_dp'])))
    status = outlet.status()
    result = {{'response': result, 'status': status}}
else:
    raise SystemExit(f'unknown action: {action}')

print(json.dumps(result))
""".format(
        device_json=json.dumps(device),
        action=action,
        power=power,
    )

    result = subprocess.run(
        [_python_bin(), "-c", script],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise LightsError(result.stderr.strip() or result.stdout.strip() or "tinytuya command failed")
    return json.loads(result.stdout)


def _extract_switch_state(status: dict[str, Any], switch_dp: str) -> Any:
    dps = status.get("dps", {})
    return dps.get(str(switch_dp))


def lights_status(device_id: str) -> dict[str, Any]:
    ready, missing, device = local_ready(device_id)
    network = reachability(device_id)
    result = {
        "device_id": device_id,
        "name": device.get("name", device_id),
        "backend": device.get("backend", "unknown"),
        "host": device.get("host"),
        "port": int(device.get("port", 6668)),
        "ready_for_local_control": ready,
        "missing": missing,
        "network": network,
        "notes": [
            "Need local_key and switch_dp before local on/off can be used.",
            "Configured device should use a meaningful house-facing name, not an OEM vendor label.",
        ],
    }

    if ready and network.get("ok"):
        try:
            normalized = _normalize_device(device_id)
            raw = _tuya_rpc(normalized, "status")
            result["state"] = _extract_switch_state(raw, str(device.get("switch_dp")))
            result["raw_status"] = raw
        except Exception as exc:  # pragma: no cover
            result["state_error"] = str(exc)
    return result


def set_lights(power: bool, device_id: str) -> dict[str, Any]:
    ready, missing, device = local_ready(device_id)
    if not ready:
        raise LightsNotConfiguredError(
            f"device '{device_id}' local control is not ready; missing: " + ", ".join(missing)
        )

    network = reachability(device_id)
    if not network.get("ok"):
        raise LightNetworkError(
            f"device '{device_id}' is not reachable at {network.get('host')}:{network.get('port')} - {network.get('error')}"
        )

    normalized = _normalize_device(device_id)
    rpc = _tuya_rpc(normalized, "set", power=power)
    status = rpc["status"]
    return {
        "device_id": device_id,
        "name": device.get("name", device_id),
        "requested_power": power,
        "response": rpc["response"],
        "state": _extract_switch_state(status, str(device.get("switch_dp"))),
        "raw_status": status,
    }
