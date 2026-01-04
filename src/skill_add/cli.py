"""CLI for skill-add command.

This module is kept for backward compatibility.
The actual implementation is in skill_add.cli.skill.
"""

from skill_add.cli.skill import app

# Re-export for backward compatibility
__all__ = ["app"]

if __name__ == "__main__":
    app()
