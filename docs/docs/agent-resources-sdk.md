# Agent Resources SDK

The Agent Resources SDK is a Python library for programmatically accessing skills, commands, and subagents from the Agent Resources hub.

!!! note "Coming Soon"
    The SDK is currently in development. This page documents the planned API.

---

## Overview

Inspired by libraries like Hugging Face Transformers, the SDK provides a simple interface to load and use agent resources in your Python applications.

```python
from agr import Skill, Command, Subagent

# Load resources from the hub
code_reviewer = Skill.from_hub("kasperjunge/code-reviewer")
run_tests = Command.from_hub("kasperjunge/run-tests")
test_writer = Subagent.from_hub("kasperjunge/test-writer")
```

---

## Installation

```bash
pip install agr
```

Or with uv:

```bash
uv add agr
```

---

## Loading Resources

### Skills

Load skills from the hub using `Skill.from_hub()`:

```python
from agr import Skill

# Load a skill
skill = Skill.from_hub("kasperjunge/code-reviewer")

# Access skill metadata
print(skill.name)
print(skill.description)
print(skill.content)
```

### Commands

Load slash commands using `Command.from_hub()`:

```python
from agr import Command

# Load a command
cmd = Command.from_hub("kasperjunge/run-tests")

# Access command metadata
print(cmd.name)
print(cmd.content)
print(cmd.arguments)  # List of input arguments
```

#### Command Arguments

Commands can define input arguments that get passed when executed:

```python
from agr import Command

# Load a command with arguments
cmd = Command.from_hub("kasperjunge/run-tests")

# Inspect available arguments
for arg in cmd.arguments:
    print(f"{arg.name}: {arg.description} (required: {arg.required})")

# Render the command with arguments
rendered = cmd.render(
    test_path="tests/unit/",
    verbose=True
)
```

### Subagents

Load subagents using `Subagent.from_hub()`:

```python
from agr import Subagent

# Load a subagent
agent = Subagent.from_hub("kasperjunge/test-writer")

# Access subagent metadata
print(agent.name)
print(agent.description)
```

---

## Version Pinning

Load specific versions of resources:

```python
from agr import Skill

# Load a specific version
skill = Skill.from_hub("kasperjunge/code-reviewer", version="1.2.0")

# Load latest version (default)
skill = Skill.from_hub("kasperjunge/code-reviewer", version="latest")
```

---

## Caching

The SDK caches downloaded resources locally to avoid repeated network requests.

```python
from agr import Skill

# Resources are cached by default
skill = Skill.from_hub("kasperjunge/code-reviewer")

# Force re-download
skill = Skill.from_hub("kasperjunge/code-reviewer", force_download=True)

# Specify custom cache directory
skill = Skill.from_hub(
    "kasperjunge/code-reviewer",
    cache_dir="~/.my-cache/agr"
)
```

### Cache Location

By default, resources are cached in:

| Platform | Default Cache Location |
|----------|----------------------|
| Linux | `~/.cache/agr/` |
| macOS | `~/Library/Caches/agr/` |
| Windows | `%LOCALAPPDATA%\agr\Cache\` |

---

## Use Cases

### Building AI Workflows

Integrate agent resources into your AI/ML pipelines:

```python
from agr import Skill, Subagent

# Load resources for a code review pipeline
reviewer_skill = Skill.from_hub("kasperjunge/code-reviewer")
security_agent = Subagent.from_hub("kasperjunge/security-checker")

# Use in your application
def review_code(code: str):
    # Apply the skill's instructions to your LLM
    prompt = f"""
    {reviewer_skill.content}
    
    Review this code:
    {code}
    """
    return call_llm(prompt)
```

### Dynamic Resource Loading

Load resources dynamically based on project needs:

```python
from agr import Skill

def get_skill_for_language(language: str) -> Skill:
    skill_map = {
        "python": "kasperjunge/python-testing",
        "javascript": "kasperjunge/js-testing",
        "rust": "kasperjunge/rust-testing",
    }
    
    skill_name = skill_map.get(language)
    if skill_name:
        return Skill.from_hub(skill_name)
    raise ValueError(f"No skill found for {language}")
```

---

## API Reference

### Skill

| Method | Description |
|--------|-------------|
| `Skill.from_hub(name, version="latest")` | Load a skill from the hub |
| `skill.name` | The skill's name |
| `skill.description` | The skill's description |
| `skill.content` | The full SKILL.md content |
| `skill.path` | Local path to the cached skill |

### Command

| Method | Description |
|--------|-------------|
| `Command.from_hub(name, version="latest")` | Load a command from the hub |
| `command.name` | The command's name |
| `command.content` | The command's markdown content |
| `command.arguments` | List of `Argument` objects defining inputs |
| `command.render(**kwargs)` | Render the command with argument values |
| `command.path` | Local path to the cached command |

### Argument

| Property | Description |
|----------|-------------|
| `argument.name` | The argument's name |
| `argument.description` | Description of the argument |
| `argument.required` | Whether the argument is required |
| `argument.default` | Default value (if not required) |

### Subagent

| Method | Description |
|--------|-------------|
| `Subagent.from_hub(name, version="latest")` | Load a subagent from the hub |
| `subagent.name` | The subagent's name |
| `subagent.description` | The subagent's description |
| `subagent.content` | The subagent's markdown content |
| `subagent.path` | Local path to the cached subagent |

---

## Next Steps

- Browse available resources on the [Agent Resources Hub](hub-prototype.html)
- Learn how to [create your own resources](create-your-own-repo.md)
- Understand [how packaging works](how-packaging-works.md)
