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

#### Placement rationale for every letter

Compact keeps the **31 letter slots of the ЙЦУКЕН comparison**: 23 letters
stay in their original slots and eight Kazakh letters replace other letters.
All nine Kazakh-specific letters remain accessible: eight are primary and
**ғ** is on **г**. The goal is direct access to commonly needed Kazakh letters
without adding a fourth row, while retaining much of the familiar layout.

The tables follow the displayed row order. Percentages are **modeled shares
of all letter occurrences under Zipf 1.0**, using the source and assumptions
below; they are not measured text frequencies. “Keep” means preserving the
ЙЦУКЕН position, not a claim that it is the fastest position for that letter.
Long-press keeps the displaced letter on its former physical key wherever
possible; **щ** moves to **ш**, while **ё**, **ъ** and **ғ** use related letters.

| Top row key | Modeled share | Long-press (share) | Why this position and access level |
| --- | ---: | --- | --- |
| й | 2.467% | — | Keep the first ЙЦУКЕН slot and familiar start of the row. |
| ү | 0.783% | ц (0.060%) | Reuse the ц slot beside у. Ү exceeds ц in all seven models; direct access and the neighboring у provide the rationale. |
| у | 1.437% | — | Keep its original slot; placing ү immediately before it gives a nearby related-letter reference. |
| к | 3.051% | — | Keep the familiar к position and direct access; қ gets its own key instead of becoming a hold on к. |
| е | 9.226% | ё (0.017%) | Keep е in its original slot. Ё is much rarer in every model and retains the recognizable е–ё spelling relationship on hold. |
| н | 6.759% | — | Keep the familiar н position and direct access; ң has a separate primary key. |
| г | 0.906% | ғ (1.127%) | Keep г in its original slot and group ғ with its base-shaped letter. This deliberately favors familiarity over the slightly higher modeled share of ғ. |
| ш | 1.358% | щ (0.028%) | Keep ш and combine the visually related ш–щ pair. Ш exceeds щ in every model, freeing the former щ slot for ң. |
| ң | 1.705% | — | Reuse the щ slot freed by the ш–щ grouping. This gives ң direct access without moving н or adding a key; proximity to н is sacrificed. |
| з | 1.569% | — | Keep the familiar з slot between the two repurposed positions. |
| қ | 3.601% | х (0.394%) | Reuse the х slot while keeping к primary. Қ exceeds х in every model; х remains reachable by holding its former key. |

| Middle row key | Modeled share | Long-press (share) | Why this position and access level |
| --- | ---: | --- | --- |
| ө | 0.656% | ф (0.112%) | Reuse the leftmost ф slot to expose ө without moving о. Ө exceeds ф in every model; this is a frequency and space choice rather than a phonetic pairing. |
| ы | 6.446% | — | Keep its familiar slot and direct access. |
| в | 0.378% | — | Keep the original slot and direct access to this less common letter. Compact preserves the remaining ЙЦУКЕН keys rather than relocating every rare letter. |
| а | 13.691% | — | Keep the familiar а slot and direct access to the most common letter in this scenario. |
| п | 2.215% | — | Keep its original slot and the familiar а–п–р sequence. |
| р | 4.653% | — | Keep its original slot and direct access. |
| о | 2.735% | — | Keep о in its original slot; ө uses a separate key to avoid a hold for every ө. |
| л | 4.245% | — | Keep its original slot and direct access. |
| д | 3.843% | — | Keep its original slot and direct access. |
| ж | 2.612% | — | Keep its original slot and direct access. |
| ә | 0.472% | э (0.032%) | Reuse the э slot to expose ә without moving а. Ә exceeds э in every model; both the replacement and its hidden alternative are explicit in the hint. |

| Bottom row key | Modeled share | Long-press (share) | Why this position and access level |
| --- | ---: | --- | --- |
| і | 3.934% | я (0.266%) | Reuse the я slot immediately after Shift. І exceeds я in every model and gains direct access without moving и; the association with я is positional rather than phonetic. |
| һ | 0.010% | ч (0.040%) | Reuse the ч slot using an approximate rotated-shape mnemonic. Һ is rarer than ч in every model: this is a deliberate visual choice, not a frequency improvement. |
| с | 5.086% | — | Keep its original slot and direct access. |
| м | 5.117% | — | Keep its original slot and direct access. |
| и | 1.148% | — | Keep и in its original slot; і is a separate primary key, preserving access to both. |
| т | 4.259% | — | Keep its original slot and direct access. |
| ь | 0.115% | ъ (0.001%) | Keep the ь slot and group the two signs. Ь exceeds ъ in every model; the rarer sign stays on hold. |
| б | 2.729% | — | Keep its original slot and direct access. |
| ұ | 0.677% | ю (0.040%) | Reuse the ю slot before Backspace. Ұ exceeds ю in every model; the у association in ю serves as a mnemonic, not a claim that their sounds are identical. |

Uppercase letters use the same positions and long-press pairs. The bottom row
has nine letter keys plus Shift and Backspace, matching the 11 key units of the
upper rows. This explains the geometry; it does not establish comfortable
reach or error rates on a phone.

#### Frequency benefits and deliberate compromises

For a pair sharing a key, making the more common letter primary reduces
holds. The difference is **10 × (primary share % − alternative share %)**
holds per 1,000 letters. For example, **қ primary / х on hold** needs about
3.9 holds per 1,000 letters for х, versus 36.0 for қ with the opposite mapping:
a saving of **32.1**. Қ is about **9.1 times** as common as х in Zipf 1.0 and
**7–16 times** as common across the seven hypotheses.

Seven replacements favor the promoted letter in all seven models. Their
Zipf 1.0 reductions in holds per 1,000 letters are **ү/ц: 7.2**, **ң/щ: 16.8**,
**қ/х: 32.1**, **ө/ф: 5.4**, **ә/э: 4.4**, **і/я: 36.7** and **ұ/ю: 6.4**.
These are individual comparisons with the displaced letter primary; for
ң/щ, щ is reached through ш. Overall layout counts below count each hidden
letter once, including щ.

There are two explicit exceptions to choosing the more common member:

- **Г stays primary over ғ.** Ғ exceeds г in every model, but reversing their
  current primary/hold roles would save only **2.2 holds per 1,000 letters**
  in Zipf 1.0. Keeping г prioritizes familiarity; this is a candidate for user
  testing, not a frequency-optimal choice.
- **Һ stays primary over ч.** This visual mnemonic adds about **0.3 holds
  per 1,000 letters** in Zipf 1.0 compared with ч primary / һ on hold. Keeping
  ч primary is a reasonable alternative if the mnemonic does not help users.

The allocation **ү at ц, ұ at ю** is a positional/mnemonic choice. The two
letters have similar modeled shares, and their frequency ordering changes
across the seven models, so frequency does not establish which should occupy
which slot. Swapping these two primary keys would leave the hidden-letter
set and modeled hold count unchanged, but could affect learning and reach.

The қ–х pairing also has a phonetic basis: қ can have a fricative realization
close to х in connected Kazakh speech. See McCollum and Chen's
[phonetic description of Kazakh](https://www.cambridge.org/core/journals/journal-of-the-international-phonetic-association/article/kazakh/353A10BD35418B48B5A6370D9F7D8CE0).
This supports a possible mnemonic, not proof of the best keyboard position.

Frequency supports which letters get direct access. It does **not** determine
their best coordinates, prove the rotated-shape mnemonic, or measure the cost
of relearning these eight positions. Compare typing time, errors, long-press
use and learning effort on phones before treating Compact as an optimum.

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

Reproduce the letter shares used in the Compact rationale with the same
calculation, treating each letter as a separate one-letter hold set:

```bash
python3 - <<'PY'
from tools import compare_cyrillic_layouts as comparison

comparison.HIDDEN = {letter: letter for letter in sorted(comparison.ALPHABET)}
_, _, _, estimates = comparison.estimate()
for letter, models in estimates.items():
    print(f"{letter}: {models['Zipf 1.0'] / 10:.3f}%")
PY
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
