#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
signal_scanner.py — Turkish AI-signature density scanner.

Companion tool for the turkish-humanizer skill. Scans a Turkish text for
the dominant and secondary AI-writing signatures defined in SKILL.md
(Phase 1), reports their locations, and normalizes the total density to
"signals per 100 words".

Usage:
    python3 signal_scanner.py <file.md | -]  [--json]

    -       read stdin
    --json  machine-readable output

Exit code 0 always (this is a report tool, not a gate).
"""

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

# ---------------------------------------------------------------------------
# Signal definitions
# ---------------------------------------------------------------------------

DOMINANT = "dominant"
SECONDARY = "secondary"


def _w(pattern):
    """Word-boundary-wrapped pattern aware of Turkish letters."""
    return r"(?<![0-9A-Za-zÇĞİÖŞÜçğıöşü_])" + pattern + r"(?![0-9A-Za-zÇĞİÖŞÜçğıöşü])"


SIGNALS = [
    # ---- Dominant: punctuation inflation -------------------------------
    {
        "id": "1a",
        "name": "Em/en dash inside text (absolute ban)",
        "class": DOMINANT,
        "pattern": re.compile(r"[—―–]"),
    },
    {
        "id": "1b",
        "name": "Semicolon (absolute ban)",
        "class": DOMINANT,
        "pattern": re.compile(r";"),
    },
    {
        "id": "1c",
        "name": "In-sentence explanatory colon",
        "class": DOMINANT,
        "pattern": None,  # special-cased (needs heading/line-end exclusion)
    },
    {
        "id": "1d",
        "name": "Mistakenly fused 'ki' (şuki, oysaki written fused wrongly)",
        "class": DOMINANT,
        "pattern": re.compile(_w("şuk[iı]|buk[iı]|durumşuk[iı]"), re.IGNORECASE),
    },
    {
        "id": "1e",
        "name": "Slash separator (A/B/C lists)",
        "class": DOMINANT,
        "pattern": re.compile(_w(r"[\wÇĞİÖŞÜçğıöşü]+/[\wÇĞİÖŞÜçğıöşü]+")),
    },
    {
        "id": "1f",
        "name": "Comma before contrastive conjunction (ama/ancak/fakat/lakin/yalnız)",
        "class": DOMINANT,
        "pattern": re.compile(r",\s*" + _w("ama|ancak|fakat|lakin|yalnız(?![cç])")),
    },
    # ---- Dominant: -mektedir epidemic -----------------------------------
    {
        "id": "3a",
        "name": "-mektedir/-deckt overload (>=4 in one paragraph)",
        "class": DOMINANT,
        "pattern": None,  # special-cased per paragraph
    },
    # ---- Dominant: bureaucratic connective pile-up ----------------------
    {
        "id": "3b",
        "name": "Bureaucratic connective (bu bağlamda, söz konusu, öte yandan...)",
        "class": DOMINANT,
        "pattern": re.compile(
            _w("bu bağlamda|söz konusu|öte yandan|bunun yanı sıra|bu doğrultuda|bu çerçevede"),
            re.IGNORECASE,
        ),
    },
    # ---- Dominant: AI closing clichés -----------------------------------
    {
        "id": "3c",
        "name": "AI closing cliché (kritik bir rol, hayati bir önem...)",
        "class": DOMINANT,
        "pattern": re.compile(
            _w("kritik bir rol|hayati bir önem|önemli bir rol|vazgeçilmez bir hale|vazgeçilmez bir ritüel"),
            re.IGNORECASE,
        ),
    },
    # ---- Dominant: "not just X, but Y" family ---------------------------
    {
        "id": "4",
        "name": "'Sadece X değil, aynı zamanda Y' family",
        "class": DOMINANT,
        "pattern": re.compile(
            r"[Ss]adece[^.;!?:]{0,80}değil"
            r"|[Yy]alnızca[^.;!?:]{0,80}değil"
            r"|[Ss]alt[^.;!?:]{0,80}değil"
            r"|değil,\s*(?:yalnızca|sadece|sırf|aynı zamanda)"
            r"|aynı zamanda[,\s]"
            r"|(?:'?[ıi]n'??[ıiuü]?['’]?)?\s*ötesinde[^.;!?]{0,60}göz ardı edilmemel"
            r"|niteliğini de taşımaktadır",
        ),
    },
    # ---- Dominant: empty praise -----------------------------------------
    {
        "id": "5a",
        "name": "Empty evaluative adjective (eşsiz, benzersiz, paha biçilmez...)",
        "class": DOMINANT,
        "pattern": re.compile(
            _w("eşsiz|benzersiz|paha biçilmez|zengin bir mozaik|çok boyutlu|adeta|vazgeçilmez"),
            re.IGNORECASE,
        ),
    },
    # ---- Dominant: "şudur:" explanation pattern --------------------------
    {
        "id": "23",
        "name": "'X şudur: Y' explanation pattern",
        "class": DOMINANT,
        "pattern": re.compile(
            _w("(?:şudur|budur|söylenmesi gereken şudur)") + r"\s*:|beklemekte\s*:|gündemde\s*:",
            re.IGNORECASE,
        ),
    },
    # ---- Secondary -------------------------------------------------------
    {
        "id": "6",
        "name": "'Adeta/sanki' vagueness crutch",
        "class": SECONDARY,
        "pattern": re.compile(_w("adeta|sanki"), re.IGNORECASE),
    },
    {
        "id": "11",
        "name": "Passive-voice dependence (-ıl/-In/-nIldı participles, rough)",
        "class": SECONDARY,
        "pattern": re.compile(
            _w(r"[\wÇĞİÖŞÜçğıöşü]{4,}(?:ılmış|ilmiş|ulmuş|ülmüş|ıldı|ildi|uldu|üldü|ılmaktadır|ilmektedir)"),
            re.IGNORECASE,
        ),
    },
    {
        "id": "12",
        "name": "English-style filler intensifier (tam da, nihayetinde, bir bakıma...)",
        "class": SECONDARY,
        "pattern": re.compile(
            _w("tam da|tam anlamıyla|gerçekten de|aslında da|kesinlikle|esasen|nihayetinde"
               r"|bir bakıma|gerçek anlamda"),
            re.IGNORECASE,
        ),
    },
]

# Sentence-initial isolated contrastive conjunction (absolute ban 4) — special-cased.
ISOLATED_CONJ = re.compile(r"^\s*(Ama|Ancak|Fakat|Lakin|Yalnız(?![cç]))\b")

MEKTEKTOR = re.compile(r"m[ae]kted[ıi]r", re.IGNORECASE)  # -mektedir/-maktadır


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

WORD_RE = re.compile(r"[0-9A-Za-zÇĞİÖŞÜçğıöşü]+(?:'[a-z]+)?")


def words(text):
    return WORD_RE.findall(text)


def split_sentences(paragraph):
    """Split a paragraph into sentences on . ! ? … keeping it simple."""
    parts = re.split(r"(?<=[.!?…])\s+", paragraph.strip())
    return [p for p in parts if p.strip()]


def line_of(text, pos):
    return text.count("\n", 0, pos) + 1


# ---------------------------------------------------------------------------
# Scanner core
# ---------------------------------------------------------------------------

def scan(text):
    hits = []  # {signal, id, class, line, excerpt}
    lines = text.split("\n")

    # Special case 1c: in-sentence colons (skip headings and line-end colons)
    for i, ln in enumerate(lines, 1):
        if ln.lstrip().startswith("#"):
            continue
        for m in re.finditer(r":(?!\s*$)", ln):
            after = ln[m.end():m.end() + 1]
            if after and after != " ":
                continue  # like "18:30" — ignore digits directly after
            # colon followed by space and more text on the same line
            rest = ln[m.end():]
            if rest.strip():
                hits.append({"signal": "1c", "id": "1c", "class": DOMINANT,
                             "line": i, "excerpt": ln.strip()[:80]})

    # Special case 3a: -mektedir per paragraph
    paragraphs = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    for p in paragraphs:
        cnt = len(MEKTEKTOR.findall(p))
        if cnt >= 4:
            first_line = line_of(text, text.find(p.strip()[:40])) if p.strip() else 0
            hits.append({"signal": "3a", "id": "3a", "class": DOMINANT,
                         "line": first_line,
                         "excerpt": f"paragraph has {cnt} -mektedir verbs"})

    # Regex signals
    for sig in SIGNALS:
        if sig["pattern"] is None:
            continue
        for m in sig["pattern"].finditer(text):
            ln = line_of(text, m.start())
            excerpt = text[max(0, m.start() - 35):m.end() + 35].replace("\n", " ")
            hits.append({"signal": sig["id"], "id": sig["id"],
                         "class": sig["class"], "line": ln,
                         "excerpt": excerpt.strip()})

    # Absolute ban 4: conjunction-initial isolated sentence
    for i, ln in enumerate(lines, 1):
        for sent in split_sentences(ln):
            if ISOLATED_CONJ.match(sent):
                hits.append({"signal": "B4", "id": "B4", "class": DOMINANT,
                             "line": i, "excerpt": sent.strip()[:80]})

    # Signal 2: sentence monotony per paragraph
    for p in paragraphs:
        sents = split_sentences(p)
        if len(sents) < 4:
            continue
        lens = [len(words(s)) for s in sents]
        mean = sum(lens) / len(lens)
        var = sum((x - mean) ** 2 for x in lens) / len(lens)
        sd = var ** 0.5
        if mean >= 22 and mean > 0 and sd / mean < 0.30:
            first_line = line_of(text, text.find(p.strip()[:40]))
            hits.append({"signal": "2", "id": "2", "class": DOMINANT,
                         "line": first_line,
                         "excerpt": f"monotony: mean {mean:.1f} words, cv {sd/mean:.2f}"})
        elif len(lens) >= 5 and min(lens) >= 8:
            first_line = line_of(text, text.find(p.strip()[:40]))
            hits.append({"signal": "2", "id": "2", "class": DOMINANT,
                         "line": first_line,
                         "excerpt": f"no sentence under 8 words (min {min(lens)})"})

    return hits


def report(text, title=""):
    hits = scan(text)
    n_words = len(words(text))
    total = len(hits)
    dominant = sum(1 for h in hits if h["class"] == DOMINANT)
    density = (total / n_words * 100) if n_words else 0.0

    by_signal = {}
    for h in hits:
        by_signal.setdefault(h["id"], []).append(h)

    out = []
    out.append("=" * 64)
    out.append(f"TURKISH AI-SIGNATURE SCAN{(' — ' + title) if title else ''}")
    out.append("=" * 64)
    out.append(f"Words: {n_words}")
    out.append(f"Total signal hits: {total}  (dominant: {dominant}, secondary: {total - dominant})")
    out.append(f"Density: {density:.1f} signals / 100 words")
    if dominant >= 3:
        out.append("Verdict: HEAVILY AI-SIGNED (>=3 dominant signal types present)")
    elif dominant >= 1:
        out.append("Verdict: lightly signed — apply Phase 1 cleanups")
    else:
        out.append("Verdict: clean — no dominant signatures found")
    out.append("")
    out.append("Per signal:")
    for sid in sorted(by_signal, key=lambda s: [int(c) if c.isdigit() else 99 for c in re.findall(r"\d+", s)] or [99]):
        hs = by_signal[sid]
        cls = "D" if hs[0]["class"] == DOMINANT else "S"
        out.append(f"  [{cls}] signal {sid}: {len(hs)} hit(s)")
        for h in hs[:6]:
            out.append(f"        line {h['line']}: {h['excerpt']}")
        if len(hs) > 6:
            out.append(f"        ... and {len(hs) - 6} more")

    # dominant type count for the >=3 rule
    dom_types = len({h["id"] for h in hits if h["class"] == DOMINANT})
    out.append("")
    out.append(f"Dominant signal TYPES present: {dom_types} (threshold for 'heavy': 3)")
    out.append("=" * 64)
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="Turkish AI-signature density scanner")
    ap.add_argument("file", help="path to text/markdown file, or '-' for stdin")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of text")
    args = ap.parse_args()

    if args.file == "-":
        text = sys.stdin.read()
        title = "stdin"
    else:
        p = Path(args.file)
        text = p.read_text(encoding="utf-8")
        title = p.name

    if args.json:
        hits = scan(text)
        n_words = len(words(text))
        print(json.dumps({
            "file": title,
            "words": n_words,
            "total_hits": len(hits),
            "dominant_hits": sum(1 for h in hits if h["class"] == DOMINANT),
            "density_per_100_words": round(len(hits) / n_words * 100, 2) if n_words else 0,
            "hits": hits,
        }, ensure_ascii=False, indent=2))
    else:
        print(report(text, title))


if __name__ == "__main__":
    main()
