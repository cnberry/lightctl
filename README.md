# lightctl 💡🤖🔌

A terminal-first local lighting control tool for flipping lights without cloud lag, app-store sludge, or mystery meat UX.

`lightctl` is a sibling of `poolctl` and `hottubctl`: small commands, readable output, and config that stays local.

## What it does

- lists configured lights and switches
- shows per-device status and readiness
- turns named devices on and off
- prefers local/LAN control over cloud dependency when possible

## Install

```bash
git clone git@github.com:your-user/lightctl.git
cd lightctl
just install
```

That installs `lightctl` with `pipx` so it behaves like a normal command on your shell path.

Useful `just` targets:

```bash
just list
just status outdoor-lights
just on outdoor-lights
just off outdoor-lights
```

## Local config

`lightctl` looks for config in this order:
- `$LIGHTCTL_CONFIG`
- `~/.config/lightctl/lights.json`
- `~/.lightctl/lights.json`
- repo-local `config/lights.json` (dev-only fallback)

Start from:
- `config/lights.example.json`

Do not commit real local keys or live device details.

## Commands

- `lightctl list`
- `lightctl device status outdoor-lights`
- `lightctl device on outdoor-lights`
- `lightctl device off outdoor-lights`

Default output is compact and human-readable.
Use `lightctl list` when you forget what you named things, which will happen because humans are like that.

## Development

For early setup or device experimentation:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python lightctl.py list
python lightctl.py device status outdoor-lights
```

Once the CLI is useful, prefer the installed command shape via `just install` / `just reinstall`.

## Why this repo exists

The point is not to become Yet Another Home Automation Platform.
The point is to keep a few useful local lighting actions scriptable, inspectable, and pleasantly boring.

## Extra docs

- `config/lights.example.json` — starter example config
- `runbooks/tuya-local-setup.md` — notes for onboarding local Tuya-family devices
- `AGENTS.md` — project principles and engineering intent
- `SKILL.md` — lets an agent/chat workflow drive the CLI directly
