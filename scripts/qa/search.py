#!/usr/bin/env python3
"""Search project knowledge base with dual FTS5 indexes and query rewrite."""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
import textwrap
from functools import lru_cache
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_DB = REPO_ROOT / "data" / "knowledge.sqlite3"
DEFAULT_ALIAS_PATH = REPO_ROOT / "docs" / "spec" / "knowledge_query_aliases.json"

COLUMN_WEIGHTS = (2.0, 6.0, 4.0, 5.0, 1.0)
FUSION_K = 20
CANDIDATE_LIMIT = 20
SNIPPET_MAX_CHARS = 320

CJK_RE = re.compile(r"[\u3400-\u9fff]")
ASCII_TOKEN_RE = re.compile(r"[a-z0-9_]+")
SPRINT_QUERY_RE = re.compile(r"(?:^|\b)(?:sprint|s)(\d{1,3})(?:\b|$)", re.IGNORECASE)
WHITESPACE_RE = re.compile(r"\s+")


def _ensure_db(db_path: Path) -> None:
    if not db_path.exists():
        print(f"Database not found: {db_path}", file=sys.stderr)
        print("Run: python3 -m scripts.qa.build_knowledge_db", file=sys.stderr)
        sys.exit(1)


def _normalize_text(text: str) -> str:
    return WHITESPACE_RE.sub(" ", text.strip().lower())


def _has_cjk(text: str) -> bool:
    return bool(CJK_RE.search(text))


@lru_cache(maxsize=1)
def _load_aliases() -> dict[str, list[str]]:
    if not DEFAULT_ALIAS_PATH.exists():
        return {}
    payload = json.loads(DEFAULT_ALIAS_PATH.read_text(encoding="utf-8"))
    alias_map = payload.get("aliases", {})
    normalized: dict[str, list[str]] = {}
    for raw_key, raw_terms in alias_map.items():
        key = _normalize_text(str(raw_key))
        if not key:
            continue
        deduped_terms: list[str] = []
        seen_terms: set[str] = set()
        for raw_term in raw_terms:
            term = _normalize_text(str(raw_term))
            if not term or term in seen_terms:
                continue
            deduped_terms.append(term)
            seen_terms.add(term)
        if deduped_terms:
            normalized[key] = deduped_terms
    return normalized


def _find_alias_keys(query: str, alias_map: dict[str, list[str]]) -> list[str]:
    occupied: list[tuple[int, int]] = []
    matches: list[tuple[int, str]] = []

    for alias_key in sorted(alias_map, key=len, reverse=True):
        start = 0
        while True:
            idx = query.find(alias_key, start)
            if idx < 0:
                break
            span = (idx, idx + len(alias_key))
            if not any(span[0] < end and span[1] > begin for begin, end in occupied):
                occupied.append(span)
                matches.append((idx, alias_key))
            start = idx + 1

    matches.sort()
    return [alias_key for _, alias_key in matches]


def _expand_query(query: str) -> tuple[list[str], list[str]]:
    alias_map = _load_aliases()
    matched_aliases = _find_alias_keys(query, alias_map)
    expanded_terms: list[str] = []
    seen_terms: set[str] = set()
    for alias_key in matched_aliases:
        for term in alias_map.get(alias_key, []):
            if term in seen_terms:
                continue
            expanded_terms.append(term)
            seen_terms.add(term)
    return matched_aliases, expanded_terms


def expand_query_aliases(query: str) -> tuple[list[str], list[str]]:
    """Expose normalized alias expansion for regression checks."""
    return _expand_query(_normalize_text(query))


def _quote_fts(term: str) -> str:
    return '"' + term.replace('"', '""') + '"'


def _unicode_term_clause(term: str) -> str | None:
    normalized = _normalize_text(term)
    if not normalized:
        return None
    if " " in normalized:
        parts = [part for part in ASCII_TOKEN_RE.findall(normalized) if part]
        if not parts:
            return None
        return "(" + " AND ".join(_unicode_term_clause(part) for part in parts if _unicode_term_clause(part)) + ")"
    if "_" in normalized:
        parts = [part for part in normalized.split("_") if part]
        split_clause = " AND ".join(_quote_fts(part) for part in parts)
        return f"({_quote_fts(normalized)} OR ({split_clause}))"
    return _quote_fts(normalized)


def _build_unicode_match(query: str) -> str | None:
    clauses = [_unicode_term_clause(token) for token in ASCII_TOKEN_RE.findall(query)]
    clauses = [clause for clause in clauses if clause]
    if not clauses:
        return None
    return " AND ".join(clauses)


def _build_unicode_broad_match(query: str) -> str | None:
    clauses = [_unicode_term_clause(token) for token in ASCII_TOKEN_RE.findall(query)]
    clauses = [clause for clause in clauses if clause]
    if len(clauses) < 2:
        return None
    return " OR ".join(clauses)


def _trigram_term_clause(term: str) -> str | None:
    normalized = _normalize_text(term)
    if not normalized:
        return None
    if " " in normalized:
        parts = [part for part in normalized.split() if part]
        if not parts:
            return None
        return "(" + " AND ".join(_quote_fts(part) for part in parts) + ")"
    return _quote_fts(normalized)


def _build_trigram_match(query: str) -> str | None:
    normalized = _normalize_text(query)
    if not normalized:
        return None
    if " " in normalized:
        return " AND ".join(_quote_fts(part) for part in normalized.split() if part)
    return _quote_fts(normalized)


def _build_trigram_broad_match(query: str) -> str | None:
    normalized = _normalize_text(query)
    parts = [part for part in normalized.split() if part]
    if len(parts) < 2:
        return None
    return " OR ".join(_quote_fts(part) for part in parts)


def _build_expansion_match(expanded_terms: list[str], *, backend: str) -> str | None:
    builder = _unicode_term_clause if backend == "unicode" else _trigram_term_clause
    clauses = [builder(term) for term in expanded_terms]
    clauses = [clause for clause in clauses if clause]
    if not clauses:
        return None
    return " OR ".join(clauses)


def _extract_sprint_refs(query: str) -> set[str]:
    return {match.group(1) for match in SPRINT_QUERY_RE.finditer(query)}


def _source_weight(source: str, has_cjk_query: bool) -> float:
    weights = {
        "raw_unicode": 3.0,
        "raw_trigram": 1.8 if has_cjk_query else 2.0,
        "expanded_unicode": 2.8 if has_cjk_query else 1.6,
        "expanded_trigram": 2.0 if has_cjk_query else 1.2,
        "broad_unicode": 1.4,
        "broad_trigram": 0.8 if has_cjk_query else 1.0,
    }
    return weights[source]


def _fetch_candidates(
    conn: sqlite3.Connection,
    *,
    table: str,
    match_expr: str,
    scope: str | None,
    limit: int,
) -> list[sqlite3.Row]:
    sql = f"""
        SELECT d.id, d.scope, d.path, d.path_tokens, d.title, d.headings, d.keywords, d.content, d.sprint_no,
               bm25({table}, ?, ?, ?, ?, ?) AS bm25_score
        FROM {table}
        JOIN docs d ON d.id = {table}.rowid
        WHERE {table} MATCH ?
    """
    params: list[Any] = [*COLUMN_WEIGHTS, match_expr]
    if scope:
        sql += " AND d.scope = ?"
        params.append(scope)
    sql += " ORDER BY bm25_score LIMIT ?"
    params.append(limit)
    try:
        rows = conn.execute(sql, params).fetchall()
    except sqlite3.OperationalError:
        return []
    return rows


def _field_boost(
    row: sqlite3.Row,
    *,
    normalized_query: str,
    query_terms: list[str],
    expanded_terms: list[str],
    sprint_refs: set[str],
) -> float:
    score = 0.0
    title_text = _normalize_text(row["title"])
    headings_text = _normalize_text(row["headings"])
    keywords_text = _normalize_text(row["keywords"])
    path_text = _normalize_text(row["path_tokens"])
    content_text = _normalize_text(row["content"])

    if normalized_query:
        if normalized_query in title_text:
            score += 3.0
        if normalized_query in headings_text:
            score += 2.2
        if normalized_query in keywords_text:
            score += 2.0
        if normalized_query in path_text:
            score += 1.5

    literal_terms = [term for term in query_terms if term]
    if literal_terms and any(term in title_text for term in literal_terms):
        score += 1.8
    if literal_terms and any(term in headings_text for term in literal_terms):
        score += 1.2
    if literal_terms and any(term in keywords_text for term in literal_terms):
        score += 1.2
    if literal_terms and any(term in path_text for term in literal_terms):
        score += 0.9
    literal_coverage = sum(
        1 for term in literal_terms if term in title_text or term in headings_text or term in keywords_text or term in path_text or term in content_text
    )
    score += min(literal_coverage, 4) * 0.35

    if expanded_terms:
        if any(term in title_text for term in expanded_terms):
            score += 1.2
        if any(term in headings_text for term in expanded_terms):
            score += 1.0
        if any(term in keywords_text for term in expanded_terms):
            score += 1.2
        if any(term in path_text for term in expanded_terms):
            score += 0.6
        if any(term in content_text for term in expanded_terms):
            score += 0.3

    if sprint_refs and row["sprint_no"] in sprint_refs:
        score += 2.5

    return score


def _snippet(content: str, terms: list[str], max_chars: int = SNIPPET_MAX_CHARS) -> str:
    normalized_content = content.lower()
    best_pos = len(content)
    for term in terms:
        pos = normalized_content.find(term.lower())
        if 0 <= pos < best_pos:
            best_pos = pos
    if best_pos >= len(content):
        snippet = content[:max_chars].strip()
        return snippet + ("..." if len(content) > max_chars else "")
    start = max(0, best_pos - max_chars // 3)
    end = min(len(content), start + max_chars)
    snippet = content[start:end].strip()
    if start > 0:
        snippet = "..." + snippet
    if end < len(content):
        snippet = snippet + "..."
    return snippet


def search(
    query: str,
    db_path: Path = DEFAULT_DB,
    scope: str | None = None,
    n_results: int = 5,
    output_json: bool = False,
) -> list[dict[str, Any]]:
    del output_json  # kept for backward compatibility with callers
    _ensure_db(db_path)

    normalized_query = _normalize_text(query)
    query_terms = [term for term in ASCII_TOKEN_RE.findall(normalized_query)]
    matched_aliases, expanded_terms = expand_query_aliases(query)
    sprint_refs = _extract_sprint_refs(" ".join([normalized_query, *expanded_terms]))
    has_cjk_query = _has_cjk(normalized_query)

    search_plans: list[tuple[str, str, str]] = []
    raw_unicode = _build_unicode_match(normalized_query)
    if raw_unicode:
        search_plans.append(("raw_unicode", "docs_fts_unicode", raw_unicode))
    broad_unicode = _build_unicode_broad_match(normalized_query)
    if broad_unicode:
        search_plans.append(("broad_unicode", "docs_fts_unicode", broad_unicode))
    raw_trigram = _build_trigram_match(normalized_query)
    if raw_trigram:
        search_plans.append(("raw_trigram", "docs_fts_trigram", raw_trigram))
    broad_trigram = _build_trigram_broad_match(normalized_query)
    if broad_trigram:
        search_plans.append(("broad_trigram", "docs_fts_trigram", broad_trigram))
    expanded_unicode = _build_expansion_match(expanded_terms, backend="unicode")
    if expanded_unicode:
        search_plans.append(("expanded_unicode", "docs_fts_unicode", expanded_unicode))
    expanded_trigram = _build_expansion_match(expanded_terms, backend="trigram")
    if expanded_trigram:
        search_plans.append(("expanded_trigram", "docs_fts_trigram", expanded_trigram))

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row

    fused: dict[int, dict[str, Any]] = {}
    for source_name, table_name, match_expr in search_plans:
        rows = _fetch_candidates(
            conn,
            table=table_name,
            match_expr=match_expr,
            scope=scope,
            limit=CANDIDATE_LIMIT,
        )
        for rank_index, row in enumerate(rows, start=1):
            doc_id = row["id"]
            current = fused.setdefault(
                doc_id,
                {
                    "row": row,
                    "fusion_score": 0.0,
                    "sources": [],
                },
            )
            current["fusion_score"] += _source_weight(source_name, has_cjk_query) / (FUSION_K + rank_index)
            current["sources"].append(source_name)

    conn.close()

    results: list[dict[str, Any]] = []
    snippet_terms = [normalized_query, *matched_aliases, *expanded_terms, *query_terms]
    snippet_terms = [term for term in snippet_terms if term]

    for candidate in fused.values():
        row = candidate["row"]
        total_score = candidate["fusion_score"] + _field_boost(
            row,
            normalized_query=normalized_query,
            query_terms=query_terms,
            expanded_terms=expanded_terms,
            sprint_refs=sprint_refs,
        )
        results.append(
            {
                "scope": row["scope"],
                "path": row["path"],
                "title": row["title"],
                "score": round(total_score, 4),
                "snippet": _snippet(row["content"], snippet_terms),
                "_sources": candidate["sources"],
            }
        )

    results.sort(key=lambda item: (-item["score"], item["path"]))
    trimmed = [
        {
            "scope": item["scope"],
            "path": item["path"],
            "title": item["title"],
            "score": item["score"],
            "snippet": item["snippet"],
        }
        for item in results[:n_results]
    ]

    if not trimmed:
        miss_log = db_path.parent / "knowledge_miss.jsonl"
        entry = {"query": query, "scope": scope, "found": 0}
        try:
            with open(miss_log, "a", encoding="utf-8") as handle:
                handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except OSError:
            pass

    return trimmed


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Search project knowledge base",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("query", help="Search query (keywords or phrase)")
    parser.add_argument(
        "--scope",
        choices=["pitfalls", "sprint", "progress", "spec", "memory"],
        help="Limit search to a specific scope",
    )
    parser.add_argument("-n", "--num", type=int, default=5, help="Number of results (default: 5)")
    parser.add_argument("--json", action="store_true", dest="output_json", help="Output as JSON")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB, help="Database path")
    args = parser.parse_args()

    results = search(args.query, args.db, args.scope, args.num, args.output_json)

    if args.output_json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return

    if not results:
        print(f"No results for: {args.query}")
        if args.scope:
            print(f"  (scope: {args.scope})")
        print("\nQuery logged to data/knowledge_miss.jsonl for Phase 2 evaluation.")
        return

    print(f"Found {len(results)} results for: {args.query}")
    if args.scope:
        print(f"  (scope: {args.scope})")
    print()

    for idx, result in enumerate(results, start=1):
        print(f"  {idx}. [{result['scope']}] {result['title']}")
        print(f"     {result['path']}")
        print(f"     score={result['score']}")
        for line in textwrap.wrap(result["snippet"], width=80):
            print(f"     {line}")
        print()


if __name__ == "__main__":
    main()
