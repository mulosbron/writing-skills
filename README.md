# Writing Skills

A comprehensive writing and fiction craft suite containing **54 skills** and **10 fiction agents** (`agents/`), combining prose drafting, copywriting, collaborative co-authoring, editorial proofreading, and multilingual AI-text humanization (`TR` / `EN` / `ZH` + `unslop` CLI) with **creative-writing-skills** (craft, simulations, style, and memory management) and **story-skills** (Markdown story bible, continuity checking, plotting, revision, and publishing).

## Install

```bash
cp -r writing-skills/ my-project/.agents/
```

Agents that read `AGENTS.md` (Antigravity, Claude Code, Codex, Gemini CLI, Cursor, Windsurf) select the appropriate workflow (Non-Fiction & Prose vs. Fiction & Long-Form Narrative) and load `skills/<skill>/SKILL.md` on demand.

## Contents

- **Prose, Humanization & Editorial (18 skills)**: `scientific-writing`, `blog-writing-guide`, `crossframe-essay`, `data-storytelling`, `content-writer-assistant`, `copywriting`, `doc-coauthoring`, `wiki-page-writer`, `beautiful-prose`, `llm-writing`, `avoid-ai-writing`, `unslop`, `turkce-humanizer`, `english-humanizer`, `humanize-chinese`, `copy-editing`, `professional-proofreader`, `wordbuilding`
- **Creative Writing Workflow & Craft (12 skills)**: `creative-writing-muse`, `story-workflow`, `project-setup`, `story-planning`, `story-memory`, `creative-writing-craft`, `creative-research`, `character-sim`, `reader-sim`, `story-review`, `writing-principles`, `writing-staffing`
- **Fiction Engineering, Story Bible & Publishing (24 skills)**: `story-init`, `premise-workshop`, `worldbuilding`, `character-management`, `plot-structure`, `theme-craft`, `voice-style`, `genre-craft`, `scene-craft`, `chapter-writing`, `discovery-drafting`, `verse-craft`, `interactive-fiction`, `research`, `revision-continuity`, `line-editing`, `reader-panel`, `feedback-triage`, `editorial-review`, `series-continuity`, `adaptation`, `story-maintenance`, `submission`, `publishing`
- **Fiction Sub-Agents (`agents/`, 10 definitions)**: `brainstormer`, `character-sim`, `continuity-checker`, `creative-researcher`, `critic`, `muse`, `outliner`, `reader-sim`, `style-creator`, `writer`
- **GitHub Templates (`templates/github/`)**: `draft-next-chapter.yml`, `review-copy.yml`, `story-checks.yml`, `ISSUE_TEMPLATE/manuscript-note.yml`

See [AGENTS.md](AGENTS.md) for the full skill matrix, orchestration workflows, and boundaries.

## Layout

```text
writing-skills/
├── .claude-plugin/plugin.json
├── .codex-plugin/plugin.json
├── AGENTS.md
├── CLAUDE.md
├── README.md
├── gemini-extension.json
├── plugin.json
├── agents/
│   └── *.md (10 fiction agents)
├── templates/
│   └── github/
└── skills/
    └── <skill-name>/SKILL.md (54 skills)
```
