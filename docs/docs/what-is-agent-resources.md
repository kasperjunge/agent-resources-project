# Resource Types

Agent Resources supports four types of resources.

---

## Skills

Skills extend your agent with new capabilities. They're directories containing a `SKILL.md` file that defines behavior, context, and instructions.

=== "Claude Code"

    ```
    .claude/skills/code-reviewer/
    └── SKILL.md
    ```

=== "Cursor"

    ```
    .cursor/skills/code-reviewer/
    └── SKILL.md
    ```

=== "OpenCode"

    ```
    .opencode/skill/code-reviewer/
    └── SKILL.md
    ```

=== "Codex"

    ```
    .codex/skills/code-reviewer/
    └── SKILL.md
    ```

=== "GitHub Copilot"

    ```
    .github/skills/code-reviewer/
    └── SKILL.md
    ```

---

## Commands

Commands give your agent new slash commands to execute. They're markdown files that define what happens when you run `/command-name`.

=== "Claude Code"

    ```
    .claude/commands/
    └── review.md
    ```

=== "Cursor"

    ```
    .cursor/commands/
    └── review.md
    ```

=== "OpenCode"

    ```
    .opencode/command/
    └── review.md
    ```

=== "Codex"

    ```
    .codex/prompts/
    └── review.md
    ```

=== "GitHub Copilot"

    ```
    .github/prompts/
    └── review.prompt.md
    ```

---

## Subagents

Subagents are specialized agents that your main agent can delegate tasks to. They're markdown files that define the agent's role and capabilities.

=== "Claude Code"

    ```
    .claude/agents/
    └── reviewer-agent.md
    ```

=== "OpenCode"

    ```
    .opencode/agent/
    └── reviewer-agent.md
    ```

=== "Cursor"

    Cursor does not support custom subagents.

=== "Codex"

    Codex does not support custom subagents.

=== "GitHub Copilot"

    GitHub Copilot does not support custom subagents.

---

## Packages

Packages bundle skills, commands, and subagents together. A single package can contain any combination of resource types, plus dependencies on other packages.

=== "Claude Code"

    ```
    .claude/packages/code-reviewer/
    └── PACKAGE.md
    ```

=== "OpenCode"

    ```
    .opencode/package/code-reviewer/
    └── PACKAGE.md
    ```

=== "Codex"

    ```
    .codex/packages/code-reviewer/
    └── PACKAGE.md
    ```

=== "Cursor"

    ```
    .cursor/packages/code-reviewer/
    └── PACKAGE.md
    ```

=== "GitHub Copilot"

    ```
    .github/packages/code-reviewer/
    └── PACKAGE.md
    ```

See [How Packaging Works](how-packaging-works.md) for more details on packages.
