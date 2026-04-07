#!/usr/bin/env python3
"""
Read an image with RapidOCR (ONNX micro-style stack), aggregate text, and
optionally verify expected phrases, regex patterns, or numeric substrings.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from extract_rules import (
    extraction_succeeded,
    extract_with_config,
    load_extract_config,
)
from reading_extractors import (
    enrich_lines_with_area,
    extract_tr7_monitor_readings,
)


def _load_expectations(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("expectations JSON root must be an object")
    return data


def _normalize(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip())


def _collect_lines(result: Any) -> list[dict[str, Any]]:
    lines: list[dict[str, Any]] = []
    txts = getattr(result, "txts", None) or ()
    scores = getattr(result, "scores", None) or ()
    for i, t in enumerate(txts):
        conf = float(scores[i]) if i < len(scores) else None
        lines.append({"text": t, "confidence": conf, "index": i})
    return lines


def _full_text(lines: list[dict[str, Any]], joiner: str = "\n") -> str:
    return joiner.join(item["text"] for item in lines)


def _verify(
    full: str,
    norm_full: str,
    exp: dict[str, Any],
) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    ok = True

    for key in ("must_contain_all", "must_contain"):
        phrases = exp.get(key)
        if not phrases:
            continue
        if isinstance(phrases, str):
            phrases = [phrases]
        for p in phrases:
            if p and p not in full and p not in norm_full:
                ok = False
                reasons.append(f"missing phrase: {p!r}")

    regex_list = exp.get("must_match_regex") or exp.get("regex_any")
    if regex_list:
        if isinstance(regex_list, str):
            regex_list = [regex_list]
        for pat in regex_list:
            if not pat:
                continue
            if not re.search(pat, full) and not re.search(pat, norm_full):
                ok = False
                reasons.append(f"regex not matched: {pat!r}")

    num_pat = exp.get("must_contain_number_regex")
    if num_pat:
        if not re.search(str(num_pat), full) and not re.search(
            str(num_pat), norm_full
        ):
            ok = False
            reasons.append(f"number regex not matched: {num_pat!r}")

    return ok, reasons


def _ensure_utf8_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, OSError):
            pass


def main() -> int:
    _ensure_utf8_stdio()
    parser = argparse.ArgumentParser(
        description="OCR image and optionally verify text/numbers (RapidOCR + ONNX)."
    )
    parser.add_argument(
        "image",
        type=str,
        help="Local image path or http(s) URL",
    )
    parser.add_argument(
        "--expect-json",
        type=Path,
        default=None,
        help="JSON file with must_contain / must_match_regex / must_contain_number_regex",
    )
    parser.add_argument(
        "--must-contain",
        action="append",
        default=[],
        help="Phrase that must appear in OCR text (repeatable)",
    )
    parser.add_argument(
        "--regex",
        action="append",
        default=[],
        help="At least one pattern must match (Python regex, repeatable)",
    )
    parser.add_argument(
        "--min-line-confidence",
        type=float,
        default=None,
        help="Fail if any line has confidence below this (0..1)",
    )
    parser.add_argument(
        "--dump-json",
        action="store_true",
        help="Print one JSON object with lines and verification to stdout",
    )
    parser.add_argument(
        "--plain",
        "-p",
        action="store_true",
        help="OCR only: print recognized text to stdout; no verification or stderr summary. Exit 0 if OCR runs.",
    )
    parser.add_argument(
        "--extract",
        choices=["tr7-monitor"],
        default=None,
        help="Built-in preset (e.g. tr7-monitor). Mutually exclusive with --extract-config.",
    )
    parser.add_argument(
        "--extract-config",
        type=Path,
        default=None,
        help="JSON file listing fields to extract (regex per field). See examples/extract_config_tr7_like.json.",
    )
    args = parser.parse_args()

    if args.extract and args.extract_config is not None:
        parser.error("Use either --extract or --extract-config, not both.")

    try:
        from rapidocr import RapidOCR
    except ImportError:
        print(
            "Missing dependency. Run: pip install -r requirements.txt",
            file=sys.stderr,
        )
        return 2

    engine = RapidOCR()
    result = engine(args.image)

    lines = _collect_lines(result)
    enrich_lines_with_area(result, lines)
    full = _full_text(lines)
    norm_full = _normalize(full)

    extract_cfg: dict[str, Any] | None = None
    extracted: dict[str, Any] | None = None
    if args.extract_config is not None:
        extract_cfg = load_extract_config(args.extract_config)
        extracted = extract_with_config(lines, extract_cfg)
    elif args.extract == "tr7-monitor":
        extracted = extract_tr7_monitor_readings(lines)

    exp: dict[str, Any] = {}
    if args.expect_json:
        exp = _load_expectations(args.expect_json)
    if args.must_contain:
        exp.setdefault("must_contain_all", []).extend(args.must_contain)
    if args.regex:
        exp.setdefault("must_match_regex", []).extend(args.regex)

    ok, reasons = _verify(full, norm_full, exp)

    threshold = args.min_line_confidence
    if threshold is None and exp.get("min_line_confidence") is not None:
        threshold = float(exp["min_line_confidence"])

    if threshold is not None:
        for item in lines:
            c = item.get("confidence")
            if c is not None and c < threshold:
                ok = False
                reasons.append(
                    f"line {item['index']} confidence {c:.4f} < {threshold}"
                )

    p = Path(args.image)
    image_ref = str(p.resolve()) if p.exists() and p.is_file() else args.image
    out: dict[str, Any] = {
        "image": image_ref,
        "ok": ok,
        "full_text": full,
        "lines": lines,
        "elapse_sec": getattr(result, "elapse", None),
        "verify_reasons": reasons,
    }
    if extracted is not None:
        out["extracted"] = extracted

    if args.dump_json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0 if ok else 1

    if (
        (args.extract or args.extract_config is not None)
        and not args.plain
        and not args.dump_json
    ):
        print(json.dumps(extracted, ensure_ascii=False, indent=2))
        if extracted is None:
            return 1
        if args.extract_config is not None and extract_cfg is not None:
            return 0 if extraction_succeeded(extract_cfg, extracted) else 1
        has_both = (
            extracted.get("temperature_c") is not None
            and extracted.get("humidity_percent") is not None
        )
        return 0 if has_both else 1

    if args.plain:
        print(full)
        return 0

    print(full)
    if reasons:
        print("--- verification ---", file=sys.stderr)
        for r in reasons:
            print(r, file=sys.stderr)
    print(f"VERIFY_OK={ok}", file=sys.stderr)

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
