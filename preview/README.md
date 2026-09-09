# Preview

`kk-Arab/` contains the shared interactive preview for the Kazakh Arabic,
Cyrillic and Latin datasets.

Keyboard layout sources stay in the separate `Agisight/ios-system-keyboard`
repository. The preview reads the Arabic mobile layout and the experimental
Kazakh Latin macOS layout from that repository at build time. CI also builds
and publishes the generated `kaz-latn-experimental.keylayout` file with the
GitHub Pages artifact.

The Cyrillic on-screen keyboard remains an adaptation of Keyman Kazakh Basic;
the Latin on-screen keyboard remains experimental. The macOS desktop layout is
also explicitly experimental and is not presented as a finalized standard.
