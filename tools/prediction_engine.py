import csv
from pathlib import Path
class Predictor:
    def __init__(self, script_dir: Path):
        self.lexicon=[]; self.bigrams={}; self.trigrams={}; self.emoji={}
        with (script_dir/"lexicon/lexicon.tsv").open(encoding="utf-8") as f:
            for r in csv.DictReader(f,delimiter="\t"): self.lexicon.append((r["token"],int(r["weight"])))
        self.lexicon.sort(key=lambda x:(x[1],x[0]))
        with (script_dir/"ngrams/bigrams.tsv").open(encoding="utf-8") as f:
            for r in csv.DictReader(f,delimiter="\t"): self.bigrams.setdefault(r["token1"],[]).append((r["token2"],int(r["weight"])))
        for v in self.bigrams.values(): v.sort(key=lambda x:(x[1],x[0]))
        with (script_dir/"ngrams/trigrams.tsv").open(encoding="utf-8") as f:
            for r in csv.DictReader(f,delimiter="\t"): self.trigrams.setdefault((r["token1"],r["token2"]),[]).append((r["token3"],int(r["weight"])))
        for v in self.trigrams.values(): v.sort(key=lambda x:(x[1],x[0]))
        with (script_dir/"emoji/word_to_emoji.tsv").open(encoding="utf-8") as f:
            for r in csv.DictReader(f,delimiter="\t"): self.emoji.setdefault(r["token"],[]).append(r["emoji"])
    def prefix(self,prefix,limit=3): return [w for w,_ in self.lexicon if w.startswith(prefix)][:limit]
    def next_word(self,previous,partial="",limit=3):
        c=[]
        if len(previous)>=2: c=self.trigrams.get((previous[-2],previous[-1]),[])
        if not c and previous: c=self.bigrams.get(previous[-1],[])
        out=[]; seen=set()
        for w,_ in c:
            if partial and not w.startswith(partial): continue
            if w in seen: continue
            seen.add(w); out.append(w)
            if len(out)==limit: break
        return out
    def emoji_for(self,token): return self.emoji.get(token,[])
