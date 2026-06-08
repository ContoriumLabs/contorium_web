# Contorium MCP

stdio MCP server — **`@contorium/mcp`**. A peer Runtime Adapter over shared `.contora/` workspace state.

**Setup:** one command for your AI tool → open the tool in your project folder. MCP starts automatically.

Full reference: [docs/mcp.html](../docs/mcp.html) · Dashboard: [docs/dashboard.html](../docs/dashboard.html)

---

## Connect (one command)

Run from **your project folder**:

```bash
# Codex
codex mcp add contorium -- npx -y @contorium/mcp

# Claude Code
claude mcp add --scope project contorium -- npx -y @contorium/mcp
```

**Cursor:** Settings → MCP → Add → command `npx`, args `-y`, `@contorium/mcp` → Reload Window.

Then open the AI tool in that project — done. No JSON file needed in normal use.

Manual config fallback: [docs/mcp.html](../docs/mcp.html#manual-config-fallback)

---

## Standard MCP v1 tools

| Tool | Purpose |
|------|---------|
| **`get_project_handoff`** | CHP v1 unified AI memory — **primary execution entry** |
| **`get_handoff_injection_status`** | Semi-auto new-chat prompt state |
| **`confirm_handoff_injection`** / **`skip_handoff_injection`** | User Y/n for context inject |
| **`get_recent_changes`** | File & symbol updates |
| **`get_understanding_graph`** | Call chains + impact |

---

## Semi-auto injection (automatic)

New AI chat → Agent asks Y/n (or terminal `[?]` → **Enter/i** · **n**) → `.contora/mcp.auto-context.md` on confirm.

Interactive setup: [mcp/index.html](./index.html)
