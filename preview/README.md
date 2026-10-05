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

## Source and status

The underlying Kazakh Latin letter order is based on the keyboard-order
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
