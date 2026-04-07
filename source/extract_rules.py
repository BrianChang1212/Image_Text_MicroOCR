"""
Load user-defined field extraction rules from JSON (per-line OCR + bbox strategy).
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


def load_extract_config(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        cfg = json.load(f)
    if not isinstance(cfg, dict):
        raise ValueError("extract config root must be a JSON object")
    ver = cfg.get("version", 1)
    if ver != 1:
        raise ValueError(f"unsupported extract config version: {ver}")
    fields = cfg.get("fields")
    if not isinstance(fields, list) or len(fields) < 1:
        raise ValueError('"fields" must be a non-empty array')
    for i, fd in enumerate(fields):
        if not isinstance(fd, dict) or "key" not in fd or "regex" not in fd:
            raise ValueError(f'fields[{i}] needs "key" and "regex"')
    return cfg


def _compile_field_regex(field: dict[str, Any]) -> re.Pattern[str]:
    flags = 0
    rf = field.get("regex_flags")
    if isinstance(rf, str):
        rf = [rf]
    if isinstance(rf, list):
        for fl in rf:
            s = str(fl).upper()
            if s in ("I", "IGNORECASE"):
                flags |= re.IGNORECASE
            if s in ("M", "MULTILINE"):
                flags |= re.MULTILINE
    return re.compile(field["regex"], flags)


def _coerce_value(raw: str, vtype: str) -> Any:
    t = (vtype or "float").lower()
    if t == "string":
        return raw
    if t == "int":
        return int(float(raw))
    if t == "float":
        return float(raw)
    raise ValueError(f"unknown value_type: {vtype}")


def _rank_lines(lines: list[dict[str, Any]]) -> list[dict[str, Any]]:
    strategy = "largest_bbox_first"
    return sorted(
        lines,
        key=lambda x: (x.get("bbox_area") is not None, x.get("bbox_area") or 0.0),
        reverse=True,
    )


def extract_with_config(
    lines: list[dict[str, Any]],
    cfg: dict[str, Any],
) -> dict[str, Any]:
    """
    strategy largest_bbox_first: scan OCR lines from largest bbox to smallest;
    for each rule, first regex match wins.
    """
    strategy = cfg.get("strategy", "largest_bbox_first")
    if strategy != "largest_bbox_first":
        raise ValueError(f'unsupported strategy "{strategy}" (only largest_bbox_first)')

    ranked = _rank_lines(lines)
    all_defs: list[dict[str, Any]] = list(cfg["fields"])
    opt = cfg.get("optional_fields")
    if isinstance(opt, list):
        all_defs = all_defs + opt

    fields_out: dict[str, Any] = {}
    sources_out: dict[str, str | None] = {}

    for fd in all_defs:
        key = str(fd["key"])
        cre = _compile_field_regex(fd)
        grp = int(fd.get("group", 1))
        vtype = fd.get("value_type", "float")
        fields_out[key] = None
        sources_out[key] = None
        for item in ranked:
            text = item.get("text") or ""
            m = cre.search(text)
            if not m:
                continue
            try:
                raw = m.group(grp)
            except IndexError as e:
                raise ValueError(f'field "{key}": regex has no group {grp}') from e
            try:
                fields_out[key] = _coerce_value(raw, vtype)
            except ValueError:
                fields_out[key] = raw
            sources_out[key] = text
            break

    return {
        "preset": cfg.get("name", "custom"),
        "config_name": cfg.get("name", "custom"),
        "fields": fields_out,
        "source_lines": sources_out,
    }


def extraction_succeeded(cfg: dict[str, Any], extracted: dict[str, Any]) -> bool:
    """True if all required field keys have non-None values."""
    if not cfg.get("success_requires_all_fields", True):
        req = cfg.get("required_fields")
        if isinstance(req, list) and req:
            vals = extracted.get("fields") or {}
            return all(vals.get(k) is not None for k in req)
        return True
    vals = extracted.get("fields") or {}
    for fd in cfg["fields"]:
        k = fd["key"]
        if vals.get(k) is None:
            return False
    return True
