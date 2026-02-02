import pandas as pd
import numpy as np


def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate technical indicators for the stock DataFrame.

    Expected columns: '收盘' (Close), '最高' (High), '最低' (Low), '成交量' (Volume)

    Adds:
    - MA5, MA20
    - RSI (14)
    - MACD, MACD_SIGNAL, MACD_HIST (12, 26, 9)
    - BOLL_UPPER, BOLL_MID, BOLL_LOWER (20, 2)
    - K, D, J (9, 3, 3)
    - OBV

    Returns:
        pd.DataFrame: DataFrame with added indicator columns
    """
    if df.empty:
        return df

    df = df.copy()

    # Ensure columns exist
    required_cols = ["收盘", "最高", "最低", "成交量"]
    if not all(col in df.columns for col in required_cols):
        # Fallback if columns missing (e.g. index data might differ)
        return df

    close = df["收盘"]
    high = df["最高"]
    low = df["最低"]
    volume = df["成交量"]

    # 1. Moving Averages
    df["MA5"] = close.rolling(window=5).mean()
    df["MA20"] = close.rolling(window=20).mean()

    # 2. RSI (14)
    delta = close.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()

    # Avoid division by zero
    rs = gain / loss.replace(0, np.nan)
    df["RSI"] = 100 - (100 / (1 + rs))
    df["RSI"] = df["RSI"].fillna(0)  # handle first 14 NaNs or div by zero

    # 3. MACD (12, 26, 9)
    # EMA12
    ema12 = close.ewm(span=12, adjust=False).mean()
    # EMA26
    ema26 = close.ewm(span=26, adjust=False).mean()
    df["MACD"] = ema12 - ema26
    df["MACD_SIGNAL"] = df["MACD"].ewm(span=9, adjust=False).mean()
    df["MACD_HIST"] = df["MACD"] - df["MACD_SIGNAL"]

    # 4. Bollinger Bands (20, 2)
    df["BOLL_MID"] = df["MA20"]
    std20 = close.rolling(window=20).std()
    df["BOLL_UPPER"] = df["BOLL_MID"] + 2 * std20
    df["BOLL_LOWER"] = df["BOLL_MID"] - 2 * std20

    # 5. KDJ (9, 3, 3)
    # RSV = (Close - LowestLow9) / (HighestHigh9 - LowestLow9) * 100
    low_min = low.rolling(window=9).min()
    high_max = high.rolling(window=9).max()

    rsv = (close - low_min) / (high_max - low_min) * 100
    rsv = rsv.fillna(0)

    # K = 2/3 * K_prev + 1/3 * RSV
    # D = 2/3 * D_prev + 1/3 * K
    # Using ewm(com=2) => alpha = 1/(1+2) = 1/3
    df["K"] = rsv.ewm(com=2, adjust=False).mean()
    df["D"] = df["K"].ewm(com=2, adjust=False).mean()
    df["J"] = 3 * df["K"] - 2 * df["D"]

    # 6. OBV
    # If Close > PrevClose, Vol is positive. Else negative.
    obv_change = pd.Series(0, index=df.index)
    obv_change[delta > 0] = volume[delta > 0]
    obv_change[delta < 0] = -volume[delta < 0]
    df["OBV"] = obv_change.cumsum()

    return df
