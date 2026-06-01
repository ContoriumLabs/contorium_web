# Contorium MCP Server

stdio MCP service for **Claude Code, Cursor Agent, OpenAI Codex, Gemini CLI**, and other MCP hosts.

**v2.2 can run standalone:** bootstraps `.contora/` without the IDE; **5s polling + event/git triggers** keep state fresh.  
Overview: [INSTALL.md](./INSTALL.md) · [Architecture v2.2](./ARCHITECTURE_V2.md) · [MCP setup page](../mcp/)

---

## Quick reference

| Phase | Command / action |
|-------|------------------|
| **Build** | `git clone … && cd contorium && npm install && npm run compile` |
| **Verify** | `set CONTORIUM_WORKSPACE=E:\your-project` then `node bin/contorium-mcp-launch.cjs` (expect `ready on stdio`) |
| **Cursor** | Settings → MCP → enable `contorium` |
| **Claude Code** | `claude mcp add --scope project contorium -- node …/contorium-mcp-launch.cjs` or `claude --plugin-dir .` |
| **Codex** | `codex mcp add contorium -- node …/contorium-mcp-launch.cjs` |
| **Daily use** | Agent calls `get_workspace_context` / `get_project_snapshot` / `store_memory` |
| **Remove** | `claude mcp remove contorium` · `codex mcp remove contorium` · Cursor Settings → MCP |

---

## Prerequisites

| Requirement | Notes |
|-------------|-------|
| Node.js | **18+** |
| Workspace | Real project directory |
| Extension (optional) | [IDE extension](./IDE_EXTENSION.md) adds event-driven precision; MCP still bootstraps alone |
| Build | `npm run compile` or `npm run build:mcp` before first use |

Artifacts:

- Entry: `packages/mcp/dist/server.js`
- Launcher: `bin/contorium-mcp-launch.cjs` (recommended for absolute paths)

---

## Install

### Build from source

```bash
git clone https://github.com/ContoriumLabs/contorium.git
cd contorium
npm install
npm run compile
```

Verify:

```bash
node packages/mcp/dist/server.js
# [contorium-mcp] ready on stdio — Ctrl+C to exit
```

### Cursor

Merge into `.cursor/mcp.json` or user MCP settings (**absolute paths**):

```json
{
  "mcpServers": {
    "contorium": {
      "command": "node",
      "args": ["E:/path/to/contorium/bin/contorium-mcp-launch.cjs"],
      "env": {
        "CONTORIUM_WORKSPACE": "E:/your-actual-workspace"
      }
    }
  }
}
```

Settings → MCP → enable `contorium` → Reload Window / restart Agent.

### Claude Code

**Plugin (recommended):**

```bash
cd /path/to/contorium
npm run build:mcp
claude --plugin-dir .
```

**MCP only (project scope):**

```bash
claude mcp add --scope project contorium -- node /path/to/contorium/bin/contorium-mcp-launch.cjs
```

Env: `CONTORIUM_WORKSPACE`, `CLAUDE_PROJECT_DIR` (injected by Claude Code).

### Codex

```bash
npm run build:mcp
codex mcp add contorium -- node ./bin/contorium-mcp-launch.cjs
```

Or use repo `.mcp.json` + `.codex-plugin/plugin.json`.

### Gemini CLI

In `~/.gemini/settings.json`:

```json
{
  "mcpServers": {
    "contorium": {
      "command": "node",
      "args": ["/absolute/path/to/contorium/bin/contorium-mcp-launch.cjs"],
      "env": {
        "CONTORIUM_WORKSPACE": "/absolute/path/to/your-workspace"
      }
    }
  }
}
```

Restart Gemini CLI session after changes.

---

## Tools (10)

| Tool | R/W | Description |
|------|-----|-------------|
| `store_memory` | write | Persist to `.contora/mcp/memories.json` |
| `search_memory` | read | Keyword search MCP memories |
| `get_memory` | read | Fetch by key |
| `get_workspace_context` | read | Extension/state `state.json` (focus, Git, files) |
| `get_project_intelligence` | read | L5 `intelligence/state-summary.json` |
| `get_intent_graph` | read | Full intent graph |
| `get_active_intents` | read | Active intent nodes |
| `get_project_state` | read | L4 `state-builder/project-state.json` |
| `get_project_snapshot` | read | L4 Markdown snapshot (`format=json` optional) |
| `get_state_conflicts` | read | v2 unresolved conflicts (audit only) |

---

## Workflows

**MCP only (no IDE):**

1. Set `CONTORIUM_WORKSPACE`  
2. Start agent — first call bootstraps `.contora/`  
3. Use `get_project_snapshot` / `get_workspace_context`  

**IDE + MCP (best precision):**

1. Open project in extension, set **Current focus**  
2. Enable MCP on same workspace  
3. Use `store_memory` for cross-session agent notes  

**CLI alternative:**

```bash
contorium init . && contorium snapshot .
```

---

## Environment variables

| Variable | Role |
|----------|------|
| `CONTORIUM_WORKSPACE` | Explicit workspace root (preferred) |
| `CODEX_PROJECT_DIR` | Codex injection |
| `CLAUDE_PROJECT_DIR` | Claude Code injection |
| `MCP_WORKSPACE_ROOT` | Some hosts |

If unset: walk up from MCP `cwd` to find `.contora/state.json`.

---

## vs Copy AI-ready context

| Method | Use when |
|--------|----------|
| **Copy AI-ready context** (IDE) | Paste into any chat — 4-layer Markdown |
| **get_project_snapshot** (MCP) | Agent pulls structured state automatically |
| **get_state_conflicts** (MCP) | Audit IDE/MCP decision conflicts |

---

## Uninstall / troubleshooting

See [INSTALL.md](./INSTALL.md) for host-specific removal.

| Issue | Fix |
|-------|-----|
| No `state.json` | Set `CONTORIUM_WORKSPACE`; run `contorium init .` |
| MCP won't start | `npm run compile`, Node 18+, absolute paths |
| Stale state | IDE: Save session state; MCP: wait 5s or touch events; CLI: `contorium sync .` |
| Wrong `workspaceRoot` | Set `CONTORIUM_WORKSPACE` to project root |

---

## Related

- [INSTALL.md](./INSTALL.md)
- [IDE extension](./IDE_EXTENSION.md)
- [CLI](./CLI.md)
- [State engine](./STATE_ENGINE.md)
- [Interactive MCP setup](../mcp/)
