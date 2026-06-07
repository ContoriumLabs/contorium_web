#!/usr/bin/env python3
"""Build static HTML docs from docs/*.md"""
from __future__ import annotations

import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

SLUG_MAP = {
    "INSTALL.md": "install.html",
    "IDE_EXTENSION.md": "ide-extension.html",
    "MCP.md": "mcp.html",
    "CLI.md": "cli.html",
    "DASHBOARD.md": "dashboard.html",
    "ARCHITECTURE_V3.md": "architecture-v3.html",
    "ARCHITECTURE_V2_2.md": "architecture-v2-2.html",
    "ARCHITECTURE_V2.md": "architecture-v2.html",
    "STATE_ENGINE.md": "state-engine.html",
    "ENGINEERING_CLOSURE.md": "engineering-closure.html",
    "RUNTIME.md": "runtime.html",
    "UPGRADE_PLAN_2.x.md": "upgrade-plan.html",
}

NAV = [
    ("Getting started", [
        ("Overview", "index.html"),
        ("Install & use", "install.html"),
    ]),
    ("Adapters", [
        ("IDE extension", "ide-extension.html"),
        ("MCP server", "mcp.html"),
        ("CLI", "cli.html"),
        ("Runtime dashboard", "dashboard.html"),
    ]),
    ("Architecture", [
        ("Architecture V3.1", "architecture-v3.html"),
        ("Architecture V2.2", "architecture-v2-2.html"),
        ("State engine", "state-engine.html"),
        ("Engineering closure", "engineering-closure.html"),
        ("Runtime package", "runtime.html"),
    ]),
    ("Reference", [
        ("Architecture V2 (legacy)", "architecture-v2.html"),
        ("Upgrade plan 2.x", "upgrade-plan.html"),
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
          <a href="../index.html#features">Product</a>
          <a href="../index.html#install">Install</a>
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
  <h1>Documentation</h1>
  <p>
    Install guides, adapter references, and architecture notes for Contorium — IDE extension,
    <code>@contorium/mcp</code>, and CLI over shared <code>.contora/</code> state.
  </p>
</div>

<section>
  <p class="docs-sidebar-title" style="padding-left:0">Quick paths</p>
  <div class="docs-card-grid">
    <a class="docs-card" href="install.html">
      <span class="docs-card-tag">Start here</span>
      <h3>Install &amp; use</h3>
      <p>Three peer adapters, command matrix, npm install, uninstall.</p>
    </a>
    <a class="docs-card" href="mcp.html">
      <span class="docs-card-tag">Agents</span>
      <h3>MCP server</h3>
      <p>Host auto-spawn, CHP v1 tools, semi-auto handoff injection.</p>
    </a>
    <a class="docs-card" href="cli.html">
      <span class="docs-card-tag">Terminal</span>
      <h3>CLI reference</h3>
      <p><code>handoff</code>, dashboard keys, export, debug commands.</p>
    </a>
    <a class="docs-card" href="dashboard.html">
      <span class="docs-card-tag">Runtime</span>
      <h3>Runtime dashboard</h3>
      <p>Passive line, Expanded view, keyboard shortcuts, artifacts.</p>
    </a>
    <a class="docs-card" href="ide-extension.html">
      <span class="docs-card-tag">IDE</span>
      <h3>IDE extension</h3>
      <p>VSIX install, sidebar, Copy AI-ready context, status bar.</p>
    </a>
    <a class="docs-card" href="architecture-v3.html">
      <span class="docs-card-tag">Architecture</span>
      <h3>Architecture V3.1</h3>
      <p>Cognitive graph, handoff.json, pipeline, MCP/CLI mirrors.</p>
    </a>
  </div>
</section>

<section style="margin-top:40px">
  <h2>What's automatic</h2>
  <ul>
    <li><strong>MCP spawn</strong> — Codex / Claude / Cursor starts <code>@contorium/mcp</code> after one-time config</li>
    <li><strong>Passive dashboard</strong> — compact <code>task | last | agent</code> line on bootstrap</li>
    <li><strong>Expanded view</strong> — press <strong>Space</strong> in the Contorium terminal</li>
    <li><strong>New chat inject</strong> — auto <code>[?]</code> prompt → Enter/i · n</li>
  </ul>
</section>

<p class="docs-footer-note">
  Markdown sources remain in <code>docs/*.md</code> for editing.
  Regenerate HTML with <code>python scripts/build-docs.py</code>.
  Interactive MCP wiring: <a href="../mcp/">mcp/</a>.
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
    text = text.replace("](../index.html)", "](../index.html)")
    text = text.replace("](../mcp/", "](../mcp/")
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
    md_ext = markdown.Markdown(extensions=["tables", "fenced_code", "nl2br", "sane_lists"])

    titles = {
        "install.html": ("Install & use", "Install, use, and uninstall Contorium — IDE, MCP, and CLI."),
        "ide-extension.html": ("IDE extension", "Contorium VS Code / Cursor extension guide."),
        "mcp.html": ("MCP server", "Contorium MCP server — @contorium/mcp setup and tools."),
        "cli.html": ("CLI", "Contorium CLI commands — handoff, dashboard, export."),
        "dashboard.html": ("Runtime dashboard", "CRBP runtime dashboard — Passive and Expanded views."),
        "architecture-v3.html": ("Architecture V3.1", "Contorium V3.1 project understanding layer."),
        "architecture-v2-2.html": ("Architecture V2.2", "Three peer adapters and dual-mode state."),
        "architecture-v2.html": ("Architecture V2", "Legacy v2.2 shared workspace state layer."),
        "state-engine.html": ("State engine", "Contorium L0–L5 state engine model."),
        "engineering-closure.html": ("Engineering closure", "Frozen V3.1 engineering boundary rules."),
        "runtime.html": ("Runtime package", "Contorium @contora/runtime package."),
        "upgrade-plan.html": ("Upgrade plan 2.x", "Contorium 2.x upgrade notes."),
    }

    for md_name, html_name in SLUG_MAP.items():
        md_path = DOCS / md_name
        if not md_path.exists():
            print(f"skip missing {md_name}")
            continue
        src = md_path.read_text(encoding="utf-8")
        html_body = md_to_html(src)
        t, desc = titles.get(html_name, (html_name, "Contorium documentation"))
        out = page(t, desc, html_name, html_body, t)
        (DOCS / html_name).write_text(out, encoding="utf-8")
        print(f"built {html_name}")

    hub = page(
        "Documentation",
        "Contorium documentation — install, MCP, CLI, dashboard, and architecture.",
        "index.html",
        HUB_CONTENT,
    )
    (DOCS / "index.html").write_text(hub, encoding="utf-8")
    print("built index.html")


if __name__ == "__main__":
    main()
