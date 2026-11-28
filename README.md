# Writing Skills

A comprehensive writing and fiction craft suite containing **59 bundled skills**, **2 external companion humanizer pointers** (linking to upstream repositories), and **10 fiction agents** (`agents/`), combining prose drafting, copywriting, collaborative co-authoring, editorial proofreading, and multilingual AI-pattern removal with **creative-writing-skills** (craft, simulations, style, and memory management) and **story-skills** (Markdown story bible, continuity checking, plotting, revision, and publishing).

## Install

```bash
cp -r writing-skills/ my-project/.agents/
```

Agents that read `AGENTS.md` (Antigravity, Claude Code, Codex, Gemini CLI, Cursor, Windsurf) select the appropriate workflow (Non-Fiction & Prose vs. Fiction & Long-Form Narrative) and load `skills/<skill>/SKILL.md` on demand.

## External Companion Repositories (Not Bundled)

Two humanizer skills belong to separate upstream GitHub repositories. Their local `skills/*/SKILL.md` files act as lightweight pointers so coding agents automatically know to fetch them from upstream when needed:

| Skill | Upstream Repository | Install / Clone |
|---|---|---|
| `turkce-humanizer` | [`bushrabeg/turkce-humanizer`](https://github.com/bushrabeg/turkce-humanizer) | `git clone https://github.com/bushrabeg/turkce-humanizer.git` or `npx skills add bushrabeg/turkce-humanizer` |
| `english-humanizer` (`humanizer`) | [`blader/humanizer`](https://github.com/blader/humanizer) | `git clone https://github.com/blader/humanizer.git` or `npx skills add blader/humanizer` |

## Contents

- **Prose, Humanization & Editorial (17 bundled + 2 external links)**: `scientific-writing`, `blog-writing-guide`, `crossframe-essay`, `data-storytelling`, `content-writer-assistant`, `copywriting`, `doc-coauthoring`, `wiki-page-writer`, `beautiful-prose`, `llm-writing`, `avoid-ai-writing`, `unslop`, `humanize-chinese`, `copy-editing`, `professional-proofreader`, `wordbuilding` (with deterministic 7-level profiler), `world-texture` (with 10-detail Locale Texture Card auditor) *(plus external links: [`turkce-humanizer`](https://github.com/bushrabeg/turkce-humanizer), [`english-humanizer`](https://github.com/blader/humanizer))*
- **Business, Social & Video Content (6)**: `video-script-prep`, `x-twitter-viral-engine`, `limited-time-promo-generator`, `livestream-mega-guide`, `business-advisor-debate`, `thirty-day-constraint-solver`
- **Creative Writing Workflow & Craft (12 bundled)**: `creative-writing-muse`, `story-workflow`, `project-setup`, `story-planning`, `story-memory`, `creative-writing-craft`, `creative-research`, `character-sim`, `reader-sim`, `story-review`, `writing-principles`, `writing-staffing`
- **Fiction Engineering, Story Bible & Publishing (24 bundled)**: `story-init`, `premise-workshop`, `worldbuilding`, `character-management`, `plot-structure`, `theme-craft`, `voice-style`, `genre-craft`, `scene-craft`, `chapter-writing`, `discovery-drafting`, `verse-craft`, `interactive-fiction`, `research`, `revision-continuity`, `line-editing`, `reader-panel`, `feedback-triage`, `editorial-review`, `series-continuity`, `adaptation`, `story-maintenance`, `submission`, `publishing`
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
    └── <skill-name>/SKILL.md (53 bundled + 2 external pointers)
```
