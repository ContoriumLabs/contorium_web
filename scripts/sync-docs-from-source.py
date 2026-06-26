#!/usr/bin/env python3
"""Sync docs from sessionrecall repo and adapt links for contorium.dev website."""
from __future__ import annotations

import re
from pathlib import Path

SOURCE_DOCS = Path(r"E:\sessionrecall\docs")
SOURCE_MCP_README = Path(r"E:\sessionrecall\packages\mcp\README.md")
TARGET_DOCS = Path(__file__).resolve().parent.parent / "docs" / "_source"
TARGET_MCP_README = Path(__file__).resolve().parent.parent / "mcp" / "README.md"

GITHUB_BASE = "https://github.com/ContoriumLabs/contorium/blob/main/docs"

# Architecture / historical docs — link to GitHub, not built as site pages
OFFSITE_DOCS = {
    "ARCHITECTURE_V3.md",
    "ARCHITECTURE_V3_CORE.md",
    "ARCHITECTURE_V2_2.md",
    "ARCHITECTURE_V2.md",
    "ENGINEERING_CLOSURE.md",
    "RUNTIME.md",
    "STATE_ENGINE.md",
    "UPGRADE_PLAN_2.x.md",
}

SYNC_FILES = [
    "OVERVIEW.md",
    "CIL.md",
    "SURFACES.md",
    "AI_LAYER.md",
    "PIL_RUNTIME.md",
    "INSTALL.md",
    "PROJECT_INTELLIGENCE_LAYER.md",
    "IDE_EXTENSION.md",
    "MCP.md",
    "CLI.md",
    "DASHBOARD.md",
    "CONTORIUM_LANGUAGE_SPEC.md",
    "COGNITIVE_DIMENSIONS.md",
]


def adapt_links(text: str) -> str:
    text = text.replace("[README](../README.md)", "[Home](../index.html)")
    text = text.replace("](../README.md)", "](../index.html)")
    text = re.sub(
        r"\[([^\]]+)\]\(\./README\.md\)",
        r"[\1](index.html)",
        text,
    )
    text = re.sub(
        r"\[([^\]]+)\]\(\.\./packages/mcp/README\.md\)",
        r"[\1](../mcp/README.md)",
        text,
    )

    def offsite(m: re.Match) -> str:
        label, path = m.group(1), m.group(2)
        name = Path(path.split("#")[0]).name
        if name in OFFSITE_DOCS:
            anchor = path[len(name) :] if "#" in path else ""
            return f"[{label}]({GITHUB_BASE}/{name}{anchor})"
        return m.group(0)

    text = re.sub(r"\[([^\]]+)\]\(\./([^)]+\.md[^)]*)\)", offsite, text)
    text = re.sub(
        r"\[([^\]]+)\]\(\.\./([^)]+\.md[^)]*)\)",
        lambda m: (
            f"[{m.group(1)}]({GITHUB_BASE}/{Path(m.group(2).split('#')[0]).name})"
            if Path(m.group(2).split("#")[0]).name in OFFSITE_DOCS
            else m.group(0)
        ),
        text,
    )

    text = re.sub(
        r"\[([^\]]+)\]\(\.\./commands/[^)]+\)",
        r"[\1](https://github.com/ContoriumLabs/contorium/blob/main/commands/setup-mcp-codex.md)",
        text,
    )
    text = re.sub(
        r"\[([^\]]+)\]\(\.\./\.mcp\.json\)",
        r"[\1](https://github.com/ContoriumLabs/contorium/blob/main/.mcp.json)",
        text,
    )
    text = re.sub(
        r"\[([^\]]+)\]\(\.\./\.codex-plugin/[^)]+\)",
        r"[\1](https://github.com/ContoriumLabs/contorium/blob/main/.codex-plugin/plugin.json)",
        text,
    )
    text = re.sub(
        r"\[([^\]]+)\]\(\.\./\.mcp\.claude\.json\)",
        r"[\1](https://github.com/ContoriumLabs/contorium/blob/main/.mcp.claude.json)",
        text,
    )

    if "manual-config-fallback" not in text:
        text = text.replace(
            "## Configuration templates",
            '<a id="manual-config-fallback"></a>\n\n## Configuration templates',
            1,
        )

    return text


def adapt_mcp_readme(text: str) -> str:
    text = adapt_links(text)
    replacements = [
        (r"\[docs/MCP\.md\]\(\.\./docs/MCP\.md\)", "[docs/mcp.html](../docs/mcp.html)"),
        (r"\[docs/INSTALL\.md\]\(\.\./docs/INSTALL\.md\)", "[docs/install.html](../docs/install.html)"),
        (r"\[docs/CLI\.md\]\(\.\./docs/CLI\.md\)", "[docs/cli.html](../docs/cli.html)"),
        (
            r"\[docs/ARCHITECTURE_V3\.md\]\(\.\./docs/ARCHITECTURE_V3\.md\)",
            f"[Architecture V3]({GITHUB_BASE}/ARCHITECTURE_V3.md)",
        ),
        (
            r"\[docs/PIL_RUNTIME\.md\]\(\.\./docs/PIL_RUNTIME\.md\)",
            f"[PIL Runtime]({GITHUB_BASE}/PIL_RUNTIME.md)",
        ),
        (
            r"\[docs/OVERVIEW\.md\]\(\.\./docs/OVERVIEW\.md\)",
            "[Overview](../docs/getting-started.html)",
        ),
        (
            r"\[Overview\]\(\.\./docs/OVERVIEW\.md\)",
            "[Overview](../docs/getting-started.html)",
        ),
        (
            r"\[docs/AI_LAYER\.md\]\(\.\./docs/AI_LAYER\.md\)",
            f"[AI Layer]({GITHUB_BASE}/AI_LAYER.md)",
        ),
        (
            r"\[Install \(three adapters\)\]\(\.\./docs/INSTALL\.md\)",
            "[Install (three adapters)](../docs/install.html)",
        ),
        (r"\[Full MCP guide\]\(\.\./docs/MCP\.md\)", "[Full MCP guide](../docs/mcp.html)"),
        (r"\[CLI guide\]\(\.\./docs/CLI\.md\)", "[CLI guide](../docs/cli.html)"),
        (
            r"\[Architecture\]\(\.\./docs/ARCHITECTURE_V3\.md\)",
            f"[Architecture]({GITHUB_BASE}/ARCHITECTURE_V3.md)",
        ),
    ]
    for pattern, repl in replacements:
        text = re.sub(pattern, repl, text)
    return text


def main() -> None:
    TARGET_DOCS.mkdir(parents=True, exist_ok=True)
    for name in SYNC_FILES:
        src = SOURCE_DOCS / name
        if not src.exists():
            print(f"skip missing source {src}")
            continue
        out = adapt_links(src.read_text(encoding="utf-8"))
        (TARGET_DOCS / name).write_text(out, encoding="utf-8")
        print(f"synced {name}")

    if SOURCE_MCP_README.exists():
        mcp = adapt_mcp_readme(SOURCE_MCP_README.read_text(encoding="utf-8"))
        TARGET_MCP_README.write_text(mcp, encoding="utf-8")
        print("synced mcp/README.md")


if __name__ == "__main__":
    main()
