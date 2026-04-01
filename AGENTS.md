# AGENTS.md

## What this repo is

`lightctl` is a terminal-first local lighting control project.

The goal is to build:
- a clean library layer
- a sharp CLI
- small, explicit commands
- enough local-device support to control real house lights reliably

Think: UNIX tool, not home-automation sludge.

## Project principles

- **Library first, CLI immediately useful.**
  The control/config logic should be reusable, while the CLI stays pleasant for direct human use.

- **Small commands, low surprise.**
  Commands should do one thing well and print useful output.

- **Meaningful house-facing names beat vendor labels.**
  Use names like `landscape-lights`, not random OEM nonsense.

- **Prefer boring local control.**
  Local LAN control beats cloud/app dependency whenever possible.

- **Update docs when the shape settles.**
  When a change feels right, update `README.md` and `AGENTS.md` in the same stretch of work.

- **Prefer pipx for installed CLI usage.**
  For daily use, these tools should behave like normal commands on the user path. Reserve local venv activation for development and testing.

## Current shape

- `lightctl/lights.py` — local config loading, reachability checks, and Tuya-backed light control
- `lightctl/cli.py` — command-line entrypoint
- `config/` — local light configuration (real config ignored, example committed)
- `runbooks/` — setup notes for device onboarding

`SKILL.md` lives at the repo root so Botty can use this CLI directly when Chris asks for house-light actions in chat.

## Near-term roadmap

1. Keep the noun-first CLI shape clean and boring
2. Add `status --json` consistency across commands
3. Add `config` subcommands if useful
4. Keep install/reinstall workflow clean via `pipx`

## Style

- Keep code boring and readable.
- Avoid needless framework energy.
- Prefer explicit names over magic.
- Don’t let the repo turn into app-store cosplay.

## Vibe

This project is a small terminal switchblade for local house lights.

💡🤖🔌
