"""CLI for install-agent command."""

from typing import Annotated

import typer

from agent_resources.cli.common import fetch_spinner, get_destination, parse_resource_ref, print_success_message
from agent_resources.exceptions import (
    ClaudeAddError,
    RepoNotFoundError,
    ResourceExistsError,
    ResourceNotFoundError,
)
from agent_resources.fetcher import ResourceType, fetch_resource

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
    Add a sub-agent from a GitHub user's agent-resources repository.

    The agent will be copied to .claude/agents/<agent-name>.md in the
    current directory (or ~/.claude/agents/ with --global).

    Example:
        install-agent kasperjunge/code-reviewer
        install-agent kasperjunge/test-writer --global
    """
    try:
        username, agent_name = parse_resource_ref(agent_ref)
    except typer.BadParameter as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)

    dest = get_destination("agents", global_install)
    scope = "user" if global_install else "project"

    try:
        with fetch_spinner():
            agent_path = fetch_resource(
                username, agent_name, dest, ResourceType.AGENT, overwrite
            )
        print_success_message("agent", agent_name, username)
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
