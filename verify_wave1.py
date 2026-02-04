import sys
import pandas as pd
from src.data.news_fetcher import fetch_stock_news, fetch_stock_announcements
from src.logic.llm_agent import analyze_news_sentiment
from src.utils.cache import save_report, load_report, report_exists


def test_news_fetcher():
    print("Testing News Fetcher...")
    try:
        df = fetch_stock_news("000001", limit=2)
        print(f"News fetched: {len(df)} items")
        if not df.empty:
            print(df.columns)

        df_anno = fetch_stock_announcements("000001", limit=1)
        print(f"Announcements fetched: {len(df_anno)} items")
    except Exception as e:
        print(f"News fetcher failed: {e}")


def test_llm_agent():
    print("\nTesting LLM Agent...")
    news = [{"标题": "测试新闻", "内容": "公司业绩大增"}]
    result = analyze_news_sentiment(news, "平安银行")
    print(f"Sentiment result: {result}")


def test_cache():
    print("\nTesting Cache...")
    report = {"score": 88, "summary": "Test"}
    save_report(report, "20260204", "000001")

    loaded = load_report("20260204", "000001")
    if loaded and loaded["score"] == 88:
        print("Cache save/load passed")
    else:
        print("Cache save/load failed")

    if report_exists("20260204", "000001"):
        print("report_exists passed")
    else:
        print("report_exists failed")


if __name__ == "__main__":
    test_news_fetcher()
    test_llm_agent()
    test_cache()
