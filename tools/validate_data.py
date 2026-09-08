#!/usr/bin/env python3
import csv, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TAGS = ("kk-Arab", "kk-Cyrl", "kk-Latn")
HEADERS = {
 "lexicon":["token","weight","state_id"],
 "bigrams":["token1","token2","weight"],
 "trigrams":["token1","token2","token3","weight"],
 "w2e":["token","emoji","emoji_id","group_id","state_id"],
 "emoji":["emoji_id","emoji","unicode_sequence"],
}
def read(path, header):
    with path.open(encoding="utf-8", newline="") as f:
        r=csv.DictReader(f, delimiter="\t")
        assert r.fieldnames == header, f"{path}: header {r.fieldnames} != {header}"
        return list(r)
def validate(tag, summary):
    d=DATA/tag
    meta=json.loads((d/"metadata/metadata.json").read_text(encoding="utf-8"))
    lex=read(d/"lexicon/lexicon.tsv",HEADERS["lexicon"])
    bi=read(d/"ngrams/bigrams.tsv",HEADERS["bigrams"])
    tri=read(d/"ngrams/trigrams.tsv",HEADERS["trigrams"])
    w2e=read(d/"emoji/word_to_emoji.tsv",HEADERS["w2e"])
    inv=read(d/"emoji/emoji_inventory.tsv",HEADERS["emoji"])
    tokens=[x["token"] for x in lex]; token_set=set(tokens)
    assert len(tokens)==len(token_set), f"{tag}: duplicate lexicon tokens"
    assert len(lex)==meta["lexicon"]["entries"]==summary["lexicon_entries"]
    assert len(bi)==meta["ngrams"]["bigrams"]==summary["bigrams"]
    assert len(tri)==meta["ngrams"]["trigram_continuations"]==summary["trigram_continuations"]
    assert len(w2e)==meta["emoji"]["mapping_records"]==summary["word_to_emoji_records"]
    state_ids=set()
    for x in lex:
        int(x["weight"]); sid=int(x["state_id"]); assert sid not in state_ids; state_ids.add(sid)
    for x in bi:
        assert x["token1"] in token_set and x["token2"] in token_set; int(x["weight"])
    for x in tri:
        assert all(x[k] in token_set for k in ("token1","token2","token3")); int(x["weight"])
    emoji_ids={int(x["emoji_id"]) for x in inv}
    assert len(emoji_ids)==len(inv), f"{tag}: duplicate emoji IDs"
    for x in w2e:
        assert x["token"] in token_set
        assert int(x["emoji_id"]) in emoji_ids
        assert int(x["state_id"]) in state_ids
    dic=d/"hunspell"/f"{tag.replace('-','_')}.dic"
    lines=dic.read_text(encoding="utf-8").splitlines()
    assert int(lines[0])==len([x for x in lines[1:] if x])==len(lex)
    jc=0
    for line in (d/"lexicon/lexicon.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip():
            obj=json.loads(line); assert set(obj)=={"token","weight","state_id"}; jc+=1
    assert jc==len(lex)
    print(f"✓ {tag}: {len(lex):,} lexicon · {len(bi):,} bigrams · {len(tri):,} trigrams · {len(w2e):,} emoji")
def main():
    root=json.loads((ROOT/"metadata.json").read_text(encoding="utf-8"))
    assert root["scripts"]==list(TAGS)
    for tag in TAGS: validate(tag, root["scripts_summary"][tag])
    print("✓ All canonical data checks passed")
if __name__=="__main__": main()
