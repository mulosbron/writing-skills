---
name: english-humanizer
description: External companion skill for removing AI-generated writing patterns from English prose based on Wikipedia's "Signs of AI writing". Upstream repository at https://github.com/blader/humanizer — install or clone from upstream if not already present locally.
---

# English Humanizer (External Upstream Skill)

This skill lives in an external repository and is **not bundled** directly inside `writing-skills`:

- **Upstream Repository:** https://github.com/blader/humanizer

## Agent Instructions (When Needed)

If `humanizer` (`blader/humanizer`) is not yet installed locally (e.g., inside `~/.agents/skills/humanizer` or your project's `.agents/skills/`), inform the user or install it directly from the upstream repository before applying it:

```bash
git clone https://github.com/blader/humanizer.git
# or install into your skills directory:
npx skills add blader/humanizer
```

Once fetched, follow the upstream `SKILL.md` for pattern detection and voice-preserving English rewrites.
