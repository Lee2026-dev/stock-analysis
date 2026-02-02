import pandas as pd
import numpy as np


def run_backtest(df: pd.DataFrame) -> dict:
    """
    Run a simple backtest strategy (MA5 vs MA20 Crossover).

    Strategy:
    - Buy when MA5 crosses above MA20.
    - Sell when MA5 crosses below MA20.
    - Execution at Close price of signal day.

    Args:
        df: DataFrame with 'MA5', 'MA20', '收盘' columns.

    Returns:
        dict: {
            'win_rate': float (0.0 - 1.0),
            'total_return': float (percentage),
            'total_trades': int,
            'trades': list of dicts
        }
    """
    if df.empty or "MA5" not in df.columns or "MA20" not in df.columns:
        return {"win_rate": 0.0, "total_return": 0.0, "total_trades": 0, "trades": []}

    # 1. Generate Signals
    # Position: 1 = Long, 0 = Cash
    # We want to catch the crossover.
    # Current state: MA5 > MA20
    long_condition = df["MA5"] > df["MA20"]

    # Shift to find crossover points
    # Buy: Prev was False (MA5 <= MA20), Curr is True (MA5 > MA20)
    # Sell: Prev was True, Curr is False

    buy_signals = long_condition & (~long_condition.shift(1).fillna(False).astype(bool))
    sell_signals = (~long_condition) & (
        long_condition.shift(1).fillna(False).astype(bool)
    )

    # Iterate to match buys and sells
    trades = []
    active_trade = None

    # We iterate through the dataframe indices where signals occur
    # Combining indices to iterate chronologically
    signal_dates = sorted(
        list(set(df[buy_signals].index) | set(df[sell_signals].index))
    )

    for date in signal_dates:
        row = df.loc[date]
        price = row["收盘"]
        is_buy = buy_signals.loc[date]
        is_sell = sell_signals.loc[date]

        if is_buy and active_trade is None:
            active_trade = {
                "entry_date": date,
                "entry_price": price,
                "stock_code": row["股票代码"] if "股票代码" in row else "",
            }

        elif is_sell and active_trade is not None:
            active_trade["exit_date"] = date
            active_trade["exit_price"] = price
            active_trade["return"] = (
                price - active_trade["entry_price"]
            ) / active_trade["entry_price"]
            trades.append(active_trade)
            active_trade = None

    # Calculate metrics
    if not trades:
        return {"win_rate": 0.0, "total_return": 0.0, "total_trades": 0, "trades": []}

    winning_trades = [t for t in trades if t["return"] > 0]
    win_rate = len(winning_trades) / len(trades)

    # Simple accumulation of returns (non-compounded for simplicity or compounded?)
    # Let's do cumulative product for Total Return
    equity = 1.0
    for t in trades:
        equity *= 1 + t["return"]
    total_return = (equity - 1.0) * 100

    return {
        "win_rate": round(win_rate * 100, 2),  # Percentage
        "total_return": round(total_return, 2),  # Percentage
        "total_trades": len(trades),
        "trades": trades,
    }
