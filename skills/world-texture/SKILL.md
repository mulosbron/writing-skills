---
name: world-texture
description: Adds high-impact micro-worldbuilding texture to a town, region, or scene without writing an encyclopedia, auditing 10 lived-in details across voice/custom, physical memory, and living people/legend plus character education and lifespan lenses. Use when a setting feels empty, generic, or like a flat stage, when preparing a session location or chapter locale, or when asked for small worldbuilding details that make a place stand out immediately.
---

# World Texture

Deep lore encyclopedias rarely reach the table or page. You can make a town, region, or campaign stop feel lived-in right away by layering ten small, concrete details across three dimensions—and filtering what characters actually know through their education and lifespan.

Scoring, synergy checks, and Texture Card formatting live deterministically in `scripts/locale_texture.py`; your job is to fill the locale JSON from conversation or setting notes and craft evocative details grounded in the setting.

## When to Use Which Tool

Run commands from this skill's directory (`skills/world-texture/`):

| Situation | Command / Reference |
|---|---|
| Preparing a new town, tavern, region, or chapter locale | `python scripts/locale_texture.py template` to generate a blank JSON |
| Auditing or formatting a locale texture card | `python scripts/locale_texture.py audit locale.json --output card.md --json result.json` |
| Enforcing a minimum coverage score in CI or prep | `python scripts/locale_texture.py audit locale.json --min-score 70` |
| Previewing output on sample data ("Cinderport") | `python scripts/locale_texture.py audit assets/sample_locale.json` |
| Reviewing examples for each of the 10 details | Read `references/ten_details.md` |
| Macro 7-level structural worldbuilding audit | See `../wordbuilding/SKILL.md` (`world_levels.py`) |
| Managing Story Bible location & glossary Markdown files | See `../worldbuilding/SKILL.md` |

## The 10 Micro-Details (3 Layers)

1. **Voice & Custom** (`local_sayings`, `regional_superstitions`, `seasonal_festivals`):
   - **Local sayings / slogans:** Everyday greetings, oaths, or idioms hinting at local history (*"By the river's mercy"*, *"Ashes to bread"*).
   - **Regional superstitions:** Peculiar local taboos (*"Never whistle at night"*). Give them a testable `hook`—if players test the taboo, let something real happen.
   - **Seasonal festivals:** Even one passing mention (*"Preparing for the Coming of Dust"*) proves the town has traditions—and can turn sinister or celebratory on arrival.
2. **Physical Memory** (`famous_monuments`, `war_memorials`, `scarred_landscapes`, `unique_animals`):
   - **Famous monuments:** Colossal remnants or landmarks (twin watchtowers, a collapsing colossus) showing past ambition and scale.
   - **War memorials:** Carved stone names or rusted blades planted on a hillside honoring unseen generations before the protagonists arrived.
   - **Scarred landscapes:** Craters, scorched woods, glassed sand—the land itself remembers past magic or natural disasters.
   - **Unique everyday wildlife:** Non-Earth background fauna living ordinary lives (giant harbor shellfish instead of seagulls, six-legged pack beasts)—dropped naturally, never as a zoology lecture.
3. **Living People & Legend** (`rival_families`, `local_heroes`, `famous_orders`):
   - **Rival families:** Everyday feuds over fishing rights, lake borders, best bread, or city turf so the place moves on its own.
   - **Local heroes:** Regular people known locally (the blacksmith who slew a troll, the midwife who delivered the king, the sailor who swam home)—instant NPC hooks.
   - **Famous parties / knightly orders:** Companies whose names still carry weight in taverns and ballads (a company that broke a siege, or vanished except for one silent survivor).

## Two Calibration Lenses (Always Fill)

- **Education lens (`education_lens`):** Who actually knows the deeper history behind monuments, memorials, or orders? A scholar or wizard recognizes ancient names; a backwoods brawler only knows the local rumor.
- **Lifespan lens (`lifespan_lens`):** How long do local species live? Events from 150 years ago are ancient myth to a human and living memory to an elf or dwarf.

## Workflow

1. **Gather existing locale notes.** Pull whatever the user has already written for the town, region, or scene; leave uninvented slots as `absent` or `sketch` until filled.
2. **Populate the locale JSON.** Set `status` (`present`, `sketch`, `absent`, or `na`), write the concrete `detail`, and add an actionable `hook` where players or characters can test or pull on it.
3. **Run the audit.** Execute `scripts/locale_texture.py audit` to score all three layers, surface missing synergy pairings (such as sayings without superstitions, or superstitions without testable consequences), and generate a ready-to-use Locale Texture Card.
4. **Fill the weakest layer first.** Pick at most three missing details from the report's priority list so the locale pops immediately without bloating into lore homework.

## Tests

After modifying `scripts/locale_texture.py`, run:

```bash
python -m unittest tests/test_locale_texture.py
```
