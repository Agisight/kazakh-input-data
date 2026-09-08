#!/usr/bin/env python3
import sys
from pathlib import Path
p=Path(sys.argv[1]); t=p.read_text(encoding="utf-8")
assert "<!doctype html>" in t.lower()
assert "__LAYOUT__" not in t and "__DATA__" not in t
assert "Kazakh Arabic input preview" in t
for key in ('"lexicon":','"bigrams":','"trigrams":','"emoji":'): assert key in t
assert p.stat().st_size > 1_000_000
print(f"✓ Preview smoke test passed: {p} ({p.stat().st_size:,} bytes)")
