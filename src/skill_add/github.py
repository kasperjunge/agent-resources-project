"""GitHub utilities for fetching skills.

This module is kept for backward compatibility.
The actual implementation is in skill_add.fetcher.
"""

from pathlib import Path

from skill_add.exceptions import (
    ClaudeAddError,
    RepoNotFoundError,
    ResourceExistsError,
    ResourceNotFoundError,
)
from skill_add.fetcher import ResourceType, fetch_resource


# Backward-compatible aliases for exception classes
class SkillAddError(ClaudeAddError):
    """Backward-compatible alias for ClaudeAddError."""

    pass


class SkillNotFoundError(ResourceNotFoundError):
    """Backward-compatible alias for ResourceNotFoundError."""

    pass


class SkillExistsError(ResourceExistsError):
    """Backward-compatible alias for ResourceExistsError."""

    pass


def fetch_skill(
    username: str, skill_name: str, dest: Path, overwrite: bool = False
) -> Path:
    """
    Fetch a skill from a user's agent-skills repo and copy it to dest.

    This function is kept for backward compatibility.
    Use fetch_resource() from skill_add.fetcher for new code.

    Args:
        username: GitHub username
        skill_name: Name of the skill to fetch
        dest: Destination directory (typically .claude/skills/)
        overwrite: Whether to overwrite existing skill

    Returns:
        Path to the installed skill directory
    """
    return fetch_resource(username, skill_name, dest, ResourceType.SKILL, overwrite)


# Re-export for backward compatibility
__all__ = [
    "SkillAddError",
    "RepoNotFoundError",
    "SkillNotFoundError",
    "SkillExistsError",
    "fetch_skill",
]
