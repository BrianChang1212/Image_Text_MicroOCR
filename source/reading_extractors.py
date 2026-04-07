"""
Heuristic extractors for structured readings from per-line OCR results.

TR-7 / TR7-style monitor: large current temperature and humidity share the
biggest bounding boxes; smaller rows (High/Low, labels) are ignored when a
larger box already matched.
"""
from __future__ import annotations

import re
from typing import Any

# Allow optional space between degree sign and C (OCR variance).
TEMP_C_RE = re.compile(r"(-?\d+\.?\d*)\s*°\s*C", re.IGNORECASE)
# Humidity percentage (avoid matching unrelated % if line also has temp).
HUM_PCT_RE = re.compile(r"(-?\d+\.?\d*)\s*%")
# e.g. Mar-30-2026 11:29:20
TS_RE = re.compile(
    r"\b([A-Za-z]{3}-\d{1,2}-\d{4}\s+\d{1,2}:\d{2}:\d{2})\b"
)


def _bbox_area(boxes: Any, index: int) -> float | None:
    if boxes is None or index < 0:
        return None
    try:
        n = len(boxes)
    except TypeError:
        return None
    if index >= n:
        return None
    pts = boxes[index]
    xs = [float(p[0]) for p in pts]
    ys = [float(p[1]) for p in pts]
    w = max(xs) - min(xs)
    h = max(ys) - min(ys)
    return float(w * h)


def enrich_lines_with_area(result: Any, lines: list[dict[str, Any]]) -> None:
    boxes = getattr(result, "boxes", None)
    for item in lines:
        idx = item.get("index", 0)
        item["bbox_area"] = _bbox_area(boxes, idx)


def extract_tr7_monitor_readings(lines: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Pick current (large-display) temperature °C and humidity % by descending
    bbox_area, then regex on each line's text.
    """
    ranked = sorted(
        lines,
        key=lambda x: (x.get("bbox_area") is not None, x.get("bbox_area") or 0.0),
        reverse=True,
    )

    temp_c: float | None = None
    humidity_pct: float | None = None
    temp_line: str | None = None
    hum_line: str | None = None

    for item in ranked:
        text = item.get("text") or ""
        if temp_c is None:
            m = TEMP_C_RE.search(text)
            if m:
                temp_c = float(m.group(1))
                temp_line = text
        if humidity_pct is None:
            m = HUM_PCT_RE.search(text)
            if m:
                humidity_pct = float(m.group(1))
                hum_line = text
        if temp_c is not None and humidity_pct is not None:
            break

    timestamp: str | None = None
    for item in ranked:
        text = item.get("text") or ""
        m = TS_RE.search(text)
        if m:
            timestamp = m.group(1)
            break

    return {
        "preset": "tr7-monitor",
        "temperature_c": temp_c,
        "humidity_percent": humidity_pct,
        "timestamp": timestamp,
        "source_lines": {
            "temperature": temp_line,
            "humidity": hum_line,
        },
    }
