#!/usr/bin/env python3
"""Prepare user-facing markdown manuals from synced source docs."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "docs" / "_source"
TARGET = ROOT / "docs"

USER_NAV = "> [Home](../index.html) · [Docs](index.html) · [Quick start](getting-started.html) · [Install](install.html)"

MCP_INTRO = """
stdio MCP server for **Claude Code, Cursor Agent, Codex, Gemini CLI**, and other MCP hosts.

**Normal use:** configure once, open your AI tool in the project folder — the host starts MCP automatically.
"""

MCP_BEFORE_START = """
## Before you start

| Requirement | Notes |
|-------------|-------|
| Node.js | **18+** |
| Workspace | A real **project folder** (not a single file) |
| Setup | One command per host — see [Connect your AI tool](#connect-your-ai-tool) |
"""

MCP_MAIN_TOOLS = """
## Main MCP tools

| Group | What it does | Examples |
|-------|--------------|----------|
| **Inspect** | Read project intelligence | `inspect_state`, `inspect_health`, `inspect_graph` |
| **Transfer** | Export context for AI chats | `transfer_context`, `transfer_handoff`, `transfer_intelligence` |
| **Capture** | Save focus, notes, decisions | `capture_focus`, `capture_note`, `capture_decision` |

On a **new AI chat**, the agent may ask to inject project state (Y/n). No terminal command needed.
"""

MCP_HOST_SETUP = """
## Connect your AI tool

Run **one command** from your project folder, then open the AI tool in that folder.  
Node.js **18+** required. No JSON editing needed in normal use.

### Codex

```bash
cd /path/to/your-project
codex mcp add contorium -- npx @contorium/mcp
```

Open Codex in the project folder. Remove: `codex mcp remove contorium`

### Claude Code

```bash
cd /path/to/your-project
claude mcp add --scope project contorium -- npx @contorium/mcp
```

Restart Claude Code in the same folder. Remove: `claude mcp remove contorium`

### Cursor

1. **Settings → MCP → Add MCP Server**
2. Name: `contorium` · Command: `npx` · Args: `@contorium/mcp`
3. Enable the server → **Developer: Reload Window**

Remove: Settings → MCP → delete `contorium`

### Gemini CLI

Add to `~/.gemini/settings.json` or `<project>/.gemini/settings.json`:

```json
{
  "mcpServers": {
    "contorium": {
      "command": "npx",
      "args": ["@contorium/mcp"],
      "env": {
        "CONTORIUM_WORKSPACE": "/path/to/your-project"
      }
    }
  }
}
```

Restart the Gemini CLI session after saving.

---

## Manual config (fallback only)

Use this **only if** the one-liner above fails. Do **not** combine with `mcp add`.

<a id="manual-config-fallback"></a>

```json
{
  "mcpServers": {
    "contorium": {
      "command": "npx",
      "args": ["@contorium/mcp"],
      "env": {
        "CONTORIUM_WORKSPACE": "/path/to/your-project"
      }
    }
  }
}
```

| Host | Config file |
|------|-------------|
| Cursor | `.cursor/mcp.json` or Settings → MCP |
| Claude Code | `.mcp.json` in project root |
| Codex | `config.toml` under `[mcp_servers.contorium]` |
| Gemini CLI | `settings.json` → `mcpServers` |
"""

GETTING_STARTED = """# Quick start

{nav}

Contorium is an **AI Project Intelligence Layer**. It keeps project understanding in your workspace so AI tools can **continue where you left off** — without re-explaining architecture every session.

**You use it by:** installing one entry point (IDE, MCP, or CLI), opening a **folder** workspace, then using **Inspect · Transfer · Capture** as you work with AI.

---

## Choose your entry point

| If you… | Start with |
|---------|------------|
| Code in VS Code / Cursor | [IDE extension](ide-extension.html) |
| Use Claude Code, Codex, or Cursor Agent | [MCP server](mcp.html) |
| Work in the terminal or CI | [CLI](cli.html) |

All three share the same `.contora/` folder in your project. You can add more later.

---

## Daily workflow

### IDE + AI chat

1. Install the extension → open a **folder** (not a single file).
2. Set **Current focus** in the Contorium sidebar.
3. Code as usual — Contorium updates `.contora/` automatically.
4. Starting a new AI chat? Confirm the **handoff prompt** (Y/n) or use **Transfer Context** from the sidebar.

### MCP + AI agent

1. Run the [one-line MCP setup](mcp.html#connect-your-ai-tool) for your host.
2. Open Codex / Claude / Cursor in your project — MCP starts automatically.
3. The agent reads project state via `inspect_*` tools and exports context via `transfer_*` when needed.

### Terminal

```bash
contorium init .
contorium inspect health .
contorium transfer context --copy
```

See the [CLI guide](cli.html) for the full command list.

---

## Three things to remember

1. **Open a folder** — Contorium needs a project root, not a lone file.
2. **Local-first** — everything lives in `.contora/` inside your repo. No cloud account.
3. **Transfer, don't re-prompt** — use Transfer Context / Handoff instead of pasting long explanations again.

---

## What Contorium is not

- Not an AI agent or code generator
- Not a project manager or task runner
- Not a cloud service

It **records and preserves** project intelligence. It does **not** make decisions for you.

---

## Next steps

- [Install all adapters](install.html)
- [Runtime dashboard](dashboard.html) — terminal status UI (starts automatically)
- [Interactive MCP setup](../mcp/)
"""

SKIP_SECTIONS: dict[str, list[str]] = {
    "INSTALL.md": [
        "Repository structure",
        "Architecture (three adapters)",
        "Build scripts (maintainers)",
        "Related docs",
    ],
    "MCP.md": [
        "PIL Runtime Contract (v3.0)",
        "Prerequisites",
        "Quick reference",
        "Install from source",
        "Configuration templates",
        "Host setup (step by step)",
        "Other MCP hosts",
        "MCP Inspector (debug)",
        "Extended tool reference (legacy + V3.1)",
        "Standard MCP v1 tools (legacy names)",
        "Project Intelligence (read-only vNext)",
        "Full tool catalog",
        "Build notes (maintainers)",
        "Related docs",
        "vs IDE one-click copy",
    ],
    "CLI.md": [
        "Relationship to IDE / MCP",
        "Related docs",
    ],
    "IDE_EXTENSION.md": [
        "Related docs",
    ],
    "DASHBOARD.md": [
        "Debug commands",
        "Worker internals (maintainers)",
        "Related docs",
    ],
}


def strip_sections(md: str, skip_titles: list[str]) -> str:
    if not skip_titles:
        return md
    skip_lower = {t.lower() for t in skip_titles}
    parts = re.split(r"(?m)^## ", md)
    if len(parts) <= 1:
        return md
    head = parts[0]
    kept = [head]
    for part in parts[1:]:
        title_line = part.split("\n", 1)[0].strip()
        title_clean = re.sub(r"\{#.*\}$", "", title_line).strip()
        if title_clean.lower() in skip_lower:
            continue
        kept.append("## " + part)
    return "".join(kept)


def clean_user_md(md: str, title: str) -> str:
    md = re.sub(r"^# .+\n+", f"# {title}\n\n{USER_NAV}\n\n", md, count=1)
    md = re.sub(r"(?m)^> Back to .+\n\n", "", md)
    md = re.sub(r"(?m)^> Related:.+\n\n", "", md)
    md = re.sub(r"(?m)^> \*\*Contorium\*\*.+\n\n", "", md)
    md = re.sub(r"(?m)^\*\*Public API unchanged:\*\*.+\n\n", "", md)
    md = re.sub(r"(?m)^\*\*Backward compatible:\*\*.+\n\n", "", md)
    md = re.sub(r"(?m)^\*\*V3\.1 additions:\*\*.+\n\n", "", md)
    md = re.sub(r"(?m)^\*\*V4 governance additions:\*\*.+\n\n", "", md)
    md = re.sub(r"(?m)^Maintainers:.*\n", "", md)
    md = re.sub(r"\[PROJECT_INTELLIGENCE_LAYER\.md\]\([^)]+\)", "[GitHub PIL spec](https://github.com/ContoriumLabs/contorium/blob/main/docs/PROJECT_INTELLIGENCE_LAYER.md)", md)
    md = re.sub(r"\[CONTORIUM_LANGUAGE_SPEC\.md\]\([^)]+\)", "[GitHub language spec](https://github.com/ContoriumLabs/contorium/blob/main/docs/CONTORIUM_LANGUAGE_SPEC.md)", md)
    md = re.sub(r"\[Language Spec\]\([^)]+\)", "[GitHub language spec](https://github.com/ContoriumLabs/contorium/blob/main/docs/CONTORIUM_LANGUAGE_SPEC.md)", md)
    md = re.sub(r"\[PIL Runtime Guide\]\([^)]+\)", "[Quick start](getting-started.html)", md)
    md = re.sub(r"\[Project Intelligence Layer[^\]]*\]\([^)]+\)", "[GitHub PIL spec](https://github.com/ContoriumLabs/contorium/blob/main/docs/PROJECT_INTELLIGENCE_LAYER.md)", md)
    md = re.sub(r"\[Documentation index\]\([^)]+\)", "[Docs](index.html)", md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip() + "\n"


def trim_install_matrix(md: str) -> str:
    """Keep command matrix but drop legacy footnotes under it."""
    marker = "## Command matrix"
    if marker not in md:
        return md
    before, rest = md.split(marker, 1)
    next_hr = rest.find("\n---\n")
    if next_hr == -1:
        return md
    section = rest[:next_hr]
    lines = section.split("\n")
    table_lines = []
    for line in lines:
        if line.startswith("| Legacy"):
            break
        if "legacy" in line.lower() and line.startswith("|"):
            continue
        table_lines.append(line)
    return before + marker + "\n".join(table_lines) + rest[next_hr:]


def prepare_mcp(md: str) -> str:
    md = strip_sections(md, SKIP_SECTIONS["MCP.md"])
    # Replace dev-focused intro block
    md = re.sub(
        r"^stdio MCP server.*?\n---\n",
        MCP_INTRO.strip() + "\n\n---\n",
        md,
        count=1,
        flags=re.DOTALL,
    )
    md = clean_user_md(md, "MCP server — User guide")
    md = md.replace("../mcp/README.md", "../mcp/")
    if "## Connect your AI tool" not in md:
        anchor = "## How MCP runs (important)"
        insert = MCP_BEFORE_START.strip() + "\n\n" + MCP_MAIN_TOOLS.strip() + "\n\n---\n\n" + MCP_HOST_SETUP.strip()
        if anchor in md:
            md = md.replace(anchor, insert + "\n\n---\n\n" + anchor)
        else:
            md = insert + "\n\n---\n\n" + md
    # User-friendly troubleshooting only
    md = re.sub(
        r"\| `npm run compile`[^\n]+\n",
        "| MCP fails to start | Node 18+; retry one-line setup; or use [manual config](#manual-config-fallback) |\n",
        md,
    )
    md = re.sub(
        r"\| Published npm 404[^\n]+\n",
        "",
        md,
    )
    md = re.sub(
        r"\| Agent shows Canceled[^\n]+\n",
        "| Agent shows Canceled | Usually host init cancel — retry opening the AI tool |\n",
        md,
    )
    md = re.sub(
        r"## Governance tools \(optional\)",
        "## Governance tools (optional)",
        md,
    )
    return md


def prepare_install(md: str) -> str:
    md = strip_sections(md, SKIP_SECTIONS["INSTALL.md"])
    md = trim_install_matrix(md)
    md = clean_user_md(md, "Install & use")
    md = md.replace("@contora/state-core", "shared local state")
    md = re.sub(
        r"Single npm package — `@contora/state-core`[^\n]+\n",
        "Optional: `npm install -g @contorium/mcp` for faster cold start.\n",
        md,
    )
    return md


def prepare_cli(md: str) -> str:
    md = strip_sections(md, SKIP_SECTIONS["CLI.md"])
    return clean_user_md(md, "CLI — User guide")


def prepare_ide(md: str) -> str:
    md = strip_sections(md, SKIP_SECTIONS["IDE_EXTENSION.md"])
    return clean_user_md(md, "IDE extension — User guide")


def prepare_dashboard(md: str) -> str:
    md = strip_sections(md, SKIP_SECTIONS["DASHBOARD.md"])
    return clean_user_md(md, "Runtime dashboard — User guide")


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(f"Missing {SOURCE} — run sync-docs-from-source.py first")

    TARGET.mkdir(parents=True, exist_ok=True)

    (TARGET / "GETTING_STARTED.md").write_text(
        GETTING_STARTED.format(nav=USER_NAV),
        encoding="utf-8",
    )
    print("prepared GETTING_STARTED.md")

    handlers = {
        "INSTALL.md": prepare_install,
        "MCP.md": prepare_mcp,
        "CLI.md": prepare_cli,
        "IDE_EXTENSION.md": prepare_ide,
        "DASHBOARD.md": prepare_dashboard,
    }

    for name, handler in handlers.items():
        src = SOURCE / name
        if not src.exists():
            print(f"skip missing {name}")
            continue
        out = handler(src.read_text(encoding="utf-8"))
        (TARGET / name).write_text(out, encoding="utf-8")
        print(f"prepared {name}")

    for orphan in [
        "PIL_RUNTIME.md",
        "PROJECT_INTELLIGENCE_LAYER.md",
        "COGNITIVE_DIMENSIONS.md",
        "CONTORIUM_LANGUAGE_SPEC.md",
    ]:
        path = TARGET / orphan
        if path.exists():
            path.unlink()
            print(f"removed user-site orphan {orphan}")


if __name__ == "__main__":
    main()
