# Install Agent Resources

There are several ways to install resources depending on what you need.

---

## Install All From packages/

If your project has a `packages/` directory with installed packages, you can install all of them:

```bash
agr install
```

This works like `npm install` — it reads from the packages directory and ensures all resources are installed.

---

## Install a Package

Packages bundle skills, commands, and subagents together:

```bash
agr install username/packagename
```

---

## Install Individual Resources

You can also install skills, commands, and subagents individually:

```bash
# Install a skill
agr install skill username/skillname

# Install a command
agr install command username/commandname

# Install a subagent
agr install agent username/agentname
```

---

## Using uvx

All commands work with `uvx` if you don't want to install `agr` globally:

```bash
uvx agr install username/packagename
```

---

## Installation Options

Install to a specific tool:

```bash
agr install username/packagename --tool=cursor
```

Install to multiple tools:

```bash
agr install username/packagename --tool=claude,cursor
```

Install globally (available in all projects):

```bash
agr install username/packagename --global
```

Overwrite an existing resource:

```bash
agr install username/packagename --overwrite
```
