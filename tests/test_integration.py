import pytest
import datetime
import os
import json
from unittest.mock import patch, MagicMock
from src.logic.report_engine import generate_report_for_stock
from src.utils.cache import save_report, load_report, report_exists


class TestIntegration:
    @patch("src.logic.report_engine.fetch_daily_history")
    @patch("src.logic.report_engine.fetch_stock_news")
    @patch("src.logic.report_engine.analyze_news_sentiment")
    def test_full_report_flow(self, mock_sentiment, mock_news, mock_history):
        # 1. Setup Mocks
        # History
        import pandas as pd

        mock_history.return_value = pd.DataFrame(
            {
                "日期": ["2026-02-01", "2026-02-02", "2026-02-03", "2026-02-04"],
                "收盘": [10.0, 10.5, 10.2, 10.8],
                "最高": [10.5, 10.8, 10.5, 11.0],
                "最低": [9.8, 10.0, 10.0, 10.2],
                "成交量": [1000, 1200, 800, 1500],
                "涨跌幅": [0.0, 5.0, -2.8, 5.8],
            }
        )

        # News
        mock_news.return_value = pd.DataFrame(
            [
                {
                    "日期": "2026-02-04",
                    "标题": "Test News",
                    "内容": "Content",
                    "来源": "Source",
                    "url": "http://test.com",
                }
            ]
        )

        # LLM
        mock_sentiment.return_value = {
            "sentiment_score": 80,
            "summary": "Positive outlook",
            "key_catalysts": ["Growth"],
            "risk_warnings": [],
        }

        # 2. Execute Generation
        code = "000001"
        date = "20260204"
        report = generate_report_for_stock(code, date)

        # 3. Verify Report Content
        assert report["stock_code"] == code
        assert report["technical_analysis"]["score"] > 0
        assert report["news_analysis"]["sentiment_score"] == 80
        assert report["prediction"]["up_probability"] > 50

        # 4. Test Persistence
        save_report(report, date, code)
        assert report_exists(date, code)

        loaded = load_report(date, code)
        assert loaded["news_analysis"]["summary"] == "Positive outlook"

        # Clean up
        path = f".sisyphus/reports/{date}/{code}.json"
        if os.path.exists(path):
            os.remove(path)
