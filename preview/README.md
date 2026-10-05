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
