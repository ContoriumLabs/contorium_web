# Contorium — Install, Use, and Uninstall (Three Adapters)

> Back to [Home](../index.html) · Per adapter: [IDE](./IDE_EXTENSION.md) · [MCP](./MCP.md) · [CLI](./CLI.md)

Contorium v2.2+: **IDE, MCP, and CLI are peer Runtime Adapters** sharing the project-local `.contora/` directory.  
Any adapter can bootstrap and maintain state independently; combined use merges via `source.mode: merged`.

| Adapter | Typical user | Standalone capability |
|---------|--------------|----------------------|
| **IDE** | VS Code / Cursor users | Events, sidebar, one-click copy, BYOK |
| **MCP** | Claude Code / Cursor Agent / Codex / Gemini | Auto-spawn `@contorium/mcp`, CHP v1 tools, **semi-auto** handoff injection |
| **CLI** | Terminal / CI / headless | `handoff`, dashboard, `sync`, `export` |

---

## Prerequisites (all adapters)

| Requirement | Notes |
|-------------|-------|
| Node.js | **18+** (MCP and CLI) |
| Workspace | Real project **folder** path (not a single file) |

Artifact layout:

```text
.contora/                    # shared by all adapters
├── state.json               # + source { mode, lastWriter, lastUpdated }
├── handoff.json             # CHP v1 AI handoff (single source for task/changes)
├── understanding_graph.json # call chains + impact (Runtime Understanding Graph)
├── change.json / graph.json / timeline.json
├── runtime.bootstrap.json   # runtime_id (session-level, not in handoff)
├── mcp.auto-context.md        # written after user confirms semi-auto injection
├── mcp.handoff-injection.json # injection state per runtime_id
├── state-builder/           # L4 snapshot (scan or IDE cognition pipeline)
├── graph/                   # V3.1 cognitive graph (knowledge.json, snapshot.json, …)
├── events/                  # IDE events (CLI/MCP read; IDE writes)
├── dashboard.*.json         # dashboard view/signals (not business state source)
└── mcp/                     # MCP store_memory (optional)
```

---

## Install

### IDE extension

| Method | Steps |
|--------|-------|
| VSIX (recommended for Cursor) | [GitHub Releases](https://github.com/ContoriumLabs/contorium/releases) → Extensions → **Install from VSIX…** → **Developer: Reload Window** |
| Marketplace | Search **Contorium** (publisher `franklee-dev`) → Install → Reload |

See [IDE_EXTENSION.md](./IDE_EXTENSION.md).

### MCP server (`@contorium/mcp`)

```bash
npm install -g @contorium/mcp
contorium-mcp bootstrap --workspace /path/to/your-project
```

**Normal use:** configure once, then open Codex / Claude / Cursor — the host **spawns MCP automatically**. You do not run MCP in a terminal first.

**MCP config** (replace paths with your project root):

```json
{
  "mcpServers": {
    "contorium": {
      "command": "npx",
      "args": ["-y", "@contorium/mcp"],
      "env": {
        "CONTORIUM_WORKSPACE": "E:/path/to/your-project"
      }
    }
  }
}
```

| Host | Setup |
|------|-------|
| Cursor | `.cursor/mcp.json` or Settings → MCP → enable `contorium` |
| Claude Code | `claude mcp add --scope project contorium -- npx -y @contorium/mcp` |
| Codex | `codex mcp add contorium -- npx -y @contorium/mcp` |
| Gemini CLI | `~/.gemini/settings.json` → `mcpServers.contorium` (same JSON block) |

See [MCP.md](./MCP.md) for step-by-step host guides.

### CLI

```bash
npm install -g @contorium/cli
contorium init .
contorium --help
```

See [CLI.md](./CLI.md).

---

## Usage scenarios

### IDE only

1. Install extension → open a **folder** workspace  
2. Set **Current focus** in the sidebar, code normally  
3. **Copy AI-ready context** into any AI chat  

No MCP or CLI required.

### MCP only

1. `npm install -g @contorium/mcp`  
2. `contorium-mcp bootstrap --workspace /path/to/project` (optional)  
3. Configure MCP with `CONTORIUM_WORKSPACE` (see [MCP.md](./MCP.md))  
4. **Open Codex / Claude / Cursor** — host starts MCP and bootstraps `.contora/`  
5. **New chat:** injection prompt appears automatically — Agent asks Y/n, or use terminal **Enter/i** / IDE **[?]**
6. Or call `get_project_handoff` / `get_understanding_graph` / `get_recent_changes` anytime  

No manual MCP terminal. No IDE required; scan/merged mode is less precise without IDE events.

See also [Runtime Dashboard](./DASHBOARD.md) (Passive line + optional Expanded view).

### CLI only

```bash
cd /path/to/your-project
contorium init .
contorium sync .
contorium snapshot .
contorium handoff .
contorium handoff --copy-to-ai
contorium graph-snapshot .
contorium knowledge .
contorium export .
contorium status .
contorium state .
```

No IDE or MCP; suitable for CI and scripts.

### Combined (recommended)

| Combo | Effect |
|-------|--------|
| IDE + MCP | IDE writes events + cognitive graph; MCP reads handoff / graph-snapshot |
| IDE + CLI | IDE daily; CLI `export` or `graph-snapshot` in CI |
| All three | `source.lastWriter` tracks last writer; task/notes are not overwritten |

---

## Command matrix (V3.1)

| Capability | IDE | MCP | CLI |
|------------|-----|-----|-----|
| Bootstrap `.contora/` | Open folder | Bootstrap on start | `contorium init` |
| Refresh git/paths | Auto scan | 5s + events/git watch | `contorium sync` |
| Read state | Sidebar | `get_workspace_context` | `contorium state` |
| L4 snapshot | Sidebar / copy | `get_project_snapshot` | `contorium snapshot` |
| **AI execution entry (CHP v1)** | Copy includes handoff | `get_project_handoff` | `contorium handoff` · `--copy-to-ai` |
| **Semi-auto new chat inject** | Auto dialog + `[?]` status bar | Agent auto-asks on new chat | Auto `[?]` Passive · debug: `--prompt-new-chat` |
| **Runtime dashboard** | Status bar Passive · auto attach | bootstrap on MCP init | **Space** toggles Expanded · debug: `handoff --show` |
| **Cognitive summary** | `# COGNITIVE SNAPSHOT` in copy | `get_project_graph_snapshot` | `contorium graph-snapshot` |
| **Knowledge graph** | AI Cortex sidebar | `get_project_knowledge_graph` | `contorium knowledge` |
| Change / graph / timeline | Cortex | `get_project_change/graph/timeline` | `contorium change/graph/timeline` |
| Status summary | Sidebar | tool JSON | `contorium status` |
| Write task/notes | Sidebar | — | — |
| Agent memory | — | `store_memory` | — |
| Canonical Markdown export | Copy AI-ready context | — | `contorium export` |

---

## Uninstall

### IDE

Extensions → Contorium → **Uninstall** → Reload Window

Manual (if corrupted):

```powershell
Remove-Item -Recurse -Force "$env:USERPROFILE\.cursor\extensions\franklee-dev.contorium-*" -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force "$env:USERPROFILE\.vscode\extensions\franklee-dev.contorium-*" -ErrorAction SilentlyContinue
```

### MCP

| Host | Command |
|------|---------|
| Cursor | Settings → MCP → remove `contorium` |
| Claude Code | `claude mcp remove contorium` |
| Codex | `codex mcp remove contorium` |
| Gemini | Remove `mcpServers.contorium` from settings.json |

Optional: `npm uninstall -g @contorium/mcp`

### CLI

```bash
npm uninstall -g @contorium/cli
```

No background service. `.contora/` is **not** deleted automatically.

### Clear workspace data (optional, all adapters)

**PowerShell (project root):**

```powershell
Remove-Item -Recurse -Force .contora -ErrorAction SilentlyContinue
```

**macOS / Linux:**

```bash
rm -rf .contora
```

---

## `contorium init` output

When `.contora/state.json` already exists with events:

```json
{
  "workspaceRoot": "E:\\your-project",
  "created": false,
  "updated": true,
  "mode": "merged",
  "source": { "mode": "merged", "lastWriter": "cli" }
}
```

| Field | Meaning |
|-------|---------|
| `created: false` | **Normal** — merged existing state, not first create |
| `mode: merged` | Events + state present; scan supplements git/paths only |
| `updated: true` | State or snapshot written this run |

First-time init: `created: true`, `mode: scan-driven`.

---

## Related docs

- [Home](../index.html)
- [IDE Extension](./IDE_EXTENSION.md)
- [MCP Server](./MCP.md)
- [CLI](./CLI.md)
- [Runtime Dashboard (CRBP)](./DASHBOARD.md)
