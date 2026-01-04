"""Shared exception classes for skill-add."""


class ClaudeAddError(Exception):
    """Base exception for claude-add errors."""

    pass


class RepoNotFoundError(ClaudeAddError):
    """Raised when the agent-skills repo doesn't exist."""

    pass


class ResourceNotFoundError(ClaudeAddError):
    """Raised when the skill/command/agent doesn't exist in the repo."""

    pass


class ResourceExistsError(ClaudeAddError):
    """Raised when the resource already exists locally."""

    pass
