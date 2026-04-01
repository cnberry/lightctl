# lightctl 💡🤖🔌

A terminal-first local light control tool for flipping house lights without app-store sludge.

## Goals

- Control local lights from a small CLI
- Prefer LAN/local control over cloud dependency
- Use meaningful house-facing names
- Keep the interface sharp, boring, and scriptable

## Status

Early local-light CLI, currently focused on configured Tuya-family devices.
The structure is being aligned with `poolctl` so both repos feel like siblings.

## Visual identity

```text
    .--.
 .-(    ).        lightctl
(___.__)__)       💡🤖🔌
   |    |
   |____|
```

## Commands

- `lightctl list`
- `lightctl status landscape-lights`
- `lightctl on landscape-lights`
- `lightctl off landscape-lights`

Default output is compact and human-readable.

## Config

Local light config lives in:
- `config/lights.json`

Template:
- `config/lights.example.json`

Do not commit real local keys.

## Install

Preferred install for a real always-available CLI:

```bash
pipx install --editable .
```

After edits:

```bash
pipx reinstall --editable .
```

That puts `lightctl` on your normal user path without requiring venv activation for daily use.

## Development

Classic direct shell flow:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python lightctl.py list
```

Or, if you have `just` and `pipx` installed:

```bash
just install
just list
just status landscape-lights
```

## Maintenance rule

When a behavior or interface change feels like a keeper, update the docs immediately:
- `README.md` for user-facing changes
- `AGENTS.md` for project principles and engineering intent

Clean code. Good code. Updated docs.

## Notes for agents and future-us

See `AGENTS.md` for project principles and repo shape.
`SKILL.md` lives at the repo root so Botty can use this CLI directly from chat requests.
