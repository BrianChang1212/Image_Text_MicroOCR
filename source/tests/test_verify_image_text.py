"""Unit tests for verify_image_text helpers (no RapidOCR)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

import verify_image_text as vit

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_SAMPLE_LABEL = _PROJECT_ROOT / "test" / "samples" / "sample_label.png"


def test_normalize_collapses_whitespace():
    assert vit._normalize("  a   b  \n c  ") == "a b c"


def test_verify_must_contain():
    ok, reasons = vit._verify("hello SN world", "hello SN world", {"must_contain_all": ["SN"]})
    assert ok is True
    assert reasons == []


def test_verify_must_contain_fails():
    ok, reasons = vit._verify("hello", "hello", {"must_contain_all": ["SN"]})
    assert ok is False
    assert any("SN" in r for r in reasons)


def test_verify_regex():
    ok, _ = vit._verify("id 8839201", "id 8839201", {"must_match_regex": [r"\d{4,}"]})
    assert ok is True


@pytest.mark.integration
def test_cli_plain_sample_label_exits_zero():
    if not _SAMPLE_LABEL.is_file():
        pytest.skip(f"missing sample: {_SAMPLE_LABEL}")
    script = Path(__file__).resolve().parent.parent / "verify_image_text.py"
    r = subprocess.run(
        [sys.executable, str(script), str(_SAMPLE_LABEL), "-p"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert r.returncode == 0
    assert "SN" in r.stdout
