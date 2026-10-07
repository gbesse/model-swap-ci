#!/usr/bin/env python3
"""Compare requested reasoning with Magpie route logs and Codex model metadata."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

TEXT = {
    "en": {"title": "Reasoning route parity", "mismatch": "Requested and routed efforts differ",
           "matched": "Requested and routed efforts match", "inconclusive": "Evidence is incomplete",
           "error": "Invalid capture"},
    "fr": {"title": "Parité du raisonnement routé", "mismatch": "Niveaux demandé et transmis différents",
           "matched": "Niveaux demandé et transmis identiques", "inconclusive": "Preuves incomplètes",
           "error": "Capture invalide"},
    "es": {"title": "Paridad del razonamiento en rutas", "mismatch": "Niveles solicitado y transmitido distintos",
           "matched": "Niveles solicitado y transmitido iguales", "inconclusive": "Pruebas incompletas",
           "error": "Captura no válida"},
}


def model_index(cache):
    models = cache.get("models") if isinstance(cache, dict) else None
    if not isinstance(models, list):
        raise ValueError("models_cache.json must contain a models array")
    return {item["slug"]: item for item in models
            if isinstance(item, dict) and isinstance(item.get("slug"), str)}


def route_effort(route):
    if not isinstance(route, dict):
        raise ValueError("route must be an object")
    selected = route.get("effort")
    tries = route.get("tries", [])
    if not isinstance(tries, list):
        raise ValueError("route.tries must be an array")
    transmitted = [row.get("effort") for row in tries
                   if isinstance(row, dict) and row.get("status") == 200]
    if len(transmitted) > 1 and len(set(transmitted)) > 1:
        return None  # The capture does not identify one comparable upstream request.
    if transmitted and selected is not None and transmitted[-1] != selected:
        return None
    # A failed route cannot establish what an upstream model received.
    value = transmitted[-1] if transmitted else (None if tries else selected)
    return value if isinstance(value, str) and value else None


def audit_case(case, models):
    identifier = case["id"]
    requested = case["requested_effort"]
    if not isinstance(identifier, str) or not identifier:
        raise ValueError("case id must be a nonempty string")
    if requested not in ("none", "ultra"):
        raise ValueError("requested_effort must be none or ultra")
    expected = "none" if requested == "none" else None
    catalog_gap = None
    if requested == "ultra":
        official = models.get(case.get("official_slug"))
        routed = models.get(case.get("candidate_slug"))
        if official and routed:
            expected = official.get("multi_agent_reasoning_effort")
            catalog_gap = routed.get("multi_agent_reasoning_effort") != expected
        baseline = route_effort(case["baseline_route"]) if "baseline_route" in case else None
        if baseline != expected:
            expected = None
    observed = route_effort(case["candidate_route"])
    status = "inconclusive" if expected is None or observed is None else (
        "matched" if observed == expected else "mismatch")
    return {"id": identifier, "status": status, "requested": requested,
            "expected_upstream": expected, "observed_route": observed,
            "candidate_catalog_differs": catalog_gap}


def audit(cases, cache):
    if not isinstance(cases, dict) or not isinstance(cases.get("cases"), list) or not cases["cases"]:
        raise ValueError("cases must be a nonempty array")
    models = model_index(cache)
    rows = [audit_case(case, models) for case in cases["cases"]]
    status = "mismatch" if any(row["status"] == "mismatch" for row in rows) else (
        "inconclusive" if any(row["status"] == "inconclusive" for row in rows) else "matched")
    return {"status": status, "cases": rows,
            "note": "The route log shows selected effort, not provider-internal reasoning or billed tokens."}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("reasoning-demo", "reasoning-check"))
    parser.add_argument("cases", nargs="?", type=Path)
    parser.add_argument("--models-cache", type=Path)
    parser.add_argument("--lang", choices=TEXT, default="en")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    if args.command == "reasoning-demo":
        base = Path(__file__).parent / "examples"
        cases_path, cache_path = base / "reasoning-cases.json", base / "models-cache-sample.json"
    else:
        if args.cases is None or args.models_cache is None:
            parser.error("reasoning-check requires CASES.json and --models-cache PATH")
        cases_path, cache_path = args.cases, args.models_cache
    try:
        cases = json.loads(cases_path.read_text(encoding="utf-8"))
        cache = json.loads(cache_path.read_text(encoding="utf-8"))
        report = audit(cases, cache)
    except (OSError, UnicodeError, ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
        print(f"{TEXT[args.lang]['error']}: {error}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        words = TEXT[args.lang]
        print(words["title"])
        for row in report["cases"]:
            print(f"{row['id']}: {words[row['status']]} "
                  f"({row['expected_upstream'] or '?'} → {row['observed_route'] or '?'})")
    if args.command == "reasoning-demo":
        return 0 if all(row["status"] == "mismatch" for row in report["cases"]) else 1
    return {"matched": 0, "mismatch": 2, "inconclusive": 3}[report["status"]]


if __name__ == "__main__":
    raise SystemExit(main())
