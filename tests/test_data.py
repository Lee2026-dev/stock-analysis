import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
import requests
from src.data.fetcher import (
    fetch_daily_history,
    fetch_northbound_flow,
    DAILY_HISTORY_COLUMNS,
    NORTHBOUND_FLOW_COLUMNS,
)


class TestFetcher:
    @patch("akshare.stock_zh_a_hist")
    def test_fetch_daily_history_success(self, mock_ak):
        fetch_daily_history.clear()
        # Setup mock return value
        mock_df = pd.DataFrame(
            {"日期": ["2023-01-01"], "股票代码": ["000001"], "收盘": [10.0]}
        )
        mock_ak.return_value = mock_df

        # Execute
        df = fetch_daily_history("000001", "20230101", "20230102")

        # Verify
        assert not df.empty
        assert "收盘" in df.columns
        mock_ak.assert_called_once()

    @patch("akshare.stock_zh_a_hist")
    def test_fetch_daily_history_failure(self, mock_ak):
        fetch_daily_history.clear()
        # Setup mock side effect (exception)
        mock_ak.side_effect = requests.exceptions.Timeout("Timeout")

        # Execute
        df = fetch_daily_history("000001", "20230101", "20230102")

        # Verify
        assert df.empty
        assert list(df.columns) == DAILY_HISTORY_COLUMNS

    @patch("akshare.stock_hsgt_hist_em")
    def test_fetch_northbound_success(self, mock_ak):
        fetch_northbound_flow.clear()
        mock_df = pd.DataFrame({"当日成交净买额": [1000]})
        mock_ak.return_value = mock_df

        df = fetch_northbound_flow()

        assert not df.empty
        assert "当日成交净买额" in df.columns

    @patch("akshare.stock_hsgt_hist_em")
    def test_fetch_northbound_failure(self, mock_ak):
        fetch_northbound_flow.clear()
        mock_ak.side_effect = Exception("API Error")

        df = fetch_northbound_flow()

        assert df.empty
        assert list(df.columns) == NORTHBOUND_FLOW_COLUMNS
