"""Scaffolding functions for creating agent-resources repository structure."""

import subprocess
from pathlib import Path

HELLO_SKILL = """\
---
name: hello-world
description: A simple example skill that demonstrates Claude Code skill structure
---

# Hello World Skill

This is a demonstration skill showing how skills work.

## When to Use

Apply this skill when the user asks you to say hello or demonstrate skills.

## Instructions

Respond with a friendly greeting explaining this came from a skill.
"""

HELLO_COMMAND = """\
---
description: Say hello - example slash command
---

When the user runs /hello, respond with a friendly greeting.
Explain that this is an example command from their agent-resources repo.
"""

HELLO_AGENT = """\
---
description: Example subagent that greets users
---

You are a friendly greeter subagent.
When invoked, introduce yourself and explain that you're an example agent
from the user's agent-resources repository.
"""

README_TEMPLATE = """\
# agent-resources

My personal collection of Claude Code skills, commands, and agents.

## Structure

```
.claude/
├── skills/       # Skill directories with SKILL.md
├── commands/     # Slash command .md files
└── agents/       # Subagent .md files
```

## Usage

Others can install my resources using:

```bash
# Install a skill
uvx install-skill {username}/hello-world

# Install a command
uvx install-command {username}/hello

# Install an agent
uvx install-agent {username}/hello-agent
```

## Adding Resources

- **Skills**: Create a directory in `.claude/skills/<name>/` with a `SKILL.md` file
- **Commands**: Create a `.md` file in `.claude/commands/`
- **Agents**: Create a `.md` file in `.claude/agents/`

## Learn More

- [agent-resources documentation](https://github.com/kasperjunge/agent-resources)
"""

GITIGNORE = """\
# Python
__pycache__/
*.py[cod]
*$py.class
.env
.venv/
venv/

# OS
.DS_Store
Thumbs.db

# IDE
.idea/
.vscode/
*.swp
*.swo
"""


def scaffold_repo(path: Path) -> None:
    """Create the complete agent-resources directory structure."""
    path.mkdir(parents=True, exist_ok=True)

    # Create .claude directory structure
    claude_dir = path / ".claude"
    (claude_dir / "skills" / "hello-world").mkdir(parents=True, exist_ok=True)
    (claude_dir / "commands").mkdir(parents=True, exist_ok=True)
    (claude_dir / "agents").mkdir(parents=True, exist_ok=True)


def write_starter_skill(path: Path) -> None:
    """Write the hello-world example skill."""
    skill_path = path / ".claude" / "skills" / "hello-world" / "SKILL.md"
    skill_path.write_text(HELLO_SKILL)


def write_starter_command(path: Path) -> None:
    """Write the hello example command."""
    command_path = path / ".claude" / "commands" / "hello.md"
    command_path.write_text(HELLO_COMMAND)


def write_starter_agent(path: Path) -> None:
    """Write the hello-agent example agent."""
    agent_path = path / ".claude" / "agents" / "hello-agent.md"
    agent_path.write_text(HELLO_AGENT)


def write_readme(path: Path, username: str = "<username>") -> None:
    """Write the README.md file."""
    readme_path = path / "README.md"
    readme_path.write_text(README_TEMPLATE.format(username=username))


def write_gitignore(path: Path) -> None:
    """Write the .gitignore file."""
    gitignore_path = path / ".gitignore"
    gitignore_path.write_text(GITIGNORE)


def init_git(path: Path) -> bool:
    """Initialize git repository and create initial commit.

    Returns True if successful, False otherwise.
    """
    try:
        subprocess.run(
            ["git", "init"],
            cwd=path,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "add", "."],
            cwd=path,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "commit", "-m", "Initial commit: agent-resources repo scaffold"],
            cwd=path,
            check=True,
            capture_output=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def create_agent_resources_repo(path: Path, username: str = "<username>") -> None:
    """Create a complete agent-resources repository with all starter content."""
    scaffold_repo(path)
    write_starter_skill(path)
    write_starter_command(path)
    write_starter_agent(path)
    write_readme(path, username)
    write_gitignore(path)
