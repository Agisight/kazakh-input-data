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
assert "STATIC_SYMBOLS" in t
assert "'symbols-1'" in t and "'symbols-2'" in t
assert "mode.textContent='123'" in t
assert "layer='symbols-1';render()" in t
assert "layer==='symbols-1'?'symbols-2':'symbols-1'" in t
for ch in ("ә","і","ң","ғ","ү","ұ","қ","ө","һ","ä","ğ","ı","ñ","ö","ş","ū","ü"): assert ch in t
assert p.stat().st_size > 5_000_000
print(f"✓ Preview v5 smoke test passed: {p} ({p.stat().st_size:,} bytes)")
