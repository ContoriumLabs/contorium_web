# Install & use

> [Home](../index.html) · [Docs](index.html) · [Quick start](getting-started.html) · [Install](install.html)

Contorium is a local **Cognitive Interaction Layer (CIL)** on a **Project Intelligence Layer (PIL)**. Install **IDE**, **MCP**, or **CLI** — all share `.contora/` in your project folder.

**Responsibility chain:** Capture → Structure → Preserve → Ask → Transfer

| Adapter | Typical user | Primary loop |
|---------|--------------|--------------|
| **IDE** | VS Code / Cursor | Ask · Capture · Transfer |
| **MCP** | Claude / Codex / Cursor Agent | Ask · Inspect · Transfer |
| **CLI** | Terminal / CI | Ask · Inspect · Transfer |


## Prerequisites (all adapters)

| Requirement | Notes |
|-------------|-------|
| Node.js | **18+** (MCP / CLI / source build) |
| Workspace | Real project **folder** path |
| Build (from source) | Repo root: `npm install && npm run compile` |

Artifact layout:

```text
.contora/                    # shared by all adapters
├── state.json               # + source { mode, lastWriter, lastUpdated }
├── handoff.json             # CHP v1 AI handoff (single source for task/changes)
├── understanding_graph.json # call chains + impact (Runtime Understanding Graph)
├── change.json / graph.json / timeline.json
├── governance/              # V4 governance artifacts
│   ├── review.json          # Review results (review command only)
│   ├── decision.json        # Decision outcome (allow, risk, rule_count, …)
│   ├── scope.json           # Scope context (files, modules, dependencies)
│   ├── trace.json           # Summary trace (≤12 steps; dashboard/export read)
│   ├── trace-full.json      # Detailed reason_chain (≤64 entries)
│   └── cycle.json           # Full cycle record + matched_rules + metrics
├── runtime.bootstrap.json   # runtime_id (session-level, not in handoff)
├── mcp.auto-context.md        # written after user confirms semi-auto injection
├── mcp.handoff-injection.json # injection state per runtime_id
├── state-builder/           # L4 snapshot (scan or IDE cognition pipeline)
├── graph/                   # V3.1 cognitive graph (knowledge.json, snapshot.json, …)
├── config/                  # LLM settings (no secrets in llm.json)
│   ├── llm.json             # provider, model, modules, intent_router
│   └── .llm-keys.json       # per-provider API keys (gitignored)
├── cache/llm/               # optional LLM response cache
├── events/                  # IDE events (CLI/MCP read; IDE writes)
├── dashboard.*.json         # dashboard view/signals (not business state source)
└── mcp/                     # MCP store_memory (optional)
```

---

## Install

### IDE extension

| Method | Steps |
|--------|-------|
| VSIX (recommended) | Download Release or `npm run vsix` → Extensions → **Install from VSIX** → Reload |
| Marketplace | Search **Contorium** (`franklee-dev`) |
| Development | `npm run compile` → F5 Extension Development Host |

See [IDE extension](ide-extension.html).

### MCP server (`@contorium/mcp`)

```bash
git clone https://github.com/ContoriumLabs/contorium.git
cd contorium
npm install
npm run compile          # or npm run build:mcp
```

**Normal use:** configure once, then open Codex / Claude / Cursor — the host **spawns MCP automatically**. You do not run MCP in a terminal first.

**Local development config** (replace paths):

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

**When published to npm:**

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

| Host | Setup |
|------|-------|
| Cursor | `.cursor/mcp.json` or Settings → MCP → enable `contorium` |
| Claude Code | `claude mcp add --scope project contorium -- npx @contorium/mcp` |
| Codex | `codex mcp add contorium -- npx @contorium/mcp` |
| Gemini CLI | `~/.gemini/settings.json` → `mcpServers.contorium` |

See [MCP](mcp.html) for step-by-step host guides.

### CLI

Ships with the same repo — no separate npm publish:

```bash
npm install
npm run compile
npx contorium --help
npx contorium init .
```

Optional global link (repo root): `npm link` → `contorium status .`

See [CLI](cli.html).

---

## Usage scenarios

### IDE only

1. Install extension → open a **folder** workspace  
2. Set **Current focus** in the sidebar, code normally  
3. **Copy AI-ready context** into any AI chat  

No MCP or CLI required.

### MCP only

1. `npm install -g @contorium/mcp` **or** `npm run compile` from source  
2. `contorium-mcp bootstrap --workspace /path/to/project` (optional)  
3. Configure MCP with `CONTORIUM_WORKSPACE` (see [MCP](mcp.html))  
4. **Open Codex / Claude / Cursor** — host starts MCP and bootstraps `.contora/`  
5. **New chat:** injection prompt appears automatically — Agent asks Y/n, or use terminal **Enter/i** / IDE **[?]**
6. Agent calls **`inspect_state`** / **`transfer_context`** / **`transfer_handoff`** as needed (legacy: `get_project_handoff`, `get_understanding_graph`, …)

No manual MCP terminal. No IDE required; scan/merged mode is less precise without IDE events.

See also [Runtime Dashboard](dashboard.html) — full-screen **Cognitive State** TUI (auto-attached after bootstrap).

### CLI only

```bash
cd /path/to/your-project
npx contorium init .
npx contorium sync .
npx contorium snapshot .
npx contorium handoff .
npx contorium handoff --copy-to-ai
# debug only:
# npx contorium handoff --prompt-new-chat
# npx contorium handoff --show
npx contorium graph-snapshot .
npx contorium knowledge .
npx contorium export .
npx contorium governance review . --target path/to/file.ts
npx contorium governance cycle .
npx contorium governance export . --copy
npx contorium status .
npx contorium state .
```

No IDE or MCP; suitable for CI and scripts.

### Combined (recommended)

| Combo | Effect |
|-------|--------|
| IDE + MCP | IDE writes events + cognitive graph; MCP reads handoff / graph-snapshot |
| IDE + CLI | IDE daily; CLI `export` or `graph-snapshot` in CI |
| All three | `source.lastWriter` tracks last writer; task/notes are not overwritten |

---

## Command matrix (PIL v3.0 + legacy)

| Capability | IDE | MCP (PIL) | CLI (PIL) |
|------------|-----|-----------|-----------|
| Bootstrap `.contora/` | Open folder | Bootstrap on start | `contorium init` |
| Refresh git/paths | Auto scan | 5s + events/git watch | `contorium sync` |
| **Inspect state** | Sidebar | `inspect_state` | `contorium inspect state` |
| **Inspect health** | Cortex panels | `inspect_health` | `contorium inspect health` |
| **Transfer Context** | Sidebar button | `transfer_context` | `contorium transfer context [--copy]` |
| **Transfer Intelligence** | Sidebar button | `transfer_intelligence` | `contorium transfer intelligence [--copy]` |
| **Transfer Handoff** | Runtime inject | `transfer_handoff` | `contorium transfer handoff [--copy]` |
| **Capture focus / note** | Sidebar | `capture_focus` · `capture_note` | `contorium capture focus\|note` |
| **Semi-auto new chat inject** | Auto dialog + `[?]` status bar | `get_handoff_injection_status` → confirm | Dashboard **`i`** · debug: `handoff --prompt-new-chat` |
| **Runtime dashboard** | Auto attach on workspace open | Auto attach on MCP init | Auto attach after `bootstrap` |
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
| Global npm | `npm uninstall -g @contorium/mcp` |

### CLI

```bash
npm unlink -g contorium   # if you ran npm link
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
