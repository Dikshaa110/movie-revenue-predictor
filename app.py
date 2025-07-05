import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from PIL import Image

# ==============================================
# 1. APP CONFIGURATION & DATA LOADING
# ==============================================
st.set_page_config(
    page_title="🎬 CineForecast Pro",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load sample data
@st.cache_data
def load_data():
    movies = pd.DataFrame({
        'budget': np.random.randint(1000000, 200000000, 100),
        'popularity': np.random.uniform(1, 100, 100),
        'runtime': np.random.randint(80, 180, 100),
        'vote_average': np.random.uniform(3, 10, 100),
        'vote_count': np.random.randint(100, 10000, 100),
        'original_language': np.random.choice(['en', 'fr', 'es', 'zh', 'hi'], 100),
        'num_genres': np.random.randint(1, 5, 100),
        'num_production_companies': np.random.randint(1, 5, 100)
    })
    
    analytics = pd.DataFrame({
        'Genre': ['Action', 'Comedy', 'Drama', 'Horror', 'Sci-Fi'],
        'Avg_Revenue': [250, 180, 120, 90, 300],
        'Avg_Budget': [100, 60, 40, 30, 120],
        'ROI': [150, 200, 200, 180, 150],
        'Movies_Count': [120, 85, 150, 60, 40]
    })
    
    return movies, analytics

movies_df, analytics_df = load_data()

# ==============================================
# 2. BLUE THEME CSS
# ==============================================
def inject_css():
    st.markdown(f"""
    <style>
    /* ===== MAIN APP STYLING ===== */
    .stApp {{
        background: linear-gradient(135deg, #0a1f3a 0%, #1a3a6a 100%);
        color: #ffffff;
    }}
    
    /* ===== HEADER STYLING ===== */
    .header {{
        background: rgba(11, 32, 63, 0.9);
        padding: 1.5rem;
        border-radius: 0 0 15px 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }}
    
    /* ===== CARD STYLING ===== */
    .card {{
        background: rgba(23, 55, 105, 0.7);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(100, 149, 237, 0.2);
        backdrop-filter: blur(5px);
    }}
    
    /* ===== PREDICTION RESULT STYLING ===== */
    /* Main metric container */
    [data-testid="stMetric"] {{
        background: rgba(11, 32, 63, 0.8) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        border-left: 4px solid #1e90ff !important;
        box-shadow: 0 4px 15px rgba(30, 144, 255, 0.2);
        transition: all 0.3s ease;
    }}

    /* Value styling (big numbers) */
    [data-testid="stMetricValue"] {{
        font-size: 2.8rem !important;
        color: #00ffaa !important;
        font-weight: 800 !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        margin: 0.5rem 0 !important;
        font-family: 'Arial', sans-serif;
    }}

    /* Label styling */
    [data-testid="stMetricLabel"] {{
        font-size: 1.3rem !important;
        color: #a8c6ff !important;
        font-weight: 500 !important;
        letter-spacing: 0.5px;
    }}

    /* ROI delta styling */
    [data-testid="stMetricDelta"] {{
        font-size: 1.2rem !important;
    }}

    /* Positive ROI */
    div[data-testid="stMetricDelta"] > div:first-child {{
        color: #00ffaa !important;
        font-weight: 600 !important;
    }}

    /* Negative ROI */
    div[data-testid="stMetricDelta"] > div:first-child[style*="color: rgb(255, 43, 43)"] {{
        color: #ff6b6b !important;
    }}

    /* ===== INPUT CONTROLS ===== */
    .stNumberInput, .stSlider, .stSelectbox {{
        background: rgba(173, 216, 230, 0.15) !important;
        border-radius: 10px !important;
        padding: 1rem !important;
        border: 1px solid rgba(100, 149, 237, 0.3) !important;
    }}
    
    /* ===== BUTTON STYLING ===== */
    .stButton>button {{
        background: linear-gradient(90deg, #1e90ff 0%, #0066cc 100%) !important;
        border: none !important;
        color: white !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        padding: 12px 32px !important;
        transition: all 0.3s !important;
    }}
    
    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(30, 144, 255, 0.4) !important;
        background: linear-gradient(90deg, #1e90ff 0%, #005bb5 100%) !important;
    }}
    
    /* ===== TAB STYLING ===== */
    [data-baseweb="tab-list"] {{
        gap: 8px;
    }}
    
    [data-baseweb="tab"] {{
        background: #1a3a6a !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        margin: 0 4px !important;
        transition: all 0.3s !important;
    }}
    
    [data-baseweb="tab"]:hover {{
        background: #254b8a !important;
    }}
    
    [aria-selected="true"] {{
        background: #1e90ff !important;
    }}
    
    /* ===== TEXT COLORS ===== */
    h1, h2, h3, h4, h5, h6 {{
        color: #e6f2ff !important;
    }}
    
    /* ===== CHART STYLING ===== */
    .js-plotly-plot .plotly, .js-plotly-plot .plotly div {{
        background: transparent !important;
    }}
    
    /* ===== ANIMATIONS ===== */
    @keyframes pulse {{
        0% {{ transform: scale(1); opacity: 0.9; }}
        50% {{ transform: scale(1.02); opacity: 1; }}
        100% {{ transform: scale(1); opacity: 0.9; }}
    }}
    
    .pulse-result {{
        animation: pulse 2s ease infinite;
    }}
    
    /* ===== RESPONSIVE ADJUSTMENTS ===== */
    @media (max-width: 768px) {{
        [data-testid="stMetricValue"] {{
            font-size: 2rem !important;
        }}
        [data-testid="stMetricLabel"] {{
            font-size: 1rem !important;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)

inject_css()

# ==============================================
# 3. PREDICTION MODEL
# ==============================================
def predict_revenue(input_data):
    language_weights = {'en': 1.2, 'zh': 1.1, 'es': 1.0, 'fr': 0.9, 'hi': 0.8}
    base_pred = (input_data['budget'] * 
                (1 + (input_data['popularity']/50)) * 
                (1 + (input_data['vote_average']/5)) *
                (1 + np.log(input_data['vote_count'])/10) *
                (1 + (input_data['runtime']-90)/200) *
                (1 + (input_data['num_genres']-1)/10) *
                (1 + (input_data['num_production_companies']-1)/15))
    return base_pred * language_weights.get(input_data['original_language'], 1.0)

# ==============================================
# 4. APP HEADER
# ==============================================
with st.container():
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/2598/2598702.png", width=120)
    with col2:
        st.title("CineForecast Pro")
        st.markdown("Predict movie success with industry-leading analytics")

# ==============================================
# 5. MULTI-PAGE NAVIGATION
# ==============================================
tab1, tab2 = st.tabs(["💰 PREDICTION ENGINE", "📊 INDUSTRY ANALYTICS"])

with tab1:
    # PREDICTION PAGE CONTENT
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            with st.container(border=True):
                st.markdown("### 🎬 PRODUCTION DETAILS")
                budget = st.number_input("BUDGET (USD MILLIONS)", 1, 500, 50) * 1000000
                popularity = st.slider("POPULARITY (1-100)", 1.0, 100.0, 50.0)
                runtime = st.slider("RUNTIME (MINUTES)", 60, 240, 120)
                num_genres = st.slider("NUMBER OF GENRES", 1, 5, 2)
                num_companies = st.slider("PRODUCTION COMPANIES", 1, 5, 2)
        
        with col2:
            with st.container(border=True):
                st.markdown("### 🎭 AUDIENCE METRICS")
                vote_average = st.slider("EXPECTED RATING (0-10)", 0.0, 10.0, 7.5)
                vote_count = st.number_input("EXPECTED VOTE COUNT", 100, 100000, 5000)
                language = st.selectbox("ORIGINAL LANGUAGE", 
                                      [("English", "en"), ("Chinese", "zh"), 
                                       ("Spanish", "es"), ("French", "fr"), 
                                       ("Hindi", "hi")],
                                      format_func=lambda x: x[0])
                language_code = language[1]
    
    if st.button("PREDICT REVENUE", use_container_width=True):
        input_data = {
            'budget': budget,
            'popularity': popularity,
            'runtime': runtime,
            'vote_average': vote_average,
            'vote_count': vote_count,
            'original_language': language_code,
            'num_genres': num_genres,
            'num_production_companies': num_companies
        }
        
        with st.spinner("Analyzing..."):
            revenue = predict_revenue(input_data)
            roi = ((revenue - budget) / budget) * 100
            
            st.balloons()
            with st.container(border=True):
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("PREDICTED REVENUE", f"${revenue/1000000:,.2f}M")
                with col2:
                    st.metric("ROI", f"{roi:.1f}%", "Profitable" if roi > 0 else "Loss")
            
            # Visualization
            features = {
                'Budget': budget,
                'Popularity': popularity * budget / 50,
                'Rating': vote_average * budget / 5,
                'Vote Count': np.log(vote_count) * budget / 10,
                'Runtime': (runtime-90) * budget / 200,
                'Genres': (num_genres-1) * budget / 10,
                'Companies': (num_companies-1) * budget / 15,
                'Language': (1.2-1) * budget if language_code == 'en' else (1.1-1) * budget
            }
            
            fig = px.bar(
                x=list(features.keys()),
                y=list(features.values()),
                color=list(features.keys()),
                color_discrete_sequence=px.colors.sequential.Blues_r,
                template="plotly_dark",
                labels={'x': 'Feature', 'y': 'Revenue Impact ($)'}
            )
            st.plotly_chart(fig, use_container_width=True)

with tab2:
    # ANALYTICS DASHBOARD CONTENT
    st.markdown("## INDUSTRY TRENDS")
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container(border=True):
            st.metric("Highest Grossing", "Sci-Fi", "42% above avg")
    with col2:
        with st.container(border=True):
            st.metric("Best ROI", "Comedy", "200% ROI")
    with col3:
        with st.container(border=True):
            st.metric("Avg Budget", "$85M", "+12% YoY")
    
    # Charts
    with st.container(border=True):
        st.markdown("### 💰 REVENUE BY GENRE")
        fig = px.bar(
            analytics_df,
            x='Genre',
            y='Avg_Revenue',
            color='Genre',
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
        st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.markdown("### 📊 BUDGET VS REVENUE")
            fig = px.scatter(
                analytics_df,
                x='Avg_Budget',
                y='Avg_Revenue',
                size='Movies_Count',
                color='Genre',
                color_discrete_sequence=px.colors.sequential.Blues_r
            )
            st.plotly_chart(fig, use_container_width=True)
    with col2:
        with st.container(border=True):
            st.markdown("### 🏆 ROI DISTRIBUTION")
            fig = px.pie(
                analytics_df,
                values='ROI',
                names='Genre',
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.Blues_r
            )
            st.plotly_chart(fig, use_container_width=True)

# ==============================================
# 6. FOOTER
# ==============================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #a8c6ff; padding: 1rem;'>
    © Blockbuster Analytics 
</div>
""", unsafe_allow_html=True)