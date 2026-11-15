# Writing Skills Orchestration Guide

This package includes **52 bundled skills**, **2 external companion skill pointers** (`turkce-humanizer`, `english-humanizer`), and **10 fiction sub-agents (`agents/`)** for **scientific/academic writing, blogs, essays, copywriting, collaborative docs, multilingual humanization** (`TR`/`EN`/`ZH`), as well as **long-form fiction, novels, short stories, verse, continuity tracking, and publishing**.

Choose one of the two primary workflows below based on the task.

---

## Workflow A: Articles, Academic Papers, Copy, and Non-Fiction Prose

Chain skills sequentially for long-form pieces; for shorter pieces you can skip stage 2 or combine stages 3 and 4.

1. **Planning and First Draft (Drafting)**
   - Scientific / Academic: `scientific-writing`
   - Blog / Standard Articles: `blog-writing-guide`
   - Critical Essays: `crossframe-essay`
   - General Long-Form Content: `content-writer-assistant`
   - Conversion Marketing Copy (Landing Pages & Emails): `copywriting`
   - Collaborative Specs / PRDs / Proposals / RFCs: `doc-coauthoring`
   - Data Storytelling: `data-storytelling`
   - Technical / Encyclopedic Wiki Pages: `wiki-page-writer`
2. **Style and Flow (Styling)**
   - Literary polish and rhythm: `beautiful-prose`
   - Reader-focused word choice free of LLM clichés: `llm-writing`
3. **Humanization and AI-Pattern Removal (Humanizing)**
   - English text: `avoid-ai-writing`, or install external [`blader/humanizer`](https://github.com/blader/humanizer) (`skills/english-humanizer/SKILL.md`)
   - Turkish text: install external [`bushrabeg/turkce-humanizer`](https://github.com/bushrabeg/turkce-humanizer) (`skills/turkce-humanizer/SKILL.md`)
   - Chinese text: `humanize-chinese`
   - Deterministic CLI post-processing: `unslop`
4. **Editorial Review and Final Pass (Editing & Proofreading)**
   - Structure, flow, and consistency: `copy-editing`
   - Spelling, grammar, and punctuation: `professional-proofreader`

---

## Workflow B: Fiction, Short Stories, and Novels (Creative Writing + Story Bible)

Depending on project needs, combine the **Muse / Craft workflow** (`creative-writing-*`, `story-*`) with the **Markdown Story Bible / CLI continuity workflow** (`story-init`, `story-maintenance`, `revision-continuity`, etc.):

1. **Setup and Premise Development**
   - Project & style initialization: `project-setup` (`kb/` and style sheets) or `story-init` (YAML frontmatter `story.md` / Story Bible)
   - Premise & ideation: `premise-workshop`, `creative-writing-muse`, `story-planning`
   - Worldbuilding & research: `worldbuilding` (setting, magic/tech, cultures, calendars, naming), `wordbuilding` (interactive/game universes), `creative-research`, `research`
2. **Structure, Character, and Drafting**
   - Plot, theme, and voice: `plot-structure`, `theme-craft`, `character-management`, `character-sim`, `voice-style`
   - Scene & chapter execution: `story-workflow`, `creative-writing-craft`, `discovery-drafting`, `scene-craft`, `chapter-writing`, `verse-craft`, `interactive-fiction`, `genre-craft`
   - Memory & continuity: `story-memory`, `series-continuity`, `story-maintenance`
3. **Reader Simulation, Critique, Revision, and Publishing**
   - Reader & editorial feedback: `story-review`, `reader-sim`, `reader-panel`, `editorial-review`, `feedback-triage`, `writing-staffing`
   - Line & continuity revision: `line-editing`, `revision-continuity`, `writing-principles`
   - Adaptation, submission & release: `adaptation`, `submission`, `publishing`

Fiction sub-agent roles (`agents/`): `muse`, `brainstormer`, `outliner`, `writer`, `style-creator`, `critic`, `continuity-checker`, `character-sim`, `reader-sim`, `creative-researcher`.

---

## Skill Inventory (52 Bundled + 2 External Pointers)

### Prose, Humanization & Editorial (16 Bundled + 2 External)
| Skill | Path | Purpose |
|---|---|---|
| `scientific-writing` | `skills/scientific-writing/SKILL.md` | Scientific and academic papers, citations, and objective prose. |
| `blog-writing-guide` | `skills/blog-writing-guide/SKILL.md` | Engaging blog posts and well-structured web articles. |
| `crossframe-essay` | `skills/crossframe-essay/SKILL.md` | Argument-driven critical insight and long-form essay drafting. |
| `data-storytelling` | `skills/data-storytelling/SKILL.md` | Turning statistics and analysis into persuasive narratives. |
| `content-writer-assistant` | `skills/content-writer-assistant/SKILL.md` | Collaborative research, outlining, section feedback, and voice preservation. |
| `copywriting` | `skills/copywriting/SKILL.md` | Conversion-focused landing page and email copy with strict no-fabrication rules. |
| `doc-coauthoring` | `skills/doc-coauthoring/SKILL.md` | 3-stage collaborative document drafting (context, refinement, reader testing). |
| `wiki-page-writer` | `skills/wiki-page-writer/SKILL.md` | Neutral, encyclopedic reference and wiki pages. |
| `beautiful-prose` | `skills/beautiful-prose/SKILL.md` | Literary cadence, clarity, and expressive prose craft. |
| `llm-writing` | `skills/llm-writing/SKILL.md` | Deliberate word choice and reader-grounded phrasing without AI clichés. |
| `avoid-ai-writing` | `skills/avoid-ai-writing/SKILL.md` | Stripping synthetic AI patterns from English drafts. |
| `unslop` | `skills/unslop/SKILL.md` | Deterministic CLI post-processing (`unslop`) to clean AI patterns before publishing. |
| `turkce-humanizer` | `skills/turkce-humanizer/SKILL.md` | External pointer -> install/clone [`bushrabeg/turkce-humanizer`](https://github.com/bushrabeg/turkce-humanizer) if missing locally. |
| `english-humanizer` | `skills/english-humanizer/SKILL.md` | External pointer -> install/clone [`blader/humanizer`](https://github.com/blader/humanizer) if missing locally. |
| `humanize-chinese` | `skills/humanize-chinese/SKILL.md` | AI-pattern detection, naturalization, and academic AIGC reduction in Chinese text. |
| `copy-editing` | `skills/copy-editing/SKILL.md` | Paragraph flow, structural coherence, and editorial tightening. |
| `professional-proofreader` | `skills/professional-proofreader/SKILL.md` | Final spelling, grammar, and punctuation inspection. |
| `wordbuilding` | `skills/wordbuilding/SKILL.md` | Worldbuilding methodology for games and interactive universes. |

### Creative Writing Workflow & Craft (12)
| Skill | Path | Purpose |
|---|---|---|
| `creative-writing-muse` | `skills/creative-writing-muse/SKILL.md` | Primary creative partner for ideation, drafting, and revision. |
| `story-workflow` | `skills/story-workflow/SKILL.md` | Intent parsing, drafting, critique, and approval loop orchestration. |
| `project-setup` | `skills/project-setup/SKILL.md` | Initial setup for story projects, `kb/` memory, and style files. |
| `story-planning` | `skills/story-planning/SKILL.md` | Brainstorming, creative direction, and story architecture. |
| `story-memory` | `skills/story-memory/SKILL.md` | Fact extraction, knowledge-base layout, and continuity logging. |
| `creative-writing-craft` | `skills/creative-writing-craft/SKILL.md` | Prose modes, scene mechanics, style analysis, and genre craft. |
| `creative-research` | `skills/creative-research/SKILL.md` | Historical, cultural, and domain-grounded fiction research. |
| `character-sim` | `skills/character-sim/SKILL.md` | Roleplay and dialogue simulation anchored to character voice and knowledge. |
| `reader-sim` | `skills/reader-sim/SKILL.md` | First-time reader reaction simulation across chapters and beats. |
| `story-review` | `skills/story-review/SKILL.md` | Developmental, line, prose critique, and continuity diagnostics. |
| `writing-principles` | `skills/writing-principles/SKILL.md` | Core craft principles, anti-patterns, and failure-mode checks. |
| `writing-staffing` | `skills/writing-staffing/SKILL.md` | Producer vs. reviewer sub-agent staffing and delegation guide. |

### Fiction Engineering, Story Bible & Publishing (24)
| Skill | Path | Purpose |
|---|---|---|
| `story-init` | `skills/story-init/SKILL.md` | Initializing Markdown + YAML frontmatter Story Bible projects. |
| `premise-workshop` | `skills/premise-workshop/SKILL.md` | Premise testing, format selection, and logline refinement. |
| `worldbuilding` | `skills/worldbuilding/SKILL.md` | Setting, magic/tech systems, cultures, calendars, and naming languages. |
| `character-management` | `skills/character-management/SKILL.md` | Character sheets, relationships, arcs, and state tracking. |
| `plot-structure` | `skills/plot-structure/SKILL.md` | Plotting, MICE threads, short fiction structure, and pacing. |
| `theme-craft` | `skills/theme-craft/SKILL.md` | Controlling idea, lie/truth arcs, and thematic antagonist design. |
| `voice-style` | `skills/voice-style/SKILL.md` | Style sheets, voice fingerprints, and prose consistency checks. |
| `genre-craft` | `skills/genre-craft/SKILL.md` | Genre conventions (mystery clues, serials, genre promises). |
| `scene-craft` | `skills/scene-craft/SKILL.md` | Scene goals, conflict, turning points, and transitions. |
| `chapter-writing` | `skills/chapter-writing/SKILL.md` | Turning scene outlines into full chapter drafts. |
| `discovery-drafting` | `skills/discovery-drafting/SKILL.md` | Exploratory (pantsing) drafting and kernel reconciliation. |
| `verse-craft` | `skills/verse-craft/SKILL.md` | Poetry, meter/scansion, rhyme schemes, and lyric craft. |
| `interactive-fiction` | `skills/interactive-fiction/SKILL.md` | Branching narrative and choice architecture design. |
| `research` | `skills/research/SKILL.md` | Real-world verification notes linked to story chapters. |
| `revision-continuity` | `skills/revision-continuity/SKILL.md` | Dead-character, timeline, and setup/payoff continuity auditing. |
| `line-editing` | `skills/line-editing/SKILL.md` | Sentence rhythm, dialogue cadence, and line-level tightening. |
| `reader-panel` | `skills/reader-panel/SKILL.md` | Multi-persona beta-reader feedback panels and reporting. |
| `feedback-triage` | `skills/feedback-triage/SKILL.md` | Classifying reader/editor notes into actionable revision plans. |
| `editorial-review` | `skills/editorial-review/SKILL.md` | Permissions, collaboration workflows, and editorial rounds. |
| `series-continuity` | `skills/series-continuity/SKILL.md` | Multi-book series bible and cross-volume continuity management. |
| `adaptation` | `skills/adaptation/SKILL.md` | Translation, audiobook, comics/screenplay, and format adaptation. |
| `story-maintenance` | `skills/story-maintenance/SKILL.md` | Story CLI validation, index repair, export, and plot diagrams. |
| `submission` | `skills/submission/SKILL.md` | Query letters, blurbs, comp titles, and market/agent submissions. |
| `publishing` | `skills/publishing/SKILL.md` | Indie production, metadata, accessibility, and rights checklists. |

## Boundaries

- **External companion skills (`turkce-humanizer`, `english-humanizer`):** Do not treat the pointer files as full rulesets. When the user needs Turkish or English humanization from those skills, check whether they are installed locally; if not, install or clone from `https://github.com/bushrabeg/turkce-humanizer` or `https://github.com/blader/humanizer` first.
- Match the target project's language and conventions; never inject uncanonical inventions into an existing Story Bible (`kb/` or `story.md`).
- Never silently alter canon decisions in finalized (`final`) chapters without author confirmation.
