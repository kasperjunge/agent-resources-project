"""CLI for agent-add command."""

from typing import Annotated

import typer

from skill_add.cli.common import get_destination, parse_resource_ref
from skill_add.exceptions import (
    ClaudeAddError,
    RepoNotFoundError,
    ResourceExistsError,
    ResourceNotFoundError,
)
from skill_add.fetcher import ResourceType, fetch_resource

app = typer.Typer(
    add_completion=False,
    help="Add Claude Code sub-agents from GitHub to your project.",
)


@app.command()
def add(
    agent_ref: Annotated[
        str,
        typer.Argument(
            help="Agent to add in format: <username>/<agent-name>",
            metavar="USERNAME/AGENT-NAME",
        ),
    ],
    overwrite: Annotated[
        bool,
        typer.Option(
            "--overwrite",
            help="Overwrite existing agent if it exists.",
        ),
    ] = False,
    global_install: Annotated[
        bool,
        typer.Option(
            "--global",
            "-g",
            help="Install to ~/.claude/ instead of ./.claude/",
        ),
    ] = False,
) -> None:
    """
    Add a sub-agent from a GitHub user's agent-skills repository.

    The agent will be copied to .claude/agents/<agent-name>.md in the
    current directory (or ~/.claude/agents/ with --global).

    Example:
        agent-add kasperjunge/code-reviewer
        agent-add kasperjunge/test-writer --global
    """
    try:
        username, agent_name = parse_resource_ref(agent_ref)
    except typer.BadParameter as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)

    dest = get_destination("agents", global_install)
    scope = "user" if global_install else "project"

    typer.echo(f"Fetching agent '{agent_name}' from {username}/agent-skills...")

    try:
        agent_path = fetch_resource(
            username, agent_name, dest, ResourceType.AGENT, overwrite
        )
        typer.echo(f"Added agent '{agent_name}' to {agent_path} ({scope} scope)")
    except RepoNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
    except ResourceNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
    except ResourceExistsError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
    except ClaudeAddError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
