import streamlit as st


def inject_custom_css():
    """
    Inject custom CSS to override Streamlit defaults and apply SaaS styling.
    """
    st.markdown(
        """
    <style>
        /* Global font override for clean look */
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; 
        }
        
        /* Card-like look for metrics */
        div[data-testid="stMetric"] {
            background-color: #ffffff;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #f0f2f6;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        
        /* Remove default Streamlit padding */
        .block-container { 
            padding-top: 2rem; 
            padding-bottom: 2rem; 
        }
        
        /* Hide hamburger menu and footer */
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        
        /* Custom Sidebar styling */
        [data-testid="stSidebar"] { 
            background-color: #f8f9fa; 
            border-right: 1px solid #dee2e6; 
        }
        
        /* Headers */
        h1, h2, h3 {
            font-weight: 600;
            color: #1a1f36;
        }
        
        /* Metric Labels */
        div[data-testid="stMetricLabel"] > label {
            font-size: 0.9rem;
            color: #6b7c93;
        }
        
        /* Metric Values */
        div[data-testid="stMetricValue"] > div {
            font-size: 1.6rem;
            font-weight: 700;
            color: #1a1f36;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )
