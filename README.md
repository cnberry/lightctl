# lightctl

Terminal-first local light control.

`lightctl` is a small CLI for local light/switch control, starting with Tuya-family devices. It is meant to hold:
- low-level device control logic
- local device configuration
- recipes for onboarding additional devices
- later scheduling/automation primitives

It is **not** the whole-house support brain. Higher-level house context belongs in `home-helper`.

## Current capabilities
- list configured devices
- read local device status
- turn configured devices on/off
- use local Tuya control over LAN

## CLI

```bash
python3 lightctl.py list
python3 lightctl.py status landscape-lights
python3 lightctl.py on landscape-lights
python3 lightctl.py off landscape-lights
```

## Config

Local device config lives in:

- `config/lights.json`

A template lives in:

- `config/lights.example.json`

Do **not** commit real local keys.

## Development

Create a venv and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Philosophy
- boring over magical
- scriptable over app-ish
- meaningful house-facing names over vendor branding
- low-level control here, higher-level house support elsewhere
