# Contorium CLI

CLI is a **peer session view** alongside IDE and MCP — same `@contora/state-core`, same `.contora/`.

Overview: [INSTALL.md](./INSTALL.md) · [Architecture v2.2](./ARCHITECTURE_V2.md)

---

## Quick reference

| Phase | Command |
|-------|---------|
| **Install** | `npm install && npm run compile` (contorium repo root) |
| **Verify** | `npx contorium status .` or `npx contorium --help` |
| **Global (optional)** | `npm link` at repo root → `contorium status .` anywhere |
| **Initialize** | `npx contorium init [path]` |
| **Refresh** | `npx contorium sync [path]` |
| **Snapshot** | `npx contorium snapshot [path]` |
| **Summary** | `npx contorium status [path]` |
| **Full state** | `npx contorium state [path]` |

Default `[path]` is current directory.

---

## Install

```bash
git clone https://github.com/ContoriumLabs/contorium.git
cd contorium
npm install
npm run compile
```

Verify:

```bash
npx contorium init .
npx contorium status .
```

Optional global link:

```bash
npm link
contorium status /path/to/project
```

---

## Commands

| Command | Action |
|---------|--------|
| `contorium init [path]` | Create or merge `state.json`, generate L4 snapshot |
| `contorium sync [path]` | Re-scan git + recent files and merge |
| `contorium snapshot [path]` | Print `PROJECT SNAPSHOT` markdown |
| `contorium status [path]` | JSON summary (mode, source, git counts, eventCount) |
| `contorium state [path]` | Print full `state.json` |

Writes set `source.lastWriter: "cli"`.

### Examples

**PowerShell:**

```powershell
cd E:\your-project
npx contorium init .
npx contorium sync .
npx contorium snapshot . | Out-File -Encoding utf8 .contora\snapshot-export.md
npx contorium status .
```

**bash:**

```bash
cd /path/to/project
npx contorium init .
npx contorium sync .
npx contorium snapshot . > .contora/snapshot-export.md
```

---

## With IDE / MCP

- **No dependency** on IDE extension or MCP process  
- **With IDE:** IDE writes events; CLI `sync` supplements git/paths without overwriting `currentTask` / `notes`  
- **With MCP:** shared `syncWorkspaceState()` logic  

---

## Uninstall

```bash
npm unlink -g contorium   # if linked
```

No background service. Does not delete `.contora/`.

Clear workspace data (optional):

```powershell
Remove-Item -Recurse -Force .contora
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `command not found` | Run from repo with `npx contorium` or `npm link` |
| Empty snapshot | Run `contorium sync .` after `init` |
| Conflicts with IDE | Check `source.lastWriter` in `state.json` |

---

## Related

- [INSTALL.md](./INSTALL.md)
- [IDE extension](./IDE_EXTENSION.md)
- [MCP](./MCP.md)
