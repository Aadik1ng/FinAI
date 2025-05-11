import streamlit as st
import sys
from pathlib import Path

# Add the src directory to the Python path
src_path = Path(__file__).parent / "src"
sys.path.append(str(src_path))

# Import modules from src directory
import src.sentiment.sentiment_analyzer as sentiment_analyzer
import src.anomaly.anomaly_detector as anomaly_detector
import src.rl_agent.trading_agent as trading_agent
import src.automl.auto_ml_module as auto_ml_module
import src.federated.federated_learning as federated_learning
import src.knowledge_graph.kg_analyzer as kg_analyzer
import src.scenario.scenario_analyzer as scenario_analyzer
import src.xai.explainable_ai as explainable_ai
import src.ingestion.data_ingestion as data_ingestion

def main():
    st.set_page_config(
        page_title="Financial Analysis Platform",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a Feature",
        [
            "Home",
            "Data Ingestion",
            "Sentiment Analysis",
            "Anomaly Detection",
            "Trading Agent (RL)",
            "AutoML",
            "Federated Learning",
            "Knowledge Graph",
            "Scenario Analysis",
            "Explainable AI"
        ]
    )

    # Main content area
    if page == "Home":
        display_home()
    elif page == "Data Ingestion":
        data_ingestion.run()
    elif page == "Sentiment Analysis":
        sentiment_analyzer.run()
    elif page == "Anomaly Detection":
        anomaly_detector.run()
    elif page == "Trading Agent (RL)":
        trading_agent.run()
    elif page == "AutoML":
        auto_ml_module.run()
    elif page == "Federated Learning":
        federated_learning.run()
    elif page == "Knowledge Graph":
        kg_analyzer.run()
    elif page == "Scenario Analysis":
        scenario_analyzer.run()
    elif page == "Explainable AI":
        explainable_ai.run()

def display_home():
    st.title("Financial Analysis Platform 📊")
    st.markdown("""
    ## Welcome to the Financial Analysis Platform
    
    This platform provides a comprehensive suite of tools for financial analysis:
    
    ### Available Features:
    
    1. **Data Ingestion** 📥
       - Import and preprocess financial data from various sources
    
    2. **Sentiment Analysis** 🎭
       - Analyze market sentiment from news and social media
    
    3. **Anomaly Detection** 🔍
       - Identify unusual patterns in financial data
    
    4. **Trading Agent** 🤖
       - AI-powered trading strategies using reinforcement learning
    
    5. **AutoML** 🎯
       - Automated machine learning for financial predictions
    
    6. **Federated Learning** 🌐
       - Distributed machine learning across multiple data sources
    
    7. **Knowledge Graph** 🕸️
       - Visualize and analyze financial relationships
    
    8. **Scenario Analysis** 📊
       - Simulate and analyze different market scenarios
    
    9. **Explainable AI** 🔬
       - Understand the reasoning behind AI predictions
    
    ### Getting Started
    
    Select a feature from the sidebar to begin your analysis.
    """)

    # Display some key metrics or recent analysis results
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Market Sentiment", value="Positive", delta="1.2%")
    with col2:
        st.metric(label="Anomalies Detected", value="3", delta="-2")
    with col3:
        st.metric(label="Active Models", value="5", delta="1")

if __name__ == "__main__":
    main() 