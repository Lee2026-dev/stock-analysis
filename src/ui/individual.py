import streamlit as st
import pandas as pd
from src.data.fetcher import fetch_daily_history
from src.logic.indicators import calculate_indicators
from src.logic.backtest import run_backtest
from src.ui.components import render_metric_card, render_chart


def render_individual_analysis(stock_code: str, start_date: str, end_date: str):
    """
    Render the Individual Stock Analysis page.
    """
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #141b2d 0%, #0f172a 100%);
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 4px solid #3b82f6;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
            margin-bottom: 1.5rem;
        ">
            <h2 style="margin: 0; color: #f8fafc; font-size: 1.75rem; font-weight: 700;">
                📈 个股分析: {stock_code}
            </h2>
        </div>
    """,
        unsafe_allow_html=True,
    )

    if not stock_code or not start_date or not end_date:
        st.info("💡 请在左侧侧边栏选择股票代码和日期范围")
        return

    with st.spinner("🔄 正在获取数据..."):
        df = fetch_daily_history(stock_code, start_date, end_date)

    if df.empty:
        st.error(f"❌ 无法获取股票 {stock_code} 的数据，请检查代码或网络。")
        return

    df = calculate_indicators(df)
    backtest_res = run_backtest(df)

    last_row = df.iloc[-1]
    prev_row = df.iloc[-2] if len(df) > 1 else last_row

    current_price = f"¥{last_row['收盘']:.2f}"
    change_val = last_row["收盘"] - prev_row["收盘"]
    change_pct = (change_val / prev_row["收盘"]) * 100

    delta_str = f"{change_val:+.2f} ({change_pct:+.2f}%)"

    win_rate = backtest_res.get("win_rate", 0.0)
    confidence = "LOW 📉"
    if win_rate >= 70:
        confidence = "HIGH 🔥"
    elif win_rate >= 50:
        confidence = "NEUTRAL ⚖️"

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_metric_card("当前价格 (Current)", current_price, delta_str)
    with col2:
        render_metric_card(
            "胜率 (Win Rate)",
            f"{win_rate}%",
            f"Confidence: {confidence}",
            color_inverse=False,
        )
    with col3:
        total_ret = backtest_res.get("total_return", 0.0)
        render_metric_card(
            "回测收益 (Return)", f"{total_ret:+.2f}%", None, color_inverse=True
        )
    with col4:
        vol_val = last_row["成交量"] / 10000
        render_metric_card("成交量 (Vol)", f"{vol_val:.0f}万", None)

    with st.container():
        st.markdown(
            """
            <div style="
                background: linear-gradient(135deg, #141b2d 0%, #0f172a 100%);
                padding: 1.5rem;
                border-radius: 12px;
                border: 1px solid #1e293b;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
                margin: 1.5rem 0;
            ">
                <h3 style="margin: 0 0 1rem 0; color: #f8fafc; font-weight: 700;">
                    📊 技术走势 (Technical Chart)
                </h3>
            </div>
        """,
            unsafe_allow_html=True,
        )
        render_chart(df, height=550)

    with st.expander("🔍 查看详细回测数据 (Backtest Details)", expanded=False):
        st.json(backtest_res)
        st.dataframe(df.tail(), use_container_width=True)
