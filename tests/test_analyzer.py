import pytest
import pandas as pd
import numpy as np
from src.logic.analyzer import calculate_technical_score


class TestAnalyzer:
    def test_calculate_score_insufficient_data(self):
        df = pd.DataFrame({"MA5": [1, 2, 3]})
        result = calculate_technical_score(df)
        assert result["score"] == 50
        assert "数据不足" in result["signals"]

    def test_calculate_score_bullish(self):
        # Create a bullish scenario
        # MA5 > MA20 (+20)
        # MACD_HIST > 0 (+15)
        # 30 < RSI < 70 (+20)
        # Close > BOLL_LOWER (+10)
        # Volume > MA5_Volume (+10)
        # K > D (+15)
        # Base (+10)
        # Total = 100

        data = {
            "MA5": [105.0] * 25,
            "MA20": [100.0] * 25,
            "MACD_HIST": [1.0] * 25,
            "RSI": [50.0] * 25,
            "收盘": [110.0] * 25,
            "BOLL_LOWER": [100.0] * 25,
            "成交量": [2000.0] * 25,
            "K": [50.0] * 25,
            "D": [40.0] * 25,
        }
        df = pd.DataFrame(data)

        # Ensure volume MA check works (current vol > rolling mean)
        # Make previous volumes smaller so rolling mean < current
        df.loc[:20, "成交量"] = 1000.0

        result = calculate_technical_score(df)

        assert result["score"] >= 90  # Depending on exact implementation details
        assert "MA5多头排列" in result["signals"]
        assert "MACD红柱" in result["signals"]
        assert "RSI正常区间" in result["signals"]

    def test_calculate_score_bearish(self):
        # Create a bearish scenario
        # MA5 < MA20
        # MACD_HIST < 0
        # RSI > 70 (-10)
        # Close < BOLL_LOWER
        # K < D

        data = {
            "MA5": [90.0] * 25,
            "MA20": [100.0] * 25,
            "MACD_HIST": [-1.0] * 25,
            "RSI": [80.0] * 25,
            "收盘": [80.0] * 25,
            "BOLL_LOWER": [85.0] * 25,
            "成交量": [1000.0] * 25,
            "K": [30.0] * 25,
            "D": [40.0] * 25,
        }
        df = pd.DataFrame(data)

        result = calculate_technical_score(df)

        assert result["score"] < 50
        assert "MA5空头排列" in result["signals"]
        assert "MACD绿柱" in result["signals"]
        assert "RSI超买" in result["signals"]
