# Contorium CLI

The CLI is a **peer Runtime Adapter** with IDE and MCP, sharing `.contora/`.  
Overview: [INSTALL.md](./INSTALL.md) · [Home](../index.html)

---

## Command cheat sheet

| Phase | Command |
|-------|---------|
| **Install** | `npm install -g @contorium/cli` |
| **Verify** | `contorium status .` or `contorium --help` |
| **Init** | `contorium init [path]` |
| **Refresh** | `contorium sync [path]` |
| **L4 snapshot** | `contorium snapshot [path]` |
| **Handoff (CHP v1)** | `contorium handoff` · `--copy-to-ai` (manual copy) |
| **Dashboard** | **No command** — auto Passive; **Space** → Expanded |
| **Semi-auto inject** | **No command** — auto on new AI chat |
| **Cognitive summary** | `contorium graph-snapshot [path]` |
| **Knowledge graph** | `contorium knowledge [path]` |
| **Change / graph / timeline** | `contorium change\|graph\|timeline [path]` |
| **AI-ready export** | `contorium export [path]` or `--format json` |
| **Status** | `contorium status [path]` |
| **state.json** | `contorium state [path]` |
| **Uninstall** | `npm uninstall -g @contorium/cli` |
| **Clear data (optional)** | `Remove-Item -Recurse -Force .contora` (PowerShell) |

Default `[path]` is the current directory.

---

## Install

```bash
npm install -g @contorium/cli
contorium --help
contorium init .
contorium status .
```

---

## Commands

### Basics

| Command | Purpose | MCP equivalent |
|---------|---------|----------------|
| `contorium init [path]` | Create/merge `state.json`, L4 snapshot | bootstrap |
| `contorium sync [path]` | Rescan git + recent files | light sync |
| `contorium snapshot [path]` | Print PROJECT SNAPSHOT markdown | `get_project_snapshot` |
| `contorium status [path]` | JSON summary (mode, source, git counts) | — |
| `contorium state [path]` | Full `state.json` | `get_workspace_context` |

### Runtime dashboard (CRBP — automatic, zero commands)

When Codex / Claude / Gemini **starts Contorium MCP**, the server runs bootstrap and attaches a Passive dashboard worker. **You never run attach or handoff --show in normal use.**

| What | How (no command) |
|------|------------------|
| **Passive line** | Appears automatically in Contorium terminal / IDE status bar |
| **Expanded view** | Press **Space** in the Contorium dashboard terminal |
| **Semi-auto inject** | New AI chat → `[?]` on Passive line → **Enter/i** or **n** |
| **Copy To AI** | Press **c** in dashboard terminal |

See [Runtime dashboard](./DASHBOARD.md).

### Advanced commands (optional)

These are rarely needed in daily use:

| Command | Purpose |
|---------|---------|
| `contorium handoff --show` | Force expand (normally use **Space**) |
| `contorium handoff --hide` | Minimize to Passive |
| `contorium handoff --prompt-new-chat` | Force inject prompt in TTY |
| `contorium handoff --copy` / `--copy-to-ai` | Manual clipboard copy |
| `contorium attach . --auto` | Start dashboard worker manually |

### V3.1 understanding layer

| Command | Purpose | MCP equivalent |
|---------|---------|----------------|
| `contorium handoff [path] [--format compact\|markdown\|json]` | **CHP v1 get_handoff** (default: compact one-liner) | `get_project_handoff` |
| `contorium graph-snapshot [path]` | Cognitive summary | `get_project_graph_snapshot` |
| `contorium knowledge [path] [--min-confidence N]` | Knowledge graph (default filter 0.7) | `get_project_knowledge_graph` |
| `contorium change [path]` | `change.json` | `get_project_change` |
| `contorium graph [path]` | Change neighborhood `graph.json` | `get_project_graph` |
| `contorium timeline [path]` | `timeline.json` | `get_project_timeline` |
| `contorium export [path] [--format json\|markdown]` | Legacy full export (manual copy fallback) | combined tools |

**PowerShell:**

```powershell
cd E:\your-project
contorium init .
contorium sync .
contorium handoff
contorium handoff --copy
contorium handoff --format markdown
contorium graph-snapshot .
contorium knowledge . --min-confidence 0.7
contorium export . | Out-File -Encoding utf8 ai-context.md
contorium export . --format json | Out-File -Encoding utf8 ai-context.json
```

**bash:**

```bash
cd /path/to/project
contorium init .
contorium sync .
contorium handoff
contorium handoff --copy
contorium handoff --format markdown
contorium graph-snapshot .
contorium knowledge . --min-confidence 0.7
contorium export . > ai-context.md
contorium export . --format json > ai-context.json
```

Writes set `state.json` → `source.lastWriter: "cli"`.

### CHP v1 — unified handoff (recommended)

Runtime maintains a single AI handoff state (`.contora/handoff.json` + `state.json`). All clients read via **get_handoff**:

| Client | How (normal — no command) |
|--------|---------------------------|
| **CLI Passive** | Auto line: `task \| last \| agent` + optional `⤷` mini-graph |
| **IDE status bar** | Same compact line; auto dialog when new chat + runtime active |
| **New AI chat** | Auto `[?]` prompt → Enter/i · n · or Agent asks Y/n |
| **Expanded dashboard** | **Space** in terminal (not `--show`) |
| **Manual copy** | **c** in terminal · `--copy-to-ai` · IDE Copy AI-ready context |

### Semi-auto inject (automatic)

When runtime is active and you open a **new AI chat**, Contorium shows `[?]` automatically.

**Manual fallback:**

```powershell
contorium handoff --copy-to-ai
contorium export . | Out-File -Encoding utf8 ai-context.md
```

### `contorium export` sections (markdown)

Uses the same `formatCanonicalAiMarkdown` as IDE **Copy AI-ready context**:

```text
# TASK ANCHOR
# PROJECT SNAPSHOT
# WORKING CONTEXT
# COGNITIVE SNAPSHOT
# CHANGE SET / IMPACT SET
# AI HANDOFF (V3.1)
# CODE EVOLUTION
# NOTES
# INSTRUCTION
```

JSON format includes `cognitiveSnapshot` when the knowledge graph exists.

---

## Relationship to IDE / MCP

- Does **not** require IDE extension or MCP process  
- With IDE: IDE writes events; CLI `sync` supplements git/paths only — **does not overwrite** `currentTask` / `notes`  
- With MCP: shares the same sync logic  

---

## Uninstall

```bash
npm uninstall -g @contorium/cli
```

Stop calling `contorium`; `.contora/` is **not** removed automatically.

Clear shared workspace data:

```powershell
Remove-Item -Recurse -Force .contora
```

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `command not found: contorium` | Reinstall: `npm install -g @contorium/cli` |
| `init` shows `created: false` | **Normal** — existing state; check `updated` and `source` |
| Generic snapshot | Without IDE events, scan-only inference; use extension for precision |
| `knowledge` / `graph-snapshot` missing | Needs code changes; run `sync` or save files in IDE |
| `state: no state.json` | Run `contorium init .` first |

---

## Related docs

- [Home](../index.html)
- [Install overview](./INSTALL.md)
- [IDE Extension](./IDE_EXTENSION.md)
- [MCP Server](./MCP.md)
- [Runtime Dashboard (CRBP)](./DASHBOARD.md)
