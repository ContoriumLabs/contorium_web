# Contorium Web

Static site for **Contorium v2** — a shared workspace state system. IDE, MCP, and CLI are peer session views over `.contora/`.

## Site structure

| Path | Page |
| ---- | ---- |
| `index.html` | Home — problem, solution, architecture, features, install |
| `docs/` | Install hub + markdown references |
| `docs/INSTALL.md` | Full three-adapter install / use / uninstall |
| `docs/MCP.md` | MCP server reference (10 tools, hosts) |
| `docs/CLI.md` | CLI commands |
| `docs/IDE_EXTENSION.md` | IDE extension (from upstream repo) |
| `docs/ARCHITECTURE_V2.md` | v2.2 shared state layer model |
| `docs/STATE_ENGINE.md` | State engine internals |
| `mcp/` | Interactive MCP setup |
| `architecture/` | Architecture overview page |

## Preview

```bash
python -m http.server 8080
```

## Links

- [github.com/ContoriumLabs/contorium](https://github.com/ContoriumLabs/contorium)
