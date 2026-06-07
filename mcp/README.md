# Contorium MCP

stdio MCP server — **`@contorium/mcp`**. A peer Runtime Adapter over shared `.contora/` workspace state.

**Normal use:** configure once → Codex / Claude / Cursor **spawns MCP automatically**. Do not run MCP in a terminal first.

Full reference: [docs/mcp.html](../docs/mcp.html) · Dashboard: [docs/dashboard.html](../docs/dashboard.html) · Install: [docs/install.html](../docs/install.html)

---

## Quick start

### From source (development)

```bash
git clone https://github.com/ContoriumLabs/contorium.git
cd contorium
npm install
npm run compile
```

**`.cursor/mcp.json`** (project root — use absolute paths):

```json
{
  "mcpServers": {
    "contorium": {
      "command": "node",
      "args": ["E:/path/to/contorium/packages/mcp/bin/contorium-mcp.js"],
      "env": {
        "CONTORIUM_WORKSPACE": "E:/path/to/your-project"
      }
    }
  }
}
```

Enable in **Cursor → Settings → MCP** → Reload Window.

### npm (when published)

```bash
npm install -g @contorium/mcp
contorium-mcp bootstrap --workspace /path/to/your-project
```

Host config:

```json
{
  "mcpServers": {
    "contorium": {
      "command": "npx",
      "args": ["@contorium/mcp"],
      "env": {
        "CONTORIUM_WORKSPACE": "E:/path/to/your-project"
      }
    }
  }
}
```

### Host-specific one-liners

```bash
# Codex
codex mcp add contorium -- node E:/path/to/contorium/bin/contorium-mcp-launch.cjs

# Claude Code (plugin)
claude --plugin-dir /path/to/contorium

# Claude Code (MCP only)
claude mcp add --scope project contorium -- node E:/path/to/contorium/bin/contorium-mcp-launch.cjs
```

Verify (debug only):

```bash
npx contorium-mcp --workspace /path/to/your-project
# expect: ready on stdio
```

---

## Standard MCP v1 tools (recommended)

| Tool | Purpose |
|------|---------|
| **`get_project_handoff`** | CHP v1 unified AI memory — **primary execution entry** |
| **`get_handoff_injection_status`** | Semi-auto new-chat prompt state |
| **`confirm_handoff_injection`** / **`skip_handoff_injection`** | User Y/n for context inject |
| **`get_recent_changes`** | File & symbol updates (`.contora/change.json`) |
| **`get_understanding_graph`** | Call chains + impact |
| **`get_runtime_state`** | Bootstrap / dashboard / session (read-only) |

Legacy tools still supported: `get_project_snapshot`, `get_workspace_context`, `store_memory`, `get_project_knowledge_graph`, etc.

---

## Semi-auto injection (automatic)

1. New AI chat → MCP sets **pending** injection state  
2. Agent asks Y/n (or terminal shows `[?]` → **Enter/i** · **n**)  
3. On confirm → `.contora/mcp.auto-context.md` written  

Debug: `contorium handoff --prompt-new-chat`

---

## CLI equivalent

```bash
npx contorium handoff
npx contorium handoff --copy-to-ai
# Dashboard: Space in Contorium terminal · c copy
```

Interactive setup: [mcp/index.html](./index.html)
