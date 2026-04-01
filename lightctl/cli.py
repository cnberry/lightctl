from __future__ import annotations

import argparse
import json
import sys

from .lights import LightsError, configured_devices, lights_status, set_lights


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="lightctl", description="Terminal-first local light control")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list", help="list configured devices")

    device = sub.add_parser("device", help="operate on a configured device")
    device_sub = device.add_subparsers(dest="device_command", required=True)

    status = device_sub.add_parser("status", help="show status for a configured device")
    status.add_argument("device", help="config device id")
    status.add_argument("--json", action="store_true", help="emit raw JSON")

    on = device_sub.add_parser("on", help="turn a configured device on")
    on.add_argument("device", help="config device id")

    off = device_sub.add_parser("off", help="turn a configured device off")
    off.add_argument("device", help="config device id")

    return parser


def cmd_list() -> int:
    devices_map = configured_devices()
    print("Configured light/switch devices")
    print("------------------------------")
    for config_id, device in devices_map.items():
        ready = "yes" if device.get("local_key") and device.get("switch_dp") else "no"
        print(f"- {config_id}: {device.get('name', config_id)} @ {device.get('host')} (local-ready={ready})")
    return 0


def cmd_status(device_id: str, as_json: bool) -> int:
    try:
        status = lights_status(device_id)
    except LightsError as exc:
        print(f"lightctl error: {exc}", file=sys.stderr)
        return 2

    if as_json:
        print(json.dumps(status, indent=2, sort_keys=True))
        return 0

    print("Light/switch status")
    print("-------------------")
    print(f"- Config id: {status['device_id']}")
    print(f"- Name: {status['name']}")
    print(f"- Backend: {status['backend']}")
    print(f"- Host: {status['host']}:{status['port']}")
    print(f"- Ready for local control: {'yes' if status['ready_for_local_control'] else 'no'}")
    if status["missing"]:
        print(f"- Missing config: {', '.join(status['missing'])}")
    network = status["network"]
    if network.get("ok"):
        print("- Network reachability: ok")
    else:
        print(f"- Network reachability: failed ({network.get('error', 'unknown error')})")
    if "state" in status:
        print(f"- Current state: {'on' if status['state'] else 'off'}")
    if "state_error" in status:
        print(f"- State read error: {status['state_error']}")
    for note in status.get("notes", []):
        print(f"- Note: {note}")
    return 0


def cmd_set(device_id: str, power: bool) -> int:
    try:
        result = set_lights(power, device_id)
    except LightsError as exc:
        print(f"lightctl error: {exc}", file=sys.stderr)
        return 2

    print(f"{result['device_id']}: {'on' if result['state'] else 'off'}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "list":
        return cmd_list()
    if args.command == "device":
        if args.device_command == "status":
            return cmd_status(args.device, args.json)
        if args.device_command == "on":
            return cmd_set(args.device, True)
        if args.device_command == "off":
            return cmd_set(args.device, False)

    parser.print_help()
    return 1
