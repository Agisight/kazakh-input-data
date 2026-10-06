#!/usr/bin/env python3
import sys
from pathlib import Path

p=Path(sys.argv[1])
t=p.read_text(encoding="utf-8")

assert "<!doctype html>" in t.lower()
assert "__LAYOUT__" not in t and "__MACOS_LAYOUT__" not in t and "__MACOS_LAYOUTS__" not in t and "__DATASETS__" not in t
assert "Kazakh input preview" in t
assert "const MACOS_LAYOUT=" in t
assert "const MACOS_LAYOUTS=" in t
assert '"geometry":"iso"' in t
assert '"geometry":"ansi"' in t
for filename in ("kaz-latn-iso-experimental.keylayout", "kaz-latn-ansi-experimental.keylayout"):
    assert filename in t
    assert (p.parent / "keylayout" / filename).is_file()

for tag in ('"kk-Arab":','"kk-Cyrl":','"kk-Latn":'):
    assert tag in t

# Primary suggestion is tracked and Space accepts it for a partial prefix.
assert "primaryCandidate=null" in t
assert "primaryCandidate=items.length?items[0][0]:null" in t
assert "function spaceAction()" in t
assert "primaryCandidate.startsWith(partial)" in t
assert "suggest(primaryCandidate)" in t

# Suggestions match typed prefixes case-insensitively while preserving
# the user's initial/all-caps style in the candidate.
assert "function matchTypedCase(w,p)" in t
assert "toLocaleLowerCase('kk')" in t
assert "toLocaleUpperCase('kk')" in t
assert "lower(w).startsWith(q)" in t
assert "matchTypedCase(w,p)" in t

# Completion-on-Space can be disabled without hiding suggestions.
assert 'id="spaceAutocomplete"' in t
assert 'Space autocomplete' in t
assert "spaceAutocomplete.checked&&partial&&primaryCandidate" in t

# Keep a visible caret without summoning the native touch keyboard.
assert "caret-color:var(--text)" in t
assert "function enableEditorCaret()" in t
assert "function suppressNativeKeyboard()" in t
assert "editor.readOnly=true" in t
assert "editor.readOnly=false" in t
assert "navigator.virtualKeyboard?.hide?.()" in t

# Responsive mobile preview controls.
assert 'id="mobileScriptSelect"' in t
assert 'class="mobile-script-picker"' in t
assert "mobileScriptSelect.onchange" in t
assert 'id="infoButton"' in t
assert 'id="infoPopover"' in t
assert "function refreshInfo()" in t
assert "suggestions-panel" in t
assert "@media(max-width:700px)" in t
assert "No suggestions" in t
assert "Lexicon:" in t
assert "Bigrams:" in t
assert "Trigrams:" in t

# Both on-screen Space controls use the same action.
assert "sp.onclick=spaceAction" in t
assert "document.getElementById('addSpace').onclick=spaceAction" in t

# Physical keyboard input is mapped by hardware key position rather than
# the active OS keyboard layout. Space still accepts the highlighted completion.
assert "function handlePhysicalKeyboard(e)" in t
assert "PHYSICAL_ROWS" in t
assert "e.code==='Space'" in t
assert "e.preventDefault();" in t
assert "spaceAction()" in t
assert "editor.addEventListener('keydown',handlePhysicalKeyboard)" in t
assert 'inputmode="none"' in t
assert "readonly" in t
assert "e.metaKey||e.ctrlKey||e.altKey" in t

# Keep v7 edge geometry.
assert "edge-row" in t
assert "margin-right:auto" in t
assert "margin-left:auto" in t
assert "mode-bottom" in t
assert "return-bottom" in t

# QWERTY4 uses Turkic dotted/dotless I casing:
# standard i -> İ, extra ı -> I.
assert "extraDefault:['ä','ğ','ı','ñ','ö','ş','ū','ü']" in t
assert "extraShift:['Ä','Ğ','I','Ñ','Ö','Ş','Ū','Ü']" in t
assert "['Q','W','E','R','T','Y','U','İ','O','P']" in t

# Keep number/symbol navigation.
assert "STATIC_SYMBOLS" in t
assert "mode.onclick=()=>setLayer('symbols-1')" in t
assert "mode.onclick=()=>setLayer('default')" in t

assert p.stat().st_size > 5_000_000
print(f"✓ Preview v8 smoke test passed: {p} ({p.stat().st_size:,} bytes)")
