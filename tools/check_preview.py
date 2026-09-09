#!/usr/bin/env python3
import sys
from pathlib import Path
p=Path(sys.argv[1]); t=p.read_text(encoding="utf-8")
assert "<!doctype html>" in t.lower()
assert "__LAYOUT__" not in t and "__DATASETS__" not in t
assert "Kazakh input preview" in t
for tag in ('"kk-Arab":','"kk-Cyrl":','"kk-Latn":'): assert tag in t
assert "Keyman Kazakh Basic" in t
assert "QWERTY + Kazakh letters" in t
for ch in ("ә","і","ң","ғ","ү","ұ","қ","ө","һ","ä","ğ","ı","ñ","ö","ş","ū","ü"): assert ch in t
assert "function initial(" in t
assert "items=initial(3)" in t
assert "entry.index===0?' primary'" in t
assert p.stat().st_size > 5_000_000
print(f"✓ Preview v4 smoke test passed: {p} ({p.stat().st_size:,} bytes)")
