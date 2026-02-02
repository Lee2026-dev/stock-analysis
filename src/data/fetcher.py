import pandas as pd
import akshare as ak
import streamlit as st
import requests
from typing import Optional

# Define expected columns for fallback
DAILY_HISTORY_COLUMNS = [
    "日期",
    "股票代码",
    "开盘",
    "收盘",
    "最高",
    "最低",
    "成交量",
    "成交额",
    "振幅",
    "涨跌幅",
    "涨跌额",
    "换手率",
]

NORTHBOUND_FLOW_COLUMNS = [
    "日期",
    "当日成交净买额",
    "买入成交额",
    "卖出成交额",
    "历史累计净买额",
    "当日资金流入",
    "当日余额",
    "持股市值",
    "领涨股",
    "领涨股-涨跌幅",
    "沪深300",
    "沪深300-涨跌幅",
    "领涨股-代码",
]


@st.cache_data(ttl=60, show_spinner=False)
def fetch_daily_history(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetch daily stock history from Akshare (Forward Adjusted - qfq).

    Args:
        symbol: Stock code (e.g., "000001")
        start_date: Start date in "YYYYMMDD" format
        end_date: End date in "YYYYMMDD" format

    Returns:
        pd.DataFrame: Stock history or empty DataFrame on failure
    """
    try:
        # qfq = forward adjusted (前复权)
        df = ak.stock_zh_a_hist(
            symbol=symbol,
            period="daily",
            start_date=start_date,
            end_date=end_date,
            adjust="qfq",
            timeout=5.0,  # Set explicit timeout
        )
        return df
    except (requests.exceptions.RequestException, Exception) as e:
        # Log error in console (production would use a logger)
        print(f"Error fetching daily history for {symbol}: {e}")
        # Return empty DataFrame with expected schema
        return pd.DataFrame(columns=DAILY_HISTORY_COLUMNS)


@st.cache_data(ttl=300, show_spinner=False)
def fetch_northbound_flow(symbol: str = "北向资金") -> pd.DataFrame:
    """
    Fetch Northbound Fund Flow data.

    Args:
        symbol: "北向资金" (default), "沪股通", or "深股通"

    Returns:
        pd.DataFrame: Fund flow history or empty DataFrame on failure
    """
    try:
        # Note: stock_hsgt_hist_em may not support timeout param directly
        # depending on version, but we wrap in try/except anyway.
        df = ak.stock_hsgt_hist_em(symbol=symbol)
        return df
    except (requests.exceptions.RequestException, Exception) as e:
        print(f"Error fetching northbound flow: {e}")
        return pd.DataFrame(columns=NORTHBOUND_FLOW_COLUMNS)
