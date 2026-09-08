#!/usr/bin/env python3
from pathlib import Path
import argparse
import csv
import json
import re

try:
    import yaml
except ImportError:
    raise SystemExit("Install PyYAML: pip install pyyaml")

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[1]
TEMPLATE = HERE / "template.html"
SCRIPT_TAGS = ("kk-Arab", "kk-Cyrl", "kk-Latn")


def load_yaml(path):
    class Loader(yaml.SafeLoader):
        pass

    def include(loader, node):
        include_path = path.parent / loader.construct_scalar(node)
        with include_path.open(encoding="utf-8") as f:
            return yaml.load(f, Loader=Loader)

    Loader.add_constructor("!include", include)
    with path.open(encoding="utf-8") as f:
        return yaml.load(f, Loader=Loader)


def rows(text):
    return [
        re.findall(r"\\s\{[^}]*\}|[^\s]+", line)
        for line in (text or "").splitlines()
        if line.strip()
    ]


def read_layout(keyboard_repo):
    path = keyboard_repo / "layout" / "kaz" / "kaz-arab-3-rows.yaml"
    data = load_yaml(path)
    layers = data["iOS"]["primary"]["layers"]
    longpress = data.get("longpress") or {}
    return {
        "source_repository": "Agisight/ios-system-keyboard",
        "source_path": "layout/kaz/kaz-arab-3-rows.yaml",
        "longpress_path": "layout/kaz/kaz-arab-longpress.yaml",
        "display_name": (data.get("displayNames") or {}).get("en", "Kazakh (Arabic)"),
        "abc": data.get("ABC", "ABC"),
        "layers": {key: rows(value) for key, value in layers.items()},
        "longpress": {
            str(key): value if isinstance(value, list) else [str(value)]
            for key, value in longpress.items()
        },
    }


def read_script_data(tag):
    data_root = REPO_ROOT / "data" / tag

    lexicon = []
    with (data_root / "lexicon" / "lexicon.tsv").open(encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            lexicon.append([row["token"], int(row["weight"])])
    lexicon.sort(key=lambda item: (item[1], item[0]))

    bigrams = []
    with (data_root / "ngrams" / "bigrams.tsv").open(encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            bigrams.append([row["token1"], row["token2"], int(row["weight"])])

    trigrams = []
    with (data_root / "ngrams" / "trigrams.tsv").open(encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            trigrams.append([
                row["token1"], row["token2"], row["token3"], int(row["weight"])
            ])

    emoji = {}
    with (data_root / "emoji" / "word_to_emoji.tsv").open(encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            emoji.setdefault(row["token"], []).append(row["emoji"])

    return {
        "tag": tag,
        "direction": "rtl" if tag == "kk-Arab" else "ltr",
        "lexicon": lexicon,
        "bigrams": bigrams,
        "trigrams": trigrams,
        "emoji": emoji,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--keyboard-repo", required=True, type=Path)
    parser.add_argument("--output", type=Path, default=HERE / "dist" / "index.html")
    args = parser.parse_args()

    datasets = {tag: read_script_data(tag) for tag in SCRIPT_TAGS}

    html = TEMPLATE.read_text(encoding="utf-8")
    html = html.replace(
        "__LAYOUT__",
        json.dumps(read_layout(args.keyboard_repo), ensure_ascii=False, separators=(",", ":")),
    )
    html = html.replace(
        "__DATASETS__",
        json.dumps(datasets, ensure_ascii=False, separators=(",", ":")),
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(html, encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
