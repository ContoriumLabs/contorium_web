# Contorium MCP Server (`@contorium/mcp`)

stdio MCP server for **Claude Code, Cursor Agent, OpenAI Codex, Gemini CLI**, and other MCP-compatible hosts.

**Normal use:** connect Contorium to your AI tool **once**, then open that tool in your project folder — the host **starts MCP automatically**. You never run MCP in a terminal yourself.

Overview: [INSTALL.md](./INSTALL.md) · [Dashboard](./DASHBOARD.md) · [CLI](./CLI.md) · [Home](../index.html)

---

## Setup (2 steps)

| Step | What you do |
|------|-------------|
| **1. Connect once** | Run **one command** for your AI tool (see below) |
| **2. Use daily** | Open Codex / Claude / Cursor **in your project folder** — MCP connects on its own |

That is the full setup. No separate `npm install`, no JSON file, no `CONTORIUM_WORKSPACE` — **unless** the one-liner fails (see [Manual config fallback](#manual-config-fallback)).

```text
One-time: codex mcp add … / claude mcp add … / Cursor MCP settings
        ↓
Daily: open AI tool in project folder
        ↓
Host spawns npx @contorium/mcp → bootstrap → Agent uses get_project_handoff
```

---

## Connect by platform (recommended)

Run from **your project folder** (`cd` into the repo you are working on).

### Codex

```bash
cd /path/to/your-project
codex mcp add contorium -- npx -y @contorium/mcp
```

Codex sets the project path automatically. Open Codex in that folder — done.

**Remove:** `codex mcp remove contorium`

---

### Claude Code

```bash
cd /path/to/your-project
claude mcp add --scope project contorium -- npx -y @contorium/mcp
```

Claude Code sets the project path automatically. Restart Claude Code in that folder — done.

**Remove:** `claude mcp remove contorium`

---

### Cursor Agent

1. Open your project in Cursor  
2. **Settings → MCP → Add server**  
3. Command: `npx` · Args: `-y`, `@contorium/mcp`  
4. Enable `contorium` → **Developer: Reload Window**

Cursor uses the open folder as workspace — no path env needed in most cases.

**Remove:** Settings → MCP → delete `contorium`

---

### Gemini CLI

Add to `~/.gemini/settings.json` or `<project>/.gemini/settings.json`:

```json
{
  "mcpServers": {
    "contorium": {
      "command": "npx",
      "args": ["-y", "@contorium/mcp"]
    }
  }
}
```

Restart Gemini CLI from your project folder.

**Remove:** delete `contorium` from `mcpServers`

---

### Other MCP hosts (Continue, Cline, …)

Any stdio MCP host: command `npx`, args `-y`, `@contorium/mcp`. Open the host from your project folder so it can detect the workspace.

Interactive walkthrough: [MCP setup page](../mcp/)

---

## Manual config fallback

Use this **only if** the one-liner above did not work — wrong project detected, custom workspace layout, or a host that requires a config file.

Create `.cursor/mcp.json`, `.mcp.json`, or your host's MCP settings file:

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

On Windows, prefer forward slashes in paths: `E:/projects/my-app`.

**How workspace is detected** (when you omit `CONTORIUM_WORKSPACE`):

1. Host-injected vars: `CODEX_PROJECT_DIR`, `CLAUDE_PROJECT_DIR`, `CLAUDE_PROJECT_ROOT`, `MCP_WORKSPACE_ROOT`
2. `CONTORIUM_WORKSPACE` in your MCP config
3. Walk up from cwd until `.contora/state.json` is found

---

## Optional extras

These are **not** required for setup:

| Command | When |
|---------|------|
| `npm install -g @contorium/mcp` | Faster cold start (skip npx download) |
| `contorium-mcp bootstrap --workspace .` | Pre-create `.contora/` before first Agent session |
| `contorium-mcp --workspace .` | Debug only — expect `ready on stdio`, then Ctrl+C |

---

## Daily use

1. Open your AI tool in the project folder  
2. MCP connects automatically — ask Agent to call `get_project_handoff`  
3. **New chat:** semi-auto inject prompt (`[?]` → Enter/i · n) — no extra command  
4. **Dashboard:** Passive line on bootstrap · **Space** → Expanded — see [Runtime dashboard](./DASHBOARD.md)

| Primary tool | Purpose |
|--------------|---------|
| `get_project_handoff` | CHP v1 — main AI memory entry |
| `get_understanding_graph` | Call chains + impact |
| `get_recent_changes` | Recent file/symbol updates |

---

## Standard MCP v1 tools

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

Legacy tools still supported: `get_project_change`, `get_project_graph`, `get_project_knowledge_graph`, `get_workspace_context`, `store_memory`, etc.

---

## Semi-auto context injection (automatic)

When runtime is active and you open a **new AI chat**:

1. MCP sets **pending** injection state  
2. Agent asks Y/n — or terminal shows `[?]` → **Enter/i** · **n**  
3. IDE status bar may show **`[?] Inject runtime?`**  
4. On confirm → `.contora/mcp.auto-context.md` (+ clipboard in IDE)

Each new chat re-prompts; skip/inject applies to the current chat only.

---

## MCP vs IDE clipboard

| Method | Use case |
|--------|----------|
| **`get_project_handoff`** (MCP) | Agent-native; semi-auto injection on new chats |
| **`get_understanding_graph`** (MCP) | Call-chain + impact view |
| **Copy AI-ready context** (IDE) | Full canonical Markdown to clipboard |
| **`contorium handoff --copy`** (CLI) | Copy To AI for next chat |
| **`contorium export`** (CLI) | Legacy full export |

---

## Environment variables

| Variable | Purpose |
|----------|---------|
| `CONTORIUM_WORKSPACE` | Explicit project root (fallback config only) |
| `CODEX_PROJECT_DIR` | Injected by Codex |
| `CLAUDE_PROJECT_DIR` / `CLAUDE_PROJECT_ROOT` | Injected by Claude Code |
| `MCP_WORKSPACE_ROOT` | Some hosts |

---

## Uninstall

| Host | Action |
|------|--------|
| Codex | `codex mcp remove contorium` |
| Claude Code | `claude mcp remove contorium` |
| Cursor | Settings → MCP → remove `contorium` |
| Gemini CLI | Remove from `mcpServers` in settings.json |
| npm (optional) | `npm uninstall -g @contorium/mcp` |

Clear MCP-only memory (optional): `Remove-Item -Recurse -Force .contora\mcp`

Does not remove `state.json`, `handoff.json`, or other shared artifacts.

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| MCP fails to start | Node 18+; retry the platform one-liner; check MCP panel shows connected |
| Wrong project | Use [manual config fallback](#manual-config-fallback) with `CONTORIUM_WORKSPACE` |
| `found: false` / no handoff | Run `contorium init .` in project (requires [CLI](./CLI.md)) |
| Stale state | Save files; wait for sync; or `contorium sync .` |
| Agent shows Canceled | Reload Agent / MCP — often init cancel, not MCP crash |
| Dashboard not visible | **Space** in Contorium terminal · see [Runtime dashboard](./DASHBOARD.md) |

---

## Related docs

- [Install overview](./INSTALL.md)
- [Runtime Dashboard (CRBP)](./DASHBOARD.md)
- [CLI](./CLI.md)
- [IDE Extension](./IDE_EXTENSION.md)
- [Interactive MCP setup](../mcp/)
