import json
import unittest
from pathlib import Path

SNAPSHOT = Path(__file__).resolve().parents[1] / "preview" / "kk-Arab" / "layout-snapshot.json"
# letters that are not on every plain keyboard row: hamza, feh, hah, heh doachashmee,
# ain, cheh, ng, oe, gaf
EXTRA_LETTERS = set("\u0621\u0641\u062d\u06be\u0639\u0686\u06ad\u06c6\u06af")
EXPECTED = ["default", "default-touch", "international", "international-touch"]


def letters(rows):
    return [token for row in rows for token in row if not token.startswith("\\s{")]


class ArabVariantsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
        cls.variants = cls.snapshot["variants"]

    def test_variant_set(self):
        self.assertEqual(list(self.variants), EXPECTED)
        self.assertEqual(len(self.snapshot["source_commit"]), 40)

    def test_every_extra_letter_is_reachable(self):
        for key, variant in self.variants.items():
            with self.subTest(key):
                on_screen = {
                    letter
                    for layer in ("default", "shift")
                    for letter in letters(variant["layers"].get(layer, []))
                }
                long_pressed = {alt for alts in variant["longpress"].values() for alt in alts}
                self.assertFalse(EXTRA_LETTERS - on_screen - long_pressed)

    def test_no_duplicate_letters_on_a_layer(self):
        for key, variant in self.variants.items():
            for layer in ("default", "shift"):
                if layer in variant["layers"]:
                    with self.subTest(key=key, layer=layer):
                        found = letters(variant["layers"][layer])
                        self.assertEqual(len(found), len(set(found)))

    def test_symbol_layers_exist(self):
        for key, variant in self.variants.items():
            with self.subTest(key):
                self.assertIn("symbols-1", variant["layers"])
                self.assertIn("symbols-2", variant["layers"])

    def test_touch_variants_have_no_shift_key(self):
        for key in ("default-touch", "international-touch"):
            tokens = [t for rows in self.variants[key]["layers"].values() for row in rows for t in row]
            self.assertFalse(any(t == "\\s{shift}" for t in tokens), key)

    def test_long_press_source_is_named(self):
        for key, variant in self.variants.items():
            with self.subTest(key):
                self.assertTrue(variant["longpress_path"].startswith("layout/kaz/"))

    def test_preview_opens_on_default(self):
        template = (SNAPSHOT.parent / "template.html").read_text(encoding="utf-8")
        self.assertIn("let arabVariant='default';", template)


if __name__ == "__main__":
    unittest.main()
