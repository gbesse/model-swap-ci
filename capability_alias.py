#!/usr/bin/env python3
"""Check explicit relay aliases against a saved model capability catalog."""

import argparse
import json
import sys
from pathlib import Path

FIELDS = ("reasoning", "vision", "context_window", "tool_calling")
WORDS = {
    "en": {"match": "Alias capabilities match", "mismatch": "Alias capabilities differ", "inconclusive": "Capability evidence is incomplete", "invalid": "Invalid catalog"},
    "fr": {"match": "Capacités de l’alias identiques", "mismatch": "Capacités de l’alias différentes", "inconclusive": "Preuve de capacités incomplète", "invalid": "Catalogue invalide"},
    "es": {"match": "Capacidades del alias iguales", "mismatch": "Capacidades del alias distintas", "inconclusive": "Evidencia de capacidades incompleta", "invalid": "Catálogo no válido"},
}


def inspect(mapping, catalog):
    if not isinstance(mapping, dict) or not isinstance(catalog, dict):
        raise ValueError("objects required")
    routed, baseline = mapping.get("routed_id"), mapping.get("catalog_id")
    if not all(isinstance(x, str) and x for x in (routed, baseline)):
        raise ValueError("explicit routed_id and catalog_id required")
    models = catalog.get("models")
    if not isinstance(models, dict):
        raise ValueError("models object required")
    actual, expected = models.get(routed), models.get(baseline)
    if not isinstance(actual, dict) or not isinstance(expected, dict):
        return {"status": "inconclusive", "missing_models": [x for x, value in ((routed, actual), (baseline, expected)) if not isinstance(value, dict)]}
    missing = [key for key in FIELDS if key not in actual or key not in expected]
    if missing:
        return {"status": "inconclusive", "missing_fields": missing}
    differences = [key for key in FIELDS if actual[key] != expected[key]]
    return {"status": "mismatch" if differences else "match", "different_fields": differences,
            "routed_id": routed, "catalog_id": baseline}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("demo", "check"))
    parser.add_argument("--mapping", type=Path)
    parser.add_argument("--catalog", type=Path)
    parser.add_argument("--lang", choices=WORDS, default="en")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "demo":
            mapping = {"routed_id": "relay/deepseek[1M]", "catalog_id": "deepseek"}
            catalog = {"models": {"deepseek": {"reasoning": True, "vision": False, "context_window": 1000000, "tool_calling": True},
                                   "relay/deepseek[1M]": {"reasoning": False, "vision": False, "context_window": 1000000, "tool_calling": True}}}
        else:
            if not args.mapping or not args.catalog:
                parser.error("check requires --mapping and --catalog")
            mapping = json.loads(args.mapping.read_text(encoding="utf-8"))
            catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
        result = inspect(mapping, catalog)
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as error:
        print(f"{WORDS[args.lang]['invalid']}: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False) if args.json else WORDS[args.lang][result["status"]])
    return 0 if args.command == "demo" or result["status"] == "match" else 2


if __name__ == "__main__":
    raise SystemExit(main())
