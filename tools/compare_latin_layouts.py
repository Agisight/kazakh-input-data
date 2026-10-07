#!/usr/bin/env python3
"""Estimate long-press events under seven hypothetical lexicon models."""

import csv
import hashlib
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEXICON = ROOT / "data/kk-Latn/lexicon/lexicon.tsv"
HIDDEN = {
    "QWERTY3 (26)": "äğıñöşūü",
    "27 letters": "äıñöūwx",
    "29 letters": "äöşūü",
    "30 letters": "äöūü",
    "31 letters": "äöū",
}
MODELS = ("Uniform", "Zipf 0.8", "Zipf 1.0", "Zipf 1.2", "Exp 10", "Exp 20", "Exp 40")


def estimate():
    groups = defaultdict(list)
    with LEXICON.open(encoding="utf-8") as source:
        for row in csv.DictReader(source, delimiter="\t"):
            groups[int(row["weight"])].append(row["token"])

    weighted = {model: Counter() for model in MODELS}
    first_rank = 1
    minimum_cost = min(groups)
    total_letters = 0
    for cost, words in sorted(groups.items()):
        counts = Counter(char for word in words for char in word if char.isalpha())
        total_letters += sum(counts.values())
        last_rank = first_rank + len(words) - 1
        weights = {"Uniform": 1.0}
        for exponent in (0.8, 1.0, 1.2):
            # All words tied on cost receive the same average rank weight.
            weights[f"Zipf {exponent}"] = sum(
                rank ** -exponent for rank in range(first_rank, last_rank + 1)
            ) / len(words)
        for half_life in (10, 20, 40):
            weights[f"Exp {half_life}"] = 2 ** (-(cost - minimum_cost) / half_life)
        for model, weight in weights.items():
            for letter, count in counts.items():
                weighted[model][letter] += count * weight
        first_rank = last_rank + 1

    shares = {
        model: {letter: count / sum(counts.values()) for letter, count in counts.items()}
        for model, counts in weighted.items()
    }
    holds = {
        name: {
            model: 1000 * sum(shares[model].get(letter, 0) for letter in hidden)
            for model in MODELS
        }
        for name, hidden in HIDDEN.items()
    }
    return first_rank - 1, total_letters, holds


def main():
    words, letters, holds = estimate()
    print(f"Source: {LEXICON.relative_to(ROOT)}")
    print(f"SHA-256: {hashlib.sha256(LEXICON.read_bytes()).hexdigest()}")
    print(f"{words:,} word entries; {letters:,} letter events")
    print("Hypothetical holds per 1,000 letters; one hold per hidden letter; no autocomplete.")
    print("| Variant | " + " | ".join(MODELS) + " |")
    print("| --- | " + " | ".join("---:" for _ in MODELS) + " |")
    for name, results in holds.items():
        print(f"| {name} | " + " | ".join(f"{results[model]:.1f}" for model in MODELS) + " |")


if __name__ == "__main__":
    main()
