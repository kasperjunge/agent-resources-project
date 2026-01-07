"""Shared CLI utilities for install-skill, install-command, and install-agent."""

import random
from contextlib import contextmanager
from pathlib import Path

import typer
from rich.console import Console
from rich.live import Live
from rich.spinner import Spinner

console = Console()


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


@contextmanager
def fetch_spinner():
    """Show spinner during fetch operation."""
    with Live(Spinner("dots", text="Fetching..."), console=console, transient=True):
        yield


def print_success_message(resource_type: str, name: str, username: str) -> None:
    """Print branded success message with rotating CTA."""
    console.print(f"✅ Added {resource_type} '{name}' via 🧩 agent-resources", style="dim")
    ctas = [
        f"💡 Create your own {resource_type} library on GitHub: uvx create-agent-resources-repo --github",
        "⭐ Star: github.com/kasperjunge/agent-resources-project",
        f"📢 Share: uvx install-{resource_type} {username}/{name}",
    ]
    console.print(random.choice(ctas), style="dim")
