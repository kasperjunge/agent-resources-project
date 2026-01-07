"""CLI for install-skill command."""

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
    help="Add Claude Code skills from GitHub to your project.",
)


@app.command()
def add(
    skill_ref: Annotated[
        str,
        typer.Argument(
            help="Skill to add in format: <username>/<skill-name>",
            metavar="USERNAME/SKILL-NAME",
        ),
    ],
    overwrite: Annotated[
        bool,
        typer.Option(
            "--overwrite",
            help="Overwrite existing skill if it exists.",
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
    Add a skill from a GitHub user's agent-resources repository.

    The skill will be copied to .claude/skills/<skill-name>/ in the current
    directory (or ~/.claude/skills/ with --global).

    Example:
        install-skill kasperjunge/analyze-paper
        install-skill kasperjunge/analyze-paper --global
    """
    try:
        username, skill_name = parse_resource_ref(skill_ref)
    except typer.BadParameter as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)

    dest = get_destination("skills", global_install)
    scope = "user" if global_install else "project"

    try:
        with fetch_spinner():
            skill_path = fetch_resource(
                username, skill_name, dest, ResourceType.SKILL, overwrite
            )
        print_success_message("skill", skill_name, username)
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
