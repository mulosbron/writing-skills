# Writing Skills (Yazarlık & Kurgu Skilleri)

Makale, akademik metin, blog, metin yazarlığı, ortak belge yazımı, Türkçe/İngilizce/Çince doğallaştırma (`unslop` CLI dahil) ve editoryal düzeltme skillerini; **creative-writing-skills** (yaratıcı yazarlık zanaatı, simülasyonlar, stil ve hafıza yönetimi) ve **story-skills** (Markdown hikâye İncili, süreklilik denetimi, olay örgüsü, revizyon ve yayıncılık) yetenekleriyle birleştiren **54 skill** ve **10 kurgu ajanından** oluşan kapsamlı yazarlık paketi.

## Install

```bash
cp -r writing-skills/ my-project/.agents/
```

`AGENTS.md` dosyasını okuyan ajanlar (Antigravity, Claude Code, Codex, Gemini CLI, Cursor, Windsurf) işe uygun iş akışını (Düz Yazı vs. Kurgu/Roman) seçer ve `skills/<skill>/SKILL.md` dosyalarını yükler.

## İçerik Özeti

- **Düz Yazı, İnsansılaştırma & Editörlük (18 skill)**: `scientific-writing`, `blog-writing-guide`, `crossframe-essay`, `data-storytelling`, `content-writer-assistant`, `copywriting`, `doc-coauthoring`, `wiki-page-writer`, `beautiful-prose`, `llm-writing`, `avoid-ai-writing`, `unslop`, `turkce-humanizer`, `english-humanizer`, `humanize-chinese`, `copy-editing`, `professional-proofreader`, `wordbuilding`
- **Yaratıcı Yazarlık İş Akışı & Zanaat (12 skill)**: `creative-writing-muse`, `story-workflow`, `project-setup`, `story-planning`, `story-memory`, `creative-writing-craft`, `creative-research`, `character-sim`, `reader-sim`, `story-review`, `writing-principles`, `writing-staffing`
- **Kurgu Mühendisliği, Hikâye İncili & Yayıncılık (24 skill)**: `story-init`, `premise-workshop`, `worldbuilding`, `character-management`, `plot-structure`, `theme-craft`, `voice-style`, `genre-craft`, `scene-craft`, `chapter-writing`, `discovery-drafting`, `verse-craft`, `interactive-fiction`, `research`, `revision-continuity`, `line-editing`, `reader-panel`, `feedback-triage`, `editorial-review`, `series-continuity`, `adaptation`, `story-maintenance`, `submission`, `publishing`
- **Kurgu Alt-Ajanları (`agents/`, 10 tanım)**: `brainstormer`, `character-sim`, `continuity-checker`, `creative-researcher`, `critic`, `muse`, `outliner`, `reader-sim`, `style-creator`, `writer`
- **GitHub Şablonları (`templates/github/`)**: `draft-next-chapter.yml`, `review-copy.yml`, `story-checks.yml`, `ISSUE_TEMPLATE/manuscript-note.yml`

Tam skill listesi ve kullanım akışı için [AGENTS.md](AGENTS.md) dosyasına bakın.

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
