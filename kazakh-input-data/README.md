# Kazakh Input Data

Language data for Kazakh input methods and NLP across three scripts:

- `kk-Arab` — Arabic script
- `kk-Cyrl` — Cyrillic script
- `kk-Latn` — Latin script

[Қазақша](README.kk.md) · [Русский](README.ru.md)

## Dataset

| Script | Lexicon | Bigrams | Trigrams | Word→emoji |
| --- | ---: | ---: | ---: | ---: |
| `kk-Arab` | 58,632 | 60,000 | 61,160 | 25 |
| `kk-Cyrl` | 90,052 | 40,002 | 4,861 | 244 |
| `kk-Latn` | 45,073 | 7,384 | 982 | 244 |

All text exports are UTF-8.

## Structure

```text
data/
├── kk-Arab/
├── kk-Cyrl/
└── kk-Latn/
```

Each script directory contains:

```text
lexicon/
  lexicon.txt
  lexicon.tsv
  lexicon.jsonl

ngrams/
  bigrams.tsv
  trigrams.tsv

emoji/
  word_to_emoji.tsv
  emoji_inventory.tsv

hunspell/
  <language_tag>.dic

metadata/
  metadata.json
```

## Canonical formats

The TSV files are the recommended canonical interchange format.

`lexicon.tsv`

```text
token    weight    state_id
```

`bigrams.tsv`

```text
token1    token2    weight
```

`trigrams.tsv`

```text
token1    token2    token3    weight
```

`word_to_emoji.tsv`

```text
token    emoji    emoji_id    group_id    state_id
```

The integer `weight` values are preserved as source ranking/cost values. They
should not be treated as literal corpus frequencies or probabilities unless the
original weighting formula is recovered.

## Hunspell

A flat `.dic` export is included for each script.

A verified `.aff` file is not included yet. Without `.aff`, these are word-list
dictionaries rather than full Hunspell morphological dictionaries.

## Derived models

ARPA, KenLM and other compiled language-model artifacts are not stored as
canonical repository data. They can be generated later from the canonical data
when an appropriate probability-estimation method is available.

## Preview

The Arabic-script data currently has an interactive preview under
`preview/kk-Arab/`. Keyboard layout specifications remain in the separate
`Agisight/ios-system-keyboard` repository.
