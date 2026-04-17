#!/usr/bin/env python3
"""
Golden-query regression harness for knowledge search quality.

Validates that the FTS5 knowledge search meets quality gates:
- Overall hit@3 >= configured threshold (default 90%)
- Per-bucket hit@3 (e.g., chinese concept queries >= 80%)
- Scope filter correctness = 100%
- Alias expansion correctness

Usage:
    python3 -m scripts.qa.golden_query_test
    python3 -m scripts.qa.golden_query_test --threshold 80

Customize: Edit GOLDEN_CASES and ALIAS_CHECKS below for your project.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from scripts.qa.search import DEFAULT_DB, expand_query_aliases, search


@dataclass(frozen=True)
class GoldenCase:
    query: str
    expected_paths: tuple[str, ...]  # any of these paths in top-k = hit
    bucket: str = "general"          # for per-bucket reporting
    scope: str | None = None         # optional scope filter


@dataclass(frozen=True)
class AliasCheck:
    query: str
    required_terms: tuple[str, ...]  # alias expansion must include these


# ============================================================================
# CUSTOMIZE THESE FOR YOUR PROJECT
# ============================================================================

ALIAS_CHECKS: tuple[AliasCheck, ...] = (
    # Example: AliasCheck(query="price precision", required_terms=("tick_size", "decimal")),
)

GOLDEN_CASES: tuple[GoldenCase, ...] = (
    # Example cases — replace with your project's queries and expected docs:
    #
    # GoldenCase(
    #     query="deployment process",
    #     expected_paths=("docs/spec/deploy_contract.md",),
    # ),
    # GoldenCase(
    #     query="price precision",
    #     bucket="chinese",
    #     expected_paths=("docs/sprint/sprint22.md",),
    # ),
    # GoldenCase(
    #     query="config parameter",
    #     bucket="memory",
    #     scope="memory",
    #     expected_paths=("memory/project_runtime_parameters.md",),
    # ),
)


# ============================================================================
# HARNESS (no project-specific logic below)
# ============================================================================

def _matches_expected(path: str, expected_paths: tuple[str, ...]) -> bool:
    return any(expected in path for expected in expected_paths)


def run_golden_queries(db_path: Path, top_k: int = 3) -> dict[str, Any]:
    cases_out: list[dict[str, Any]] = []
    alias_checks_out: list[dict[str, Any]] = []
    overall_hits = 0
    bucket_hits: dict[str, int] = {}
    bucket_totals: dict[str, int] = {}
    scope_ok = True

    for alias_check in ALIAS_CHECKS:
        _, expanded_terms = expand_query_aliases(alias_check.query)
        missing = [t for t in alias_check.required_terms if t not in expanded_terms]
        alias_checks_out.append({
            "query": alias_check.query,
            "required": list(alias_check.required_terms),
            "expanded": expanded_terms,
            "missing": missing,
            "ok": len(missing) == 0,
        })

    for case in GOLDEN_CASES:
        results = search(case.query, db_path=db_path, scope=case.scope, n_results=top_k)
        got_paths = [r["path"] for r in results]
        hit = any(_matches_expected(p, case.expected_paths) for p in got_paths)

        if hit:
            overall_hits += 1
        bucket_totals[case.bucket] = bucket_totals.get(case.bucket, 0) + 1
        if hit:
            bucket_hits[case.bucket] = bucket_hits.get(case.bucket, 0) + 1

        if case.scope and results:
            for r in results:
                if r.get("scope") != case.scope:
                    scope_ok = False

        cases_out.append({
            "query": case.query,
            "scope": case.scope,
            "bucket": case.bucket,
            "hit": hit,
            "expected_any_of": list(case.expected_paths),
            "got_top": got_paths,
        })

    total = len(GOLDEN_CASES)
    overall_rate = (overall_hits / total * 100) if total > 0 else 100.0
    bucket_rates = {
        b: (bucket_hits.get(b, 0) / bucket_totals[b] * 100) if bucket_totals[b] > 0 else 100.0
        for b in bucket_totals
    }

    return {
        "overall_hit_rate": overall_rate,
        "overall_hits": overall_hits,
        "overall_total": total,
        "bucket_rates": bucket_rates,
        "scope_ok": scope_ok,
        "alias_checks": alias_checks_out,
        "cases": cases_out,
    }


def main():
    parser = argparse.ArgumentParser(description="Golden-query regression test")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--threshold", type=float, default=90.0, help="Overall hit@k threshold %%")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if not GOLDEN_CASES:
        print("No golden cases defined. Edit GOLDEN_CASES in this file for your project.")
        print("See examples in the comments above.")
        sys.exit(0)

    result = run_golden_queries(args.db, args.top_k)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    bucket_str = ", ".join(f"{b}={r:.0f}%" for b, r in result["bucket_rates"].items())
    print(
        f"Golden query test: overall hit@{args.top_k}={result['overall_hit_rate']:.1f}% "
        f"({result['overall_hits']}/{result['overall_total']}), "
        f"{bucket_str}, scope_ok={result['scope_ok']}"
    )

    for ac in result["alias_checks"]:
        status = "OK" if ac["ok"] else f"MISSING {ac['missing']}"
        print(f"  ALIAS {ac['query']!r} → {status}")

    for case in result["cases"]:
        if not case["hit"]:
            print(
                f"  MISS query={case['query']!r} scope={case['scope']} "
                f"expected_any_of={case['expected_any_of']} got_top={case['got_top']}"
            )

    passed = result["overall_hit_rate"] >= args.threshold
    if not passed:
        print(f"\nFAILED: {result['overall_hit_rate']:.1f}% < {args.threshold}% threshold")
        sys.exit(1)


if __name__ == "__main__":
    main()
