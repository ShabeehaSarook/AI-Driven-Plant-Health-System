"""PDF report file management utilities."""

from __future__ import annotations

import os
import time
from datetime import datetime
from typing import Optional


def ensure_reports_dir(reports_dir: str) -> None:
    os.makedirs(reports_dir, exist_ok=True)


def cleanup_reports(reports_dir: str, retention_days: int) -> int:
    """Delete report files older than retention_days.

    Returns number of deleted files.
    """
    if retention_days <= 0:
        return 0

    ensure_reports_dir(reports_dir)

    now = time.time()
    cutoff = now - (retention_days * 24 * 60 * 60)

    deleted = 0
    for name in os.listdir(reports_dir):
        if not name.lower().endswith(".pdf"):
            continue
        path = os.path.join(reports_dir, name)
        try:
            if not os.path.isfile(path):
                continue
            mtime = os.path.getmtime(path)
            if mtime < cutoff:
                os.remove(path)
                deleted += 1
        except Exception:
            # Best-effort cleanup
            continue

    return deleted


def unique_report_filename(prefix: str = "plant_health_report") -> str:
    """Generate a unique, filesystem-safe filename."""
    # Include microseconds for uniqueness, but still add a pid/time-based uniqueness.
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")
    return f"{prefix}_{ts}.pdf"
