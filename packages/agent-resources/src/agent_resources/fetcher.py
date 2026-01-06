"""Generic resource fetcher for skills, commands, and agents."""

import shutil
import tarfile
import tempfile
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

import httpx

from agent_resources.exceptions import (
    ClaudeAddError,
    RepoNotFoundError,
    ResourceExistsError,
    ResourceNotFoundError,
)


class ResourceType(Enum):
    """Type of resource to fetch."""

    SKILL = "skill"
    COMMAND = "command"
    AGENT = "agent"


@dataclass
class ResourceConfig:
    """Configuration for a resource type."""

    resource_type: ResourceType
    source_subdir: str  # e.g., ".claude/skills", ".claude/commands"
    dest_subdir: str  # e.g., "skills", "commands"
    is_directory: bool  # True for skills, False for commands/agents
    file_extension: str | None  # None for skills, ".md" for commands/agents


RESOURCE_CONFIGS: dict[ResourceType, ResourceConfig] = {
    ResourceType.SKILL: ResourceConfig(
        resource_type=ResourceType.SKILL,
        source_subdir=".claude/skills",
        dest_subdir="skills",
        is_directory=True,
        file_extension=None,
    ),
    ResourceType.COMMAND: ResourceConfig(
        resource_type=ResourceType.COMMAND,
        source_subdir=".claude/commands",
        dest_subdir="commands",
        is_directory=False,
        file_extension=".md",
    ),
    ResourceType.AGENT: ResourceConfig(
        resource_type=ResourceType.AGENT,
        source_subdir=".claude/agents",
        dest_subdir="agents",
        is_directory=False,
        file_extension=".md",
    ),
}

# Pattern-based search for different repository structures
RESOURCE_SEARCH_PATTERNS = {
    ResourceType.SKILL: [
        ".claude/skills/{name}/",  # Current (first for backward compat)
        "skills/{name}/",  # Anthropics pattern
        "skill/{name}/",  # opencode pattern
    ],
    ResourceType.COMMAND: [
        ".claude/commands/{name}.md",  # Current
        "commands/{name}.md",
        "command/{name}.md",  # opencode pattern
    ],
    ResourceType.AGENT: [
        ".claude/agents/{name}.md",  # Current
        "agents/{name}.md",
        "agent/{name}.md",  # opencode pattern
    ],
}

# Name of the repository to fetch resources from
REPO_NAME = "agent-resources"


def validate_repository_structure(repo_dir: Path) -> dict:
    """Simple validation that provides useful feedback"""

    # Check for any recognizable patterns
    patterns_found = []
    for pattern in [
        ".claude/skills",
        "skills",
        "skill",
        ".claude/commands",
        "commands",
        "command",
        ".claude/agents",
        "agents",
        "agent",
    ]:
        if (repo_dir / pattern).exists():
            patterns_found.append(pattern)

    # Simple suggestions
    suggestions = []
    if not patterns_found:
        suggestions.append("Repository doesn't match common agent-resources patterns")
        suggestions.append("Expected: .claude/skills/, skills/, or skill/ directories")

    return {"patterns_found": patterns_found, "suggestions": suggestions}


def find_resource_in_repo(
    repo_dir: Path, resource_type: ResourceType, name: str
) -> Path | None:
    """Simple pattern-based search - no caching, no complexity"""
    config = RESOURCE_CONFIGS[resource_type]

    for pattern in RESOURCE_SEARCH_PATTERNS[resource_type]:
        search_path = pattern.format(name=name)
        if config.file_extension and not search_path.endswith(config.file_extension):
            search_path += config.file_extension

        resource_path = repo_dir / search_path
        if resource_path.exists():
            return resource_path

    return None


def fetch_resource(
    username: str,
    name: str,
    dest: Path,
    resource_type: ResourceType,
    overwrite: bool = False,
    repo: str = "agent-resources",  # Simple repo name override
) -> Path:
    """
    Fetch a resource from a user's agent-resources repo and copy it to dest.

    Args:
        username: GitHub username
        name: Name of the resource to fetch
        dest: Destination directory (e.g., .claude/skills/, .claude/commands/)
        resource_type: Type of resource (SKILL, COMMAND, or AGENT)
        overwrite: Whether to overwrite existing resource

    Returns:
        Path to the installed resource

    Raises:
        RepoNotFoundError: If the agent-resources repo doesn't exist
        ResourceNotFoundError: If the resource doesn't exist in the repo
        ResourceExistsError: If resource exists locally and overwrite=False
    """
    config = RESOURCE_CONFIGS[resource_type]

    # Determine destination path
    if config.is_directory:
        resource_dest = dest / name
    else:
        resource_dest = dest / f"{name}{config.file_extension}"

    # Check if resource already exists locally
    if resource_dest.exists() and not overwrite:
        raise ResourceExistsError(
            f"{resource_type.value.capitalize()} '{name}' already exists at {resource_dest}\n"
            f"Use --overwrite to replace it."
        )

    # Download tarball
    tarball_url = f"https://github.com/{username}/{repo}/archive/refs/heads/main.tar.gz"

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        tarball_path = tmp_path / "repo.tar.gz"

        # Download
        try:
            with httpx.Client(follow_redirects=True, timeout=30.0) as client:
                response = client.get(tarball_url)
                if response.status_code == 404:
                    raise RepoNotFoundError(
                        f"Repository '{username}/{repo}' not found on GitHub."
                    )
                response.raise_for_status()

                tarball_path.write_bytes(response.content)
        except httpx.HTTPStatusError as e:
            raise ClaudeAddError(f"Failed to download repository: {e}")
        except httpx.RequestError as e:
            raise ClaudeAddError(f"Network error: {e}")

        # Extract
        extract_path = tmp_path / "extracted"
        with tarfile.open(tarball_path, "r:gz") as tar:
            tar.extractall(extract_path)

        # Find the resource in extracted content using pattern-based search
        # Tarball extracts to: <repo>-main/<patterns>
        repo_dir = extract_path / f"{repo}-main"

        # Use pattern-based search to find the resource
        resource_source = find_resource_in_repo(repo_dir, resource_type, name)

        if resource_source is None or not resource_source.exists():
            patterns_tried = [
                p.format(name=name) for p in RESOURCE_SEARCH_PATTERNS[resource_type]
            ]
            patterns_list = "\n".join([f"- {p}" for p in patterns_tried])

            # Validate repository structure for helpful suggestions
            validation = validate_repository_structure(repo_dir)

            error_msg = (
                f"{resource_type.value.capitalize()} '{name}' not found in {username}/{repo}.\n"
                f"Tried these locations:\n{patterns_list}\n"
            )

            # Add validation suggestions if available
            if validation["suggestions"]:
                error_msg += "\nRepository structure issues:\n"
                error_msg += "\n".join([f"• {s}" for s in validation["suggestions"]])
                error_msg += "\n"
            elif validation["patterns_found"]:
                error_msg += (
                    f"\nFound directories: {', '.join(validation['patterns_found'])}\n"
                )

            error_msg += (
                "\nQuick fixes:\n"
                "• Double-check the resource name\n"
                "• Try --repo REPO_NAME if using a different repository\n"
                "• Try --dest PATH for custom installation location\n"
                f"• Visit https://github.com/{username}/{repo} to verify the resource exists"
            )

            raise ResourceNotFoundError(error_msg)

        # Remove existing if overwriting
        if resource_dest.exists():
            if config.is_directory:
                shutil.rmtree(resource_dest)
            else:
                resource_dest.unlink()

        # Ensure destination parent exists
        dest.mkdir(parents=True, exist_ok=True)

        # Copy resource to destination
        if config.is_directory:
            shutil.copytree(str(resource_source), str(resource_dest))
        else:
            shutil.copy2(str(resource_source), str(resource_dest))

    return resource_dest
