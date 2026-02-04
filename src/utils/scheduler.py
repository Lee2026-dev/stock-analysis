import datetime
import akshare as ak
import pandas as pd
from typing import List, Optional
from src.utils.cache import report_exists


def is_trading_day(date: Optional[datetime.date] = None) -> bool:
    """
    Check if a date is a trading day.
    """
    if date is None:
        date = datetime.date.today()

    try:
        df = ak.tool_trade_date_hist_sina()
        trade_dates = pd.to_datetime(df["trade_date"]).dt.date.tolist()
        return date in trade_dates
    except:
        return date.weekday() < 5


def should_generate_report(watchlist: Optional[List[str]] = None) -> bool:
    """
    Check if report generation should trigger.
    """
    now = datetime.datetime.now()

    if now.hour < 16:
        return False

    if not is_trading_day(now.date()):
        return False

    if watchlist and all_reports_exist_today(watchlist):
        return False

    return True


def all_reports_exist_today(watchlist: List[str]) -> bool:
    """
    Check if reports exist for all stocks in watchlist for today.
    """
    today_str = datetime.date.today().strftime("%Y%m%d")
    return all(report_exists(today_str, code) for code in watchlist)
