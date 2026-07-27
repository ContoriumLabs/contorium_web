# Quick start

> [Home](../index.html) · [Docs](index.html) · [Quick start](getting-started.html) · [Install](install.html)

**Project Intelligence Layer for AI-assisted development.**

AI can read your code. Contorium helps it understand **why your project became what it is.**

Contorium preserves decisions, reasoning, constraints, history, and evolving state — across AI tools, models, and sessions.

Install **IDE**, **MCP**, or **CLI**; all share `.contora/` in your project folder.

---

## Ask your project (CIL)

| Question | Where it routes |
|----------|-----------------|
| What happened this week? | Project History |
| Why was MCP added? | Decision Center |
| What should I do next? | Action Engine (suggestions only) |
| What needs review? | [Knowledge Lifecycle](lifecycle.html) · Review Queue |
| Is this decision still valid? | Lifecycle · Knowledge Health |

| Surface | How to ask |
|---------|------------|
| **CLI** | `contorium ask "Why was MCP added?"` · `contorium lifecycle` |
| **MCP** | `ask_project` · `get_knowledge_health` · `get_review_queue` |
| **IDE** | **Ask Contorium…** · Explore → Review Queue |

CIL suggests and explains. It **never executes tasks** for you.

---

## Choose your entry point

| If you… | Start with |
|---------|------------|
| Code in VS Code / Cursor | [IDE extension](ide-extension.html) |
| Use Claude Code, Codex, or Cursor Agent | [MCP server](mcp.html) |
| Work in the terminal or CI | [CLI](cli.html) |

---

## Daily workflow

### IDE + AI chat

1. Install the extension → open a **folder** (not a single file).
2. Set **Current focus** in the sidebar.
3. Use **Ask Contorium…** or Explore (**Review Queue · Knowledge Health**).
4. New AI chat? Confirm the **handoff prompt** (Y/n) or **Transfer Context**.

### MCP + AI agent

1. [One-line MCP setup](mcp.html#connect-your-ai-tool) for your host.
2. Open Codex / Claude / Cursor in your project.
3. Agent uses `ask_project`, `get_knowledge_health`, or `transfer_project` as needed.

### Terminal

```bash
contorium init .
contorium ask "What is this project about?"
contorium lifecycle
contorium review
contorium transfer context --copy
```

See [CLI guide](cli.html) · [Lifecycle guide](lifecycle.html).

---

## Three things to remember

1. **Open a folder** — not a single file.
2. **Git remembers changes. Contorium remembers why.**
3. **Local-first** — everything in `.contora/` inside your repo.

---

## Next steps

- [Install all adapters](install.html)
- [Knowledge Lifecycle](lifecycle.html)
- [MCP setup wizard](../mcp/)
- [Runtime dashboard](dashboard.html)
