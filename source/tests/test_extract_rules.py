"""Unit tests for extract_rules (no RapidOCR)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from extract_rules import (
    extract_with_config,
    extraction_succeeded,
    load_extract_config,
)

_SOURCE = Path(__file__).resolve().parent.parent
_EXAMPLE_TR7 = _SOURCE / "examples" / "extract_config_tr7_like.json"


def test_load_extract_config_from_example():
    cfg = load_extract_config(_EXAMPLE_TR7)
    assert cfg["version"] == 1
    assert isinstance(cfg["fields"], list)
    assert cfg["fields"][0]["key"] == "temperature_c"


def test_load_extract_config_rejects_bad_version(tmp_path):
    p = tmp_path / "c.json"
    p.write_text(json.dumps({"version": 99, "fields": [{"key": "a", "regex": "."}]}), encoding="utf-8")
    with pytest.raises(ValueError, match="unsupported"):
        load_extract_config(p)


def test_extract_with_config_largest_bbox_first():
    cfg = {
        "version": 1,
        "name": "t",
        "strategy": "largest_bbox_first",
        "fields": [
            {"key": "temperature_c", "regex": r"(-?\d+\.?\d*)\s*°\s*C", "value_type": "float"},
            {"key": "humidity_percent", "regex": r"(-?\d+\.?\d*)\s*%", "value_type": "float"},
        ],
    }
    lines = [
        {"text": "noise 10°C", "bbox_area": 10.0},
        {"text": "30.0°C", "bbox_area": 500.0},
        {"text": "70%", "bbox_area": 400.0},
    ]
    out = extract_with_config(lines, cfg)
    assert out["fields"]["temperature_c"] == 30.0
    assert out["fields"]["humidity_percent"] == 70.0


def test_extract_with_config_unsupported_strategy():
    cfg = {"version": 1, "fields": [{"key": "a", "regex": "."}], "strategy": "other"}
    with pytest.raises(ValueError, match="unsupported strategy"):
        extract_with_config([], cfg)


def test_extraction_succeeded_all_required():
    cfg = {
        "fields": [{"key": "a"}, {"key": "b"}],
        "success_requires_all_fields": True,
    }
    ok = {"fields": {"a": 1, "b": 2}}
    bad = {"fields": {"a": 1, "b": None}}
    assert extraction_succeeded(cfg, ok) is True
    assert extraction_succeeded(cfg, bad) is False


def test_extraction_succeeded_required_fields_subset():
    cfg = {
        "fields": [{"key": "a"}, {"key": "b"}],
        "success_requires_all_fields": False,
        "required_fields": ["a"],
    }
    partial = {"fields": {"a": 1, "b": None}}
    assert extraction_succeeded(cfg, partial) is True
