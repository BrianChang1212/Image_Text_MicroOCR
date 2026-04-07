"""Unit tests for reading_extractors (no RapidOCR)."""
from __future__ import annotations

from reading_extractors import extract_tr7_monitor_readings


def test_tr7_prefers_large_bbox_for_temp_and_humidity():
    lines = [
        {"text": "High 99.0°C", "bbox_area": 50.0, "index": 0},
        {"text": "25.7°C", "bbox_area": 800.0, "index": 1},
        {"text": "55.0%", "bbox_area": 750.0, "index": 2},
    ]
    out = extract_tr7_monitor_readings(lines)
    assert out["temperature_c"] == 25.7
    assert out["humidity_percent"] == 55.0
    assert out["source_lines"]["temperature"] == "25.7°C"
    assert out["source_lines"]["humidity"] == "55.0%"


def test_tr7_internal_temp_rh_labels():
    lines = [
        {"text": "Internal Temp: 28.5 °C", "bbox_area": 400.0, "index": 0},
        {"text": "Internal Humid: 40.0% RH", "bbox_area": 390.0, "index": 1},
    ]
    out = extract_tr7_monitor_readings(lines)
    assert out["temperature_c"] == 28.5
    assert out["humidity_percent"] == 40.0


def test_tr7_optional_space_before_c():
    lines = [
        {"text": "21.0 ° C", "bbox_area": 500.0, "index": 0},
        {"text": "60%", "bbox_area": 400.0, "index": 1},
    ]
    out = extract_tr7_monitor_readings(lines)
    assert out["temperature_c"] == 21.0
    assert out["humidity_percent"] == 60.0


def test_tr7_timestamp_when_present():
    lines = [
        {"text": "Mar-30-2026 11:29:20", "bbox_area": 100.0, "index": 0},
        {"text": "22.0°C", "bbox_area": 900.0, "index": 1},
        {"text": "50%", "bbox_area": 800.0, "index": 2},
    ]
    out = extract_tr7_monitor_readings(lines)
    assert out["timestamp"] == "Mar-30-2026 11:29:20"


def test_tr7_missing_readings():
    lines = [{"text": "SN: 1", "bbox_area": 10.0, "index": 0}]
    out = extract_tr7_monitor_readings(lines)
    assert out["temperature_c"] is None
    assert out["humidity_percent"] is None
