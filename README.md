<div align="center">

# 🧩 agent-resources

**Share and install Claude Code skills, commands, and agents with a single command.**

*Like pip or npm, but for Claude Code resources.*

[![PyPI](https://img.shields.io/pypi/v/agent-resources?color=blue)](https://pypi.org/project/agent-resources/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[Try It Now](#-try-it-now) • [Install Resources](#-install-any-resource) • [Create Your Own](#-create-your-own-toolkit) • [Share](#-share-with-others)

</div>

---

## ⚡ Try It Now

No installation needed. Just run:

```bash
uvx add-skill kasperjunge/hello-world
```

**That's it.** The skill is now available in Claude Code.

---

## 📦 Install Any Resource

```bash
uvx add-skill <github-username>/<skill-name>       # Skills
uvx add-command <github-username>/<command-name>   # Slash commands
uvx add-agent <github-username>/<agent-name>       # Sub-agents
```

---

## 🛠 Create Your Own Toolkit

Build a personal collection of resources that travels with you.

### Step 1: Create your repo

Create a GitHub repository named **`agent-resources`**:

```
your-username/agent-resources/
└── .claude/
    ├── skills/
    │   └── my-skill/
    │       └── SKILL.md
    ├── commands/
    │   └── my-command.md
    └── agents/
        └── my-agent.md
```

### Step 2: There is no step 2

Your resources are now installable:

```bash
uvx add-skill your-username/my-skill
```

No publishing. No registry. Push to GitHub and it works.

---

## 🌍 Share With Others

Found a useful resource? Share it anywhere:

> *"This skill saves me hours — try `uvx add-skill kasperjunge/hello-world`"*

**That's the entire onboarding.** One command, zero friction.

---

## 🗂 Community Resources

*Coming soon — be the first!*

**Built something useful?** [Open an issue](https://github.com/kasperjunge/agent-resources-project/issues) with a link to your `agent-resources` repo and we'll add it here.

---

<div align="center">

**MIT License** · Made for the [Claude Code](https://claude.ai/code) community

</div>
