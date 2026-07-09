"""
Agent Spark · CLI Entry
========================
Unified CLI for knowledge base management and pipeline tasks.

Usage:
    agent-spark presets list                    # List all domains
    agent-spark presets show <domain>           # Show domain details
    agent-spark presets add <domain> ...        # Add custom presets
    agent-spark presets import <file.json>      # Batch import
    agent-spark run <domain> --json             # Full pipeline → JSON output
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from agent_spark import find_domain, list_domains, Filter
from agent_spark.locale import detect, _
from agent_spark.filter.five_layer_filter import five_layer_filter

_PRESETS_PATH = Path(__file__).resolve().parent / "presets" / "domains.json"


def _load_raw() -> list[dict[str, Any]]:
    try:
        return json.loads(_PRESETS_PATH.read_text("utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def _save_raw(data: list[dict[str, Any]]) -> None:
    _PRESETS_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), "utf-8"
    )


def cmd_presets_list(args: argparse.Namespace) -> None:
    """List all available domains with pain-point counts."""
    raw = _load_raw()
    loc = detect(*[p.get("domain", "") for p in raw])
    if not raw:
        print(_("No presets found.", "未找到预置数据。", loc))
        return
    print(_("Available domains:", "可用领域：", loc))
    print("─" * 50)
    for p in sorted(raw, key=lambda x: x["domain"]):
        name = p["domain"]
        cn = p.get("domain_zh", "")
        pains = len(p.get("pain_points", []))
        evidence = len(p.get("evidence", []))
        label = f"{name}  {cn}" if cn else name
        print(f"  {label:<40} {pains}p / {evidence}e")


def cmd_presets_show(args: argparse.Namespace) -> None:
    """Show details for a specific domain."""
    d = find_domain(args.domain)
    if not d:
        loc = detect(args.domain)
        print(_(f"Domain '{args.domain}' not found.", f"领域「{args.domain}」未找到。", loc))
        sys.exit(1)
    loc = detect(d.domain, *(d.pain_points or []))
    print(f"  {_('Domain:', '领域：', loc)}  {d.domain}  {d.domain_zh or ''}")
    print(f"  {_('Pain points:', '痛点：', loc)}")
    for i, p in enumerate(d.pain_points or [], 1):
        print(f"    {i}. {p}")
    print(f"  {_('Evidence:', '证据来源：', loc)}")
    for i, e in enumerate(d.evidence or [], 1):
        print(f"    {i}. {e}")


def cmd_presets_add(args: argparse.Namespace) -> None:
    """Add a new domain to the preset library."""
    raw = _load_raw()
    loc = detect(args.domain)

    # Check duplicate
    for p in raw:
        if p["domain"].lower() == args.domain.lower():
            print(_(f"Domain '{args.domain}' already exists.", f"领域「{args.domain}」已存在。", loc))
            sys.exit(1)

    pains = [p.strip() for p in args.pains.split(",") if p.strip()] if args.pains else []
    ev = [e.strip() for e in args.evidence.split(",") if e.strip()] if args.evidence else []

    entry = {
        "domain": args.domain.lower(),
        "domain_zh": args.zh or "",
        "pain_points": pains,
        "evidence": ev,
    }
    raw.append(entry)
    _save_raw(raw)
    print(_(f"Added '{args.domain}' ({len(pains)} pains, {len(ev)} evidence).",
            f"已添加「{args.domain}」（{len(pains)} 痛点，{len(ev)} 证据）。", loc))


def cmd_presets_import(args: argparse.Namespace) -> None:
    """Batch import presets from a JSON file."""
    try:
        data = json.loads(Path(args.file).read_text("utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading {args.file}: {e}")
        sys.exit(1)

    if not isinstance(data, list):
        print("JSON file must contain an array of domain objects.")
        sys.exit(1)

    raw = _load_raw()
    existing = {p["domain"].lower() for p in raw}
    added = 0
    skipped = 0

    for entry in data:
        name = entry.get("domain", "").lower()
        if not name:
            skipped += 1
            continue
        if name in existing:
            skipped += 1
            continue
        entry["domain"] = name
        entry.setdefault("domain_zh", "")
        entry.setdefault("pain_points", [])
        entry.setdefault("evidence", [])
        raw.append(entry)
        existing.add(name)
        added += 1

    _save_raw(raw)
    loc = detect(*[p.get("domain", "") for p in data])
    print(_(f"Imported {added} domains ({skipped} skipped).",
            f"导入 {added} 个领域（{skipped} 个跳过）。", loc))


def cmd_run(args: argparse.Namespace) -> None:
    """Run the full pipeline for a domain and output results."""
    d = find_domain(args.domain)
    if not d:
        loc = detect(args.domain)
        print(_(f"Domain '{args.domain}' not found.", f"领域「{args.domain}」未找到。", loc))
        sys.exit(1)

    loc = detect(d.domain, *(d.pain_points or []))
    results = Filter.run(
        d.ideas, d.pain_points, d.evidence,
        verbose=not args.json,
        locale=loc,
    )

    if args.json:
        output = {
            "domain": d.domain,
            "total": 1,
            "passed": len(results),
            "passed_ideas": [r["title"] for r in results],
            "reports": results,
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="agent-spark",
        description="Offline creative idea convergence engine for AI Agents.",
    )
    sub = parser.add_subparsers(dest="command")

    # presets
    p_presets = sub.add_parser("presets", help="Manage domain presets")
    psub = p_presets.add_subparsers(dest="action")

    p_list = psub.add_parser("list", help="List all domains")
    p_list.set_defaults(func=cmd_presets_list)

    p_show = psub.add_parser("show", help="Show domain details")
    p_show.add_argument("domain", help="Domain name")
    p_show.set_defaults(func=cmd_presets_show)

    p_add = psub.add_parser("add", help="Add a domain")
    p_add.add_argument("domain", help="Domain name (English)")
    p_add.add_argument("--zh", help="Chinese name", default="")
    p_add.add_argument("--pains", help="Comma-separated pain points", default="")
    p_add.add_argument("--evidence", help="Comma-separated evidence", default="")
    p_add.set_defaults(func=cmd_presets_add)

    p_import = psub.add_parser("import", help="Batch import from JSON")
    p_import.add_argument("file", help="JSON file path")
    p_import.set_defaults(func=cmd_presets_import)

    # run
    p_run = sub.add_parser("run", help="Run pipeline for a domain")
    p_run.add_argument("domain", help="Domain name")
    p_run.add_argument("--json", action="store_true", help="JSON output for CI/CD")
    p_run.add_argument("--locale", default=None, help="en or zh")
    p_run.set_defaults(func=cmd_run)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
