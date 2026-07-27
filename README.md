# Contorium Web

Static site for **Contorium** — Project Intelligence Layer for AI-assisted development. IDE, MCP, and CLI are peer runtime surfaces over `.contora/`.

## Site structure

| Path | Page |
| ---- | ---- |
| `index.html` | Home — product story, ask demo, architecture |
| `docs/` | **Documentation hub** (sidebar navigation, readable HTML) |
| `docs/install.html` | Install & use — three adapters, command matrix |
| `docs/mcp.html` | MCP server — `@contorium/mcp`, ask_project, CIL tools |
| `docs/cli.html` | CLI — ask, lifecycle, transfer |
| `docs/dashboard.html` | Runtime dashboard (CRBP) |
| `docs/ide-extension.html` | IDE extension |
| `mcp/` | Interactive MCP setup |

## Documentation build

Markdown sources live in `docs/*.md`. Regenerate HTML after edits:

```bash
python scripts/prepare-user-docs.py
python scripts/build-docs.py
```

## Preview

```bash
python -m http.server 8080
```

Open `http://localhost:8080/docs/` for the documentation hub.

## Links

- [github.com/ContoriumLabs/contorium](https://github.com/ContoriumLabs/contorium)
