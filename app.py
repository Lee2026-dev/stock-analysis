import streamlit as st
import warnings
from streamlit_autorefresh import st_autorefresh
from src.ui.styles import inject_custom_css
from src.ui.layout import render_sidebar, render_header
from src.ui.individual import render_individual_analysis
from src.ui.market import render_market_overview
from src.ui.reports import render_daily_reports
from src.utils.scheduler import should_generate_report
from src.logic.report_engine import generate_all_reports

# Suppress pandas future warnings
warnings.simplefilter(action="ignore", category=FutureWarning)

# 1. Page Config (Must be first)
st.set_page_config(
    page_title="Alpha-X | B2B Quantitative Analysis",
    layout="wide",
    page_icon="📈",
    initial_sidebar_state="expanded",
)

# 2. Inject Styles
inject_custom_css()

# 3. Sidebar & Inputs
user_inputs = render_sidebar()

# 4. Auto Refresh Logic
if user_inputs["auto_refresh"]:
    # Refresh every 60 seconds (60000ms)
    st_autorefresh(interval=60000, key="data_refresh_loop")

# 5. Header
render_header()

# 6. Routing
page = user_inputs["page"]

if "个股" in page:
    render_individual_analysis(
        user_inputs["stock_code"], user_inputs["start_date"], user_inputs["end_date"]
    )
elif "市场" in page:
    render_market_overview()
elif "报告" in page:
    # Auto-trigger check
    if should_generate_report(user_inputs["watchlist"]):
        with st.spinner("⏳ 正在生成今日智能分析报告（技术面 + 消息面 + AI预测）..."):
            generate_all_reports(user_inputs["watchlist"])
            st.toast("✅ 报告生成完成！", icon="🎉")

    render_daily_reports()

if __name__ == "__main__":
    import sys
    from streamlit.web import cli as stcli
    from streamlit import runtime

    # Only run the CLI if we're not already running in a Streamlit runtime
    if not runtime.exists():
        sys.argv = ["streamlit", "run", __file__]
        sys.exit(stcli.main())
