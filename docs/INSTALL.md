# Contorium — Install · Use · Uninstall (three peer adapters)

> [Home](../index.html) · Per-adapter: [IDE](./IDE_EXTENSION.md) · [MCP](./MCP.md) · [CLI](./CLI.md) · [Architecture](./ARCHITECTURE_V2.md)

Contorium v2.2: **IDE / MCP / CLI are peer-level session views** over the same `@contora/state-core` and `.contora/` directory. Any adapter can initialize and maintain state independently; combined use merges automatically (`source.mode: merged`).

| Adapter | Typical user | Standalone capability |
|---------|--------------|----------------------|
| **IDE** | VS Code / Cursor developers | Event stream, sidebar, copy context, BYOK |
| **MCP** | Claude Code / Cursor Agent / Codex / Gemini | Bootstrap, 5s + event sync, 10 MCP tools |
| **CLI** | Terminal / CI / headless | `init` / `sync` / `snapshot` / `status` / `state` |

**Public interface unchanged:** `state.json` fields remain backward compatible; MCP tool names and extension command IDs unchanged. v2.2 adds optional `source` metadata.

---

## Prerequisites (all adapters)

| Requirement | Notes |
|-------------|-------|
| Node.js | **18+** (MCP / CLI / source builds) |
| Workspace | Real project **folder** path |
| Build (from source) | `npm install && npm run compile` at repo root |

Shared artifacts:

```text
.contora/                    # all adapters read/write here
├── state.json               # + source { mode, lastWriter, lastUpdated }
├── state-builder/           # L4 snapshot (scan or IDE pipeline)
├── events/                  # IDE events (CLI/MCP readable, IDE writes)
└── mcp/                     # MCP store_memory (optional)
```

---

## Install

### IDE extension

| Method | Action |
|--------|--------|
| VSIX (recommended) | Release download or `npm run vsix` → Extensions → **Install from VSIX** → Reload |
| Marketplace | Search **Contorium** (`franklee-dev`) |
| Development | `npm run compile` → F5 Extension Development Host |

See [IDE_EXTENSION.md](./IDE_EXTENSION.md).

### MCP server

```bash
git clone https://github.com/ContoriumLabs/contorium.git
cd contorium
npm install
npm run compile          # or npm run build:mcp
```

Configure host (**use absolute paths**):

```json
{
  "mcpServers": {
    "contorium": {
      "command": "node",
      "args": ["E:/path/to/contorium/bin/contorium-mcp-launch.cjs"],
      "env": {
        "CONTORIUM_WORKSPACE": "E:/path/to/your-project"
      }
    }
  }
}
```

| Host | Setup |
|------|-------|
| Cursor | Settings → MCP → enable `contorium` |
| Claude Code | `claude mcp add ...` or `claude --plugin-dir .` |
| Codex | `codex mcp add contorium -- node .../contorium-mcp-launch.cjs` |
| Gemini CLI | `~/.gemini/settings.json` → `mcpServers.contorium` |

See [MCP.md](./MCP.md) and [mcp/](../mcp/).

### CLI

Build with the same repo:

```bash
npm install
npm run compile
```

Usage:

```bash
npx contorium --help
npx contorium init .
```

Optional global link: `npm link` at repo root → `contorium status .` anywhere.

See [CLI.md](./CLI.md).

---

## Use (standalone scenarios)

### IDE only

1. Install extension → open a **folder** workspace  
2. Set **Current focus** in sidebar, code normally  
3. **Copy AI-ready context** to any AI chat  

No MCP / CLI required.

### MCP only

1. `npm run compile`  
2. Configure MCP with `CONTORIUM_WORKSPACE` pointing at project root  
3. Start agent — MCP **bootstraps** `.contora/` if missing  
4. Call `get_workspace_context` / `get_project_snapshot`  

No IDE required; scan/merged mode without IDE events is less precise than extension + events.

### CLI only

```bash
cd /path/to/your-project
npx contorium init .
npx contorium sync .
npx contorium snapshot .
npx contorium status .
npx contorium state .
```

No IDE / MCP; suitable for CI, terminal, scripts.

### Combined (recommended)

| Combo | Effect |
|-------|--------|
| IDE + MCP | IDE writes events + cognition; MCP reads latest snapshot |
| IDE + CLI | IDE daily; CLI `snapshot` in CI |
| All three | `source.lastWriter` tracks last writer; task/notes not overwritten |

---

## Command matrix (v2.2)

| Capability | IDE | MCP | CLI |
|------------|-----|-----|-----|
| Initialize `.contora/` | Open folder | Bootstrap on start | `contorium init` |
| Refresh git/paths | Auto scan | 5s + events/git watch | `contorium sync` |
| Read state | Sidebar | `get_workspace_context` | `contorium state` |
| Read snapshot | Sidebar / copy | `get_project_snapshot` | `contorium snapshot` |
| Status summary | Sidebar | tool JSON | `contorium status` |
| Write task/notes | Sidebar | — | — |
| Agent memory | — | `store_memory` | — |
| Copy markdown | Copy AI-ready context | — | — |

---

## Uninstall

### IDE

Extensions → Contorium → **Uninstall** → Reload Window

### MCP

| Host | Command |
|------|---------|
| Claude Code | `claude mcp remove contorium` |
| Codex | `codex mcp remove contorium` |
| Cursor | Settings → MCP → remove `contorium` |
| Gemini | Remove from `settings.json` |

### CLI

```bash
npm unlink -g contorium   # if linked
```

CLI has no background service. Does **not** delete `.contora/` automatically.

### Clear workspace data (optional)

```powershell
Remove-Item -Recurse -Force .contora
```

```bash
rm -rf .contora
```

---

## Related docs

- [IDE extension](./IDE_EXTENSION.md)
- [MCP server](./MCP.md)
- [CLI](./CLI.md)
- [Architecture v2.2](./ARCHITECTURE_V2.md)
- [State engine](./STATE_ENGINE.md) (internals)
- [GitHub repository](https://github.com/ContoriumLabs/contorium)
