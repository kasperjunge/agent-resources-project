"""CLI for skill-add command."""

from typing import Annotated

import typer

from agent_resources.cli.common import get_destination, parse_resource_ref
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
    repo: Annotated[
        str,
        typer.Option(
            "--repo",
            help="Repository name to fetch from (default: agent-resources)",
        ),
    ] = "agent-resources",
    dest: Annotated[
        str,
        typer.Option(
            "--dest",
            help="Custom destination path",
        ),
    ] = "",
    environment: Annotated[
        str,
        typer.Option(
            "--env",
            help="Target environment (claude, opencode, codex)",
        ),
    ] = "",
) -> None:
    """
    Add a skill from a GitHub user's agent-resources repository.

    The skill will be copied to .claude/skills/<skill-name>/ in the current
    directory (or ~/.claude/skills/ with --global).

    Example:
        skill-add kasperjunge/analyze-paper
        skill-add kasperjunge/analyze-paper --global
    """
    try:
        username, skill_name = parse_resource_ref(skill_ref)
    except typer.BadParameter as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)

    # Simple destination handling
    dest_path = get_destination(
        "skills", global_install, dest if dest else None, environment if environment else None
    )
    scope = "user" if global_install else "project"

    typer.echo(f"Fetching skill '{skill_name}' from {username}/{repo}...")

    try:
        skill_path = fetch_resource(
            username, skill_name, dest_path, ResourceType.SKILL, overwrite, repo
        )
        typer.echo(f"Added skill '{skill_name}' to {skill_path} ({scope} scope)")
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
