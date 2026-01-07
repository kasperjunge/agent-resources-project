"""CLI for create-agent-resources-repo command."""

from pathlib import Path
from typing import Annotated

import typer

from agent_resources.github import (
    check_gh_cli,
    create_github_repo,
    get_github_username,
    repo_exists,
)
from agent_resources.scaffold import create_agent_resources_repo, init_git

app = typer.Typer(
    add_completion=False,
    help="Create a personal agent-resources repository.",
)


@app.command()
def create(
    path: Annotated[
        Path | None,
        typer.Option(
            "--path",
            "-p",
            help="Directory to create (default: ./agent-resources)",
        ),
    ] = None,
    github: Annotated[
        bool,
        typer.Option(
            "--github",
            "-g",
            help="Create GitHub repository and push (requires gh CLI)",
        ),
    ] = False,
) -> None:
    """
    Create a new agent-resources repository with starter content.

    Creates a directory structure with example skill, command, and agent.
    Initializes git and optionally creates a GitHub repository.

    Example:
        create-agent-resources-repo
        create-agent-resources-repo --github
        create-agent-resources-repo --path ~/my-agent-resources
    """
    # Determine output path
    output_path = path or Path.cwd() / "agent-resources"

    # Check if directory already exists
    if output_path.exists():
        typer.echo(f"Error: Directory already exists: {output_path}", err=True)
        raise typer.Exit(1)

    # Get username for README (if GitHub integration enabled)
    username = "<username>"
    if github:
        if not check_gh_cli():
            typer.echo(
                "Error: GitHub CLI (gh) is not installed or not authenticated.",
                err=True,
            )
            typer.echo("Install: https://cli.github.com/", err=True)
            typer.echo("Then run: gh auth login", err=True)
            raise typer.Exit(1)

        # Check if repo already exists on GitHub
        if repo_exists():
            typer.echo(
                "Error: Repository 'agent-resources' already exists on GitHub.",
                err=True,
            )
            typer.echo(
                "Delete it first or use a different approach.",
                err=True,
            )
            raise typer.Exit(1)

        username = get_github_username() or "<username>"

    # Create the repository structure
    typer.echo(f"Creating agent-resources repository at {output_path}...")
    create_agent_resources_repo(output_path, username)
    typer.echo("  Created directory structure")
    typer.echo("  Added hello-world skill")
    typer.echo("  Added hello command")
    typer.echo("  Added hello-agent agent")
    typer.echo("  Created README.md")

    # Initialize git
    if init_git(output_path):
        typer.echo("  Initialized git repository")
    else:
        typer.echo("  Warning: Could not initialize git repository", err=True)

    # GitHub integration
    if github:
        typer.echo("Creating GitHub repository...")
        repo_url = create_github_repo(output_path)
        if repo_url:
            typer.echo(f"  Pushed to {repo_url}")
            typer.echo("")
            typer.echo("Your agent-resources repo is ready!")
            typer.echo("Others can now install your resources:")
            typer.echo(f"  uvx install-skill {username}/hello-world")
            typer.echo(f"  uvx install-command {username}/hello")
            typer.echo(f"  uvx install-agent {username}/hello-agent")
        else:
            typer.echo("  Error: Could not create GitHub repository", err=True)
            raise typer.Exit(1)
    else:
        typer.echo("")
        typer.echo("Next steps:")
        typer.echo("  1. Create a GitHub repository named 'agent-resources'")
        typer.echo(f"  2. cd {output_path}")
        typer.echo("  3. git remote add origin <your-repo-url>")
        typer.echo("  4. git push -u origin main")
        typer.echo("")
        typer.echo("Or use --github flag to automate this (requires gh CLI)")


if __name__ == "__main__":
    app()
