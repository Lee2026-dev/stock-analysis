import pandas as pd
import datetime
import streamlit as st
from typing import Dict, List, Any

from src.data.fetcher import fetch_daily_history, fetch_northbound_flow
from src.data.news_fetcher import fetch_stock_news
from src.logic.indicators import calculate_indicators
from src.logic.analyzer import calculate_technical_score
from src.logic.llm_agent import analyze_news_sentiment
from src.logic.verification import verify_prediction
from src.utils.cache import save_report, load_previous_report


def generate_report_for_stock(stock_code: str, date: str) -> Dict[str, Any]:
    """
    Generate comprehensive daily report for a single stock.
    """
    end_date = date
    start_date = (
        datetime.datetime.strptime(date, "%Y%m%d") - datetime.timedelta(days=100)
    ).strftime("%Y%m%d")
    df = fetch_daily_history(stock_code, start_date, end_date)

    if df.empty:
        return {"error": "No price data"}

    df = calculate_indicators(df)

    tech_result = calculate_technical_score(df)
    tech_score = tech_result["score"]

    news_df = fetch_stock_news(stock_code, limit=5)
    news_list = news_df.to_dict("records")

    stock_name = stock_code

    sentiment_result = analyze_news_sentiment(news_list, stock_name)
    sentiment_score = sentiment_result.get("sentiment_score", 50)

    up_prob = tech_score * 0.6 + sentiment_score * 0.4
    up_prob = min(99, max(1, int(up_prob)))

    report = {
        "stock_code": stock_code,
        "date": date,
        "technical_analysis": {
            "score": tech_score,
            "signals": tech_result["signals"],
            "last_close": float(df.iloc[-1]["收盘"]),
            "change_pct": float(df.iloc[-1]["涨跌幅"]),
        },
        "news_analysis": sentiment_result,
        "prediction": {"up_probability": up_prob, "down_probability": 100 - up_prob},
        "generated_at": datetime.datetime.now().isoformat(),
    }

    prev_report = load_previous_report(date, stock_code)
    if prev_report:
        verification = verify_prediction(prev_report, report)
        if verification:
            report["verification"] = verification

    return report


def generate_all_reports(watchlist: List[str]) -> None:
    """
    Generate reports for all stocks in watchlist.
    """
    date_str = datetime.date.today().strftime("%Y%m%d")

    progress_bar = st.progress(0)
    status_text = st.empty()

    total = len(watchlist)
    for i, code in enumerate(watchlist):
        status_text.text(f"正在分析 {code} ({i + 1}/{total})...")
        try:
            report = generate_report_for_stock(code, date_str)
            save_report(report, date_str, code)
        except Exception as e:
            print(f"Failed to generate report for {code}: {e}")

        progress_bar.progress((i + 1) / total)

    status_text.text(f"分析完成！共 {total} 只股票。")
