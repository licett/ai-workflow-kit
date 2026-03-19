#!/usr/bin/env python3
import argparse
import json
import os
import re

LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def is_local_link(link: str) -> bool:
    if not link:
        return False
    if link.startswith("#"):
        return False
    if "://" in link:
        return False
    if link.startswith("mailto:"):
        return False
    return True


def normalize_link(base_dir: str, link: str) -> str | None:
    target = link.split("#", 1)[0].strip()
    if not target:
        return None
    if not target.lower().endswith((".md", ".markdown")):
        return None
    return os.path.normpath(os.path.join(base_dir, target))


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a docs markdown link graph.")
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()

    root = os.path.abspath(args.root)
    docs_root = os.path.join(root, "docs")
    edges = []

    if not os.path.isdir(docs_root):
        print(json.dumps({"root": root, "edges": []}, indent=2))
        return 0

    for dirpath, _, filenames in os.walk(docs_root):
        for name in filenames:
            if not name.lower().endswith((".md", ".markdown")):
                continue
            file_path = os.path.join(dirpath, name)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception:
                continue

            for match in LINK_RE.finditer(content):
                link = match.group(1).strip()
                if not is_local_link(link):
                    continue
                target = normalize_link(dirpath, link)
                if not target:
                    continue
                edges.append(
                    {
                        "from": os.path.relpath(file_path, root),
                        "to": os.path.relpath(os.path.abspath(target), root),
                    }
                )

    print(json.dumps({"root": root, "edges": edges}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
