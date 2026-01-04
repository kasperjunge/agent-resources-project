"""Shared CLI utilities for skill-add, command-add, and agent-add."""

from pathlib import Path

import typer


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


def get_destination(resource_subdir: str, global_install: bool) -> Path:
    """
    Get the destination directory for a resource.

    Args:
        resource_subdir: The subdirectory name (e.g., "skills", "commands", "agents")
        global_install: If True, install to ~/.claude/, else to ./.claude/

    Returns:
        Path to the destination directory
    """
    if global_install:
        base = Path.home() / ".claude"
    else:
        base = Path.cwd() / ".claude"

    return base / resource_subdir
