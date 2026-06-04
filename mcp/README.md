# Contorium MCP

stdio MCP server — a **peer Runtime Adapter** over shared `.contora/` workspace state.

Works with **Codex**, **Claude Code**, **Cursor Agent**, and **Gemini CLI**. Bootstraps state without the IDE extension; **18 MCP tools** in V3.1.

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

# Claude Code (plugin)
claude --plugin-dir .

# Claude Code (MCP only, project scope)
claude mcp add --scope project contorium -- node /path/to/contorium/bin/contorium-mcp-launch.cjs

# Verify
set CONTORIUM_WORKSPACE=E:\your-project   # Windows
node bin/contorium-mcp-launch.cjs
# expect: ready on stdio
```

Set `CONTORIUM_WORKSPACE` to your project root **absolute path**.

---

## Recommended tools (V3.1)

| Tool | Description |
|------|-------------|
| `get_project_handoff` | **Recommended AI execution entry** — `.contora/handoff.json` |
| `get_project_graph_snapshot` | **Cognitive summary** — `.contora/graph/snapshot.json` |
| `get_project_knowledge_graph` | Full knowledge graph; optional `minConfidence` (default 0.7) |
| `get_project_snapshot` | L4 Markdown snapshot |
| `get_workspace_context` | Read `state.json` (focus, Git, files) |
| `store_memory` | Write to `.contora/mcp/memories.json` |

Also: `get_project_change`, `get_project_graph`, `get_project_timeline`, `get_project_state`, `get_project_intelligence`, `get_intent_graph`, `get_active_intents`, `get_state_conflicts`, `search_memory`, `get_memory`.

Deprecated: `get_project_impact`, `get_project_intent` — use `get_project_handoff`.

---

## CLI equivalent

```bash
npx contorium init .
npx contorium handoff .
npx contorium graph-snapshot .
npx contorium export .
```

---

## Session views

| View | Role |
|------|------|
| **IDE extension** | Event-driven precision, AI Cortex, Copy AI-ready context |
| **MCP** | Agent-callable tools, bootstrap + 5s sync |
| **CLI** | `init` / `sync` / `handoff` / `graph-snapshot` / `export` |

All read/write the same `.contora/` — not separate memory stores.

Interactive setup: [mcp/index.html](./index.html)
