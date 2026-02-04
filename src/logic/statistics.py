import datetime
from pathlib import Path
from typing import Dict, List
from src.utils.cache import REPORTS_DIR, load_report


def collect_verifications_for_stock(
    stock_code: str, days_back: int = None
) -> List[Dict]:
    """
    Collect all verification results for a stock within specified days.

    Args:
        stock_code: Stock code
        days_back: Number of days to look back (None = all history)

    Returns:
        List of verification dicts
    """
    verifications = []

    if days_back:
        start_date = datetime.date.today() - datetime.timedelta(days=days_back)
    else:
        start_date = None

    for date_dir in sorted(REPORTS_DIR.glob("*")):
        if not date_dir.is_dir():
            continue

        try:
            date_str = date_dir.name
            report_date = datetime.datetime.strptime(date_str, "%Y%m%d").date()

            if start_date and report_date < start_date:
                continue

            report = load_report(date_str, stock_code)
            if report and "verification" in report:
                verifications.append(report["verification"])
        except Exception:
            continue

    return verifications


def calculate_multi_period_accuracy(stock_code: str) -> Dict[str, float]:
    """
    Calculate accuracy for multiple time periods.

    Args:
        stock_code: Stock code

    Returns:
        Dict with keys: '7d', '30d', 'all'
    """
    from src.logic.verification import calculate_accuracy_rate

    return {
        "7d": calculate_accuracy_rate(collect_verifications_for_stock(stock_code, 7)),
        "30d": calculate_accuracy_rate(collect_verifications_for_stock(stock_code, 30)),
        "all": calculate_accuracy_rate(collect_verifications_for_stock(stock_code)),
    }


def calculate_overall_accuracy(watchlist: List[str]) -> Dict[str, Dict]:
    """
    Calculate overall accuracy across all stocks in watchlist.

    Args:
        watchlist: List of stock codes

    Returns:
        Dict with overall stats and per-stock breakdown
    """
    from src.logic.verification import calculate_accuracy_rate

    all_verifications_7d = []
    all_verifications_30d = []
    all_verifications_all = []

    per_stock = {}

    for code in watchlist:
        verifications_7d = collect_verifications_for_stock(code, 7)
        verifications_30d = collect_verifications_for_stock(code, 30)
        verifications_all = collect_verifications_for_stock(code)

        all_verifications_7d.extend(verifications_7d)
        all_verifications_30d.extend(verifications_30d)
        all_verifications_all.extend(verifications_all)

        per_stock[code] = {
            "7d": calculate_accuracy_rate(verifications_7d),
            "30d": calculate_accuracy_rate(verifications_30d),
            "all": calculate_accuracy_rate(verifications_all),
            "count_7d": len(verifications_7d),
            "count_30d": len(verifications_30d),
            "count_all": len(verifications_all),
        }

    return {
        "overall": {
            "7d": calculate_accuracy_rate(all_verifications_7d),
            "30d": calculate_accuracy_rate(all_verifications_30d),
            "all": calculate_accuracy_rate(all_verifications_all),
            "count_7d": len(all_verifications_7d),
            "count_30d": len(all_verifications_30d),
            "count_all": len(all_verifications_all),
        },
        "per_stock": per_stock,
    }
