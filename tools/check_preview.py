#!/usr/bin/env python3
import sys
from pathlib import Path

p=Path(sys.argv[1])
t=p.read_text(encoding="utf-8")

assert "<!doctype html>" in t.lower()
assert "__LAYOUT__" not in t and "__DATASETS__" not in t
assert "Kazakh input preview" in t

for tag in ('"kk-Arab":','"kk-Cyrl":','"kk-Latn":'):
    assert tag in t

# All three scripts must expose alphabet + numeric/symbol navigation.
assert "STATIC_SYMBOLS" in t
assert "'symbols-1'" in t and "'symbols-2'" in t
assert "mode.dataset.role='layer-mode'" in t
assert "mode.textContent='123'" in t
assert "mode.onclick=()=>setLayer('symbols-1')" in t
assert "mode.onclick=()=>setLayer('default')" in t
assert "setLayer(layer==='symbols-1'?'symbols-2':'symbols-1')" in t

# Shift/backspace/mode spacing.
assert "shift-key" in t
assert "backspace-key" in t
assert "mode-key" in t
assert "margin-right:12px" in t
assert "margin-left:12px" in t

# Latin uses distinct Turkic uppercase forms: i -> İ, ı -> I.
assert "['Ä','Ğ','I','Ñ','Ö','Ş','Ū','Ü']" in t
assert "['Q','W','E','R','T','Y','U','İ','O','P']" in t
assert "Turkic i/ı casing" in t

# Existing script-specific letters remain.
for ch in ("ә","і","ң","ғ","ү","ұ","қ","ө","һ","ä","ğ","ı","ñ","ö","ş","ū","ü"):
    assert ch in t

assert p.stat().st_size > 5_000_000
print(f"✓ Preview v6 smoke test passed: {p} ({p.stat().st_size:,} bytes)")
