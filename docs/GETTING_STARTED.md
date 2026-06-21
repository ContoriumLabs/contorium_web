# Quick start

> [Home](../index.html) · [Docs](index.html) · [Quick start](getting-started.html) · [Install](install.html)

Contorium is an **AI Project Intelligence Layer**. It keeps project understanding in your workspace so AI tools can **continue where you left off** — without re-explaining architecture every session.

**You use it by:** installing one entry point (IDE, MCP, or CLI), opening a **folder** workspace, then using **Inspect · Transfer · Capture** as you work with AI.

---

## Choose your entry point

| If you… | Start with |
|---------|------------|
| Code in VS Code / Cursor | [IDE extension](ide-extension.html) |
| Use Claude Code, Codex, or Cursor Agent | [MCP server](mcp.html) |
| Work in the terminal or CI | [CLI](cli.html) |

All three share the same `.contora/` folder in your project. You can add more later.

---

## Daily workflow

### IDE + AI chat

1. Install the extension → open a **folder** (not a single file).
2. Set **Current focus** in the Contorium sidebar.
3. Code as usual — Contorium updates `.contora/` automatically.
4. Starting a new AI chat? Confirm the **handoff prompt** (Y/n) or use **Transfer Context** from the sidebar.

### MCP + AI agent

1. Run the [one-line MCP setup](mcp.html#connect-your-ai-tool) for your host.
2. Open Codex / Claude / Cursor in your project — MCP starts automatically.
3. The agent reads project state via `inspect_*` tools and exports context via `transfer_*` when needed.

### Terminal

```bash
contorium init .
contorium inspect health .
contorium transfer context --copy
```

See the [CLI guide](cli.html) for the full command list.

---

## Three things to remember

1. **Open a folder** — Contorium needs a project root, not a lone file.
2. **Local-first** — everything lives in `.contora/` inside your repo. No cloud account.
3. **Transfer, don't re-prompt** — use Transfer Context / Handoff instead of pasting long explanations again.

---

## What Contorium is not

- Not an AI agent or code generator
- Not a project manager or task runner
- Not a cloud service

It **records and preserves** project intelligence. It does **not** make decisions for you.

---

## Next steps

- [Install all adapters](install.html)
- [Runtime dashboard](dashboard.html) — terminal status UI (starts automatically)
- [Interactive MCP setup](../mcp/)
