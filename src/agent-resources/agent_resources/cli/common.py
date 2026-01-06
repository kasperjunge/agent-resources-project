"""Shared CLI utilities for skill-add, command-add, and agent-add."""

import random
from contextlib import contextmanager
from pathlib import Path
from urllib.parse import urlparse

import typer
from rich.console import Console
from rich.live import Live
from rich.spinner import Spinner

console = Console()


def parse_resource_ref(ref: str) -> tuple[str, str, str]:
    """
    Parse '<username>/<name>' into components, with optional host.

    Args:
        ref: Resource reference in format 'username/name', 'host/username/name',
             or a full URL like 'https://host/username/name(.git)'

    Returns:
        Tuple of (host, username, name)

    Raises:
        typer.BadParameter: If the format is invalid
    """
    ref = ref.strip()
    if not ref:
        raise typer.BadParameter("Resource reference cannot be empty.")

    host = "github.com"
    path = ref

    if "://" in ref:
        parsed = urlparse(ref)
        if not parsed.netloc:
            raise typer.BadParameter(
                f"Invalid format: '{ref}'. Expected: <username>/<name> or URL."
            )
        host = parsed.netloc
        path = parsed.path.lstrip("/")

    parts = [part for part in path.split("/") if part]
    if len(parts) == 3 and host == "github.com" and "." in parts[0]:
        host, username, name = parts
    elif len(parts) == 2:
        username, name = parts
    else:
        raise typer.BadParameter(
            f"Invalid format: '{ref}'. Expected: <username>/<name> or <host>/<username>/<name>"
        )

    if name.endswith(".git"):
        name = name[: -len(".git")]
    if not username or not name:
        raise typer.BadParameter(
            f"Invalid format: '{ref}'. Expected: <username>/<name> or <host>/<username>/<name>"
        )
    return host, username, name


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


def print_success_message(resource_type: str, host: str, name: str, username: str) -> None:
    """Print branded success message with rotating CTA."""
    console.print(f"✅ Added {resource_type} '{name}' via 🧩 agent-resources", style="dim")

    host_visible = host + "/"
    if host == "github.com":
        host_visible = ""

    ctas = [
        f"💡 Create your own {resource_type} library on GitHub: uvx create-agent-resources-repo --github",
        "⭐ Star: github.com/kasperjunge/agent-resources-project",
        f"📢 Share: uvx add-{resource_type} {host_visible}{username}/{name}",
    ]
    console.print(random.choice(ctas), style="dim")
