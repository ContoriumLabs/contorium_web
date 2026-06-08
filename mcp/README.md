# Contorium MCP

stdio MCP server — **`@contorium/mcp`**. A peer Runtime Adapter over shared `.contora/` workspace state.

**Normal use:** configure once → Codex / Claude / Cursor **spawns MCP automatically**. Do not run MCP in a terminal first.

Full reference: [docs/mcp.html](../docs/mcp.html) · Dashboard: [docs/dashboard.html](../docs/dashboard.html) · Install: [docs/install.html](../docs/install.html)

---

## Quick start

```bash
npm install -g @contorium/mcp
contorium-mcp bootstrap --workspace /path/to/your-project
```

**`.cursor/mcp.json`** (project root — use absolute paths):

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

Enable in **Cursor → Settings → MCP** → Reload Window.

### Host-specific one-liners

```bash
# Codex
codex mcp add contorium -- npx -y @contorium/mcp

# Claude Code
claude mcp add --scope project contorium -- npx -y @contorium/mcp
```

Verify (debug only):

```bash
contorium-mcp --workspace /path/to/your-project
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

---

## CLI equivalent

```bash
contorium handoff
contorium handoff --copy-to-ai
# Dashboard: Space in Contorium terminal · c copy
```

Interactive setup: [mcp/index.html](./index.html)
