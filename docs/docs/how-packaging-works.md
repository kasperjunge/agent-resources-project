# How Packaging Works

Agent Resources is designed to be the universal package manager and system for AI agents. This page explains the core concepts.

---

## Core Principles

| Principle | What it means |
|-----------|---------------|
| **Simplicity over features** | 1-3 operations for all tasks |
| **Decentralized by default** | GitHub paths work directly, no gatekeeping |
| **Cross-tool first** | Write once, deploy to Claude Code, Cursor, Codex, GitHub Copilot, OpenCode |
| **Dev = Installed** | Same structure everywhere |
| **Zero overhead** | No lock files, no metadata directories |

---

## The PACKAGE.md Manifest

Every package has a `PACKAGE.md` file that contains metadata and documentation in one place.

```markdown
---
name: code-reviewer
version: 1.2.0
description: AI-powered code review with security scanning
author: anthropics
license: MIT

resources:
  skills:
    - code-reviewer
  commands:
    - review
    - quick-check
  subagents:
    - reviewer-agent

dependencies:
  anthropics/security-rules: "^2.0.0"
---

# Code Reviewer

A comprehensive code review toolkit.

## Usage

Run `/review` on any file or directory.
```

---

## Package Structure

### Development (Author's Repo)

=== "Claude Code"

    ```
    my-project/
    └── .claude/
        ├── packages/
        │   └── code-reviewer/
        │       └── PACKAGE.md
        ├── skills/
        │   └── code-reviewer/
        │       └── SKILL.md
        ├── commands/
        │   ├── review.md
        │   └── quick-check.md
        └── agents/
            └── reviewer-agent.md
    ```

=== "Cursor"

    ```
    my-project/
    └── .cursor/
        ├── packages/
        │   └── code-reviewer/
        │       └── PACKAGE.md
        ├── skills/
        │   └── code-reviewer/
        │       └── SKILL.md
        └── commands/
            ├── review.md
            └── quick-check.md
    ```

=== "Codex"

    ```
    my-project/
    └── .codex/
        ├── packages/
        │   └── code-reviewer/
        │       └── PACKAGE.md
        ├── skills/
        │   └── code-reviewer/
        │       └── SKILL.md
        └── prompts/
            ├── review.md
            └── quick-check.md
    ```

=== "GitHub Copilot"

    ```
    my-project/
    └── .github/
        ├── packages/
        │   └── code-reviewer/
        │       └── PACKAGE.md
        ├── skills/
        │   └── code-reviewer/
        │       └── SKILL.md
        └── prompts/
            ├── review.prompt.md
            └── quick-check.prompt.md
    ```

=== "OpenCode"

    ```
    my-project/
    └── .opencode/
        ├── package/
        │   └── code-reviewer/
        │       └── PACKAGE.md
        ├── skill/
        │   └── code-reviewer/
        │       └── SKILL.md
        ├── command/
        │   ├── review.md
        │   └── quick-check.md
        └── agent/
            └── reviewer-agent.md
    ```

### Installed (User's Project)

After `agr install anthropics/code-reviewer`:

=== "Claude Code"

    ```
    user-project/
    └── .claude/
        ├── packages/
        │   ├── code-reviewer/
        │   │   └── PACKAGE.md
        │   └── security-rules/        # dependency
        │       └── PACKAGE.md
        ├── skills/
        │   └── code-reviewer/
        │       └── code-reviewer/
        │           └── SKILL.md
        ├── commands/
        │   └── code-reviewer/
        │       ├── review.md
        │       └── quick-check.md
        └── agents/
            └── code-reviewer/
                └── reviewer-agent.md
    ```

=== "Cursor"

    ```
    user-project/
    └── .cursor/
        ├── packages/
        │   ├── code-reviewer/
        │   │   └── PACKAGE.md
        │   └── security-rules/        # dependency
        │       └── PACKAGE.md
        ├── skills/
        │   └── code-reviewer/
        │       └── code-reviewer/
        │           └── SKILL.md
        └── commands/
            └── code-reviewer/
                ├── review.md
                └── quick-check.md
    ```

=== "Codex"

    ```
    user-project/
    └── .codex/
        ├── packages/
        │   ├── code-reviewer/
        │   │   └── PACKAGE.md
        │   └── security-rules/        # dependency
        │       └── PACKAGE.md
        ├── skills/
        │   └── code-reviewer/
        │       └── code-reviewer/
        │           └── SKILL.md
        └── prompts/
            └── code-reviewer/
                ├── review.md
                └── quick-check.md
    ```

=== "GitHub Copilot"

    ```
    user-project/
    └── .github/
        ├── packages/
        │   ├── code-reviewer/
        │   │   └── PACKAGE.md
        │   └── security-rules/        # dependency
        │       └── PACKAGE.md
        ├── skills/
        │   └── code-reviewer/
        │       └── code-reviewer/
        │           └── SKILL.md
        └── prompts/
            └── code-reviewer/
                ├── review.prompt.md
                └── quick-check.prompt.md
    ```

=== "OpenCode"

    ```
    user-project/
    └── .opencode/
        ├── package/
        │   ├── code-reviewer/
        │   │   └── PACKAGE.md
        │   └── security-rules/        # dependency
        │       └── PACKAGE.md
        ├── skill/
        │   └── code-reviewer/
        │       └── code-reviewer/
        │           └── SKILL.md
        ├── command/
        │   └── code-reviewer/
        │       ├── review.md
        │       └── quick-check.md
        └── agent/
            └── code-reviewer/
                └── reviewer-agent.md
    ```

Resources are namespaced by package name to prevent collisions.

---

## Dependencies

Packages can depend on other packages. Dependencies are resolved using Minimal Version Selection:

1. Build dependency graph from all requirements
2. Select the minimum version that satisfies all constraints
3. On conflict, fail with clear guidance

No lock file needed. The installed `PACKAGE.md` files contain exact resolved versions.

---

## Cross-Tool Support

Agent Resources translates packages to work across tools:

```bash
$ agr install anthropics/code-reviewer

Detected tools: Claude Code, Cursor

Installing to:
  Claude Code: .claude/skills/code-reviewer/
  Cursor: .cursor/skills/code-reviewer/

Done
```

---

## Team Workflow

Share packages with your team by committing the packages directory:

```bash
# Developer A adds a package
agr install anthropics/code-reviewer
git add .claude/packages/   # or .cursor/packages/, .codex/packages/, etc.
git commit -m "Add code-reviewer package"
git push

# Developer B gets the same packages
git pull
agr install
```

Running `agr install` without arguments reads the packages directory and ensures all resources are installed.
