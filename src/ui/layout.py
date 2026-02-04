import streamlit as st
import datetime
import pandas as pd
from src.data.fetcher import fetch_spot_data


def render_header():
    """
    Render the top header of the application.
    """
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #60a5fa 100%);
            padding: 2rem 2rem 2rem 2rem;
            border-radius: 16px;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(59, 130, 246, 0.2);
        ">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <h1 style="
                        color: white;
                        font-size: 2.5rem;
                        margin: 0;
                        font-weight: 800;
                        letter-spacing: -0.02em;
                        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                    ">🚀 盈立方 ALPHA-X</h1>
                    <p style="
                        color: rgba(255, 255, 255, 0.9);
                        font-size: 1.125rem;
                        margin: 0.5rem 0 0 0;
                        font-weight: 500;
                    ">专业量化分析系统 | Professional Quantitative Analysis Platform</p>
                </div>
                <div style="
                    background: rgba(255, 255, 255, 0.15);
                    backdrop-filter: blur(10px);
                    padding: 1rem 1.5rem;
                    border-radius: 12px;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                ">
                    <div style="color: rgba(255, 255, 255, 0.8); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em;">系统状态</div>
                    <div style="color: white; font-size: 1.25rem; font-weight: 700; margin-top: 0.25rem;">● 在线</div>
                </div>
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )


def render_watchlist_card(stock_code: str, spot_data: pd.DataFrame):
    """
    Render a real-time card for a stock in the sidebar.
    """
    # Find data for this stock
    # Spot data usually has columns: 代码, 名称, 最新价, 涨跌幅, etc.
    # Akshare columns might vary, so we handle safely
    row = None
    if not spot_data.empty and "代码" in spot_data.columns:
        match = spot_data[spot_data["代码"] == stock_code]
        if not match.empty:
            row = match.iloc[0]

    if row is not None:
        price = row.get("最新价", 0)
        change_pct = row.get("涨跌幅", 0)
        name = row.get("名称", stock_code)

        color = "#ef4444" if change_pct >= 0 else "#10b981"  # Red Up, Green Down
        arrow = "▲" if change_pct >= 0 else "▼"

        card_html = f"""
        <div style="
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 8px;
            border-left: 4px solid {color};
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="font-weight: bold; color: #e2e8f0;">{name}</div>
                <div style="color: #94a3b8; font-size: 0.8em;">{stock_code}</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 4px;">
                <div style="font-size: 1.1em; font-weight: bold; color: white;">{price}</div>
                <div style="color: {color}; font-weight: bold;">{arrow} {change_pct}%</div>
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
    else:
        st.markdown(f"**{stock_code}** (无数据)")


def render_sidebar():
    """
    Render the sidebar navigation and inputs.
    """
    if "watchlist" not in st.session_state:
        st.session_state.watchlist = [
            "000001",
            "600519",
            "000858",
        ]  # Default: PingAn, Moutai, Wuliangye

    if "selected_stock" not in st.session_state:
        st.session_state.selected_stock = st.session_state.watchlist[0]

    with st.sidebar:
        # Navigation
        st.markdown("### 🧭 导航菜单")
        page = st.radio(
            "选择页面",
            ["🏠 工作台", "📊 个股分析", "📈 市场概览", "📋 每日报告"],
            index=1,
            label_visibility="collapsed",
        )

        st.markdown("---")

        inputs = {
            "page": page,
            "stock_code": st.session_state.selected_stock,
            "start_date": "",
            "end_date": "",
            "auto_refresh": False,
            "watchlist": st.session_state.watchlist,
        }

        # Watchlist Section
        if "个股" in page or "报告" in page:
            st.markdown("### 🔭 自选股监控")

            # Fetch real-time data for all watchlist stocks
            spot_df = fetch_spot_data(st.session_state.watchlist)

            # Selection
            selected_stock = st.selectbox(
                "切换当前分析股票",
                options=st.session_state.watchlist,
                index=st.session_state.watchlist.index(st.session_state.selected_stock)
                if st.session_state.selected_stock in st.session_state.watchlist
                else 0,
            )
            st.session_state.selected_stock = selected_stock
            inputs["stock_code"] = selected_stock

            # Render cards for all watchlist stocks
            with st.expander("实时行情卡片", expanded=True):
                for code in st.session_state.watchlist:
                    # Highlight selected
                    if code == selected_stock:
                        st.markdown(f"**👉 当前选中: {code}**")
                    render_watchlist_card(code, spot_df)

            # Manage Watchlist
            with st.expander("⚙️ 管理自选股"):
                new_stock = st.text_input("输入代码 (如 000001)", max_chars=6)
                if st.button("添加股票"):
                    if new_stock and new_stock not in st.session_state.watchlist:
                        st.session_state.watchlist.append(new_stock)
                        st.rerun()

                if len(st.session_state.watchlist) > 1:
                    to_remove = st.selectbox("移除股票", st.session_state.watchlist)
                    if st.button("确认移除"):
                        st.session_state.watchlist.remove(to_remove)
                        if st.session_state.selected_stock == to_remove:
                            st.session_state.selected_stock = (
                                st.session_state.watchlist[0]
                            )
                        st.rerun()

            st.markdown("---")

            # Date Range
            st.markdown("### 📅 分析周期")
            today = datetime.date.today()
            last_year = today - datetime.timedelta(days=365)

            date_range = st.date_input(
                "选择时间范围", value=(last_year, today), max_value=today
            )

            if isinstance(date_range, tuple) and len(date_range) == 2:
                inputs["start_date"] = date_range[0].strftime("%Y%m%d")
                inputs["end_date"] = date_range[1].strftime("%Y%m%d")
            else:
                inputs["start_date"] = last_year.strftime("%Y%m%d")
                inputs["end_date"] = today.strftime("%Y%m%d")

        elif "市场" in page:
            st.info("展示全市场资金流向与板块热度")

        elif "工作台" in page:
            st.info("欢迎使用 Alpha-X 量化终端")

        return inputs
