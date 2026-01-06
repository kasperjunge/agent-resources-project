"""Shared CLI utilities for skill-add, command-add, and agent-add."""

from pathlib import Path

import typer
import yaml


# Default environment configurations
DEFAULT_ENVIRONMENTS = {
    "claude": {
        "skill_dir": ".claude/skills",
        "command_dir": ".claude/commands",
        "agent_dir": ".claude/agents",
    },
    "opencode": {
        "skill_dir": ".opencode/skill",
        "command_dir": ".opencode/command",
        "agent_dir": ".opencode/agent",
        "global_skill_dir": ".config/opencode/skill",
        "global_command_dir": ".config/opencode/command",
        "global_agent_dir": ".config/opencode/agent",
    },
    "codex": {
        "skill_dir": ".codex/skills",
        "command_dir": ".codex/commands",
        "agent_dir": ".codex/agents",
    },
}


def get_environment_config(environment: str | None = None) -> dict:
    """Simple config loading - no caching, no complexity"""
    config_path = Path.home() / ".agent-resources-config.yaml"
    
    # Load user config if exists
    user_config: dict = {}
    if config_path.exists():
        with config_path.open("r") as f:
            user_config = yaml.safe_load(f) or {}
    
    # Merge with defaults - simple and straightforward
    environments = {**DEFAULT_ENVIRONMENTS, **user_config.get("environments", {})}
    
    # Default to claude if no environment specified
    env_name = environment or "claude"
    
    if env_name not in environments:
        raise typer.BadParameter(
            f"Unknown environment: '{env_name}'. "
            f"Available: {', '.join(environments.keys())}"
        )
    
    return environments[env_name]


def parse_resource_ref(ref: str) -> tuple[str, str]:
    """
    Parse '<username>/<name>' into components.

    Args:
        ref: Resource reference in format 'username/name'

    Returns:
        Tuple of (username, name)

    Raises:
        typer.BadParameter: If the format is invalid
    """
    parts = ref.split("/")
    if len(parts) != 2:
        raise typer.BadParameter(
            f"Invalid format: '{ref}'. Expected: <username>/<name>"
        )
    username, name = parts
    if not username or not name:
        raise typer.BadParameter(
            f"Invalid format: '{ref}'. Expected: <username>/<name>"
        )
    return username, name


def get_destination(
    resource_subdir: str,
    global_install: bool,
    custom_dest: str | None = None,
    environment: str | None = None,
) -> Path:
    """
    Get the destination directory for a resource.

    Args:
        resource_subdir: The subdirectory name (e.g., "skills", "commands", "agents")
        global_install: If True, install to home directory, else to current directory
        custom_dest: Optional custom destination path
        environment: Optional environment name (claude, opencode, codex)

    Returns:
        Path to the destination directory
    """
    if custom_dest:
        return Path(custom_dest).expanduser()
    
    # Get environment configuration
    env_config = get_environment_config(environment)
    
    # Build config key based on resource type and global flag
    prefix = "global_" if global_install else ""
    key = f"{prefix}{resource_subdir.rstrip('s')}_dir"  # "skills" -> "skill_dir"
    
    # Get the directory, fallback to non-global if global key doesn't exist
    env_dir = env_config.get(key, env_config[key.replace("global_", "")])
    
    # Determine base path
    base = Path.home() if global_install else Path.cwd()
    
    return base / env_dir
