# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

skill-add is a CLI tool that fetches Claude Code resources (skills, slash commands, and sub-agents) from GitHub and installs them locally. It downloads resources from a user's `agent-skills` repository and copies them to `.claude/` in the current directory or `~/.claude/` for global installation.

## Commands

```bash
# Install dependencies
uv sync

# Run the CLI locally
uv run skill-add <username>/<skill-name>
uv run skill-add <username>/<skill-name> --overwrite
uv run skill-add <username>/<skill-name> --global

uv run command-add <username>/<command-name>
uv run agent-add <username>/<agent-name>

# Build the package
uv build
```

## Architecture

The codebase is a Python CLI with these main modules:

### Core Modules

- `src/skill_add/exceptions.py` - Shared exception classes (`ClaudeAddError`, `RepoNotFoundError`, `ResourceNotFoundError`, `ResourceExistsError`)
- `src/skill_add/fetcher.py` - Generic resource fetcher with `ResourceType` enum and `fetch_resource()` function

### CLI Modules

- `src/skill_add/cli/common.py` - Shared CLI utilities (`parse_resource_ref()`, `get_destination()`)
- `src/skill_add/cli/skill.py` - `skill-add` CLI (for skills - directories)
- `src/skill_add/cli/command.py` - `command-add` CLI (for slash commands - .md files)
- `src/skill_add/cli/agent.py` - `agent-add` CLI (for sub-agents - .md files)

### Backward Compatibility

- `src/skill_add/cli.py` - Re-exports from `cli/skill.py`
- `src/skill_add/github.py` - Re-exports from `fetcher.py` with legacy exception aliases

## Resource Types

| Resource | Source Path | Local Path | Type |
|----------|-------------|------------|------|
| Skill | `.claude/skills/<name>/` | `.claude/skills/<name>/` | Directory |
| Command | `.claude/commands/<name>.md` | `.claude/commands/<name>.md` | File |
| Agent | `.claude/agents/<name>.md` | `.claude/agents/<name>.md` | File |

The tool expects resources to be located at the corresponding paths within the source `agent-skills` repository.
