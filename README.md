<div align="center">

# agent-resources

**Share and install Claude Code skills, commands, and agents with a single command.**

*Like pip or npm, but for Claude Code resources.*

[![PyPI](https://img.shields.io/pypi/v/agent-resources?color=blue)](https://pypi.org/project/agent-resources/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[Try It](#-try-it-now) • [Install](#-install-any-resource) • [Create Your Own](#-create-your-own) • [Community](#-community-resources)

</div>

---

## Try It Now

No installation needed. Just run:

```bash
uvx install-skill kasperjunge/hello-world
```

**That's it.** The skill is now available in Claude Code.

---

## Install Any Resource

```bash
uvx install-skill <username>/<skill-name>       # Skills
uvx install-command <username>/<command-name>   # Slash commands
uvx install-agent <username>/<agent-name>       # Sub-agents
```

---

## Create Your Own

Ready to share your own skills? Create your personal toolkit in 30 seconds:

```bash
uvx create-agent-resources-repo --github
```

**Done.** You now have a GitHub repo that anyone can install from.

> Requires [GitHub CLI](https://cli.github.com/). Run without `--github` to set up manually.

### What You Get

- A ready-to-use `agent-resources` repo on your GitHub
- Example skill, command, and agent to learn from
- Instant shareability — tell others:

```bash
uvx install-skill <your-username>/hello-world
```

### Add Your Own Resources

Edit the files in your repo:

```
your-username/agent-resources/
└── .claude/
    ├── skills/          # Skill folders with SKILL.md
    ├── commands/        # Slash command .md files
    └── agents/          # Sub-agent .md files
```

Push to GitHub. No registry, no publishing step.

---

## Share With Others

Sharing is just a message:

> *"This skill saves me hours — try `uvx install-skill yourname/cool-skill`"*

**One command. Zero friction.** The more you share, the more the community grows.

---

## Community Resources

### Go Development Toolkit — [@dsjacobsen](https://github.com/dsjacobsen/agent-resources)

A comprehensive Claude Code toolkit for Go developers.

```bash
uvx install-skill dsjacobsen/golang-pro      # Expert Go knowledge
uvx install-agent dsjacobsen/go-reviewer     # Code review agent
uvx install-command dsjacobsen/go-check      # Quick code check
```

**Includes**: 1 skill, 9 agents, 11 commands covering scaffolding, testing, API building, refactoring, and more.

---

**Built something useful?** [Open an issue](https://github.com/kasperjunge/agent-resources-project/issues) with a link to your `agent-resources` repo and we'll add it here.

---

<div align="center">

**MIT License** · Made for the [Claude Code](https://claude.ai/code) community

</div>
