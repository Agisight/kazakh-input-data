#!/usr/bin/env python3
import sys
from pathlib import Path

p = Path(sys.argv[1])
t = p.read_text(encoding="utf-8")

assert "<!doctype html>" in t.lower()
assert "__LAYOUT__" not in t and "__DATASETS__" not in t
assert "Kazakh input preview" in t
for tag in ("kk-Arab", "kk-Cyrl", "kk-Latn"):
    assert f'"{tag}":' in t
assert 'id="clearAll"' in t
assert 'data-script="kk-Arab"' in t
assert 'data-script="kk-Cyrl"' in t
assert 'data-script="kk-Latn"' in t
assert p.stat().st_size > 5_000_000

print(f"✓ Multi-script preview smoke test passed: {p} ({p.stat().st_size:,} bytes)")
