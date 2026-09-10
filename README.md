# Kazakh Input Data

Language data for Kazakh input methods and NLP across three scripts:

- `kk-Arab` — Arabic script
- `kk-Cyrl` — Cyrillic script
- `kk-Latn` — Latin script

[Қазақша](README.kk.md) · [Русский](README.ru.md)

**[Live interactive demo](https://agisight.github.io/kazakh-input-data/)**

## Dataset

| Script | Lexicon | Bigrams | Trigrams | Word→emoji |
| --- | ---: | ---: | ---: | ---: |
| `kk-Arab` | 58,632 | 60,833 | 73,645 | 25 |
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

## Interactive preview

A live interactive demo is available at:

**https://agisight.github.io/kazakh-input-data/**

The preview is a reference implementation showing how the datasets in this
repository can work together with keyboard layouts in an input-method UI.

It currently demonstrates:

- script switching between `kk-Arab`, `kk-Cyrl` and `kk-Latn`;
- prefix completion from the lexicon;
- next-word prediction from bigrams;
- contextual prediction from trigrams;
- word-to-emoji suggestions;
- source ranking weights;
- interactive on-screen keyboards;
- Shift, Backspace, Space, number and symbol layers;
- long-press alternatives where the source keyboard layout defines them.

The highest-ranked suggestion is shown in the center. While an unfinished word
is being typed, pressing Space accepts the highlighted completion and inserts a
space. Next-word predictions are not accepted automatically by Space; they must
be selected explicitly.

### Keyboard layouts used by the demo

- **Arabic (`kk-Arab`)** — uses the Kazakh Arabic / Töte jazu layout from
  [`Agisight/ios-system-keyboard`](https://github.com/Agisight/ios-system-keyboard).
- **Cyrillic (`kk-Cyrl`)** — the preview keyboard is adapted from the Keyman
  **Kazakh Basic** touch layout.
- **Latin (`kk-Latn`)** — currently uses an experimental preview layout based on
  standard QWERTY with an additional row for Kazakh Latin letters.

The Latin layout is **not a finalized or standardized Kazakh Latin keyboard**.
Its alphabet, character set, casing and key placement require further research
and validation.

The preview is a demo of the language data and keyboard behavior, not a
production input method or a keyboard-layout standard.
