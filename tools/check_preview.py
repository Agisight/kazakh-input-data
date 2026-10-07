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

# Extra Kazakh letter rows inherit key geometry from the first
# standard letter row instead of stretching to fill the keyboard.
assert "row extra-row" in t
assert "const baseCount=printableRow(rows[0]).length" in t
assert "er.style.setProperty('--base-count',baseCount)" in t
assert "var(--base-count) * 76px" in t
assert "Math.floor((baseCount-extras.length)/2)" in t
assert "gridTemplateColumns=`repeat(${baseCount},minmax(0,1fr))`" in t

# Cyrillic mobile long-press follows the compact iOS-style layout.
assert "'е':['ё']" in t
assert "'Е':['Ё']" in t
assert "'ь':['ъ']" in t
assert "'Ь':['Ъ']" in t
assert "['й','ц','у','к','е','н','г','ш','щ','з','х']" in t
assert "['Й','Ц','У','К','Е','Н','Г','Ш','Щ','З','Х']" in t
assert "function longPressOptions(t)" in t
assert "currentTag==='kk-Cyrl'" in t

# Arabic RTL preview mirrors only the edge action keys.
assert "function rtlEdgeKeys(row)" in t
assert "out.findIndex(t=>t.includes('shift'))" in t
assert "out.findIndex(t=>t.includes('backspace'))" in t
assert "renderRow(rtlEdgeKeys(row))" in t

# Long-press supports native-style hold, slide, and release selection.
assert "function updateLongPressSelection(x,y)" in t
assert "function finishLongPress()" in t
assert "longPressPointerId" in t
assert "longPressSelection" in t
assert "setPointerCapture" in t
assert "pointermove" in t
assert "b.classList.toggle('active',b===hit)" in t
assert "if(value)token(value)" in t
assert "touch-action:none" in t
assert "!e.isPrimary" in t
assert "e.button!==0" in t
assert "if(e.pointerId!==longPressPointerId)return" in t
assert "lostpointercapture" in t
assert "window.addEventListener('blur',hideLP)" in t

# Long-press alternatives use a compact native-like anchored popup.
assert "const center=r.left+r.width/2" in t
assert "center-w/2" in t
assert "r.top-h-10" in t
assert ".lp::after" in t
assert "min-width:48px" in t

# Latin layout selector lives with the input/info controls.
assert '<div class="latin-variant-switch" id="latinVariantSwitch"' in t
assert 'data-latin-variant="qwerty4"' in t
assert 'data-latin-variant="qwerty3"' in t
assert '<span class="variant-label" data-short-label="Q4">QWERTY4</span>' in t
assert '<span class="variant-label" data-short-label="Q3">QWERTY3</span>' in t
assert 'data-latin-variant="qwerty27"' in t
assert 'data-short-label="27">27 letters</span>' in t
assert 'qwerty27:LATN_QWERTY27' in t
for count in (29, 30, 31):
    assert f'data-latin-variant="qwerty{count}"' in t
    assert f'data-short-label="{count}">{count} letters</span>' in t
    assert f'qwerty{count}:expandedLatinLayout({count})' in t
assert 'role="group" aria-label="Latin layout variant"' in t

# Latin variant selector uses full labels on desktop and compact labels on mobile.
assert 'aria-pressed="true"' in t
assert 'aria-pressed="false"' in t
assert "x.setAttribute('aria-pressed',String(active))" in t
assert "content:attr(data-short-label)" in t

# Experimental three-row Latin QWERTY variant.
assert "const LATN_QWERTY3={" in t
assert "'a':['ä'],'A':['Ä']" in t
assert "'g':['ğ'],'G':['Ğ']" in t
assert "'i':['ı'],'I':['İ']" in t
assert "'n':['ñ'],'N':['Ñ']" in t
assert "'o':['ö'],'O':['Ö']" in t
assert "'s':['ş'],'S':['Ş']" in t
assert "'u':['ū'],'U':['Ū']" in t
assert "'y':['ü'],'Y':['Ü']" in t
assert "function latinLayout()" in t
assert "LATN_LAYOUTS[latinVariant]||LATN_QWERTY4" in t
assert "if(extras?.length)" in t

# Expanded Latin layouts use row geometry independent of fixed edge-key widths.
assert "function expandedLatinLayout(letterCount)" in t
assert "edgeWeight:letterCount===30?1.5:1" in t
assert "r.classList.add('expanded-latin-row')" in t
assert "renderRow(row,L.geometry)" in t

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
