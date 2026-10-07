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

The Cyrillic on-screen keyboard remains an adaptation of Keyman Kazakh Basic;
the Latin on-screen keyboard remains experimental. The macOS desktop layouts
are also explicitly experimental and are not presented as finalized standards.

## Experimental Latin touch variants

Select **Latin**, then **26 swap**, **29 letters**, **30 letters** or **31 letters**
beside the input field. On narrow screens the selector uses **Q4**, **Q3**, **26**, **29**,
**30**, **31**. QWERTY4 and QWERTY3 remain available as comparison layouts.
The numeric labels count visible letters, not rows or service keys.
Latin keys with long-press alternatives show a small gray hint in their upper
corner. The hint follows the active letter case and exposes the alternative to
screen readers; tap and hold-slide-release behavior stays the same.

The 29–31-letter variants keep the 26 ASCII QWERTY letters, in their original
relative row order. Added letters shift some positions; familiarity and typing
speed therefore still need testing. The preview is a touch-layout experiment,
not a change to the exported macOS ISO/ANSI layouts.

### 26 swap: replace w, x and c with ü, ş and ğ

```text
q ü e r t y u i o p
 a s d f g h j k l
⇧ z ş ğ v b n m ⌫
```

- **ü** occupies the original **w** position, **ş** replaces **x**, and **ğ** replaces **c**.
- Displaced letters remain available through **ü → w, ş → x, ğ → c** long-press.
- Other long-press pairs: **a → ä, i → ı, n → ñ, o → ö, u → ū**.
- There are 26 visible letters in **10 / 9 / 7** letter rows. The middle row
  is centered; Shift and Backspace each use 1.5 grid units, giving the bottom
  row the same total width as the 10-unit top row.
- Each of the 34 supported letters is reachable once per case. There are no
  duplicate **g → ğ**, **s → ş** or **y → ü** alternatives in this variant.
- Hardware **KeyW / KeyX / KeyC** in the preview type **ü / ş / ğ** respectively;
  Shift types **Ü / Ş / Ğ**. This is a separate selectable experiment.

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

The 26 swap and 29–31-letter variants use Turkic I casing: **i ↔ İ**, **ı ↔ I**. Long-press
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
| 26 swap | ä, ı, ñ, ö, ū, w, x, c | 75.6 | 56.4–92.0 |
| 29 visible | ä, ö, ş, ū, ü | 36.7 | 28.9–44.1 |
| 30 visible | ä, ö, ū, ü | 25.2 | 20.5–28.5 |
| 31 visible | ä, ö, ū | 18.0 | 14.3–21.2 |

Adding **ş** to the 29-letter layout saves **11.5 holds per 1,000 letters** under
Zipf 1.0; adding **ü** to the 30-letter layout saves another **7.2**. Keeping **ı**
visible avoids **42.9** holds per 1,000 letters under that model, compared with
**7.2** for ü. Moving ü from long-press on y to long-press on w would not change
the counted events; the 29- and 30-letter variants keep **y → ü**.

The 29–31-letter layouts keep all ASCII letters visible, including **c, w, x**,
which are absent from this particular lexicon. The 26 swap layout instead puts
those three letters on long-press and saves **32.7 holds per 1,000 letters**
against QWERTY3 under Zipf 1.0. Zero observations do not measure their usefulness
for names, other languages or URLs; such input can add holds in the swap layout.

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
