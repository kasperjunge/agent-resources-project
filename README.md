# skill-add

Add Claude Code skills, slash commands, and sub-agents from GitHub to your project.

## Usage

```bash
# Add a skill (directory)
uvx skill-add <username>/<skill-name>

# Add a slash command (.md file)
uvx --from skill-add command-add <username>/<command-name>

# Add a sub-agent (.md file)
uvx --from skill-add agent-add <username>/<agent-name>
```

These commands fetch resources from the user's `agent-skills` repository on GitHub and copy them to your local `.claude/` directory.

### Options

All commands support these options:

- `--overwrite`: Replace an existing resource if it exists
- `--global, -g`: Install to `~/.claude/` (user-level) instead of `./.claude/` (project-level)

### Examples

```bash
# Add a skill to current project
uvx skill-add kasperjunge/analyze-paper

# Add a skill globally (available in all projects)
uvx skill-add kasperjunge/analyze-paper --global

# Overwrite an existing skill
uvx skill-add kasperjunge/analyze-paper --overwrite

# Add a slash command
uvx --from skill-add command-add kasperjunge/commit

# Add a sub-agent globally
uvx --from skill-add agent-add kasperjunge/code-reviewer --global
```

## Repository Structure

Your `agent-skills` repository should have this structure:

```
agent-skills/
└── .claude/
    ├── skills/
    │   ├── skill-one/
    │   │   └── SKILL.md
    │   └── skill-two/
    │       ├── SKILL.md
    │       └── scripts/
    │           └── helper.py
    ├── commands/
    │   ├── commit.md
    │   └── review-pr.md
    └── agents/
        ├── code-reviewer.md
        └── test-writer.md
```

- **Skills**: Directories containing at minimum a `SKILL.md` file
- **Commands**: Single markdown files (`.md`) defining slash commands
- **Agents**: Single markdown files (`.md`) defining sub-agents

## Installation

```bash
# Run directly with uvx (recommended)
uvx skill-add <username>/<skill-name>
uvx --from skill-add command-add <username>/<command-name>
uvx --from skill-add agent-add <username>/<agent-name>

# Or install globally
pip install skill-add
```
