---
name: turkce-humanizer
description: External companion skill for removing AI-generated writing patterns from Turkish prose and restoring natural Turkish rhythm. Upstream repository at https://github.com/bushrabeg/turkce-humanizer — install or clone from upstream if not already present locally.
---

# Turkish Humanizer (External Upstream Skill)

This skill lives in an external repository and is **not bundled** directly inside `writing-skills`:

- **Upstream Repository:** https://github.com/bushrabeg/turkce-humanizer

## Agent Instructions (When Needed)

If `turkce-humanizer` is not yet installed locally (e.g., inside `~/.agents/skills/turkce-humanizer` or your project's `.agents/skills/`), inform the user or install it directly from the upstream repository before applying it:

```bash
git clone https://github.com/bushrabeg/turkce-humanizer.git
# or install into your skills directory:
npx skills add bushrabeg/turkce-humanizer
```

Once fetched, follow the upstream `SKILL.md` (which is written in Turkish and enforces TDK punctuation, Turkish prose rhythm, and register-aware two-phase humanization).

## Bundled CLI Scanner (`scripts/signal_scanner.py`)

This repo bundles the companion Turkish AI-signature density scanner so you can audit Turkish text immediately (reports dominant/secondary AI signals and signals per 100 words):

```bash
python scripts/signal_scanner.py draft.md --json
```
