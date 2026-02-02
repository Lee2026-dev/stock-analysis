import streamlit as st
import datetime


def render_header():
    """
    Render the top header of the application.
    """
    with st.container():
        col1, col2 = st.columns([1, 6])
        with col1:
            st.markdown("### 🚀 **Alpha-X**")
        with col2:
            st.markdown("#### B2B 量化分析系统 (MVP)")
        st.markdown("---")


def render_sidebar():
    """
    Render the sidebar navigation and inputs.

    Returns:
        dict: User inputs {
            'page': str,
            'stock_code': str,
            'start_date': str (YYYYMMDD),
            'end_date': str (YYYYMMDD),
            'auto_refresh': bool
        }
    """
    with st.sidebar:
        st.markdown("### 导航")
        page = st.radio(
            "选择页面", ["个股分析 (Individual)", "市场概览 (Market Overview)"], index=0
        )

        st.markdown("---")

        inputs = {
            "page": page,
            "stock_code": "000001",  # Default
            "start_date": "",
            "end_date": "",
            "auto_refresh": False,
        }

        if "个股" in page:
            st.markdown("### 参数设置")
            stock_code = st.text_input("股票代码", value="000001", max_chars=6)

            # Date Range
            today = datetime.date.today()
            last_year = today - datetime.timedelta(days=365)

            date_range = st.date_input(
                "日期范围",
                value=(last_year, today),
                min_value=datetime.date(2000, 1, 1),
                max_value=today,
            )

            if isinstance(date_range, tuple) and len(date_range) == 2:
                start_d, end_d = date_range
                inputs["start_date"] = start_d.strftime("%Y%m%d")
                inputs["end_date"] = end_d.strftime("%Y%m%d")
            else:
                # Fallback if user only picked one date
                inputs["start_date"] = last_year.strftime("%Y%m%d")
                inputs["end_date"] = today.strftime("%Y%m%d")

            inputs["stock_code"] = stock_code

        elif "市场" in page:
            st.markdown("### 市场设置")
            st.info("展示北向资金实时流向")

        st.markdown("---")
        inputs["auto_refresh"] = st.checkbox("自动刷新 (Auto Refresh)", value=False)

        return inputs
