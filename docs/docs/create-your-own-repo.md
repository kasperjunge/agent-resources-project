# Create Your Own Repo

You can host skills, commands, and subagents in any public GitHub repository. This guide shows you how to set up a repo and install resources from it.

---

## Repository Structure

Your repo must follow this structure:

=== "Claude Code"

    ```
    your-repo/
    └── .claude/
        ├── skills/
        │   └── my-skill/
        │       └── SKILL.md
        ├── commands/
        │   └── my-command.md
        └── agents/
            └── my-agent.md
    ```

=== "Cursor"

    ```
    your-repo/
    └── .cursor/
        ├── skills/
        │   └── my-skill/
        │       └── SKILL.md
        └── commands/
            └── my-command.md
    ```

=== "Codex"

    ```
    your-repo/
    └── .codex/
        ├── skills/
        │   └── my-skill/
        │       └── SKILL.md
        └── prompts/
            └── my-command.md
    ```

=== "GitHub Copilot"

    ```
    your-repo/
    └── .github/
        ├── skills/
        │   └── my-skill/
        │       └── SKILL.md
        └── prompts/
            └── my-command.prompt.md
    ```

=== "OpenCode"

    ```
    your-repo/
    └── .opencode/
        ├── skill/
        │   └── my-skill/
        │       └── SKILL.md
        ├── command/
        │   └── my-command.md
        └── agent/
            └── my-agent.md
    ```

**Key requirements:**

- Skills are directories containing a `SKILL.md` file
- Commands and subagents are `.md` files directly in their folders
- Your repo must have a `main` branch

---

## Quick Setup

Scaffold a new repo with example resources:

```bash
agr init repo my-agent-resources
```

This creates the directory structure with example skill, command, and subagent files.

To create individual resources:

```bash
agr init skill my-skill
agr init command my-command
agr init agent my-agent
agr init my-package
```

Push to GitHub and you're ready to share.

---

## Install from Any Repo

By default, `agr` looks for resources in a repo named `agent-resources`:

```bash
# Installs from github.com/username/agent-resources
agr install skill username/my-skill
```

If you name your repo `agent-resources`, users only need to specify your username and resource name. This is the recommended convention for sharing resources.

To install from a differently named repo, use the three-part format:

```bash
# Installs from github.com/username/custom-repo
agr install skill username/custom-repo/my-skill
```
