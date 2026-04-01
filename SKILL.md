---
name: lightctl
description: Control Chris's local house lights from the `lightctl` CLI. Use when asked to list configured lights, check light status, turn named lights on or off, inspect local light config/readiness, or operate supported local Tuya-family devices from this repo.
---

# lightctl

Use the local `lightctl` CLI from this repository.

## Rules

- Prefer the `lightctl` CLI over ad-hoc Python when the command already exists.
- Keep responses short and action-oriented.
- Report compact final CLI output, not raw internal debugging unless asked.
- Use meaningful configured device names like `landscape-lights`.

## Run from repo root

```bash
cd REPO_ROOT/lightctl
. .venv/bin/activate
```

## Command map

### Inspection

```bash
lightctl list
lightctl device status landscape-lights
```

### Control

```bash
lightctl device on landscape-lights
lightctl device off landscape-lights
```

Use for requests like:
- "turn on the landscape lights"
- "turn off outdoor lights"
- "is landscape lighting on?"
- "list configured lights"

## Response style

Examples:
- "Done. landscape-lights: on"
- "landscape-lights: off"
- "Configured lights: landscape-lights"

If a command fails, quote the relevant error briefly and say what you’ll do next.
