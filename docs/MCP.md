# Contorium MCP Server (`@contorium/mcp`)

stdio MCP server for **Claude Code, Cursor Agent, OpenAI Codex, Gemini CLI**, and other MCP-compatible hosts.

**You do not start MCP manually in normal use.** After one-time configuration, the AI host (Codex, Claude, Cursor, etc.) **spawns** `@contorium/mcp` automatically when a session starts.

Overview: [INSTALL.md](./INSTALL.md) · [Dashboard](./DASHBOARD.md) · [CLI](./CLI.md) · [Home](../index.html)

---

## Quick reference

| Phase | Action |
|-------|--------|
| **Install** | `npm install -g @contorium/mcp` · `contorium-mcp bootstrap --workspace .` |
| **Configure** | Add `mcpServers.contorium` with `CONTORIUM_WORKSPACE` (see below) |
| **Daily use** | Open Codex / Claude / Cursor — host starts MCP automatically |
| **Primary AI tool** | `get_project_handoff` (CHP v1) |
| **New chat** | `get_handoff_injection_status` → `confirm_handoff_injection` |
| **Remove** | Host-specific: see [Uninstall](#uninstall--disable) |

---

## Prerequisites

| Requirement | Notes |
|-------------|-------|
| Node.js | **18+** |
| Workspace | Real project **folder** (not a single file) |

---

## How MCP runs (important)

```text
You open Codex / Claude Code / Cursor Agent
        ↓
Host reads .mcp.json / MCP settings
        ↓
Host spawns: npx @contorium/mcp
        ↓
MCP connects over stdio
        ↓
On initialize: bootstrap runtime + semi-auto handoff prompt (user confirm)
        ↓
AI calls tools (get_project_handoff, …) when needed
```

| Do | Don't |
|----|-------|
| Configure MCP once per host | Run MCP in a terminal before opening Codex (unless debugging) |
| Set `CONTORIUM_WORKSPACE` to your **project** root | Point workspace at the wrong folder |
| Restart Agent / reload MCP after config changes | Expect MCP to stay running after you close the AI client (host manages lifecycle) |

---

## Install

```bash
npm install -g @contorium/mcp
contorium-mcp bootstrap --workspace /path/to/your-project
```

Optional verify (debug — press Ctrl+C to exit):

```bash
contorium-mcp --workspace /path/to/your-project
# Expect:
# [contorium-mcp] workspace: …
# [contorium-mcp] ready on stdio
```

**Bootstrap only** (sync `.contora` without stdio server):

```bash
contorium-mcp bootstrap --workspace /path/to/your-project
```

---

## Workspace resolution

The server resolves the project root in this order:

1. CLI flag: `--workspace /path/to/project`
2. Environment: `CONTORIUM_WORKSPACE` (also `CODEX_PROJECT_DIR`, `CLAUDE_PROJECT_DIR`, `CLAUDE_PROJECT_ROOT`, `MCP_WORKSPACE_ROOT`)
3. `.mcp.json` or `.cursor/mcp.json` → `mcpServers.contorium.env.CONTORIUM_WORKSPACE`
4. Walk up from cwd to find `.contora/state.json`

---

## Configuration template

Replace paths with **your** absolute paths. On Windows, prefer forward slashes: `E:/projects/my-app`.

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

---

## Host setup (step by step)

### Cursor

1. Create **`.cursor/mcp.json`** in your **project** root (or use Cursor Settings → MCP):

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

2. **Settings → MCP** → enable `contorium`.
3. **Developer: Reload Window** or restart Agent.
4. Confirm MCP shows connected; ask Agent to call `get_project_handoff`.

**Uninstall:** Settings → MCP → remove `contorium`, or delete the config entry.

---

### Claude Code

**Option 1 — CLI register (project scope, recommended)**

```bash
cd /path/to/your-project
claude mcp add --scope project contorium -- npx -y @contorium/mcp
```

**Option 2 — Project `.mcp.json`**

Use the [configuration template](#configuration-template) in your project root.

**Uninstall:** `claude mcp remove contorium`

---

### OpenAI Codex

**Option 1 — CLI**

```bash
cd /path/to/your-project
codex mcp add contorium -- npx -y @contorium/mcp
```

Codex injects `CODEX_PROJECT_DIR`; often no extra env is needed when working inside the project directory.

**Option 2 — `config.toml` (some Codex versions)**

```toml
[mcp_servers.contorium]
command = "npx"
args = ["-y", "@contorium/mcp"]

[mcp_servers.contorium.env]
CONTORIUM_WORKSPACE = "E:/path/to/your-project"
```

Interactive setup: [MCP setup page](../mcp/#codex).

**Uninstall:** `codex mcp remove contorium`

---

### Gemini CLI

Edit global or project settings:

- Global: `~/.gemini/settings.json`
- Project: `<project>/.gemini/settings.json`

Use the [configuration template](#configuration-template).

Restart the Gemini CLI session after saving.

**Uninstall:** Remove `contorium` from `mcpServers`.

---

### Other MCP hosts (Continue, Cline, custom TUIs, …)

Any host that supports **stdio MCP** can use the [configuration template](#configuration-template). Paste the `mcpServers.contorium` block into that host's MCP configuration format.

---

## Standard MCP v1 tools (recommended)

| Tool | Purpose | Output |
|------|---------|--------|
| **`get_handoff_injection_status`** | Semi-auto new-chat prompt state | pending / prompt / compact |
| **`confirm_handoff_injection`** | User confirmed (Y) — write context file | `.contora/mcp.auto-context.md` |
| **`skip_handoff_injection`** | User declined (N) for this runtime | state only |
| **`get_project_handoff`** | CHP v1 unified AI memory | `compact` / `markdown` / `json` |
| **`get_recent_changes`** | File & symbol updates | `.contora/change.json` |
| **`get_understanding_graph`** | Call chains + impact | `.contora/understanding_graph.json` |
| **`get_runtime_state`** | Bootstrap / dashboard / session (read-only) | JSON |

### `get_project_handoff` parameters

| Param | Values | Default |
|-------|--------|---------|
| `format` | `compact`, `markdown`, `json` | compact + legacy `handoff` object when omitted |
| `filter` | symbol substring | none |
| `workspaceRoot` | override path | auto-detect |

### Legacy tools (still supported)

`get_project_change`, `get_project_graph`, `get_project_knowledge_graph`, `get_project_graph_snapshot`, `get_workspace_context`, `store_memory`, and others remain available for backward compatibility.

---

## Semi-Auto Context Injection (automatic — no CLI command)

When runtime is active and the host opens a **new AI chat** (new MCP stdio session):

1. MCP initialize calls `prepareHandoffInjection({ newChat: true })` → **pending** state.
2. Server **instructions** tell the Agent to call `get_handoff_injection_status` and ask the user Y/n.
3. User confirms via UI (no command):
   - **Terminal dashboard:** `[?]` on Passive line → **Enter/i** · **n**
   - **IDE:** auto notification + status bar **`[?] Inject runtime?`**
   - **Agent:** `confirm_handoff_injection` / `skip_handoff_injection`
4. On confirm → `.contora/mcp.auto-context.md` + clipboard (IDE).

Each new chat re-prompts; skip/inject applies to the current chat only (`chat_session_id`).

---

## Runtime bootstrap (automatic)

When MCP starts, it schedules bootstrap and dashboard workers automatically:

- Sync `.contora/` and start Passive dashboard
- MCP light sync — 5s poll + watch on `.contora/events` and `.git/HEAD`
- Dashboard wake on file/git changes

See [Runtime dashboard](./DASHBOARD.md). No manual setup in normal use.

---

## Environment variables

| Variable | Purpose |
|----------|---------|
| `CONTORIUM_WORKSPACE` | Explicit project root (**preferred**) |
| `CODEX_PROJECT_DIR` | Injected by Codex |
| `CLAUDE_PROJECT_DIR` / `CLAUDE_PROJECT_ROOT` | Injected by Claude Code |
| `MCP_WORKSPACE_ROOT` | Some hosts |

---

## vs IDE one-click copy

| Method | Use case |
|--------|----------|
| **`get_project_handoff`** (MCP) | Agent-native; use semi-auto injection for new chats |
| **`get_understanding_graph`** (MCP) | Call-chain + impact view |
| **Copy AI-ready context** (IDE) | Full canonical Markdown to clipboard |
| **`contorium handoff --copy`** (CLI) | Copy To AI for next chat |
| **`contorium export`** (CLI) | Legacy full export |

---

## Uninstall / disable

| Host | Action |
|------|--------|
| Cursor | Settings → MCP → remove `contorium` |
| Claude Code | `claude mcp remove contorium` |
| Codex | `codex mcp remove contorium` |
| Gemini CLI | Remove from `mcpServers` in settings.json |
| npm package | `npm uninstall -g @contorium/mcp` |

Clear MCP-only memory (optional, project root):

```powershell
Remove-Item -Recurse -Force .contora\mcp -ErrorAction SilentlyContinue
```

Does not remove `state.json`, `handoff.json`, or other shared artifacts.

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| MCP fails to start | Node 18+; reinstall `@contorium/mcp`; use absolute paths in config |
| `found: false` / no handoff | Set `CONTORIUM_WORKSPACE`; run `contorium init .` in project |
| Wrong project | `CONTORIUM_WORKSPACE` must be the **application** root |
| Stale state | Save files; wait for MCP sync; or `contorium sync .` |
| Agent shows Canceled | Often Agent init cancel, not MCP crash; retry after reload |
| Dashboard not visible | Press **Space** in Contorium terminal tab, or enable IDE status bar — see [Runtime dashboard](./DASHBOARD.md) |
| npm install fails | Check network and Node version; try `npm install -g @contorium/mcp` again |

---

## `contorium-mcp` subcommands

| Command | Purpose |
|---------|---------|
| `contorium-mcp` | Start stdio MCP server (default — host spawns this) |
| `contorium-mcp bootstrap [--workspace PATH]` | Pre-sync `.contora` + schedule dashboard **without** starting stdio |

---

## Related docs

- [Install overview](./INSTALL.md)
- [Runtime Dashboard (CRBP)](./DASHBOARD.md)
- [CLI](./CLI.md)
- [IDE Extension](./IDE_EXTENSION.md)
- [Interactive MCP setup](../mcp/)
