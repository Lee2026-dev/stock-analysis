import streamlit as st


def inject_custom_css():
    """
    Inject custom CSS to override Streamlit defaults and apply SaaS styling (Dark Theme).
    """
    st.markdown(
        """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        :root {
            --bg-primary: #0a0e27;
            --bg-secondary: #141b2d;
            --accent-primary: #00d4ff;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --bull-green: #10b981;
            --bear-red: #ef4444;
            --border-color: #1e293b;
        }

        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; 
            background-color: var(--bg-primary);
            color: var(--text-primary);
        }
        
        .stApp {
            background-color: var(--bg-primary);
        }
        
        .main {
            background: linear-gradient(180deg, var(--bg-primary) 0%, #0f172a 100%);
        }
        
        /* Metric Cards */
        div[data-testid="stMetric"] {
            background: linear-gradient(135deg, var(--bg-secondary) 0%, #0f172a 100%);
            padding: 20px;
            border-radius: 12px;
            border: 1px solid var(--border-color);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        div[data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
            border-color: var(--accent-primary);
        }
        
        div[data-testid="stMetricLabel"] > label {
            color: var(--text-secondary);
        }
        
        div[data-testid="stMetricValue"] > div {
            color: var(--text-primary);
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] { 
            background: linear-gradient(180deg, #050816 0%, #0a0e27 100%);
            border-right: 1px solid var(--border-color);
        }
        
        [data-testid="stSidebar"] * {
            color: var(--text-primary) !important;
        }
        
        /* Inputs in Sidebar */
        [data-testid="stSidebar"] input, [data-testid="stSidebar"] div[data-baseweb="select"] > div {
            background-color: #0f172a !important;
            border-color: #334155 !important;
            color: white !important;
        }
        
        /* Headers */
        h1, h2, h3, h4 {
            color: var(--text-primary) !important;
        }
        
        h1 {
            background: linear-gradient(135deg, #60a5fa 0%, var(--accent-primary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        /* Report Cards */
        .report-card {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 16px;
        }
        
        .score-bar-bg {
            background-color: #334155;
            height: 8px;
            border-radius: 4px;
            overflow: hidden;
            margin-top: 8px;
        }
        
        .score-bar-fill {
            height: 100%;
            background: linear-gradient(90deg, #3b82f6, var(--accent-primary));
            border-radius: 4px;
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            color: white;
            border: none;
        }
        
        /* Expanders */
        .stExpander {
            background-color: var(--bg-secondary);
            border: 1px solid var(--border-color);
        }
        
        .stExpander p {
            color: var(--text-secondary);
        }
        
        /* Streamlit Elements */
        div[data-baseweb="popover"], div[data-baseweb="menu"] {
            background-color: var(--bg-secondary) !important;
        }
        
        /* Remove whitespace */
        .block-container { 
            padding-top: 2rem; 
            padding-bottom: 3rem;
        }
        
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        
    </style>
    """,
        unsafe_allow_html=True,
    )
