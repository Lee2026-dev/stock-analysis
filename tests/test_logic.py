import pytest
import pandas as pd
import numpy as np
from src.logic.indicators import calculate_indicators
from src.logic.backtest import run_backtest


@pytest.fixture
def sample_df():
    # Create 100 days of data
    dates = pd.date_range(start="2023-01-01", periods=100)
    # Sine wave to ensure crossovers
    x = np.linspace(0, 4 * np.pi, 100)
    prices = 100 + 10 * np.sin(x)

    df = pd.DataFrame(
        {
            "日期": dates,
            "收盘": prices,
            "最高": prices + 1,
            "最低": prices - 1,
            "成交量": 1000,
            "股票代码": "TEST",
        }
    )
    df.set_index("日期", inplace=True)
    return df


def test_indicators_calculation(sample_df):
    df_ind = calculate_indicators(sample_df)

    # Check columns
    expected = ["MA5", "MA20", "RSI", "MACD", "BOLL_UPPER", "K", "D", "J", "OBV"]
    for col in expected:
        assert col in df_ind.columns

    # Check values are not all NaN (after some warmup period)
    assert not df_ind["MA20"].iloc[20:].isna().all()


def test_backtest_execution(sample_df):
    # Calculate indicators first
    df_ind = calculate_indicators(sample_df)

    # Run backtest
    result = run_backtest(df_ind)

    # Check structure
    assert "win_rate" in result
    assert "total_return" in result
    assert "trades" in result
    assert isinstance(result["trades"], list)

    # With sine wave, we should have trades
    # MA5 crosses MA20 roughly every pi (25 points)
    assert result["total_trades"] > 0


def test_empty_dataframe():
    df = pd.DataFrame()
    res_ind = calculate_indicators(df)
    assert res_ind.empty

    res_back = run_backtest(df)
    assert res_back["total_trades"] == 0
