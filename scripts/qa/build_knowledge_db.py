#!/usr/bin/env python3
"""
Build dual-index FTS5 search database from project knowledge sources.

Sources indexed:
  - docs/qa/pitfalls_archive/*.md   (pitfalls)
  - docs/sprint/sprint*.md          (sprint)
  - docs/task/archive/*.md          (progress)
  - docs/spec/*.md                  (spec)

Output: data/knowledge.sqlite3

Usage:
    python3 -m scripts.qa.build_knowledge_db
    python3 -m scripts.qa.build_knowledge_db --db /custom/path.sqlite3
"""

from __future__ import annotations

import argparse
import re
import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

MEMORY_DIR = Path.home() / ".claude" / "projects" / "-Users-pig-project-arbitrage-betting-polyinit" / "memory"

SOURCES = {
    "pitfalls": "docs/qa/pitfalls_archive/*.md",
    "sprint": "docs/sprint/sprint*.md",
    "progress": "docs/task/archive/*.md",
    "spec": "docs/spec/*.md",
}

# Memory is outside repo root, handled separately
MEMORY_GLOB = "*.md"

EXCLUDE_NAMES = {"README.md"}
DEFAULT_DB = REPO_ROOT / "data" / "knowledge.sqlite3"

HEADING_RE = re.compile(r"^#{1,6}\s+(.*\S)\s*$")
SEARCH_KEYWORDS_INLINE_RE = re.compile(r"^-\s*Search keywords:\s*(.*)$", re.IGNORECASE)
SPRINT_RE = re.compile(r"(?:^|\b)sprint(\d+)\b", re.IGNORECASE)
SPRINT_SHORT_RE = re.compile(r"(?:^|\b)s(\d{1,3})\b", re.IGNORECASE)
WORD_BREAK_RE = re.compile(r"[^0-9A-Za-z_]+")


@dataclass(frozen=True)
class DocRow:
    scope: str
    path: str
    path_tokens: str
    title: str
    headings: str
    keywords: str
    content: str
    sprint_no: str
    mtime: float


def _read_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _extract_title(content: str, filename: str) -> str:
    for line in content.splitlines()[:10]:
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return filename


def _extract_headings(content: str) -> str:
    headings: list[str] = []
    for line in content.splitlines():
        match = HEADING_RE.match(line.strip())
        if match:
            headings.append(match.group(1).strip())
    return "\n".join(headings)


def _split_keyword_text(raw_text: str) -> list[str]:
    cleaned = raw_text.replace("`", " ").replace("[", " ").replace("]", " ")
    parts = re.split(r"[,，;；|/]", cleaned)
    keywords: list[str] = []
    for part in parts:
        candidate = " ".join(part.strip().split())
        if candidate:
            keywords.append(candidate)
    return keywords


def _extract_keywords(content: str) -> str:
    keywords: list[str] = []
    capture_block = False

    for line in content.splitlines():
        stripped = line.strip()
        inline_match = SEARCH_KEYWORDS_INLINE_RE.match(stripped)
        if inline_match:
            keywords.extend(_split_keyword_text(inline_match.group(1)))
            capture_block = False
            continue
        if stripped.lower() in {"## search keywords", "### search keywords"}:
            capture_block = True
            continue
        if not capture_block:
            continue
        if stripped.startswith("#"):
            capture_block = False
            continue
        if not stripped:
            continue
        keywords.extend(_split_keyword_text(stripped.lstrip("-* ")))

    deduped: list[str] = []
    seen: set[str] = set()
    for keyword in keywords:
        lowered = keyword.lower()
        if lowered in seen:
            continue
        deduped.append(keyword)
        seen.add(lowered)
    return "\n".join(deduped)


def _extract_sprint_no(path_text: str, title: str) -> str:
    search_text = f"{path_text} {title}"
    match = SPRINT_RE.search(search_text)
    if match:
        return match.group(1)
    match = SPRINT_SHORT_RE.search(search_text)
    if match:
        return match.group(1)
    return ""


def _extract_path_tokens(rel_path: str, scope: str, sprint_no: str) -> str:
    raw_path = rel_path.replace("/", " ").replace(".", " ")
    normalized_path = WORD_BREAK_RE.sub(" ", rel_path)
    parts = [raw_path, normalized_path, scope]
    if sprint_no:
        parts.append(f"sprint{sprint_no} s{sprint_no} sprint {sprint_no}")
    return " ".join(part for part in parts if part).strip()


def _iter_docs() -> tuple[list[DocRow], dict[str, int]]:
    rows: list[DocRow] = []
    scope_counts: dict[str, int] = {}

    for scope, glob_pattern in SOURCES.items():
        count = 0
        for fpath in sorted(REPO_ROOT.glob(glob_pattern)):
            if fpath.name in EXCLUDE_NAMES:
                continue
            content = _read_file(fpath)
            if not content.strip():
                continue
            rel_path = str(fpath.relative_to(REPO_ROOT))
            title = _extract_title(content, fpath.name)
            headings = _extract_headings(content)
            keywords = _extract_keywords(content)
            sprint_no = _extract_sprint_no(rel_path, title)
            path_tokens = _extract_path_tokens(rel_path, scope, sprint_no)
            rows.append(
                DocRow(
                    scope=scope,
                    path=rel_path,
                    path_tokens=path_tokens,
                    title=title,
                    headings=headings,
                    keywords=keywords,
                    content=content,
                    sprint_no=sprint_no,
                    mtime=fpath.stat().st_mtime,
                )
            )
            count += 1
        scope_counts[scope] = count

    # Index CC auto-memory (outside repo root)
    if MEMORY_DIR.exists():
        count = 0
        for fpath in sorted(MEMORY_DIR.glob(MEMORY_GLOB)):
            if fpath.name in EXCLUDE_NAMES or fpath.name == "MEMORY.md":
                continue
            content = _read_file(fpath)
            if not content.strip():
                continue
            title = _extract_title(content, fpath.name)
            headings = _extract_headings(content)
            keywords = _extract_keywords(content)
            sprint_no = _extract_sprint_no(fpath.name, title)
            path_tokens = _extract_path_tokens(f"memory/{fpath.name}", "memory", sprint_no)
            rows.append(
                DocRow(
                    scope="memory",
                    path=f"memory/{fpath.name}",
                    path_tokens=path_tokens,
                    title=title,
                    headings=headings,
                    keywords=keywords,
                    content=content,
                    sprint_no=sprint_no,
                    mtime=fpath.stat().st_mtime,
                )
            )
            count += 1
        scope_counts["memory"] = count

    return rows, scope_counts


def _create_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE docs (
            id          INTEGER PRIMARY KEY,
            scope       TEXT NOT NULL,
            path        TEXT NOT NULL UNIQUE,
            path_tokens TEXT NOT NULL,
            title       TEXT NOT NULL,
            headings    TEXT NOT NULL,
            keywords    TEXT NOT NULL,
            content     TEXT NOT NULL,
            sprint_no   TEXT NOT NULL,
            mtime       REAL NOT NULL
        );

        CREATE INDEX docs_scope_idx ON docs(scope);

        CREATE VIRTUAL TABLE docs_fts_unicode USING fts5(
            path_tokens,
            title,
            headings,
            keywords,
            content,
            content='docs',
            content_rowid='id',
            tokenize="unicode61 remove_diacritics 2 tokenchars '_'"
        );

        CREATE VIRTUAL TABLE docs_fts_trigram USING fts5(
            path_tokens,
            title,
            headings,
            keywords,
            content,
            content='docs',
            content_rowid='id',
            tokenize='trigram'
        );
        """
    )


def build(db_path: Path = DEFAULT_DB) -> tuple[int, dict[str, int], int]:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()

    rows, scope_counts = _iter_docs()

    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA journal_mode=OFF")
    conn.execute("PRAGMA synchronous=OFF")
    conn.execute("PRAGMA temp_store=MEMORY")

    _create_schema(conn)

    conn.executemany(
        """
        INSERT INTO docs (
            scope, path, path_tokens, title, headings, keywords, content, sprint_no, mtime
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                row.scope,
                row.path,
                row.path_tokens,
                row.title,
                row.headings,
                row.keywords,
                row.content,
                row.sprint_no,
                row.mtime,
            )
            for row in rows
        ],
    )
    conn.commit()

    conn.execute("INSERT INTO docs_fts_unicode(docs_fts_unicode) VALUES ('rebuild')")
    conn.execute("INSERT INTO docs_fts_trigram(docs_fts_trigram) VALUES ('rebuild')")
    conn.commit()

    db_size = db_path.stat().st_size
    conn.close()
    return len(rows), scope_counts, db_size


def main() -> None:
    parser = argparse.ArgumentParser(description="Build knowledge FTS5 database")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB, help="Output database path")
    args = parser.parse_args()

    t0 = time.monotonic()
    total, scope_counts, db_size = build(args.db)
    elapsed = time.monotonic() - t0

    print(f"Indexed {total} documents in {elapsed:.2f}s")
    for scope, count in scope_counts.items():
        print(f"  {scope}: {count}")
    print(f"Database: {args.db} ({db_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
