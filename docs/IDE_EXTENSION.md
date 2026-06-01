# Contorium IDE Extension (VS Code / Cursor)

> Overview: [INSTALL.md](./INSTALL.md) · Architecture: [ARCHITECTURE_V2.md](./ARCHITECTURE_V2.md)

Extension ID: `franklee-dev.contorium`  
Display name: **Contorium**  
Requires VS Code / Cursor **1.85+** and a **folder workspace** (single-file windows are limited).

The IDE is a **session view** over shared `.contora/` state — peer-level with [MCP](./MCP.md) and [CLI](./CLI.md). It provides sidebar UI, file/Git scanning, `state.json`, State Engine artifacts, and **Copy AI-ready context**.

---

## Command cheat sheet

| Phase | Action |
|-------|--------|
| **Install (VSIX)** | `npm run vsix` → Extensions → **Install from VSIX…** → **Developer: Reload Window** |
| **Install (dev)** | `npm install && npm run compile` → **F5** → open project folder in Extension Development Host |
| **Verify** | Activity bar **Contorium** → sidebar shows Current focus / Copy button |
| **Daily use** | Sidebar **Copy AI-ready context**; `Ctrl+Shift+P` → `Contorium:` commands |
| **Uninstall** | Extensions → Contorium → **Uninstall** → Reload |
| **Clear data (optional)** | Project root: `Remove-Item -Recurse -Force .contora` (PowerShell) |

---

## Install

### Option A — From VSIX (recommended)

For release packages or local builds.

1. Get `contorium-0.7.0.vsix`:
   - [GitHub Releases](https://github.com/ContoriumLabs/contorium/releases), or
   - Run `npm run vsix` at repo root (Node.js 18+)
2. Open **VS Code** or **Cursor**
3. **Extensions** → `…` → **Install from VSIX…**
4. Select the `.vsix` file
5. Run **Developer: Reload Window**

### Option B — From source (development)

```bash
git clone https://github.com/ContoriumLabs/contorium.git
cd contorium
npm install
npm run compile
```

Open the repo in VS Code/Cursor → **F5** (Run Extension) → open your project folder in the new Extension Development Host window.

### Option C — Marketplace

Search **Contorium**, publisher **franklee-dev**, install, then Reload Window.

---

## Verify installation

1. **Contorium** icon appears in the activity bar
2. Open a project with **File → Open Folder** (not single file only)
3. Open the Contorium sidebar — you should see:
   - Current focus input
   - **Copy AI-ready context** button
   - Workspace snapshot / Git areas

If the sidebar stays blank, see [Troubleshooting](#troubleshooting).

---

## Usage

### Sidebar (main UI)

| Action | Description |
|--------|-------------|
| **Current focus** | L0 task anchor — written to `state.json`, not auto-inferred |
| **Context notes** | Local notes included in export |
| **Copy AI-ready context** | Copy converged 4-layer context to clipboard |
| **Sync state to disk** | Persist `state.json` immediately |
| **Restore editors** | Reopen editors from last saved state |
| **Project state** | L4 snapshot preview (full content via copy button) |
| **State conflicts** | Shown when unresolved (v2 audit, no auto-resolution) |
| **Intent graph** | L5 weak inference preview — not in main copy export |

### Command palette

`Ctrl+Shift+P` (macOS: `Cmd+Shift+P`), search **Contorium**:

| Command | Purpose |
|---------|---------|
| Copy AI-ready context (clipboard) | One-click export |
| Save session state now | Persist immediately |
| Restore editors from saved state | Restore editor layout |
| Configure API key… (BYOK) | Optional cloud model key |
| Observe workspace (AI summary) | BYOK workspace summary |
| Learn workspace intent (AI) | BYOK intent learning |
| Tighten context preview (AI) | BYOK compression preview |
| Start fresh AI context session | Clear session events + cognition artifacts |

### Copy export structure (v2.1)

```text
# TASK ANCHOR
# PROJECT SNAPSHOT      (pure project state)
# WORKING CONTEXT       (active files + recent work)
# INSIGHTS              (max 3 lightweight hints, optional)
# NOTES / INSTRUCTION   (when set)
```

### Local data (`.contora/`)

All data stays in the project — **not uploaded by default**:

```text
.contora/
├── state.json                 # runtime state (focus, files, Git, notes)
├── events/<sessionId>.jsonl   # event log (can disable)
├── intelligence/              # L5 semantic summary
├── intent-graph/              # L5 intent graph
├── state-builder/             # L4 project state + snapshot.md
├── state-engine/              # v2 conflict audit
└── mcp/                       # MCP store_memory (if using MCP)
```

Add `.contora/` to `.gitignore` (example provided in repo).

### With MCP / CLI (optional)

All three adapters are **peer-level** — the extension is not a prerequisite for MCP or CLI.

| Scenario | Description |
|----------|-------------|
| IDE only | Sidebar + copy — enough for daily use |
| IDE + MCP | IDE writes events; agents read snapshot via MCP |
| No IDE | MCP or `contorium init` can bootstrap alone |

Same `.contora/` directory. See [INSTALL.md](./INSTALL.md).

---

## Uninstall

### Remove extension (keep project data)

**UI:**

1. **Extensions** → search **Contorium**
2. **Uninstall**
3. **Developer: Reload Window**

**Manual removal (if corrupted):**

Windows PowerShell:

```powershell
Remove-Item -Recurse -Force "$env:USERPROFILE\.cursor\extensions\franklee-dev.contorium-*" -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force "$env:USERPROFILE\.vscode\extensions\franklee-dev.contorium-*" -ErrorAction SilentlyContinue
```

macOS / Linux:

```bash
rm -rf ~/.cursor/extensions/franklee-dev.contorium-*
rm -rf ~/.vscode/extensions/franklee-dev.contorium-*
```

Restart the IDE.

### Clear workspace data (optional)

Uninstalling the extension does **not** delete `.contora/`.

**PowerShell (project root):**

```powershell
Remove-Item -Recurse -Force .contora -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force .context-recall -ErrorAction SilentlyContinue
```

**macOS / Linux:**

```bash
rm -rf .contora .context-recall
```

### Clear BYOK keys (optional)

API keys use VS Code **SecretStorage**. They may persist after uninstall depending on IDE behavior. Use **Configure API key** while installed to clear or overwrite.

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Sidebar loading / blank | Usually **`@contora/state-core` not built**: run `npm run compile` → Reload; compile before F5; reinstall VSIX from `npm run vsix`. Check **Output → Extension Host** for `state-core` |
| Cursor "installation corrupt" | Remove extension dirs manually (see Uninstall), reinstall VSIX; reinstall Cursor if needed |
| Copy content empty or stale | Edit/save files, wait ~7s or run **Save session state now**, then copy |
| No `.contora` folder | Open a folder workspace; trigger save or **Sync state to disk** |
| VSIX install fails | Confirm `npm run vsix` succeeds; package ~350–400KB; avoid broken symlink packages |

**Logs:** `Ctrl+Shift+P` → **Developer: Show Logs** → **Extension Host**, filter `Contorium`.

---

## Related docs

- [INSTALL.md](./INSTALL.md)
- [MCP.md](./MCP.md)
- [CLI.md](./CLI.md)
- [STATE_ENGINE.md](./STATE_ENGINE.md)
- [ARCHITECTURE_V2.md](./ARCHITECTURE_V2.md)
