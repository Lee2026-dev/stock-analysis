import streamlit as st
import warnings
from streamlit_autorefresh import st_autorefresh
from src.ui.styles import inject_custom_css
from src.ui.layout import render_sidebar, render_header
from src.ui.individual import render_individual_analysis
from src.ui.market import render_market_overview

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

if __name__ == "__main__":
    import sys
    from streamlit.web import cli as stcli
    from streamlit import runtime

    # Only run the CLI if we're not already running in a Streamlit runtime
    if not runtime.exists():
        sys.argv = ["streamlit", "run", __file__]
        sys.exit(stcli.main())
