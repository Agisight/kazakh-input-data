# Tools

The canonical repository data is stored as UTF-8 TXT/TSV/JSONL.

Useful derived artifacts can be generated from these files. ARPA/KenLM binaries
are intentionally not stored as canonical data.

Current extraction logic supports:

- compact FST lexicons
- bigram/trigram source tables
- word-to-emoji tables

Generated model binaries should remain derived artifacts rather than source data.

`python3 tools/compare_latin_layouts.py` reproduces the hypothetical Latin
long-press estimates documented in [the preview README](../preview/README.md#frequency-assumptions-and-comparison).
It reads the canonical lexicon and reports seven weight scenarios without
modifying the source data.
