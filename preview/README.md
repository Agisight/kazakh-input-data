# Preview

`kk-Arab/` contains the shared interactive preview for the Kazakh Arabic,
Cyrillic and Latin datasets.

Keyboard layout sources stay in the separate `Agisight/ios-system-keyboard`
repository. The preview reads the Arabic mobile layout plus the experimental
Kazakh Latin macOS desktop layouts from that repository at build time.

The macOS desktop preview exposes two physical geometries:

- **ISO** — primary experimental geometry;
- **ANSI** — optional adaptation for ANSI hardware.

CI builds and publishes both generated `.keylayout` files with the GitHub Pages artifact:

- `kaz-latn-iso-experimental.keylayout`
- `kaz-latn-ansi-experimental.keylayout`

The default Cyrillic on-screen keyboard remains an adaptation of Keyman Kazakh
Basic; two experimental three-row comparisons are also available. The Latin
on-screen keyboard remains experimental. The macOS desktop layouts
are also explicitly experimental and are not presented as finalized standards.

## Experimental Cyrillic touch variants

Select **Cyrillic**, then one of three clearly labeled variants beside the
input field: **4 rows**, **3 rows** (ЙЦУКЕН) or **Compact**
(our compact variant). **4 rows** keeps the existing layout with 40 visible letters
and an additional Kazakh letter row. The other two have **11 / 11 / 9** visible-letter rows; Shift and
Backspace complete the bottom row to 11 equal-width buttons. All 42 Cyrillic
letters are reachable exactly once per case in both three-row variants.
Small gray hints show long-press alternatives, including uppercase equivalents.
Hold, slide to the alternative and release to enter it; releasing outside
the popup cancels. Physical input inside the demo follows displayed positions.

### Compact: 31 letters, eight Kazakh letters in familiar positions

```text
й ү у к е н г ш ң з қ
ө ы в а п р о л д ж ә
⇧ і һ с м и т ь б ұ ⌫
```

Relative to the ЙЦУКЕН base, replace **ц → ү, щ → ң, х → қ, ф → ө,
э → ә, я → і, ч → һ, ю → ұ**. Keep **к** and **г** in their familiar positions.
The long-press mappings are:

| Visible | Long-press | Visible | Long-press |
| --- | --- | --- | --- |
| г | ғ | ш | щ |
| е | ё | ь | ъ |
| ө | ф | ү | ц |
| і | я | һ | ч |
| ә | э | ұ | ю |
| қ | х | | |

These choices combine frequency hypotheses with familiarity and visual
mnemonics. In the source models **ғ** is slightly more frequent than **г**,
but keeping **г** primary costs only 2.2 additional holds per 1,000 letters under
Zipf 1.0 compared with reversing that pair. **һ** is rarer than **ч** in all seven
models; using **һ** primary is a deliberate mnemonic choice, costing about
0.3 additional holds per 1,000 letters compared with reversing their pair.
Neither this reasoning nor the count model establishes optimal key placement.

### 3 rows: familiar ЙЦУКЕН base with Kazakh long-press

```text
й ц у к е н г ш щ з х
ф ы в а п р о л д ж э
⇧ я ч с м и т ь б ю ⌫
```

Long-press: **а → ә, г → ғ, к → қ, н → ң, о → ө, у → ұ / ү,
х → һ, и → і, е → ё, ь → ъ**. Both alternatives on **у** remain selectable
with the same hold-slide-release gesture.

This is an iOS-style three-row comparison built from the existing ЙЦУКЕН base,
not a verified replica of a particular Apple Kazakh keyboard or iOS release.

### Cyrillic frequency assumptions

Source: [`data/kk-Cyrl/lexicon/lexicon.tsv`](../data/kk-Cyrl/lexicon/lexicon.tsv),
SHA-256 `534fb2c24b3e747aceaad35d61205089a963833363043fc574eebe47bd2be331`.
Of 90,052 source entries, three entries without letters (`!`, `)`, `?`) are
excluded before assigning ranks. The retained 90,049 entries contain 710,258
letter occurrences. NFC normalization and case folding pool letter counts;
case-equivalent source entries retain their own weights and rank contributions.
Only the 42 supported letters are counted; punctuation and digits are ignored.
There is no language or spelling filtering.

We use the same seven hypotheses described for Latin below: uniform weight,
Zipf 0.8 / 1.0 / 1.2 with averaged tied ranks, and Exp H=10 / 20 / 40.
The minimum retained Cyrillic cost is **28**. These cost values are ranking
inputs, not measured corpus frequencies.

| Variant | Hidden letters | Holds / 1,000 letters, Zipf 1.0 | Range across 7 models |
| --- | --- | ---: | ---: |
| 4 rows (40 visible letters) | ё, ъ | 0.2 | 0.1–0.3 |
| Compact (31 visible letters) | ғ, ё, ф, х, ц, ч, щ, ъ, э, ю, я | 21.2 | 16.8–26.2 |
| 3 rows (ЙЦУКЕН, 31 visible letters) | ә, ғ, қ, ң, ө, ұ, ү, һ, і, ё, ъ | 129.8 | 121.2–143.0 |

The compact variant saves about **108.7 holds per 1,000 letters** versus the
ЙЦУКЕН comparison under Zipf 1.0. The 40-letter layout needs fewer holds but
uses an additional letter row. The event count assumes one hold for each
hidden-letter occurrence; it excludes typing time, key travel, errors,
spaces, Shift and autocomplete. Compare these tradeoffs on phones before
selecting a layout. The seven models are sensitivity scenarios, not independent
measurements of real-world usage.

Reproduce the Cyrillic estimates with Python's standard library:

```bash
python3 tools/compare_cyrillic_layouts.py
```

## Experimental Latin touch variants

Select **Latin**, then **27 letters**, **29 letters**, **30 letters** or **31 letters**
beside the input field. On narrow screens the selector uses **Q4**, **Q3**, **27**, **29**,
**30**, **31**. QWERTY4 and QWERTY3 remain available as comparison layouts.
The numeric labels count visible letters, not rows or service keys.
Latin keys with long-press alternatives show a small gray hint in their upper
corner. The hint follows the active letter case and exposes the alternative to
screen readers; tap and hold-slide-release behavior stays the same.

The 29–31-letter variants keep the 26 ASCII QWERTY letters, in their original
relative row order. Added letters shift some positions; familiarity and typing
speed therefore still need testing. The preview is a touch-layout experiment,
not a change to the exported macOS ISO/ANSI layouts.

### 27 letters: replace w/x and add ğ beside g

A good compact option for a small on-screen keyboard: two ten-letter upper
rows, direct access to ü/ş/ğ, and a visible c. Typing speed, errors and learning
effort still need testing on phones.

```text
q ü e r t y u i o p
a s d f g ğ h j k l
⇧ z ş c v b n m ⌫
```

- **ü** occupies the original **w** position and **ş** replaces **x**.
- **c** stays in its original position; **ğ** has a separate key immediately after **g**.
- Displaced letters remain available through **ü → w, ş → x** long-press.
- Other long-press pairs: **a → ä, i → ı, n → ñ, o → ö, u → ū**.
- There are 27 visible letters in **10 / 10 / 7** letter rows. The two upper
  rows share the same width; Shift and Backspace each use 1.5 grid units,
  giving the bottom row the same total width of 10 units.
- Each of the 34 supported letters is reachable once per case. There are no
  duplicate **g → ğ**, **s → ş** or **y → ü** alternatives in this variant.
- Hardware **KeyW / KeyX / KeyC** in the preview type **ü / ş / c** respectively;
  **KeyH** types the added **ğ** according to its middle-row position. Shift
  types the uppercase equivalents. This is a separate selectable experiment.

### 29 letters: three added visible letters

```text
q w e r t y u i ı o p
 a s d f g ğ h j k l
  ⇧ z x c v b n ñ m ⌫
```

- Visible additions: **ı, ğ, ñ**.
- Long-press: **a → ä, o → ö, s → ş, u → ū, y → ü**.
- Letter rows: **11 / 10 / 8**. Including Shift and Backspace: **11 / 10 / 10**.
- The lower two rows are centered; letter and edge keys use the same width.

### 30 letters: expose ş, keep ü on y

```text
q w e r t y u i ı o p
a s ş d f g ğ h j k l
⇧  z x c v b n ñ m  ⌫
```

- Visible additions: **ı, ğ, ñ, ş**.
- Long-press: **a → ä, o → ö, u → ū, y → ü**. **w has no alternative**.
- Letter rows: **11 / 11 / 8**. Including service keys: **11 / 11 / 10 buttons**.
- Shift and Backspace each receive 1.5 grid units, so the bottom row occupies
  11 units and shares the outer width of the upper rows.

### 31 letters: expose ü and use three equal button counts

```text
q w e r t y u i ı o p
a s ş d f g ğ h j k l
⇧ z x c v b n ñ m ü ⌫
```

- Visible additions: **ı, ğ, ñ, ş, ü**.
- Long-press: **a → ä, o → ö, u → ū**.
- Letter rows: **11 / 11 / 9**. Including service keys: **11 / 11 / 11**.
- Letter, Shift and Backspace keys use the same width.

The 27-letter and 29–31-letter variants use Turkic I casing: **i ↔ İ**, **ı ↔ I**. Long-press
alternatives have uppercase equivalents. Hold a key, slide into the popup and
release to enter an alternative; releasing outside the popup cancels selection.
Hardware input within the on-screen preview follows displayed row positions,
including inserted letters. Use **Desktop** for the separate ISO/ANSI mappings.

### Frequency assumptions and comparison

The source is [`data/kk-Latn/lexicon/lexicon.tsv`](../data/kk-Latn/lexicon/lexicon.tsv):
**45,073 word entries**, **340,167 letter occurrences**, **161 distinct costs**.
The source SHA-256 is
`7a5deb666873abf4a9eb6f6be55e1fae744b802797433f93be7e796acb9e6b06`.
Its `weight` values are ranking/cost inputs, not measured word frequencies.

We assume lower cost means more likely input and compare seven hypothetical
word-weight models:

- **Uniform:** every word has weight 1.
- **Zipf 0.8 / 1.0 / 1.2:** sort by ascending cost and use `q = rank^(-s)`.
  Words tied on cost share the average weight over all ranks occupied by that
  group, avoiding an arbitrary alphabetical preference.
- **Exp 10 / 20 / 40:** `q = 2^(-(cost - minimum_cost)/H)`, for `H = 10, 20, 40`.

Each letter's share is `sum(q(word) × occurrences_in_word) / sum(q(word) × word_length)`.
Estimated holds per 1,000 letters are `1000 × sum(shares of long-press letters)`.
This counts one hold per hidden-letter event. It does not estimate typing time,
errors, pointer travel, uppercase input, spaces or autocomplete savings. The source is not
filtered by language or spelling, and the seven models are sensitivity scenarios,
not independent empirical observations.

| Layout | Hidden letters | Holds / 1,000 letters, Zipf 1.0 | Range across 7 models |
| --- | --- | ---: | ---: |
| QWERTY3, 26 visible | ä, ğ, ı, ñ, ö, ş, ū, ü | 108.3 | 83.8–129.5 |
| 27 letters | ä, ı, ñ, ö, ū, w, x | 75.6 | 56.4–92.0 |
| 29 visible | ä, ö, ş, ū, ü | 36.7 | 28.9–44.1 |
| 30 visible | ä, ö, ū, ü | 25.2 | 20.5–28.5 |
| 31 visible | ä, ö, ū | 18.0 | 14.3–21.2 |

Adding **ş** to the 29-letter layout saves **11.5 holds per 1,000 letters** under
Zipf 1.0; adding **ü** to the 30-letter layout saves another **7.2**. Keeping **ı**
visible avoids **42.9** holds per 1,000 letters under that model, compared with
**7.2** for ü. Moving ü from long-press on y to long-press on w would not change
the counted events; the 29- and 30-letter variants keep **y → ü**.

The 29–31-letter layouts keep all ASCII letters visible, including **c, w, x**,
which are absent from this particular lexicon. The 27-letter layout puts
**w/x** on long-press while keeping **c** visible, and saves **32.7 holds per 1,000 letters**
against QWERTY3 under Zipf 1.0. Zero observations do not measure their usefulness
for names, other languages or URLs; such input can add holds in the 27-letter layout.

Reproduce the estimates with Python's standard library:

```bash
python3 tools/compare_latin_layouts.py
```

With all 26 ASCII letters retained, the chosen added letters minimize holds
under Zipf 1.0 for their respective key budgets. That establishes an optimum
only for this count-based model and constraint. It does not establish optimal
key placement, geometry or typing performance. Compare speed, errors, actual
holds and learning effort on phones before selecting a layout or recommending
a standard.

## Source and status

The experimental macOS layouts use the Kazakh Latin keyboard-order
proposal presented by Kazakhstan's Minister of Digital Development at the
National Commission meeting on 28 January 2021:

- Government publication:
  https://primeminister.kz/ru/news/a-mamin-provel-zasedanie-nackomissii-po-perevodu-alfavita-kazahskogo-yazyka-na-latinskuyu-grafiku-280497

The government publication presents a proposed ordering of Kazakh letters on a
keyboard. This repository does not claim that the hardware-specific layouts
below are an adopted Kazakh national keyboard standard.

The physical keyboard geometries are based on established desktop keyboard
standards:

- ISO geometry — ISO/IEC 9995:
  https://www.iso.org/standard/51644.html
- ANSI-style geometry — INCITS 154:
  https://webstore.ansi.org/standards/incits/INCITS1541988S2009

In this preview:

- **ISO** is the primary experimental hardware adaptation.
- **ANSI** is an optional experimental adaptation for ANSI hardware.

Both mappings are experimental adaptations of the Kazakh Latin letter-order
proposal to those physical keyboard geometries.
