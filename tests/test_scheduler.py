import pytest
import datetime
from unittest.mock import patch, MagicMock
from src.utils.scheduler import is_trading_day, should_generate_report


class TestScheduler:
    @patch("akshare.tool_trade_date_hist_sina")
    def test_is_trading_day_api_success(self, mock_ak):
        import pandas as pd

        mock_ak.return_value = pd.DataFrame({"trade_date": [datetime.date(2026, 2, 4)]})

        assert is_trading_day(datetime.date(2026, 2, 4)) == True
        assert is_trading_day(datetime.date(2026, 2, 5)) == False

    @patch("akshare.tool_trade_date_hist_sina")
    def test_is_trading_day_api_fail(self, mock_ak):
        mock_ak.side_effect = Exception("API Error")

        # 2026-02-04 is Wednesday (weekday 2) -> True
        assert is_trading_day(datetime.date(2026, 2, 4)) == True
        # 2026-02-07 is Saturday (weekday 5) -> False
        assert is_trading_day(datetime.date(2026, 2, 7)) == False

    @patch("src.utils.scheduler.is_trading_day")
    @patch("src.utils.scheduler.datetime")
    def test_should_generate_report(self, mock_datetime_mod, mock_is_trading):
        # We need to mock datetime.datetime.now()
        # In src.utils.scheduler, it calls datetime.datetime.now()

        # Create a mock for 'now' object
        mock_now = MagicMock()

        # Configure the mock chain: datetime.datetime.now() returns mock_now
        mock_datetime_mod.datetime.now.return_value = mock_now

        # Case 1: Early morning (10:00)
        mock_now.hour = 10
        mock_now.date.return_value = datetime.date(2026, 2, 4)

        assert should_generate_report() == False

        # Case 2: After 16:00, Trading Day
        mock_now.hour = 16
        mock_is_trading.return_value = True
        assert should_generate_report() == True

        # Case 3: After 16:00, Non-Trading Day
        mock_is_trading.return_value = False
        assert should_generate_report() == False
