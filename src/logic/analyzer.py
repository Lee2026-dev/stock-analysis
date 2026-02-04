import pandas as pd
from typing import Dict, List, Any


def calculate_technical_score(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate technical score (0-100) based on indicators.

    Args:
        df: DataFrame with indicators (MA5, MA20, MACD, RSI, etc.)

    Returns:
        Dict: {"score": int, "signals": List[str]}
    """
    if df.empty or len(df) < 20:
        return {"score": 50, "signals": ["数据不足"]}

    current = df.iloc[-1]
    prev = df.iloc[-2]

    score = 0
    signals = []

    # 1. Trend (MA) - Weight: 20
    if current["MA5"] > current["MA20"]:
        score += 20
        signals.append("MA5多头排列")
    elif current["MA5"] < current["MA20"]:
        signals.append("MA5空头排列")

    # 2. Momentum (MACD) - Weight: 15
    if current["MACD_HIST"] > 0:
        score += 15
        signals.append("MACD红柱")
    else:
        signals.append("MACD绿柱")

    # 3. Strength (RSI) - Weight: 20
    rsi = current["RSI"]
    if 30 < rsi < 70:
        score += 20
        signals.append("RSI正常区间")
    elif rsi <= 30:
        score += 5
        signals.append("RSI超卖")
    else:
        score -= 10
        signals.append("RSI超买")

    # 4. Support/Resistance (BOLL) - Weight: 10
    # Using BOLL_LOWER as support check
    if current["收盘"] > current["BOLL_LOWER"]:
        score += 10
    else:
        signals.append("跌破布林下轨")

    # 5. Volume - Weight: 10
    # Compare with 5-day average volume
    vol_ma5 = df["成交量"].rolling(window=5).mean().iloc[-1]
    if current["成交量"] > vol_ma5:
        score += 10
        signals.append("成交量放大")

    # 6. KDJ - Weight: 15 (Added to reach closer to 100)
    if "K" in current and "D" in current:
        if current["K"] > current["D"]:
            score += 15
            signals.append("KDJ金叉状态")

    # Base score adjustment or scaling
    # Max possible: 20+15+20+10+10+15 = 90
    # Add 10 base points
    score += 10

    # Cap at 100, min 0
    score = max(0, min(100, score))

    return {"score": score, "signals": signals}
