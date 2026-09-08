#!/usr/bin/env python3
from pathlib import Path
import argparse, csv, json, re
try:
    import yaml
except ImportError:
    raise SystemExit("Install PyYAML: pip install pyyaml")

ROOT=Path(__file__).resolve().parent.parent

def load_yaml(path):
    class Loader(yaml.SafeLoader): pass
    def include(loader,node):
        p=path.parent/loader.construct_scalar(node)
        with p.open(encoding="utf-8") as f:
            return yaml.load(f,Loader=Loader)
    Loader.add_constructor("!include",include)
    with path.open(encoding="utf-8") as f:
        return yaml.load(f,Loader=Loader)

def rows(s):
    return [re.findall(r'\\s\{[^}]*\}|[^\s]+',line) for line in (s or "").splitlines() if line.strip()]

def layout(repo):
    p=repo/"layout/kaz/kaz-arab-3-rows.yaml"
    d=load_yaml(p); ls=d["iOS"]["primary"]["layers"]; lp=d.get("longpress") or {}
    return {
      "source_repository":"Agisight/ios-system-keyboard",
      "source_path":"layout/kaz/kaz-arab-3-rows.yaml",
      "longpress_path":"layout/kaz/kaz-arab-longpress.yaml",
      "display_name":(d.get("displayNames") or {}).get("en","Kazakh (Arabic)"),
      "abc":d.get("ABC","ABC"),
      "layers":{k:rows(v) for k,v in ls.items()},
      "longpress":{str(k):(v if isinstance(v,list) else [str(v)]) for k,v in lp.items()}
    }

def data():
    lex=[]
    with (ROOT/"extracted/lexicon/lexicon.tsv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f,delimiter="\t"): lex.append([r["token"],int(r["weight"])])
    lex.sort(key=lambda x:(x[1],x[0]))
    bi=[]
    with (ROOT/"extracted/ngrams/bigrams.tsv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f,delimiter="\t"): bi.append([r["token1"],r["token2"],int(r["weight"])])
    tri=[]
    with (ROOT/"extracted/ngrams/trigrams.tsv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f,delimiter="\t"): tri.append([r["token1"],r["token2"],r["token3"],int(r["weight"])])
    emo={}
    with (ROOT/"extracted/emoji/word_to_emoji.tsv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f,delimiter="\t"): emo.setdefault(r["token"],[]).append(r["emoji"])
    return {"lexicon":lex,"bigrams":bi,"trigrams":tri,"emoji":emo}

ap=argparse.ArgumentParser()
ap.add_argument("--keyboard-repo",required=True,type=Path)
ap.add_argument("--output",type=Path,default=ROOT/"preview/dist/kazakh-arabic-preview.html")
args=ap.parse_args()
tpl=(ROOT/"preview/template.html").read_text(encoding="utf-8")
out=tpl.replace("__LAYOUT__",json.dumps(layout(args.keyboard_repo),ensure_ascii=False,separators=(",",":")))
out=out.replace("__DATA__",json.dumps(data(),ensure_ascii=False,separators=(",",":")))
args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(out,encoding="utf-8")
print(args.output)
