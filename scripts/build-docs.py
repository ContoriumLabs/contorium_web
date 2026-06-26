#!/usr/bin/env python3
"""Build user-facing HTML manuals from docs/*.md"""
from __future__ import annotations

import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

SLUG_MAP = {
    "GETTING_STARTED.md": "getting-started.html",
    "INSTALL.md": "install.html",
    "IDE_EXTENSION.md": "ide-extension.html",
    "MCP.md": "mcp.html",
    "CLI.md": "cli.html",
    "DASHBOARD.md": "dashboard.html",
}

NAV = [
    ("Getting started", [
        ("Overview", "index.html"),
        ("Quick start", "getting-started.html"),
        ("Install & use", "install.html"),
    ]),
    ("Guides", [
        ("IDE extension", "ide-extension.html"),
        ("MCP server", "mcp.html"),
        ("CLI", "cli.html"),
        ("Runtime dashboard", "dashboard.html"),
    ]),
]

HEADER = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="{description}" />
    <title>{title} — Contorium Docs</title>
    <link rel="icon" href="../logo.png" type="image/png" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=JetBrains+Mono:wght@400;500&display=swap"
      rel="stylesheet"
    />
    <link rel="stylesheet" href="../styles.css" />
    <link rel="stylesheet" href="docs.css" />
  </head>
  <body class="docs-body">
    <header class="site-header">
      <nav class="nav-inner" aria-label="Primary">
        <a href="../index.html" class="logo">
          <img class="logo-img" src="../logo.png" width="36" height="36" alt="Contorium" />
          Contorium
        </a>
        <div class="nav-links">
          <a href="../index.html#ask">Product</a>
          <a href="install.html">Install</a>
          <a href="../mcp/">MCP setup</a>
          <a href="index.html" class="nav-active">Docs</a>
          <a href="https://github.com/ContoriumLabs/contorium" target="_blank" rel="noopener noreferrer">GitHub</a>
        </div>
      </nav>
    </header>
    <div class="docs-shell">
      <aside class="docs-sidebar" aria-label="Documentation">
        {sidebar}
      </aside>
      <main class="docs-main">
        {breadcrumb}
        <article class="docs-prose">
          {content}
        </article>
      </main>
    </div>
  </body>
</html>
"""

HUB_CONTENT = """
<div class="docs-hub-hero">
  <h1>User guide</h1>
  <p>
    <strong>Ask your project</strong> — Contorium is a local Cognitive Interaction Layer (CIL) on a Project Intelligence Layer (PIL).
    Install <strong>IDE</strong>, <strong>MCP</strong>, or <strong>CLI</strong>; all share the same
    <code>.contora/</code> folder in your project.
  </p>
</div>

<section>
  <p class="docs-sidebar-title" style="padding-left:0">Start here</p>
  <div class="docs-card-grid">
    <a class="docs-card" href="getting-started.html">
      <span class="docs-card-tag">New user</span>
      <h3>Quick start</h3>
      <p>Ask via CLI, MCP, or IDE — choose an entry point and daily workflow.</p>
    </a>
    <a class="docs-card" href="install.html">
      <span class="docs-card-tag">Setup</span>
      <h3>Install &amp; use</h3>
      <p>Install IDE, MCP, or CLI · usage scenarios · uninstall.</p>
    </a>
    <a class="docs-card" href="../mcp/">
      <span class="docs-card-tag">Interactive</span>
      <h3>MCP setup wizard</h3>
      <p>Step-by-step wiring for Codex, Claude Code, and Cursor.</p>
    </a>
  </div>
</section>

<section style="margin-top:40px">
  <p class="docs-sidebar-title" style="padding-left:0">Guides by tool</p>
  <div class="docs-card-grid">
    <a class="docs-card" href="ide-extension.html">
      <span class="docs-card-tag">IDE</span>
      <h3>IDE extension</h3>
      <p>Ask Contorium, Cortex panels, focus, Transfer Context.</p>
    </a>
    <a class="docs-card" href="mcp.html">
      <span class="docs-card-tag">MCP</span>
      <h3>MCP server</h3>
      <p><code>ask_project</code>, one-line setup, Inspect · Transfer · Capture.</p>
    </a>
    <a class="docs-card" href="cli.html">
      <span class="docs-card-tag">CLI</span>
      <h3>CLI</h3>
      <p><code>contorium ask</code>, <code>health</code>, <code>transfer</code>, <code>capture</code>.</p>
    </a>
    <a class="docs-card" href="dashboard.html">
      <span class="docs-card-tag">Dashboard</span>
      <h3>Runtime dashboard</h3>
      <p>Terminal status UI, Project History view — starts automatically.</p>
    </a>
  </div>
</section>

<section style="margin-top:40px">
  <h2>CIL — Ask your project</h2>
  <table>
    <thead>
      <tr><th>Question</th><th>CLI</th><th>MCP</th></tr>
    </thead>
    <tbody>
      <tr><td>Natural language</td><td><code>contorium ask "…"</code></td><td><code>ask_project</code></td></tr>
      <tr><td>Project history</td><td><code>contorium history</code></td><td><code>get_project_history</code></td></tr>
      <tr><td>Decisions</td><td><code>contorium decisions</code></td><td><code>get_decisions</code></td></tr>
      <tr><td>Health</td><td><code>contorium health</code></td><td><code>get_cognitive_health</code></td></tr>
    </tbody>
  </table>
</section>

<section style="margin-top:40px">
  <h2>What happens automatically</h2>
  <ul>
    <li>MCP spawns when you open Codex / Claude / Cursor (after one-time setup)</li>
    <li><code>.contora/</code> is created or merged on first use</li>
    <li>New AI chats can prompt to inject project context (Y/n)</li>
    <li>Dashboard shows Cognitive State in the terminal</li>
  </ul>
</section>

<p class="docs-footer-note">
  Architecture / CIL spec:
  <a href="https://github.com/ContoriumLabs/contorium/tree/main/docs" target="_blank" rel="noopener noreferrer">GitHub docs</a>
</p>
"""


def slug_for_href(href: str) -> str:
    if href.startswith("http") or href.startswith("#") or href.startswith("../"):
        return href
    base = href.split("#")[0].lstrip("./")
    anchor = href[len(href.split("#")[0]) :] if "#" in href else ""
    if base in SLUG_MAP:
        return SLUG_MAP[base] + anchor
    if base.endswith(".md"):
        stem = base[:-3].lower().replace("_", "-").replace(".", "-")
        return stem + ".html" + anchor
    return href


def rewrite_links(text: str) -> str:
    def repl_md(m: re.Match) -> str:
        return f"]({slug_for_href(m.group(1))})"

    text = re.sub(r"\]\((\./[^)]+)\)", repl_md, text)
    return text


def render_sidebar(active: str) -> str:
    parts: list[str] = []
    for group, items in NAV:
        parts.append(f'<div class="docs-sidebar-group"><p class="docs-sidebar-title">{group}</p><ul class="docs-nav">')
        for label, href in items:
            cls = ' class="is-active"' if href == active else ""
            parts.append(f'<li><a href="{href}"{cls}>{label}</a></li>')
        parts.append("</ul></div>")
    return "\n".join(parts)


def breadcrumb(active: str, label: str | None = None) -> str:
    if active == "index.html":
        return ""
    title = label or active.replace(".html", "").replace("-", " ").title()
    return f'<nav class="docs-breadcrumb" aria-label="Breadcrumb"><a href="index.html">Docs</a> / {title}</nav>'


def md_to_html(body: str) -> str:
    body = rewrite_links(body)
    return markdown.markdown(
        body,
        extensions=["tables", "fenced_code", "nl2br", "sane_lists"],
        output_format="html5",
    )


def page(title: str, description: str, active: str, content: str, crumb: str | None = None) -> str:
    return HEADER.format(
        title=title,
        description=description,
        sidebar=render_sidebar(active),
        breadcrumb=breadcrumb(active, crumb),
        content=content,
    )


def main() -> None:
    titles = {
        "getting-started.html": ("Quick start", "Ask your project with Contorium — CIL, IDE, MCP, or CLI."),
        "install.html": ("Install & use", "Install, use, and uninstall Contorium."),
        "ide-extension.html": ("IDE extension", "Ask Contorium, Cortex panels, and IDE workflow."),
        "mcp.html": ("MCP server", "Connect @contorium/mcp — ask_project and CIL tools for AI agents."),
        "cli.html": ("CLI", "contorium ask, health, transfer, and capture from the terminal."),
        "dashboard.html": ("Runtime dashboard", "Cognitive State terminal UI — shortcuts and daily use."),
    }

    for md_name, html_name in SLUG_MAP.items():
        md_path = DOCS / md_name
        if not md_path.exists():
            print(f"skip missing {md_name}")
            continue
        src = md_path.read_text(encoding="utf-8")
        html_body = md_to_html(src)
        t, desc = titles.get(html_name, (html_name, "Contorium user guide"))
        out = page(t, desc, html_name, html_body, t)
        (DOCS / html_name).write_text(out, encoding="utf-8")
        print(f"built {html_name}")

    hub = page(
        "User guide",
        "Contorium user guide — install, MCP, CLI, IDE extension, and dashboard.",
        "index.html",
        HUB_CONTENT,
    )
    (DOCS / "index.html").write_text(hub, encoding="utf-8")
    print("built index.html")

    for orphan_html in [
        "pil-runtime.html",
        "project-intelligence-layer.html",
        "cognitive-dimensions.html",
        "contorium-language-spec.html",
    ]:
        path = DOCS / orphan_html
        if path.exists():
            path.unlink()
            print(f"removed {orphan_html}")


if __name__ == "__main__":
    main()
