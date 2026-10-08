#!/usr/bin/env python3
"""Estimate Cyrillic holds under seven lexicon-weight hypotheses, not corpus frequencies."""

import csv
import hashlib
import math
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEXICON = ROOT / "data/kk-Cyrl/lexicon/lexicon.tsv"
ALPHABET = set("аәбвгғдеёжзийкқлмнңоөпрстуұүфхһцчшщъыіьэюя")
HIDDEN = {
    "4 rows (40 letters)": "ёъ",
    "3 rows (ЙЦУКЕН)": "әғқңөұүһіёъ",
    "Compact (31 letters)": "ғёфхцчщъэюя",
}
MODELS = ("Uniform", "Zipf 0.8", "Zipf 1.0", "Zipf 1.2", "Exp 10", "Exp 20", "Exp 40")


def estimate():
    groups = defaultdict(lambda: {"entries": 0, "letters": Counter()})
    excluded = 0
    with LEXICON.open(encoding="utf-8") as source:
        for row in csv.DictReader(source, delimiter="\t"):
            word = unicodedata.normalize("NFC", row["token"]).lower()
            unknown = {char for char in word if char.isalpha() and char not in ALPHABET}
            if unknown:
                raise ValueError(f"Unsupported letters in {row['token']!r}: {unknown}")
            counts = Counter(char for char in word if char in ALPHABET)
            if not counts:
                excluded += 1
                continue
            # Case-equivalent source entries keep their individual weight and rank contribution.
            group = groups[int(row["weight"])]
            group["entries"] += 1
            group["letters"].update(counts)

    weighted = {model: Counter() for model in MODELS}
    first_rank = 1
    minimum_cost = min(groups)
    total_letters = 0
    for cost, group in sorted(groups.items()):
        entries, counts = group["entries"], group["letters"]
        total_letters += sum(counts.values())
        last_rank = first_rank + entries - 1
        weights = {"Uniform": 1.0}
        for exponent in (0.8, 1.0, 1.2):
            weights[f"Zipf {exponent}"] = math.fsum(
                rank ** -exponent for rank in range(first_rank, last_rank + 1)
            ) / entries
        for half_life in (10, 20, 40):
            weights[f"Exp {half_life}"] = 2 ** (-(cost - minimum_cost) / half_life)
        for model, weight in weights.items():
            for letter, count in counts.items():
                weighted[model][letter] += count * weight
        first_rank = last_rank + 1

    holds = {
        name: {
            model: 1000 * math.fsum(weighted[model][c] for c in hidden)
            / math.fsum(weighted[model].values())
            for model in MODELS
        }
        for name, hidden in HIDDEN.items()
    }
    return first_rank - 1, total_letters, excluded, holds


def main():
    entries, letters, excluded, holds = estimate()
    print(f"Source: {LEXICON.relative_to(ROOT)}")
    print(f"SHA-256: {hashlib.sha256(LEXICON.read_bytes()).hexdigest()}")
    print(f"{entries:,} retained entries; {letters:,} letter events; {excluded} entries without letters excluded")
    print("Hypothetical holds per 1,000 letters; one hold per hidden letter; no autocomplete.")
    print("| Variant | " + " | ".join(MODELS) + " |")
    print("| --- | " + " | ".join("---:" for _ in MODELS) + " |")
    for name, results in holds.items():
        print(f"| {name} | " + " | ".join(f"{results[model]:.1f}" for model in MODELS) + " |")


if __name__ == "__main__":
    main()
