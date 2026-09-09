#!/usr/bin/env python3
import sys
from pathlib import Path

p=Path(sys.argv[1])
t=p.read_text(encoding="utf-8")

assert "<!doctype html>" in t.lower()
assert "__LAYOUT__" not in t and "__MACOS_LAYOUT__" not in t and "__DATASETS__" not in t
assert "Kazakh input preview" in t
assert "const MACOS_LAYOUT=" in t
assert "kaz-latn-experimental.keylayout" in t
assert (p.parent / "keylayout" / "kaz-latn-experimental.keylayout").is_file()

for tag in ('"kk-Arab":','"kk-Cyrl":','"kk-Latn":'):
    assert tag in t

# Primary suggestion is tracked and Space accepts it for a partial prefix.
assert "primaryCandidate=null" in t
assert "primaryCandidate=items.length?items[0][0]:null" in t
assert "function spaceAction()" in t
assert "primaryCandidate.startsWith(partial)" in t
assert "suggest(primaryCandidate)" in t

# Both on-screen Space controls use the same action.
assert "sp.onclick=spaceAction" in t
assert "document.getElementById('addSpace').onclick=spaceAction" in t

# Physical keyboard Space accepts the highlighted completion too.
assert "editor.addEventListener('keydown'" in t
assert "if(e.key===' ')" in t
assert "e.preventDefault();spaceAction()" in t

# Keep v7 edge geometry.
assert "edge-row" in t
assert "margin-right:auto" in t
assert "margin-left:auto" in t
assert "mode-bottom" in t
assert "return-bottom" in t

# Keep number/symbol navigation.
assert "STATIC_SYMBOLS" in t
assert "mode.onclick=()=>setLayer('symbols-1')" in t
assert "mode.onclick=()=>setLayer('default')" in t

assert p.stat().st_size > 5_000_000
print(f"✓ Preview v8 smoke test passed: {p} ({p.stat().st_size:,} bytes)")
