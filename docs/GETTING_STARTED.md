# Quick start

> [Home](../index.html) · [Docs](index.html) · [Quick start](getting-started.html) · [Install](install.html)

**Contorium lets you ask your project.**

It is a local **Cognitive Interaction Layer (CIL)** on a **Project Intelligence Layer (PIL)**. Ask what happened, why a decision was made, or what comes next — then switch between Cursor, Claude Code, Codex, Gemini CLI, and VS Code without re-explaining your architecture.

**You use it by:** installing one entry point (IDE, MCP, or CLI), opening a **folder** workspace, then **Ask · Capture · Transfer** as you work with AI.

---

## Ask your project (CIL)

| Question | Where it routes |
|----------|-----------------|
| What happened this week? | Project History |
| Why was MCP added? | Decision Center |
| What should I do next? | Action Engine (suggestions only) |
| Tell me everything about auth | Knowledge Graph |
| What was state last Friday? | Time Travel (Snapshot) |

| Surface | How to ask |
|---------|------------|
| **CLI** | `contorium ask "Why was MCP added?"` |
| **MCP** | Agent calls `ask_project` |
| **IDE** | Command palette → **Ask Contorium…** · Cortex panel |

CIL suggests and explains. It **never executes tasks** for you.

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
3. Use **Ask Contorium…** or Cortex (**History · Decisions · Ask**) to explore project understanding.
4. Starting a new AI chat? Confirm the **handoff prompt** (Y/n) or use **Transfer Context** from the sidebar.

### MCP + AI agent

1. Run the [one-line MCP setup](mcp.html#connect-your-ai-tool) for your host.
2. Open Codex / Claude / Cursor in your project — MCP starts automatically.
3. Ask via `ask_project` or use `inspect_*` / `transfer_*` when the agent needs structured facts.

### Terminal

```bash
contorium init .
contorium ask "What is this project about?"
contorium health .
contorium transfer context --copy
```

See the [CLI guide](cli.html) for the full command list.

---

## Three things to remember

1. **Open a folder** — Contorium needs a project root, not a lone file.
2. **Ask, don't re-prompt** — use `contorium ask` or `ask_project` instead of pasting long explanations.
3. **Local-first** — everything lives in `.contora/` inside your repo. No cloud account.

---

## What Contorium is not

- Not an AI agent or code generator
- Not a project manager or task runner
- Not a cloud service

CIL suggests. PIL records. **Neither executes work for you.**

---

## Next steps

- [Install all adapters](install.html)
- [MCP setup wizard](../mcp/)
- [Runtime dashboard](dashboard.html) — terminal status UI (starts automatically)
