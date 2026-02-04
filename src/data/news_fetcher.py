import akshare as ak
import pandas as pd
import streamlit as st
import requests
from typing import Optional


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_stock_news(symbol: str, limit: int = 5) -> pd.DataFrame:
    """
    Fetch stock news from EastMoney with fallback to JRJ (market news).

    Args:
        symbol: Stock code (e.g., "000001")
        limit: Number of news items to return

    Returns:
        pd.DataFrame: Columns ['日期', '标题', '内容', '来源', 'url']
    """
    try:
        df = ak.stock_news_em(symbol=symbol)

        if df is None or df.empty:
            raise ValueError("Empty news data")

        column_map = {
            "发布时间": "日期",
            "文章标题": "标题",
            "文章内容": "内容",
            "新闻来源": "来源",
            "文章链接": "url",
        }
        df = df.rename(columns=column_map)

        required = ["日期", "标题", "内容", "来源", "url"]
        for col in required:
            if col not in df.columns:
                df[col] = ""

        if "日期" in df.columns:
            df = df.sort_values("日期", ascending=False)

        return df.head(limit)[required]

    except Exception as e:
        print(f"Error fetching news for {symbol}: {e}")
        return pd.DataFrame(columns=["日期", "标题", "内容", "来源", "url"])


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_stock_announcements(symbol: str, limit: int = 3) -> pd.DataFrame:
    """
    Fetch stock announcements.
    """
    try:
        if hasattr(ak, "stock_notice_report_em"):
            df = ak.stock_notice_report_em(symbol=symbol)
        else:
            return pd.DataFrame(columns=["日期", "标题", "类型"])

        if df is None or df.empty:
            return pd.DataFrame(columns=["日期", "标题", "类型"])

        return df.head(limit)

    except Exception as e:
        print(f"Error fetching announcements for {symbol}: {e}")
        return pd.DataFrame(columns=["日期", "标题", "类型"])
