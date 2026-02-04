import json
import os
from pathlib import Path
from typing import Dict, Optional

REPORTS_DIR = Path(".sisyphus/reports")


def get_report_path(date: str, stock_code: str) -> Path:
    return REPORTS_DIR / date / f"{stock_code}.json"


def save_report(report: Dict, date: str, stock_code: str) -> None:
    path = get_report_path(date, stock_code)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)


def load_report(date: str, stock_code: str) -> Optional[Dict]:
    path = get_report_path(date, stock_code)
    if not path.exists():
        return None

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading report {path}: {e}")
        return None


def report_exists(date: str, stock_code: str) -> bool:
    return get_report_path(date, stock_code).exists()


def load_previous_report(date: str, stock_code: str) -> Optional[Dict]:
    """
    Load report from previous trading day.

    Args:
        date: Current date in YYYYMMDD format
        stock_code: Stock code

    Returns:
        Previous day's report if exists, None otherwise
    """
    from datetime import datetime, timedelta

    current_date = datetime.strptime(date, "%Y%m%d")

    for days_back in range(1, 8):
        prev_date = current_date - timedelta(days=days_back)
        prev_date_str = prev_date.strftime("%Y%m%d")

        prev_report = load_report(prev_date_str, stock_code)
        if prev_report is not None:
            return prev_report

    return None
