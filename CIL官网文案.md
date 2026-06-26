# Contorium 官网优化文案（CIL 核心版）

> **版本：** v4.0 · CIL-first  
> **对照站点：** https://www.contorium.dev/（当前为 PIL 叙事）  
> **目标：** 从「存储层介绍」升级为「可对话的项目认知系统」——用户第一眼理解 *Ask your project*，技术读者仍能看到 PIL 地基  
> **语言：** 正文为可直接上站的英文；各节附中文说明与替换理由

---

## 一、定位升级摘要

| 维度 | 当前官网（PIL 版） | 新版（CIL 版） |
|------|-------------------|----------------|
| 第一眼 | AI Project Intelligence Layer | **Cognitive Interaction Layer — Ask your project** |
| 核心动词 | Preserve / Transfer | **Ask · Explore · Capture · Transfer** |
| 用户感知 | 像数据库 / 状态层 | 像 **项目认知接口** — 能问、能查、能续接 |
| PIL 角色 | 首页主角 | **底层事实存储**（Solution 下半段 / 独立小节） |
| MCP 角色 | Install MCP Runtime | **CIL 的 Agent 入口**（ask_project 等） |
| 类比句 | Like Git for project cognition | **Git for facts. CIL for questions.** |

**一句话定位（对内）：**

> Contorium = 本地 PIL（存什么）+ CIL v3（怎么问、怎么讲、怎么交接）+ 可选 AI 解释层。

**一句话定位（对外 Hero）：**

> Ask your project anything — and pick up where you left off across every AI coding tool.

---

## 二、SEO / Meta

```html
<title>Contorium — Cognitive Interaction Layer for AI Coding</title>

<meta name="description" content="Contorium CIL lets you ask your project what happened, why decisions were made, and what to do next — with persistent intelligence across Cursor, Claude Code, Codex, Gemini CLI, and VS Code. Local-first. MCP-ready." />
```

**中文说明：** 标题把 CIL 写进品牌检索词；description 用问句能力做差异化，而非只讲 layer 概念。

---

## 三、导航（Nav）

| 链接文案 | 锚点 | 说明 |
|----------|------|------|
| CIL | `#cil` | 原 `#pil`，改 ID 与文案 |
| Problem | `#problem` | 保留 |
| Solution | `#solution` | 保留，内容改为 CIL+PIL 双层 |
| Architecture | `#architecture` | 保留，图改为 Kernel 优先 |
| Install | `#install` | 保留 |
| Docs | `docs/` | 保留 |
| GitHub | 外链 | 保留 |
| **Ask CIL**（CTA 按钮，可选） | `#install` | 替代纯 Install，更贴近 CIL 叙事 |

---

## 四、全站区块文案（可直接替换）

---

### §1 Hero（首页首屏）

**Eyebrow**

```text
Cognitive Interaction Layer
```

**H1**

```text
Ask your project — across every AI tool
```

**Lead**

```text
Contorium is a local Cognitive Interaction Layer (CIL) built on a persistent Project Intelligence Layer (PIL).

Ask what happened, why a decision was made, or what the project is trying to become — then switch between Cursor, Claude Code, Codex, Gemini CLI, and VS Code without re-explaining your architecture.
```

**Flow line**

```text
Ask → Explore → Capture → Transfer
```

**Tagline（blockquote）**

```text
Git stores code history. Contorium stores project intelligence — and CIL lets you talk to it.
```

**CTA 按钮**

```text
Get Started · View Docs · Install MCP
```

**Tools line**

```text
Works with Cursor · Claude Code · Codex · Gemini CLI · VS Code · MCP agents
```

**Scroll**

```text
Scroll ↓
```

---

#### Hero 对比面板（Compare Panel）

**Header**

```text
Without CIL          With Contorium
```

**左侧（Before）**

```text
Stateless session

"What was the auth decision again?"
"Why did we add MCP?"
"Summarize this project from scratch…"
Context reset — starting over.
```

**右侧（After）**

```text
CIL connected

ask_project → decision rationale retrieved
.contora/ loaded — story & handoff ready
Continue without re-explaining ✓
```

**中文说明：** 对比面板从「有没有 PIL」改为「能不能问项目」——更贴近 CIL 价值。

---

### §2 Problem — `#problem`

**Title**

```text
AI coding tools forget your project
```

**Lead**

```text
Modern AI assistants are powerful — but every new session starts from zero. Chat history is not project intelligence.
```

**Cards**

| 图标建议 | 标题 | 正文 |
|----------|------|------|
| ↺ | **Re-explain architecture** | You re-describe modules, conventions, and structure — every session, every tool switch. |
| ⇄ | **Re-discover decisions** | Why you chose JWT, why MCP exists, what tradeoffs you accepted — gone when the chat ends. |
| ◎ | **Broken continuity** | Cursor → Claude → Codex breaks the thread. You lose persistence, not capability. |

**Closer**

```text
You are not missing intelligence. You are missing a way to <strong>ask your project</strong> — and carry the answer forward.
```

---

### §3 Solution — `#solution`

**Title**

```text
Contorium gives your project a voice
```

**Lead**

```text
<strong>CIL (Cognitive Interaction Layer)</strong> is how you and AI agents explore project understanding.
<strong>PIL (Project Intelligence Layer)</strong> is where that understanding lives — structured, local, and durable.
```

**Chain**

```text
Ask → Explore → Capture → Transfer
```

**双栏布局**

#### 左栏 · What CIL answers

**Panel title**

```text
What you can ask
```

**List**

```text
What happened this week?          → Project History
Why was this decision made?     → Decision Center
What should I focus on next?    → Next Actions (suggestions only)
What is this project about?     → Story · Essence · DNA
What was the state on a date?   → Time Travel (Snapshot)
Everything about MCP / auth?    → Knowledge Graph
Is project cognition healthy?   → Cognitive Health
```

**Note**

```text
CIL suggests and explains. It never executes tasks for you.
```

#### 右栏 · Where PIL stores it

**Panel title**

```text
Where intelligence lives
```

**Terminal block**

```text
.contora/
  state.json · handoff.json
  intent/ · timeline/ · graph/
  cognitive-events/
  intelligence/ · governance/
  events/
```

**Note**

```text
Local-first — deterministic facts, no cloud account required.
```

---

### §4 CIL Core — `#cil`（原 `#pil` 区块升级）

**Title**

```text
Cognitive Interaction Layer (CIL)
```

**Lead**

```text
CIL routes natural-language questions through a Cognitive Kernel — reading structured facts from PIL, never guessing from chat memory.
```

**双栏**

#### Query Router → Kernel

**Panel title**

```text
How a question flows
```

**Steps**

```text
1. You or an agent asks          → ask_project / contorium ask
2. Query Router picks engines    → History · Decision · State · Graph
3. Cognitive Kernel assembles    → facts from .contora/
4. Formatter returns narrative   → markdown-ready for AI or human
```

#### CIL capability groups

**Panel title**

```text
CIL surfaces
```

**List**

```text
Query      — ask_project · get_next_actions · get_suggested_questions
History    — get_recent_events · get_project_history · get_module_history
Decisions  — get_decisions · get_decision_graph
Narrative  — get_project_story · get_project_essence · get_project_dna
Explore    — get_entity_knowledge · get_blast_radius · get_evolution_journey
Health     — get_cognitive_health · get_snapshot (time travel)
Transfer   — transfer_project (context · intelligence · story · essence · handoff)
```

**Footnote**

```text
MCP exposes CIL to agents. CLI and IDE expose the same kernel through Ask, History, and Decision Center panels.
```

---

### §5 PIL Foundation — `#pil`（降为支撑层，可选折叠或短节）

**Title**

```text
Project Intelligence Layer (PIL)
```

**Lead**

```text
Under CIL sits PIL — deterministic, local storage. PIL records facts. It does not answer questions by itself.
```

**Core Objects**

```text
STATE    — what exists now
INTENT   — what the project is trying to achieve
DECISION — what was decided
WHY      — why it was decided
```

**Intelligence Dimensions**

```text
TIMELINE   — how it evolved
IMPACT     — what it affects
CONFIDENCE — reliability of records
EVOLUTION  — structural changes over time
PROVENANCE — origin of knowledge
```

**One-liner**

```text
Capture → Structure → Preserve → Retrieve → Transfer
```

---

### §6 Architecture — `#architecture`

**Title**

```text
Architecture
```

**Lead**

```text
One Cognitive Kernel. Three peer runtimes. One local intelligence store.
```

**Diagram 文案（自上而下）**

```text
Query Layer          ask_project · contorium ask · Ask Contorium…
        ↓
Query Router
        ↓
Cognitive Kernel (CIL v3)
        ↓
Event · Decision · State · Graph · Action engines
        ↓
IDE  ·  MCP  ·  CLI  ·  Dashboard
        ↓
@contora/state-core  (PIL + CIL + optional AI)
        ↓
.contora/
```

**Caption**

```text
PIL stores facts. CIL interprets them. Optional AI Layer polishes explanations — facts stay rule-based.
```

---

### §7 Three Runtimes — `#runtimes`

**Title**

```text
Three peer runtimes
```

**Lead**

```text
Same CIL kernel everywhere — capture in the IDE, ask via MCP, audit in the terminal.
```

| Runtime | Lead | Bullets |
|---------|------|---------|
| **IDE Runtime** | Ask and capture while you code. | Ask Contorium… · Project History · Decision Center · Focus & decision capture · Project visualization |
| **MCP Runtime** | CIL for AI agents. | ask_project · get_project_story · transfer_project · capture_focus / note / decision · Cognitive Health |
| **CLI Runtime** | CIL + PIL in the terminal. | contorium ask · health · dna · questions · inspect_* · transfer_* · Cognitive State dashboard |

---

### §8 How it works — `#how`

**Title**

```text
How it works
```

**Lead**

```text
From first question to captured decision — one loop in your project folder.
```

**Steps（6 步）**

| # | 标题 | 正文 |
|---|------|------|
| 1 | **Connect a runtime** | IDE, MCP, or CLI attaches to your workspace. |
| 2 | **CIL syncs from `.contora/`** | Cognitive Kernel loads structured project facts. |
| 3 | **Ask or inspect** | You or an agent queries history, decisions, health, or story. |
| 4 | **Work with full context** | AI continues with project understanding — not a blank chat. |
| 5 | **Capture what changed** | Focus, notes, and decisions flow back into PIL. |
| 6 | **Transfer to the next session** | Context, handoff, or full intelligence export — tool-agnostic. |

---

### §9 Transfer — `#transfer`

**Title**

```text
AI continuity without re-explaining
```

**Lead**

```text
CIL Transfer exports the right depth for the next session — across Cursor, Claude Code, Codex, and Gemini CLI.
```

**Modes**

| Mode | Subtitle | Tokens | 说明文案 |
|------|----------|--------|----------|
| **Transfer Context** | Quick continuation | ~300–800 | Resume a chat with essentials |
| **Transfer Intelligence** | Full project understanding | ~8000 | Deep handoff for new agent |
| **Transfer Handoff** | Runtime continuation | ~100–300 | Compact session bridge |
| **Transfer Story** *(可选第四卡)* | Narrative export | variable | Goal, events, decisions as one story |
| **Transfer Essence** *(可选)* | Compressed DNA | variable | Maximum signal, minimum tokens |

**Tagline**

```text
Cursor → Claude Code → Codex → Gemini CLI — same project, same understanding
```

---

### §10 CIL Features — `#features`（新节，可选）

**Title**

```text
Built for long-lived AI-assisted projects
```

**Lead**

```text
CIL v3 ships a consistent cognitive toolkit across CLI, MCP, and IDE.
```

**Feature grid（2×4 或 3×3）**

```text
Project History      — unified timeline of cognitive events
Decision Center      — ADR-style records with Why, risk, alternatives
Time Travel          — snapshot replay for any date
Knowledge Graph      — everything related to an entity (MCP, auth, module…)
Cognitive Health     — missing WHY, stale decisions, conflict warnings
Project Story        — goal + journey narrative for onboarding
Project DNA          — identity fingerprint for agent handoff
Suggested Questions  — onboarding prompts when .contora/ is new
Evolution Journey    — how the project grew over time
Blast Radius         — impact explorer for modules and files
```

---

### §11 Value — `#value`

**Title**

```text
Why developers use Contorium
```

**Items**

```text
Ask your project instead of re-explaining it
Maintain continuity across AI coding tools
Preserve decision reasoning — not just code diffs
Share one consistent project story with every agent
Build long-lived, multi-tool AI-assisted codebases
```

---

### §12 Not a… — `#not-a`

**Title**

```text
Contorium is not
```

**List**

```text
Not an AI agent
Not a task automation system
Not a project manager
Not a code generator
Not an autonomous decision maker
```

**Closer**

```text
CIL suggests. PIL records. <strong>Neither executes work for you.</strong> They preserve and explain the intelligence behind your software.
```

---

### §13 Works with — `#tools`

**Title**

```text
Works with
```

**Pills**

```text
Cursor · Claude Code · OpenAI Codex · Gemini CLI · VS Code · Any MCP-compatible agent
```

---

### §14 Local-first — `#trust`

**Title**

```text
Local-first by design
```

**Lead**

```text
All intelligence stays in your workspace. No cloud account. No vendor lock-in. Optional LLM enhances explanations — core facts remain deterministic.
```

**Tree**

```text
.contora/
├── state.json
├── handoff.json
├── intent/
├── timeline/
├── graph/
├── cognitive-events/
├── intelligence/
├── config/llm.json      ← optional, no secrets in repo
└── events/
```

**Trust grid**

```text
Local-first · MIT License
No cloud dependency
No vendor lock-in
MCP-compatible ecosystem
Facts without LLM (AI Layer optional)
```

---

### §15 Install — `#install`

**Title**

```text
Install CIL via MCP
```

**Lead**

```text
One command connects your AI host to Contorium's Cognitive Kernel. Open your project folder, then ask.
```

**Optional bar**

```text
Optional    npm install -g @contorium/mcp    Faster cold start — or use npx @contorium/mcp directly
```

**Host cards**

**Codex**

```bash
codex mcp add contorium -- npx @contorium/mcp
```

**Claude Code**

```bash
claude mcp add --scope project contorium -- npx @contorium/mcp
```

**Cursor**

```text
Settings → MCP → Add server
Command: npx · Args: @contorium/mcp
Reload Window
```

**Try it（新增提示行）**

```text
After install, try: ask_project — "What is this project about?" or "What happened recently?"
```

**Also available**

| Label | Desc | Link |
|-------|------|------|
| IDE extension | VS Code / Cursor · Ask Contorium, History, Decisions | docs/ide-extension.html |
| CLI | contorium ask · health · transfer | docs/cli.html |
| Full install guide | All adapters · uninstall · scenarios | docs/install.html |

---

### §16 CTA — `#cta`

**Eyebrow**

```text
Ready to ask your project
```

**H2**

```text
A cognitive layer for AI-native development
```

**Lead**

```text
Stop restarting context in every chat. Contorium CIL turns project intelligence into questions you can ask — and answers you can carry to the next tool.
```

**Buttons**

```text
Get Started · View Docs · Install MCP
```

**Footnote**

```text
Local-first · MIT License · CIL v3 · Works with Cursor, Claude, Codex, Gemini CLI
```

---

### §17 Footer

**Oneliner**

```text
Contorium — Cognitive Interaction Layer on a local Project Intelligence Layer. Ask, explore, capture, and transfer project understanding across AI coding tools.
```

**Trust**

```text
Local-first · No telemetry · MCP-compatible ecosystem
```

**Links**

```text
Docs · Install · MCP · GitHub
```

**Copyright**

```text
© Contorium. MIT License.
```

---

## 五、首页信息架构（推荐顺序）

```text
Hero (CIL-first + compare panel)
  ↓
Problem
  ↓
Solution (CIL answers + PIL store)
  ↓
CIL Core (#cil)          ← 新主角
  ↓
PIL Foundation (#pil)    ← 缩短，支撑叙事
  ↓
Architecture (Kernel-first diagram)
  ↓
Three Runtimes
  ↓
How it works
  ↓
Transfer
  ↓
CIL Features (#features)  ← 可选新节
  ↓
Value
  ↓
Not a…
  ↓
Works with
  ↓
Local-first
  ↓
Install (Install CIL via MCP)
  ↓
CTA
```

---

## 六、与现版逐节差异对照

| 区块 | 现版关键词 | CIL 版关键词 |
|------|-----------|-------------|
| Hero eyebrow | Project Intelligence Layer | **Cognitive Interaction Layer** |
| Hero H1 | AI Project Intelligence Layer | **Ask your project — across every AI tool** |
| Hero flow | Capture → Structure → Preserve… | **Ask → Explore → Capture → Transfer** |
| Hero quote | Like Git for project cognition | **Git stores code history. CIL lets you talk to intelligence.** |
| Compare | Without PIL / Persistent intelligence | **Without CIL / CIL connected + ask_project** |
| Solution | What gets preserved | **What you can ask** + Where intelligence lives |
| §4 主节 | PIL 四对象五维度 | **CIL 问句路由 + Kernel + MCP 工具面** |
| Architecture | PIL Core 在上 | **Query Layer → Cognitive Kernel 在上** |
| MCP 定位 | Expose intelligence | **CIL for AI agents — ask_project first** |
| Install 标题 | Install MCP Runtime | **Install CIL via MCP** |
| CTA | A new layer for AI-native development | **A cognitive layer for AI-native development** |

---

## 七、Docs 站 Hub 同步建议（一句话）

**Docs 首页 lead 替换为：**

```text
Contorium is a local Cognitive Interaction Layer (CIL) on top of a Project Intelligence Layer (PIL). Use Ask, History, and Transfer to keep AI coding tools aligned — without re-explaining your project every session.
```

**Getting Started 首段：**

```text
Install MCP or CLI, open a project folder, then run contorium ask "What is this project about?" — CIL reads .contora/ and returns a structured answer.
```

---

## 八、术语表（站内统一用词）

| 术语 | 英文 | 站内用法 |
|------|------|----------|
| CIL | Cognitive Interaction Layer | 首屏与 MCP 节主语；全称首次出现写缩写 |
| PIL | Project Intelligence Layer | Solution 下半 / Architecture 底层；不说「PIL 回答问题」 |
| Kernel | Cognitive Kernel | Architecture、CIL Core 节 |
| Ask | ask_project / contorium ask | Hero、Install 试用提示 |
| 三动作 | Capture · Inspect · Transfer | PIL 运行时契约；CIL 侧强调 Ask/Explore |
| AI Layer | Optional explanation layer | Local-first 节一句带过；默认 off |
| 禁止表述 | agent / automation / executes | Not-a 节 + CIL footnote 重复强调 |

---

## 九、实施检查清单

- [ ] `index.html` Hero / Solution / `#pil` → `#cil` 区块替换
- [ ] Nav `#pil` → `#cil`；Compare panel 文案更新
- [ ] Architecture 示意图改为 Kernel-first
- [ ] Install 标题 +「Try it」提示行
- [ ] `<meta description>` 与 `<title>` 更新
- [ ] Footer oneliner 更新
- [ ] `docs/index.html` / `getting-started.html` hub 文案同步（第七节）
- [ ] `mcp/index.html` 首段改为 CIL Integration 叙事

---

*文档生成对照：contorium.dev 现网 + sessionrecall README / CIL.md / OVERVIEW.md / packages/mcp README v3。*
