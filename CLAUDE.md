# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project Overview

This is a Python monorepo containing CLI tools for installing Claude Code resources (skills, commands, and sub-agents) from GitHub repositories.

## Repository Structure

```
agent-resources-project/
├── src/
│   ├── agent-resources/           # Python core library
│   │   ├── pyproject.toml         # Package config
│   │   └── agent_resources/       # Source code
│   │       ├── cli/               # CLI implementations
│   │       ├── fetcher.py         # GitHub tarball fetching
│   │       ├── exceptions.py      # Custom exceptions
│   │       └── ...
│   └── agent-resources-npm/       # npm core library (future)
├── command-packages/
│   ├── pypi/                      # PyPI wrapper packages
│   │   ├── install-skill/         # `uvx install-skill`
│   │   ├── install-command/       # `uvx install-command`
│   │   ├── install-agent/         # `uvx install-agent`
│   │   └── create-agent-resources-repo/
│   └── npm/                       # npm wrapper packages (future)
├── CLAUDE.md
└── README.md
```

**Primary usage pattern** is via uvx for one-off execution:
```bash
uvx install-skill <username>/<skill-name>
uvx install-command <username>/<command-name>
uvx install-agent <username>/<agent-name>
uvx create-agent-resources-repo
```

The wrapper packages in `command-packages/pypi/` exist to enable this clean uvx UX. They are thin wrappers that depend on `agent-resources`, which contains the shared core logic.


## Architecture

**Core Components** (in `src/agent-resources/agent_resources/`):
- `fetcher.py` - Generic resource fetcher that downloads from GitHub tarballs and extracts resources
- `cli/common.py` - Shared CLI utilities (argument parsing, destination resolution)
- `cli/skill.py`, `cli/command.py`, `cli/agent.py` - Typer CLI apps for each resource type
- `exceptions.py` - Custom exception hierarchy

**Resource Types**:
- Skills: Directories copied to `.claude/skills/<name>/`
- Commands: Single `.md` files copied to `.claude/commands/<name>.md`
- Agents: Single `.md` files copied to `.claude/agents/<name>.md`

**Fetching Pattern**: Resources are fetched from `https://github.com/<username>/agent-resources/` repositories by downloading the main branch tarball and extracting the specific resource.

## Dependencies

- `httpx` - HTTP client for downloading from GitHub
- `typer` - CLI framework
