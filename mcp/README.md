# Contorium MCP

stdio MCP server — a **session view** over shared `.contora/` workspace state.

Works with **Codex**, **Claude Code**, **Cursor Agent**, and **Gemini CLI**. Can bootstrap state without the IDE extension.

Full reference: [docs/MCP.md](../docs/MCP.md) · Install hub: [docs/INSTALL.md](../docs/INSTALL.md)

---

## Quick start

```bash
git clone https://github.com/ContoriumLabs/contorium.git
cd contorium
npm install
npm run compile

# Codex
codex mcp add contorium -- node ./bin/contorium-mcp-launch.cjs

# Claude Code
claude --plugin-dir .

# Verify
node bin/contorium-mcp-launch.cjs
# expect: ready on stdio
```

Set `CONTORIUM_WORKSPACE` to your project root absolute path.

---

## Tools (10)

| Tool | Description |
|------|-------------|
| `get_workspace_context` | Read `state.json` (focus, Git, files) |
| `get_project_snapshot` | L4 Markdown snapshot |
| `get_project_state` | L4 structured state |
| `store_memory` | Write to `.contora/mcp/memories.json` |
| `search_memory` | Keyword search MCP memories |
| `get_memory` | Fetch by key |
| `get_project_intelligence` | L5 intelligence summary |
| `get_intent_graph` | Full intent graph |
| `get_active_intents` | Active intent nodes |
| `get_state_conflicts` | v2 conflict audit |

---

## Session views

| View | Role |
|------|------|
| **IDE extension** | Event-driven precision, sidebar, copy export |
| **MCP** | Agent-callable tools, bootstrap + 5s sync |
| **CLI** | `contorium init` / `sync` / `snapshot` |

All read/write the same `.contora/` — not separate memory stores.

Interactive setup: [mcp/index.html](./index.html)
