from pathlib import Path
import unittest
from tools.prediction_engine import Predictor
ROOT=Path(__file__).resolve().parents[1]
TAGS=("kk-Arab","kk-Cyrl","kk-Latn")
class PredictionTests(unittest.TestCase):
    def test_prefix_completion(self):
        for tag in TAGS:
            with self.subTest(tag=tag):
                p=Predictor(ROOT/"data"/tag)
                word=next(w for w,_ in p.lexicon if len(w)>=3); prefix=word[:2]
                r=p.prefix(prefix,10); self.assertTrue(r); self.assertTrue(all(x.startswith(prefix) for x in r))
    def test_bigram_ranking(self):
        for tag in TAGS:
            with self.subTest(tag=tag):
                p=Predictor(ROOT/"data"/tag); source=next(k for k,v in p.bigrams.items() if v)
                self.assertEqual(p.next_word([source],limit=1),[p.bigrams[source][0][0]])
    def test_trigram_ranking(self):
        for tag in TAGS:
            with self.subTest(tag=tag):
                p=Predictor(ROOT/"data"/tag); ctx=next(k for k,v in p.trigrams.items() if v)
                self.assertEqual(p.next_word(list(ctx),limit=1),[p.trigrams[ctx][0][0]])
    def test_emoji(self):
        for tag in TAGS:
            with self.subTest(tag=tag):
                p=Predictor(ROOT/"data"/tag); word=next(iter(p.emoji)); self.assertEqual(p.emoji_for(word),p.emoji[word])
if __name__=="__main__": unittest.main()
