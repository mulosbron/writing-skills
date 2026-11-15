---
name: turkce-humanizer
description: Removes AI-generated writing signatures from Turkish text and injects natural Turkish prose rhythm where the register allows. Triggered by phrases like "Türkçeleştir", "AI kokusunu at", "bu Türkçe metni doğallaştır", "humanize turkish", or when given AI-sounding Turkish prose.
---

# Turkish Humanizer (`turkce-humanizer`)

This skill operates in two phases. **Phase 1** strips AI-generated structural and stylistic signatures unconditionally across every text. **Phase 2** injects human Turkish prose rhythm conditionally according to the document's register.

The goal is not merely "evading AI detectors"—it is restoring authentic human breath and Turkish syntax to sterile prose, strictly bounded by genre register (for example, a KVKK legal contract should not become colloquial, while an essay or newspaper column should breathe naturally).

## Structure Preservation (Core Principle)

**Do not alter the document's structural skeleton.** This rule applies before Phase 1 and Phase 2:

- Keep bullet and numbered lists as lists (never collapse into prose paragraphs).
- Preserve heading hierarchy (`H1`, `H2`, `H3`).
- Keep Markdown tables as tables.
- Keep blockquotes and code blocks intact.
- Leave template/form fields and instruction boxes untouched.

Only edit phrasing at the sentence and paragraph level unless the user explicitly asks to restructure the document.

## Register Diagnosis

Classify the text into one of five registers before editing:

| Register | Example Text Types | Phase 2 Application |
|---|---|---|
| **Legal-Administrative** | Contracts, KVKK notices, regulations, statutory drafts | None (Phase 1 only). |
| **Academic-Institutional** | Theses, research papers, official/corporate reports | Restricted (sentence-length variance and self-correction only). |
| **Analytical-Journalistic** | News reports, op-ed analysis, briefings, think-tank reports | Full application, excluding colloquial discourse markers. |
| **Essay-Blog** | Essays, columns, blog posts, long-form social posts | Full application (all Phase 2 signals). |
| **Literary-Creative** | Novels, short stories, narrative nonfiction | Full application plus sensory detail and tense fluidity. |

**Confirmation rule:** If the user did not specify the register upfront, state your diagnosis and proposed Phase 2 actions and confirm before proceeding; if specified ("this is a blog post", "academic paper"), skip confirmation and apply directly.

## Phase 1 — Stripping AI Signatures (Unconditional)

Phase 1 has **dominant signals** (the five primary phenotypes of AI-written Turkish—3+ in a passage indicate heavy AI authorship) and **secondary supporting signals**.

### Dominant Signals (Five Primary Phenotypes)

#### Signal 1 — Punctuation Inflation (English Punctuation Calques)

Turkish punctuation under TDK rules is deliberately sparse compared to English. AI imports English punctuation habits verbatim:

- **1a. Em-dash inflation (`—`).** Per TDK rules, the long dash (`—`) is reserved strictly for dialogue lines; parenthetical asides use tight hyphens (`-dört inekle birkaç koyun-`) or commas.
  - Threshold: `1+` mid-sentence em-dashes.
- **1b. Semicolon abuse (`;`).** TDK limits semicolons to grouping comma-separated series, separating complex coordinate clauses containing commas, or marking emphasis after a long subject—not linking arbitrary ideas (`"; aynı zamanda..."`).
  - Threshold: `2+` semicolons per paragraph.
- **1c. Inline colon explanations (`:`).** Use colons at the end of sentences introducing lists/examples or dialogue, not English-style inline `"X: Y"` definitions.
  - Threshold: `2+` inline colons per paragraph.
- **1d. Merging the conjunction `ki`.** AI writes `"bu ki,"`, `"şu ki,"`, `"durum şu ki"`. Conjunction `ki` is always separate except fixed lexicalized words (*belki, çünkü, mademki, meğerki, oysaki, sanki, hâlbuki*).
- **1e. Slash-separated alternatives.** Replace `"kullanıcı/müşteri/istemci"` or `"hızlı/verimli/etkili"` with natural Turkish `"kullanıcı, müşteri veya istemci"`.
  - Threshold: `2+` slash chains.

**Repair:** Replace mid-sentence em-dashes with commas or split sentences; split semicolon splices into separate sentences; keep colons only where TDK permits; separate conjunction `ki`; convert slash chains into `"A, B veya C"`.

#### Signal 2 — Sentence Monotony (Low Burstiness)

Human writing mixes short punchy lines with longer analytical sentences. AI Turkish clusters uniformly around 18–25 words with zero short breaks.

- Threshold: low sentence-length variance AND average length `22+` words, or zero sentences under 5 words.

**Repair:** Split the longest sentences and introduce natural short beats (`"Bitti."`, `"Kalakaldı."`, `"Yani bir kaza."`) where meaning pauses.

#### Signal 3 — Template Repetition

- **3a. `"-mektedir/-maktadır"` epidemic.** `4+` verbs ending in `-mektedir/-maktadır` in a single paragraph signals robotic prose (natural Turkish academic prose keeps it around 20–25% mixed with past/present tenses).
- **3b. Bureaucratic connector stacking.** Overuse of `"Bu bağlamda,"`, `"söz konusu,"`, `"öte yandan,"`, `"bunun yanı sıra,"`, `"bu doğrultuda,"`, `"bu çerçevede"` (`3+` across a short text).
- **3c. Hollow AI closers.** `"Kritik bir rol oynamaktadır,"`, `"hayati bir önem taşımaktadır,"`, `"önemli bir rol üstlenmektedir,"`, `"vazgeçilmez bir hale gelmiştir"` (`2+` occurrences, especially at paragraph ends).

**Repair:** Vary tenses and active voice; swap bureaucratic connectors for direct logical links (`"Ama,"`, `"Çünkü,"`, `"Nitekim"`); delete empty closing sentences so paragraphs end on substance.

#### Signal 4 — `"Sadece X Değil, Aynı Zamanda Y"` Family

Direct calque of English *"It's not just X, it's Y"* (`"Yalnızca X söz konusu değildir; Y de..."`, `"X olmakla birlikte, Y niteliğini de taşımaktadır"`, `"X'in ötesinde, Y boyutu..."`, `"Salt X değil; bir Y meselesi"`).

- Threshold: `1+` occurrence.

**Repair:** Break into two sentences with the real logical link, rewrite as natural `"hem X hem Y"`, or cut the artificial contrast.

#### Signal 5 — Empty Praise + Empty Closures

- **5a. Evaluative adjective clusters:** `"eşsiz,"`, `"benzersiz,"`, `"paha biçilmez,"`, `"zengin bir mozaik,"`, `"çok boyutlu,"`, `"hayati,"`, `"kritik,"`, `"adeta bir zaman kapsülü,"`, `"vazgeçilmez bir ritüel"` (`2+` per paragraph).
- **5b. Summary filler endings:** Every paragraph ends with an evaluative platitude instead of new information.

**Repair:** Delete empty adjectives and leave bare nouns or concrete examples; remove filler closing lines.

### Secondary Signals (Supporting Indicators)

- **Signal 6 — `"Adeta"` / `"Sanki"` dependency:** Replace vague similes (`"adeta bir zaman kapsülü gibi"`) with concrete examples or delete.
- **Signal 7 — Forced triads (`A, B ve C`):** Collapse redundant three-item lists (`"hız, kapsayıcılık ve sürdürülebilirlik"`) to the single most specific term if items lack distinct meaning.
- **Signal 8 — Absence of inverted word order (`devrik cümle`):** Natural Turkish occasionally places the verb earlier for emphasis; LLMs almost strictly stay SOV. Introduce natural inversion sparingly where cadence calls for it.
- **Signal 9 — Register drift:** Avoid mixing bureaucratic/technical diction (`"yapay zekâ teknolojileri"`) with sudden poetic clichés (`"adeta bir zaman kapsülü"`) in the same paragraph.
- **Signal 10 — Missing concrete anchors:** Follow abstract claims with real dates, names, or facts—ask the user if missing, never fabricate specific examples.
- **Signal 11 — Passive voice dependency:** Prefer active subjects over impersonal passives (`"yapılmaktadır, edilmektedir, kılınmaktadır"`).
- **Signal 12 — English emphasis fillers:** Strip calqued intensifiers that add zero meaning in Turkish (`"tam da"`, `"tam anlamıyla"`, `"gerçekten de"`, `"aslında da"`, `"kesinlikle"`, `"esasen"`, `"nihayetinde"`, `"bir bakıma"`, `"gerçek anlamda"` — threshold `2+`). Express emphasis through word order and short beats instead.
- **Signal 13 — Synonym rotation ("elegant variation"):** Unlike English, rotating labels for the same referent in one Turkish paragraph (`"kullanıcı / müşteri / istemci"`, `"firma / şirket / kuruluş"`, `"vatandaş / birey / kişi"`) creates ambiguity. Pick one term and repeat it for clarity.
- **Signal 14 — Fragment dependency:** Complete colon-led sentence fragments (`"Üç seçenek: A, B, C."` -> `"Üç seçenek var: A, B, C."`, `"Sonuç şu: ..."` -> full predicate).

## Phase 2 — Injecting Human Rhythm (Conditional by Register)

Apply **only if missing** and **permitted by the target register**:

- **Signal 15 — Sentence length bursts** (*Academic-Institutional+*): Insert natural 1–3 word beats (`"Bitti dedim."`, `"Kalakaldı."`) at genuine pauses.
- **Signal 16 — Conversational/natural connectors** (*Analytical-Journalistic+*): Use `"Ama,"`, `"Zaten,"`, `"Oysa,"`, `"Ne var ki,"`, `"Meğer,"`, `"Nitekim,"`, `"Hem de"` instead of bureaucratic padding (plus colloquial particles like `"yani"`, `"valla"` only in *Literary-Creative* when voice allows).
- **Signal 17 — Rhetorical questions** (*Essay-Blog+*): Invite the reader into inquiry (`"Peki bu doğru mu?"`, `"Ne yapabilirsin ki?"`) rather than purely declarative lecturing.
- **Signal 18 — Self-correction and reformulation** (*Academic-Institutional+*): Genuine thinking shows revision (`"Ya da hayır, şöyle demek daha doğru olur"`, or parenthetical `"(daha doğrusu ...)"`).
- **Signal 19 — Concrete sensory detail** (*Literary-Creative*): Anchor descriptions in smell, sound, touch, and physical texture rather than abstract visuals.
- **Signal 20 — Fluid tense shifts** (*Literary-Creative*): Allow natural transitions between narrative past, present interiority, and gnomic present instead of locking onto one tense mechanically.
- **Signal 21 — Embedded dialogue traces** (*Literary-Creative*): Let character voices surface inside narrative reflection.
- **Signal 22 — First-person plural (`biz`)** (*Academic-Institutional+*, analytical prose only): Engage the reader as co-thinker (`"Sanıyoruz,"`, `"görüyoruz,"`, `"belirttiğimiz gibi"` — classical Turkish academic prose tradition as in Ortaylı or Keyder) rather than hiding behind passive `-mektedir`.

## Long-Document Behavior (`3+` Paragraphs)

Follow a scan-before-edit maker/checker flow:
1. **Scan** paragraph by paragraph and count dominant signals per paragraph.
2. **Classify** paragraphs: High AI-signature (`3+`), Medium (`1–2`), Clean (`0`, leave untouched).
3. **Report summary** with counts, paragraph IDs, diagnosed register, and proposed Phase 2 scope.
4. **Offer execution mode**: full pass at once, block-by-block with check-ins, or high-signature paragraphs only.
5. **Apply and annotate** what changed per paragraph.

## Output Format (Mandatory)

Unless the user explicitly requests only the rewritten text, every pass includes:
1. **Detection Report**: Exact dominant and secondary signals found with sentence/paragraph locations.
2. **Signal Density Metric**: Signals per 100 words before vs. after (e.g., `8.4 -> 1.2 signals/100 words`), or raw signal counts when under 200 words.
3. **Repaired Version**: Full revised Turkish text with Phase 1 (+ approved Phase 2) applied.
4. **Editorial Notes**: Signals preserved intentionally for author voice, register constraints applied, Phase 2 injections used, and clean aspects worth recognizing.

## Boundaries and Ethics

- **Structural, not synonym-swapping:** Never run blind word-replacement; fix sentence architecture and punctuation logic.
- **Natural Turkish first:** Authenticity and clarity come first; detector scores are incidental and never guaranteed.
- **Respect deliberate authorial style:** Preserve intentional stylistic choices (e.g., Ayfer Tunç-style double dots `..`, Tanpınar-style classical conjunctions, Bıçakçı-style literary semicolons, or deliberate rhythmic repetition/fragments) whenever specified or clearly intentional.
- **Reduce density in formal prose:** In heavy academic prose, lower `-mektedir` frequency to natural ~20–25% levels rather than stripping it completely.
- **Preserve factual content:** Never alter facts, claims, or invent concrete examples; rephrase structure or ask the user when concrete anchors are missing.
- **Preserve layout:** Never alter lists, headings, tables, code blocks, or document structure.

## References

Turkish punctuation and spelling follow TDK Orthography Guidelines (`tdk.gov.tr/kategori/icerik/yazim-kurallari`). Natural rhythm and academic voice signals draw on stylometric analysis of established Turkish authors (Ahmet Hamdi Tanpınar, Ayfer Tunç, Barış Bıçakçı, Ahmet Ümit, Ortaylı, Keyder, Aksoy, Karpat), quantitative defect density inspired by ASD-STE100, and architecture inspired by `harshaneel/humanize` and `makotofalcon/humanizer-ja`.

---

**Version:** v2.1
