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
stdio MCP server — **CIL for AI agents** on top of a local **Project Intelligence Layer (PIL)**.

Connect once to Claude Code, Cursor Agent, Codex, Gemini CLI, or VS Code MCP. Agents can **`ask_project`**, inspect state, capture decisions, and transfer context — without you re-explaining architecture every session.

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

### Ask (CIL — recommended first)

Natural-language queries route through the **Cognitive Kernel**. CIL suggests and explains — it never executes tasks.

| Tool | Purpose |
|------|---------|
| `ask_project` | Ask anything — history, decisions, impact, next steps |
| `get_suggested_questions` | Onboarding prompts when `.contora/` is new |
| `get_project_history` | Event feed for a time range |
| `get_decisions` | Decision Center (ADR-style records) |
| `get_next_actions` | Suggested next focus (suggestions only) |
| `get_cognitive_health` | Missing WHY, stale decisions, conflicts |
| `get_entity_knowledge` | Knowledge Graph for a module or topic |
| `get_snapshot` | Time travel — state nearest a date |
| `transfer_project` | Unified export — `context` · `intelligence` · `story` · `essence` · `handoff` |
| `get_knowledge_health` | Decision trust scores and lifecycle dashboard |
| `get_review_queue` | What needs review — invalidation triggers |
| `set_decision_lifecycle_meta` | Record owner, verification, expiry |

CLI mirror: `contorium ask "…"` · `contorium lifecycle` · `contorium review` · `contorium health`

### PIL (Inspect · Transfer · Capture)

| Group | What it does | Examples |
|-------|--------------|----------|
| **Inspect** | Read structured project facts | `inspect_state`, `inspect_health`, `inspect_decision` |
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

**Give AI a memory of your project.**

Contorium preserves decisions, architecture context, and evolution history — so AI can understand your codebase without starting from zero every session.

Install **IDE**, **MCP**, or **CLI**; all share `.contora/` in your project folder.

---

## Ask your project (CIL)

| Question | Where it routes |
|----------|-----------------|
| What happened this week? | Project History |
| Why was MCP added? | Decision Center |
| What should I do next? | Action Engine (suggestions only) |
| What needs review? | [Knowledge Lifecycle](lifecycle.html) · Review Queue |
| Is this decision still valid? | Lifecycle · Knowledge Health |

| Surface | How to ask |
|---------|------------|
| **CLI** | `contorium ask "Why was MCP added?"` · `contorium lifecycle` |
| **MCP** | `ask_project` · `get_knowledge_health` · `get_review_queue` |
| **IDE** | **Ask Contorium…** · Explore → Review Queue |

CIL suggests and explains. It **never executes tasks** for you.

---

## Choose your entry point

| If you… | Start with |
|---------|------------|
| Code in VS Code / Cursor | [IDE extension](ide-extension.html) |
| Use Claude Code, Codex, or Cursor Agent | [MCP server](mcp.html) |
| Work in the terminal or CI | [CLI](cli.html) |

---

## Daily workflow

### IDE + AI chat

1. Install the extension → open a **folder** (not a single file).
2. Set **Current focus** in the sidebar.
3. Use **Ask Contorium…** or Explore (**Review Queue · Knowledge Health**).
4. New AI chat? Confirm the **handoff prompt** (Y/n) or **Transfer Context**.

### MCP + AI agent

1. [One-line MCP setup](mcp.html#connect-your-ai-tool) for your host.
2. Open Codex / Claude / Cursor in your project.
3. Agent uses `ask_project`, `get_knowledge_health`, or `transfer_project` as needed.

### Terminal

```bash
contorium init .
contorium ask "What is this project about?"
contorium lifecycle
contorium review
contorium transfer context --copy
```

See [CLI guide](cli.html) · [Lifecycle guide](lifecycle.html).

---

## Three things to remember

1. **Open a folder** — not a single file.
2. **Git remembers changes. Contorium remembers why.**
3. **Local-first** — everything in `.contora/` inside your repo.

---

## Next steps

- [Install all adapters](install.html)
- [Knowledge Lifecycle](lifecycle.html)
- [MCP setup wizard](../mcp/)
- [Runtime dashboard](dashboard.html)
"""

CLI_CIL_SECTION = """
## Ask your project (CIL)

```bash
contorium ask "Why was MCP added?"
contorium ask "What happened this week?"
contorium health .
contorium lifecycle          # knowledge health dashboard
contorium review             # review queue only
contorium transfer --mode=story --copy
```

| Capability | CLI | MCP equivalent |
|------------|-----|----------------|
| Ask | `contorium ask "…"` | `ask_project` |
| History | `contorium history` | `get_project_history` |
| Decisions | `contorium decisions` | `get_decisions` |
| Lifecycle | `contorium lifecycle` · `review` | `get_knowledge_health` · `get_review_queue` |
| Health | `contorium health` | `get_cognitive_health` |
| Transfer | `contorium transfer --mode=…` | `transfer_project` |

See [Knowledge Lifecycle](lifecycle.html).

---

"""

SKIP_SECTIONS: dict[str, list[str]] = {
    "INSTALL.md": [
        "Repository structure",
        "Architecture (three adapters)",
        "Build scripts (maintainers)",
        "Related docs",
        "What Contorium does",
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
    "LIFECYCLE.md": [
        "Related",
        "Pipeline",
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
    md = re.sub(r"\[Project Overview\]\(\./OVERVIEW\.md\)", "[Quick start](getting-started.html)", md)
    md = re.sub(r"\[Overview\]\(\./OVERVIEW\.md\)", "[Quick start](getting-started.html)", md)
    md = re.sub(r"\[AI Layer\]\(\./AI_LAYER\.md\)", "[AI Layer (GitHub)](https://github.com/ContoriumLabs/contorium/blob/main/docs/AI_LAYER.md)", md)
    md = re.sub(r"\[AI_LAYER\.md\]\(\./AI_LAYER\.md\)", "[AI Layer (GitHub)](https://github.com/ContoriumLabs/contorium/blob/main/docs/AI_LAYER.md)", md)
    md = re.sub(r"\[CIL_V3\.md\]\(\./CIL_V3\.md\)", "[CIL v3 spec (GitHub)](https://github.com/ContoriumLabs/contorium/blob/main/docs/CIL_V3.md)", md)
    md = re.sub(r"\[SURFACES\.md\]\(\./SURFACES\.md\)", "[Surfaces (GitHub)](https://github.com/ContoriumLabs/contorium/blob/main/docs/SURFACES.md)", md)
    md = re.sub(r"\[DASHBOARD\.md\]\(\./DASHBOARD\.md\)", "[Runtime dashboard](dashboard.html)", md)
    md = re.sub(r"\[CLI\.md\]\(\./CLI\.md\)", "[CLI](cli.html)", md)
    md = re.sub(r"\[INSTALL\.md\]\(\./INSTALL\.md\)", "[Install](install.html)", md)
    md = re.sub(r"\[MCP\.md\]\(\./MCP\.md\)", "[MCP](mcp.html)", md)
    md = re.sub(r"\[IDE_EXTENSION\.md\]\(\./IDE_EXTENSION\.md\)", "[IDE extension](ide-extension.html)", md)
    md = re.sub(r"\[LIFECYCLE\.md\]\(\./LIFECYCLE\.md\)", "[Knowledge Lifecycle](lifecycle.html)", md)
    md = re.sub(r"\[CIL\.md\]\(\./CIL\.md\)", "[Quick start — CIL](getting-started.html)", md)
    md = re.sub(
        r"\[MCP_TOOL_CALLABILITY\.md\]\(\./MCP_TOOL_CALLABILITY\.md\)",
        "[MCP tool callability (GitHub)](https://github.com/ContoriumLabs/contorium/blob/main/docs/MCP_TOOL_CALLABILITY.md)",
        md,
    )
    md = re.sub(
        r"\[MCP tools\]\(\./MCP\.md\)",
        "[MCP server](mcp.html)",
        md,
    )
    # Internal doc cross-links → HTML slugs
    internal = {
        "INSTALL.md": "install.html",
        "MCP.md": "mcp.html",
        "CLI.md": "cli.html",
        "DASHBOARD.md": "dashboard.html",
        "IDE_EXTENSION.md": "ide-extension.html",
        "LIFECYCLE.md": "lifecycle.html",
        "OVERVIEW.md": "getting-started.html",
        "CIL.md": "getting-started.html",
    }
    for src, dst in internal.items():
        md = re.sub(rf"\]\(\./{re.escape(src)}\)", f"]({dst})", md)
        md = re.sub(rf"\]\(\./{re.escape(src)}#([^)]+)\)", rf"]({dst}#\1)", md)
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
    md = clean_user_md(md, "MCP server — User guide")
    md = md.replace("../mcp/README.md", "../mcp/")
    if "CIL for AI agents" not in md:
        md = re.sub(
            r"stdio MCP server[^\n]+\n\n(?:- \[[^\n]+\n\n)?",
            MCP_INTRO.strip() + "\n\n",
            md,
            count=1,
        )
    md = re.sub(
        r"- \[Quick start\]\([^\)]+\) · \[Quick start\]\([^\)]+\)",
        "- [Quick start](getting-started.html)",
        md,
    )
    md = md.replace("[Dashboard](./DASHBOARD.md)", "[Runtime dashboard](dashboard.html)")
    md = md.replace("[CLI](./CLI.md)", "[CLI](cli.html)")
    md = md.replace("[Install](./INSTALL.md)", "[Install](install.html)")
    if "## Connect your AI tool" not in md:
        anchor = "## How MCP runs (important)"
        insert = (
            MCP_BEFORE_START.strip()
            + "\n\n"
            + MCP_MAIN_TOOLS.strip()
            + "\n\n---\n\n"
            + MCP_HOST_SETUP.strip()
        )
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
    intro = """Contorium is a local **Cognitive Interaction Layer (CIL)** on a **Project Intelligence Layer (PIL)**. Install **IDE**, **MCP**, or **CLI** — all share `.contora/` in your project folder.

**Responsibility chain:** Capture → Structure → Preserve → Ask → Transfer

| Adapter | Typical user | Primary loop |
|---------|--------------|--------------|
| **IDE** | VS Code / Cursor | Ask · Capture · Transfer |
| **MCP** | Claude / Codex / Cursor Agent | Ask · Inspect · Transfer |
| **CLI** | Terminal / CI | Ask · Inspect · Transfer |

"""
    if "Cognitive Interaction Layer (CIL)" not in md:
        md = re.sub(
            r"Contorium is an \*\*AI Project Intelligence Layer.*?(?=\n## Prerequisites)",
            intro,
            md,
            count=1,
            flags=re.DOTALL,
        )
    md = re.sub(
        r"Single npm package — `shared local state`[^\n]+\n",
        "Optional: `npm install -g @contorium/mcp` for faster cold start.\n",
        md,
    )
    return md


def prepare_cli(md: str) -> str:
    md = strip_sections(md, SKIP_SECTIONS["CLI.md"])
    md = clean_user_md(md, "CLI — User guide")
    anchor = "## PIL commands (v3.0 — primary)"
    if anchor in md and "## Ask your project (CIL)" not in md:
        md = md.replace(anchor, CLI_CIL_SECTION.strip() + "\n\n" + anchor)
    return md


def prepare_ide(md: str) -> str:
    md = strip_sections(md, SKIP_SECTIONS["IDE_EXTENSION.md"])
    return clean_user_md(md, "IDE extension — User guide")


def prepare_lifecycle(md: str) -> str:
    md = strip_sections(md, SKIP_SECTIONS["LIFECYCLE.md"])
    md = clean_user_md(md, "Knowledge Lifecycle — User guide")
    intro = """Contorium tracks whether project knowledge is still trustworthy — **how stale** decisions are and **why** they may need review.

**Git remembers changes. Contorium remembers why — and whether that reasoning still holds.**

"""
    if "Git remembers changes" not in md:
        md = re.sub(
            r"Contorium v3\+ tracks[^\n]+\n\n\*\*Schema:\*\*[^\n]+\n\n",
            intro,
            md,
            count=1,
        )
    md = re.sub(
        r"Lifecycle is rebuilt on \*\*Sync\*\* via `persistKnowledgeLifecycle\(\)`[^\n]+\n",
        "Lifecycle updates when you sync the workspace — it is a projection of decisions and events, not a separate source of truth.\n",
        md,
    )
    md = re.sub(r"Implementation:.*", "", md)
    return md


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
        "LIFECYCLE.md": prepare_lifecycle,
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
        "OVERVIEW.md",
        "CIL.md",
        "SURFACES.md",
        "AI_LAYER.md",
        "README.md",
        "MCP_TOOL_CALLABILITY.md",
    ]:
        path = TARGET / orphan
        if path.exists():
            path.unlink()
            print(f"removed user-site orphan {orphan}")


if __name__ == "__main__":
    main()
