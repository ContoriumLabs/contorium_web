# MCP server — User guide

> [Home](../index.html) · [Docs](index.html) · [Quick start](getting-started.html) · [Install](install.html)

stdio MCP server — **PIL Runtime** for Claude Code, Cursor Agent, OpenAI Codex, Gemini CLI, and other MCP hosts.

- [Quick start](getting-started.html) · [Package README](../mcp/) · [Dashboard](./DASHBOARD.md) · [CLI](./CLI.md) · [Install](./INSTALL.md)

---

## Before you start

| Requirement | Notes |
|-------------|-------|
| Node.js | **18+** |
| Workspace | A real **project folder** (not a single file) |
| Setup | One command per host — see [Connect your AI tool](#connect-your-ai-tool) |

## Main MCP tools

| Group | What it does | Examples |
|-------|--------------|----------|
| **Inspect** | Read project intelligence | `inspect_state`, `inspect_health`, `inspect_graph` |
| **Transfer** | Export context for AI chats | `transfer_context`, `transfer_handoff`, `transfer_intelligence` |
| **Capture** | Save focus, notes, decisions | `capture_focus`, `capture_note`, `capture_decision` |

On a **new AI chat**, the agent may ask to inject project state (Y/n). No terminal command needed.

---

## Connect your AI tool

Run **one command** from your project folder, then open the AI tool in that folder.  
Node.js **18+** required. No JSON editing needed in normal use.

### Codex

```bash
cd /path/to/your-project
codex mcp add contorium -- npx @contorium/mcp
```

Open Codex in the project folder. Remove: `codex mcp remove contorium`

### Claude Code

```bash
cd /path/to/your-project
claude mcp add --scope project contorium -- npx @contorium/mcp
```

Restart Claude Code in the same folder. Remove: `claude mcp remove contorium`

### Cursor

1. **Settings → MCP → Add MCP Server**
2. Name: `contorium` · Command: `npx` · Args: `@contorium/mcp`
3. Enable the server → **Developer: Reload Window**

Remove: Settings → MCP → delete `contorium`

### Gemini CLI

Add to `~/.gemini/settings.json` or `<project>/.gemini/settings.json`:

```json
{
  "mcpServers": {
    "contorium": {
      "command": "npx",
      "args": ["@contorium/mcp"],
      "env": {
        "CONTORIUM_WORKSPACE": "/path/to/your-project"
      }
    }
  }
}
```

Restart the Gemini CLI session after saving.

---

## Manual config (fallback only)

Use this **only if** the one-liner above fails. Do **not** combine with `mcp add`.

<a id="manual-config-fallback"></a>

```json
{
  "mcpServers": {
    "contorium": {
      "command": "npx",
      "args": ["@contorium/mcp"],
      "env": {
        "CONTORIUM_WORKSPACE": "/path/to/your-project"
      }
    }
  }
}
```

| Host | Config file |
|------|-------------|
| Cursor | `.cursor/mcp.json` or Settings → MCP |
| Claude Code | `.mcp.json` in project root |
| Codex | `config.toml` under `[mcp_servers.contorium]` |
| Gemini CLI | `settings.json` → `mcpServers` |

---

## How MCP runs (important)

```text
You open Codex / Claude Code / Cursor Agent
        ↓
Host reads .mcp.json / MCP settings
        ↓
Host spawns: npx @contorium/mcp   (or node …/contorium-mcp.js)
        ↓
MCP connects over stdio
        ↓
On initialize: bootstrap runtime + semi-auto handoff prompt (user confirm)
        ↓
AI calls tools (get_project_handoff, …) when needed
```

| Do | Don't |
|----|-------|
| Configure MCP once per host | Run `npx contorium-mcp` in a terminal before opening Codex (unless debugging) |
| Set `CONTORIUM_WORKSPACE` to your **project** root | Point workspace at the contorium source repo unless you develop contorium itself |
| Restart Agent / reload MCP after config changes | Expect MCP to stay running after you close the AI client (host manages lifecycle) |

---

## Workspace resolution

The server resolves the project root in this order:

1. CLI flag: `--workspace /path/to/project`
2. Environment: `CONTORIUM_WORKSPACE` (also `CODEX_PROJECT_DIR`, `CLAUDE_PROJECT_DIR`, `CLAUDE_PROJECT_ROOT`, `MCP_WORKSPACE_ROOT`)
3. `.mcp.json` or `.cursor/mcp.json` → `mcpServers.contorium.env.CONTORIUM_WORKSPACE`
4. Walk up from cwd to find `.contora/state.json`

---

## Decision Provenance tools (preferred)

Single decision pipeline shared with IDE and CLI. Artifacts persist under `.contora/governance/`.  
See [GitHub language spec](https://github.com/ContoriumLabs/contorium/blob/main/docs/CONTORIUM_LANGUAGE_SPEC.md).

| Tool | Purpose | IDE equivalent | CLI equivalent |
|------|---------|----------------|----------------|
| **`inspect_cognition_ready`** | Verify Decision Provenance layer initialized | Startup ensure | `contorium cognition inspect ready` |
| **`get_decision_context`** | Read decision provenance rules and context | View Rules | `contorium cognition inspect governance` |
| **`resolve_scope_context`** | Resolve scope from open files + git | Review scope selector | Built into derive |
| **`derive_decision_provenance`** | Derive decision provenance chain | Review Change (cycle path) | `contorium decision derive` |
| **`synthesize_context_payload`** | Synthesize inject text for AI chat | Smart/Diff Inject | Dashboard Enter |
| **`export_decision_provenance`** | Export decision provenance appendix | Copy AI context appendix | `[c]` · `decision synthesize` |

**Semantic separation:**

- Review-only flows write **`review.json`**
- `derive_decision_provenance` writes **decision / scope / trace / cycle** (and optional trace-full)

### Legacy governance tool aliases

| Legacy | Preferred |
|--------|-----------|
| `ensure_control_ready` | `inspect_cognition_ready` |
| `get_control_context` | `get_decision_context` |
| `run_governance_cycle` · `build_decision_provenance` | `derive_decision_provenance` |
| `generate_inject_payload` | `synthesize_context_payload` |
| `export_governance_context` | `export_decision_provenance` |

### Governance auxiliary tools

| Tool | Purpose |
|------|---------|
| **`record_project_intent`** | Record project direction text |
| **`analyze_project`** | Analyze project structure and intent |
| **`get_cognitive_state`** | Read cognitive projection state |
| **`get_change_log`** | Read structured change log |

---

## Cognitive mode tools (A/B)

| Tool | Purpose |
|------|---------|
| **`get_cognitive_mode`** | Read current mode (A = default, B = overlay) |
| **`set_cognitive_mode`** | Switch cognitive mode |
| **`get_cognitive_insights`** | Read cognitive insights for workspace |
| **`get_skill_suggestions`** | Skill suggestions (mode B only; display-only links) |
| **`get_model_preset`** | Read recommended model preset |

Mode B overlay suggests skills from open sources (GitHub, npm, local registry). Display-only — nothing is auto-installed. Switch modes from the runtime dashboard (↑↓ select, Enter apply) or via MCP tools.

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

**Debug only:** `contorium handoff --prompt-new-chat` (TTY fallback).

Each new chat re-prompts; skip/inject applies to the current chat only (`chat_session_id`).

---

## Runtime bootstrap (automatic)

When MCP starts, it schedules (via CLI adapter, detached):

- `contorium bootstrap --source mcp` — sync + Passive dashboard worker
- MCP light sync — 5s poll + watch on `.contora/events` and `.git/HEAD`
- Dashboard wake on file/git changes

See [DASHBOARD.md](./DASHBOARD.md). No manual `contorium attach` in normal use.

---

## Environment variables

| Variable | Purpose |
|----------|---------|
| `CONTORIUM_WORKSPACE` | Explicit project root (**preferred**) |
| `CODEX_PROJECT_DIR` | Injected by Codex |
| `CLAUDE_PROJECT_DIR` / `CLAUDE_PROJECT_ROOT` | Injected by Claude Code |
| `MCP_WORKSPACE_ROOT` | Some hosts |

---

## Uninstall / disable

| Host | Action |
|------|--------|
| Cursor | Settings → MCP → remove `contorium` |
| Claude Code | `claude mcp remove contorium` |
| Codex | `codex mcp remove contorium` |
| Gemini CLI | Remove from `mcpServers` in settings.json |
| Global npm | `npm uninstall -g @contorium/mcp` |

Clear MCP-only memory (optional, project root):

```powershell
Remove-Item -Recurse -Force .contora\mcp -ErrorAction SilentlyContinue
```

Does not remove `state.json`, `handoff.json`, or other shared artifacts.

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| MCP fails to start | MCP fails to start | Node 18+; retry one-line setup; or use [manual config](#manual-config-fallback) |
| `found: false` / no handoff | Set `CONTORIUM_WORKSPACE`; run `npx contorium init .` in project |
| Wrong project | `CONTORIUM_WORKSPACE` must be the **application** root, not contorium repo |
| Stale state | Save files; wait for MCP sync; or `npx contorium sync .` |
| Agent shows Canceled | Usually host init cancel — retry opening the AI tool |
| Dashboard not visible | Press **Space** in Contorium terminal tab, or enable IDE status bar — debug: `handoff --show` — see [DASHBOARD.md](./DASHBOARD.md) |

---
