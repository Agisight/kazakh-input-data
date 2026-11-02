#!/usr/bin/env python3
from pathlib import Path
import argparse
import csv
import json
import re
from collections import OrderedDict

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


# key, layout file (None = the International layout read by read_layout), button label,
# short label for narrow screens
ARAB_VARIANT_SPECS = (
    ("default", "kaz-arab-3-rows-default.yaml", "Default", "Default"),
    ("default-touch", "kaz-arab-3-rows-default-touch.yaml", "Default Touch", "Def Touch"),
    ("international", None, "International", "Intl"),
    ("international-touch", "kaz-arab-3-rows-international-touch.yaml", "International Touch", "Intl Touch"),
)


def swap_edge_keys(row):
    """The template swaps shift and backspace for RTL, so keep shift first and backspace last."""
    if len(row) > 1 and "backspace" in row[0] and row[-1] == "\\s{shift}":
        return [row[-1], *row[1:-1], row[0]]
    return row


def read_arab_variant_file(keyboard_repo, filename):
    path = keyboard_repo / "layout" / "kaz" / filename
    data = load_yaml(path)
    raw_layers = data["iOS"]["primary"]["layers"]
    layers = {
        key: [swap_edge_keys(row) for row in rows(value)]
        for key, value in raw_layers.items()
        if key != "longpress"
    }
    longpress = {
        str(key): value if isinstance(value, list) else [str(value)]
        for key, value in (data.get("longpress") or {}).items()
    }
    # a file's own `longpress` layer ("key : alternative ...") comes first for matching keys
    for line in (raw_layers.get("longpress") or "").splitlines():
        base, separator, alternatives = line.strip().partition(":")
        own = alternatives.split()
        if separator and base.strip() and own:
            base = base.strip()
            longpress[base] = own + [a for a in longpress.get(base, []) if a not in own]
    include = re.search(r"^longpress:\s*!include\s+(\S+)", path.read_text(encoding="utf-8"), re.M)
    return {
        "source_path": f"layout/kaz/{filename}",
        "longpress_path": f"layout/kaz/{include.group(1)}" if include else None,
        "display_name": (data.get("displayNames") or {}).get("en", "Kazakh (Arabic)"),
        "abc": data.get("ABC", "ABC"),
        "layers": layers,
        "longpress": longpress,
    }


def read_arab_variants(keyboard_repo):
    variants = OrderedDict()
    for key, filename, label, short in ARAB_VARIANT_SPECS:
        if filename is None:
            variant = read_layout(keyboard_repo)
            variant.pop("source_repository", None)
        else:
            variant = read_arab_variant_file(keyboard_repo, filename)
        variant.update({
            "key": key,
            "label": label,
            "short": short,
            "source": f"Arabic \u00b7 {label} \u00b7 Agisight/ios-system-keyboard \u00b7 {variant['source_path']}",
        })
        variants[key] = variant
    return variants


def write_snapshot(keyboard_repo, output, source_commit):
    base = read_layout(keyboard_repo)
    snapshot = OrderedDict()
    snapshot["source_repository"] = base.pop("source_repository")
    snapshot["source_commit"] = source_commit
    snapshot.update(base)
    snapshot["variants"] = OrderedDict(
        (key, {
            "label": value["label"],
            "source_path": value["source_path"],
            "longpress_path": value["longpress_path"],
            "layers": value["layers"],
            "longpress": value["longpress"],
        })
        for key, value in read_arab_variants(keyboard_repo).items()
    )
    output.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_macos_layout_file(keyboard_repo, filename, keylayout_file):
    path = keyboard_repo / "layout" / "kaz" / filename
    data = load_yaml(path)
    layers = data["macOS"]["primary"]["layers"]
    names = data.get("displayNames") or {}
    geometry = str(data.get("geometry") or "ISO").lower()
    return {
        "source_repository": "Agisight/ios-system-keyboard",
        "source_path": f"layout/kaz/{filename}",
        "display_name": names.get("kaz") or names.get("en") or "Kazakh Latin",
        "display_name_en": names.get("en") or "Kazakh Latin",
        "label": data.get("label") or "Experimental",
        "geometry": geometry,
        "recommended": bool(data.get("recommended")),
        "keylayout_file": keylayout_file,
        "layers": {
            key: rows(value)
            for key, value in layers.items()
            if isinstance(value, str)
        },
    }


def read_macos_layouts(keyboard_repo):
    specs = (
        ("iso", "kaz-latn-macos-iso-experimental.yaml", "kaz-latn-iso-experimental.keylayout"),
        ("ansi", "kaz-latn-macos-ansi-experimental.yaml", "kaz-latn-ansi-experimental.keylayout"),
    )
    layouts = {}
    for key, filename, keylayout_file in specs:
        path = keyboard_repo / "layout" / "kaz" / filename
        if path.exists():
            layouts[key] = read_macos_layout_file(keyboard_repo, filename, keylayout_file)

    if not layouts:
        old = keyboard_repo / "layout" / "kaz" / "kaz-latn-macos-experimental.yaml"
        if old.exists():
            layouts["iso"] = read_macos_layout_file(
                keyboard_repo,
                "kaz-latn-macos-experimental.yaml",
                "kaz-latn-experimental.keylayout",
            )
            layouts["iso"]["geometry"] = "iso"
            layouts["iso"]["recommended"] = True

    if not layouts:
        raise FileNotFoundError("No Kazakh Latin macOS desktop layout found")

    default_geometry = next(
        (key for key, value in layouts.items() if value.get("recommended")),
        next(iter(layouts)),
    )
    return {"default_geometry": default_geometry, "layouts": layouts}


def read_macos_layout(keyboard_repo):
    layouts = read_macos_layouts(keyboard_repo)
    return layouts["layouts"][layouts["default_geometry"]]


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
    parser.add_argument("--write-snapshot", type=Path,
                        help="write layout-snapshot.json for the pinned --source-commit and exit")
    parser.add_argument("--source-commit", help="ios-system-keyboard commit the snapshot is taken from")
    args = parser.parse_args()

    if args.write_snapshot:
        if not args.source_commit:
            raise SystemExit("--write-snapshot needs --source-commit")
        write_snapshot(args.keyboard_repo, args.write_snapshot, args.source_commit)
        print(args.write_snapshot)
        return

    datasets = {tag: read_script_data(tag) for tag in SCRIPT_TAGS}

    html = TEMPLATE.read_text(encoding="utf-8")
    html = html.replace(
        "__LAYOUT__",
        json.dumps(read_layout(args.keyboard_repo), ensure_ascii=False, separators=(",", ":")),
    )
    html = html.replace(
        "__ARAB_VARIANTS__",
        json.dumps(read_arab_variants(args.keyboard_repo), ensure_ascii=False, separators=(",", ":")),
    )
    macos_layouts = read_macos_layouts(args.keyboard_repo)
    html = html.replace(
        "__MACOS_LAYOUT__",
        json.dumps(
            macos_layouts["layouts"][macos_layouts["default_geometry"]],
            ensure_ascii=False,
            separators=(",", ":"),
        ),
    )
    html = html.replace(
        "__MACOS_LAYOUTS__",
        json.dumps(macos_layouts, ensure_ascii=False, separators=(",", ":")),
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
