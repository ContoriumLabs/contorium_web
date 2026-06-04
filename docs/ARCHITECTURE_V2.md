# Contorium v2.2 �?Shared Workspace State Layer

Contorium is a **shared workspace state layer** for AI tools. **IDE, MCP, and CLI are peer session views** over the same `.contora/` artifacts. `state-core` is the single state engine; state-builder, normalization, and snapshot live inside state-core.

> Product overview: [contorium.dev](../index.html) · Install: [INSTALL.md](./INSTALL.md)

---

## Principles

1. **State first** �?`state.json` stays backward compatible; v2.2 adds optional `source` (writer + mode).
2. **Dual-mode state engine**
   - **Mode A (event-driven)** �?IDE `events/*.jsonl`
   - **Mode B (scan-driven)** �?workspace scan
   - **Merged** �?when events exist, scan only supplements git/paths; does not overwrite task/notes
3. **Three peer views** �?IDE / MCP / CLI are equal; not “CLI optional�?
4. **Public interface unchanged** �?MCP tool names, extension command IDs, existing `state.json` fields

---

## Mental model (v2)

```text
                Workspace (filesystem)
                      �?
        Contorium State Layer (.contora/)
                      �?
──────────────────────────────────
 Session views (NOT separate memory)
──────────────────────────────────
 IDE windows · MCP agents · CLI processes
```

| Concept | v2 definition |
|---------|----------------|
| IDE | session view |
| MCP | session view |
| CLI | session view |
| Window / Agent | session view |
| `state.json` | workspace truth |
| `.contora/` | system root |

Each session is a **view** over the same workspace state �?not independent memory.

---

## Package layout

```text
packages/state-core/
  src/scanner/          # workspace + git scan
  src/bootstrap/        # state.json read/write
  src/state-builder/    # L2/L3/L4: buildFromScan, snapshot, store
  src/dualMode.ts
  src/sourceMetadata.ts
packages/cli/           # CLI session view
packages/mcp/           # MCP session view + 5s poll + event/git triggers
src/adapters/           # IDE session view bridge
```

---

## `state.json` source metadata (v2.2)

```json
{
  "source": {
    "mode": "merged",
    "lastWriter": "ide",
    "lastUpdated": "2026-05-20T12:00:00.000Z"
  }
}
```

MCP / CLI use this to see whether state came from IDE bootstrap or scan.

---

## MCP sync

- **5 second** lightweight poll (was 30s)
- **Event-driven:** watch `.contora/events/` and `.git/HEAD`, debounced refresh

---

## Data flow

| View | Input | Output |
|------|-------|--------|
| IDE | Editor / git events | `state.json` + cognition artifacts |
| MCP | Bootstrap + 5s/event sync | `state.json` + state-builder (no events) |
| CLI | `init` / `sync` / `snapshot` | Same scan path |

Intent graph and BYOK are upper-layer capabilities; they do not block standalone adapter use.

---

## `.contora/` layout

```text
<workspace-root>/
└── .contora/
    ├── state.json
    ├── events/
    ├── state-builder/
    ├── intelligence/       # optional L5
    ├── intent-graph/       # optional L5
    ├── state-engine/       # v2 conflict audit
    └── mcp/                # store_memory
```

---

## Related

- [INSTALL.md](./INSTALL.md)
- [MCP.md](./MCP.md)
- [CLI.md](./CLI.md)
- [IDE extension](./IDE_EXTENSION.md)
- [State engine internals](./STATE_ENGINE.md)
