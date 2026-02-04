"""
AI Startup Survival Prediction Platform - Main Application
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pathlib import Path
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from model.predictor import StartupSurvivalModel, train_model_from_data
from utils.data_processing import (
    generate_sample_data, validate_data, calculate_features, 
    get_feature_columns, get_risk_level, calculate_survival_timeline
)
from utils.recommendations import (
    generate_recommendations, generate_action_plan, get_risk_indicators
)
from utils.visualizations import (
    create_gauge_chart, create_feature_importance_chart,
    create_metrics_comparison, create_risk_radar, create_timeline_chart,
    create_shap_waterfall
)

# Page configuration
st.set_page_config(
    page_title="AI Startup Survival Prediction Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
    h1 {
        color: #1f77b4;
        padding-bottom: 1rem;
    }
    h2 {
        color: #2c3e50;
        padding-top: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if 'model' not in st.session_state:
        st.session_state.model = None
    if 'training_data' not in st.session_state:
        st.session_state.training_data = None
    if 'metrics' not in st.session_state:
        st.session_state.metrics = None


def display_header():
    """Display application header"""
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🚀 AI Startup Survival Prediction Platform")
        st.markdown("**Tesla Autopilot for Startups** - Predict failures, prevent disasters")
    with col2:
        st.image("https://img.icons8.com/fluency/96/rocket.png", width=80)


def train_model_section():
    """Model training section"""
    st.header("📊 Step 1: Train AI Model")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Upload Training Data")
        uploaded_file = st.file_uploader(
            "Upload CSV with historical startup data", 
            type=['csv'],
            help="CSV should contain: burn_rate, revenue, funding_raised, team_size, months_since_founding, monthly_growth_rate, customer_count, market_competition, team_experience, pivots_count, investor_count, survived"
        )
        
        use_sample = st.checkbox("Use Sample Dataset (for demo)", value=True)
    
    with col2:
        st.info("""
        **Required Columns:**
        - burn_rate
        - revenue
        - funding_raised
        - team_size
        - months_since_founding
        - monthly_growth_rate
        - customer_count
        - market_competition
        - team_experience
        - pivots_count
        - investor_count
        - survived (0/1)
        """)
    
    # Load data
    if use_sample:
        if st.button("🎯 Generate & Train with Sample Data", type="primary"):
            with st.spinner("Generating sample data and training model..."):
                # Generate sample data
                df = generate_sample_data(n_samples=200)
                st.session_state.training_data = df
                
                # Train model
                model_type = st.selectbox("Select Model", ["xgboost", "random_forest"], index=0)
                model, metrics = train_model_from_data(df, model_type=model_type)
                
                st.session_state.model = model
                st.session_state.metrics = metrics
                
                st.success("✅ Model trained successfully!")
                
                # Display metrics
                col1, col2, col3, col4, col5 = st.columns(5)
                col1.metric("Accuracy", f"{metrics['accuracy']:.2%}")
                col2.metric("Precision", f"{metrics['precision']:.2%}")
                col3.metric("Recall", f"{metrics['recall']:.2%}")
                col4.metric("F1 Score", f"{metrics['f1_score']:.2%}")
                col5.metric("ROC AUC", f"{metrics['roc_auc']:.2%}")
                
                # Show data preview
                with st.expander("📋 View Training Data Sample"):
                    st.dataframe(df.head(10), use_container_width=True)
    
    elif uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            
            # Validate data
            is_valid, errors = validate_data(df)
            
            if not is_valid:
                st.error("❌ Data validation failed:")
                for error in errors:
                    st.error(f"- {error}")
                return
            
            # Check for target column
            if 'survived' not in df.columns:
                st.error("❌ Missing 'survived' column (target variable)")
                return
            
            st.success(f"✅ Data loaded: {len(df)} samples")
            st.session_state.training_data = df
            
            if st.button("🎯 Train Model", type="primary"):
                with st.spinner("Training model..."):
                    model_type = st.selectbox("Select Model", ["xgboost", "random_forest"], index=0)
                    model, metrics = train_model_from_data(df, model_type=model_type)
                    
                    st.session_state.model = model
                    st.session_state.metrics = metrics
                    
                    st.success("✅ Model trained successfully!")
                    
                    # Display metrics
                    col1, col2, col3, col4, col5 = st.columns(5)
                    col1.metric("Accuracy", f"{metrics['accuracy']:.2%}")
                    col2.metric("Precision", f"{metrics['precision']:.2%}")
                    col3.metric("Recall", f"{metrics['recall']:.2%}")
                    col4.metric("F1 Score", f"{metrics['f1_score']:.2%}")
                    col5.metric("ROC AUC", f"{metrics['roc_auc']:.2%}")
        
        except Exception as e:
            st.error(f"❌ Error loading data: {str(e)}")


def prediction_section():
    """Prediction section"""
    if st.session_state.model is None:
        st.warning("⚠️ Please train a model first (Step 1)")
        return
    
    st.header("🔮 Step 2: Predict Startup Survival")
    
    tab1, tab2 = st.tabs(["📝 Manual Input", "📤 Upload CSV"])
    
    with tab1:
        manual_input_form()
    
    with tab2:
        batch_prediction_form()


def manual_input_form():
    """Manual input form for single prediction"""
    st.subheader("Enter Startup Details")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**💰 Financial Metrics**")
        burn_rate = st.number_input("Monthly Burn Rate ($)", min_value=0, value=50000, step=5000)
        revenue = st.number_input("Monthly Revenue ($)", min_value=0, value=30000, step=5000)
        funding_raised = st.number_input("Total Funding Raised ($)", min_value=0, value=500000, step=50000)
    
    with col2:
        st.markdown("**👥 Team Metrics**")
        team_size = st.number_input("Team Size", min_value=1, value=10, step=1)
        team_experience = st.number_input("Avg Team Experience (years)", min_value=0, value=5, step=1)
        months_since_founding = st.number_input("Months Since Founding", min_value=1, value=12, step=1)
    
    with col3:
        st.markdown("**📈 Growth Metrics**")
        monthly_growth_rate = st.number_input("Monthly Growth Rate (%)", value=15.0, step=1.0)
        customer_count = st.number_input("Total Customers", min_value=0, value=500, step=10)
        market_competition = st.slider("Market Competition (1-10)", 1, 10, 5)
        pivots_count = st.number_input("Number of Pivots", min_value=0, value=1, step=1)
        investor_count = st.number_input("Number of Investors", min_value=0, value=3, step=1)
    
    if st.button("🎯 Predict Survival", type="primary"):
        # Create dataframe
        input_data = pd.DataFrame([{
            'burn_rate': burn_rate,
            'revenue': revenue,
            'funding_raised': funding_raised,
            'team_size': team_size,
            'months_since_founding': months_since_founding,
            'monthly_growth_rate': monthly_growth_rate,
            'customer_count': customer_count,
            'market_competition': market_competition,
            'team_experience': team_experience,
            'pivots_count': pivots_count,
            'investor_count': investor_count,
        }])
        
        # Calculate features
        input_features = calculate_features(input_data)
        feature_cols = get_feature_columns()
        X = input_features[feature_cols]
        
        # Make prediction
        with st.spinner("Analyzing startup..."):
            prediction_result = st.session_state.model.predict_single(X)
            explanation = st.session_state.model.explain_prediction(X)
            
            display_prediction_results(
                prediction_result, explanation, input_features
            )


def batch_prediction_form():
    """Batch prediction from CSV"""
    st.subheader("Upload Startup Data for Batch Prediction")
    
    uploaded_file = st.file_uploader(
        "Upload CSV (without 'survived' column)", 
        type=['csv'],
        key='batch_upload'
    )
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            
            # Validate data (without target)
            is_valid, errors = validate_data(df)
            
            if not is_valid:
                st.error("❌ Data validation failed:")
                for error in errors:
                    st.error(f"- {error}")
                return
            
            st.success(f"✅ Data loaded: {len(df)} startups")
            
            if st.button("🎯 Predict All", type="primary"):
                with st.spinner("Making predictions..."):
                    # Calculate features
                    df_features = calculate_features(df)
                    feature_cols = get_feature_columns()
                    X = df_features[feature_cols]
                    
                    # Predict
                    predictions, probabilities = st.session_state.model.predict(X)
                    
                    # Add results to dataframe
                    results_df = df.copy()
                    results_df['Prediction'] = ['SURVIVE' if p == 1 else 'FAIL' for p in predictions]
                    results_df['Failure_Probability'] = probabilities[:, 0]
                    results_df['Survival_Probability'] = probabilities[:, 1]
                    
                    st.success("✅ Predictions completed!")
                    
                    # Summary
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Total Startups", len(results_df))
                    col2.metric("Predicted to Survive", sum(predictions))
                    col3.metric("Predicted to Fail", len(predictions) - sum(predictions))
                    
                    # Display results
                    st.dataframe(results_df, use_container_width=True)
                    
                    # Download button
                    csv = results_df.to_csv(index=False)
                    st.download_button(
                        "📥 Download Results",
                        csv,
                        "predictions.csv",
                        "text/csv",
                        key='download-csv'
                    )
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")


def display_prediction_results(prediction_result, explanation, input_features):
    """Display detailed prediction results"""
    failure_prob = prediction_result['failure_probability']
    survival_prob = prediction_result['survival_probability']
    
    # Main prediction
    st.markdown("---")
    st.header("🎯 Prediction Results")
    
    # Risk level
    risk_level, risk_color = get_risk_level(failure_prob)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"### Prediction: **{prediction_result['prediction']}**")
        st.markdown(f"### Risk Level: :{risk_color}[**{risk_level}**]")
        st.metric("Confidence", f"{prediction_result['confidence']:.1%}")
    
    with col2:
        fig = create_gauge_chart(failure_prob * 100, "Failure Probability (%)")
        st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        fig = create_gauge_chart(survival_prob * 100, "Survival Probability (%)")
        st.plotly_chart(fig, use_container_width=True)
    
    # Timeline
    st.subheader("📅 Survival Timeline")
    timeline_data = calculate_survival_timeline(input_features, failure_prob)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Current Runway", f"{timeline_data['runway_months']:.1f} months")
        st.metric("Predicted Survival Time", f"{timeline_data['estimated_survival_months']:.1f} months")
    
    with col2:
        fig = create_timeline_chart(timeline_data)
        st.plotly_chart(fig, use_container_width=True)
    
    # Risk Indicators
    st.subheader("📊 Health Score Dashboard")
    indicators = get_risk_indicators(input_features)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Metrics
        st.markdown("**Health Scores (0-100)**")
        col_a, col_b = st.columns(2)
        col_a.metric("Financial Health", f"{indicators['financial_health_score']:.0f}")
        col_a.metric("Growth Health", f"{indicators['growth_health_score']:.0f}")
        col_b.metric("Team Health", f"{indicators['team_health_score']:.0f}")
        col_b.metric("Market Risk", f"{indicators['market_risk_score']:.0f}")
    
    with col2:
        fig = create_risk_radar(indicators)
        st.plotly_chart(fig, use_container_width=True)
    
    # Key Metrics
    st.subheader("📈 Key Metrics Overview")
    fig = create_metrics_comparison(input_features)
    st.plotly_chart(fig, use_container_width=True)
    
    # Feature Importance
    st.subheader("🔍 AI Explainability - What Drives the Prediction?")
    
    if explanation.get('error'):
        st.warning(f"⚠️ {explanation['error']}")
        # Fallback to model feature importance
        feature_importance = st.session_state.model.get_feature_importance()
    else:
        feature_importance = explanation['feature_importance']
    
    if feature_importance:
        fig = create_feature_importance_chart(feature_importance)
        st.plotly_chart(fig, use_container_width=True)
        
        # SHAP Waterfall
        if explanation.get('shap_values') is not None:
            st.subheader("💧 SHAP Waterfall Analysis")
            fig = create_shap_waterfall(
                explanation['shap_values'],
                input_features[get_feature_columns()],
                get_feature_columns(),
                explanation['base_value']
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Recommendations
    st.subheader("💡 AI-Generated Recommendations")
    recommendations = generate_recommendations(input_features, failure_prob, feature_importance)
    
    for rec in recommendations:
        with st.expander(f"{rec['category']} - {rec['issue']} [{rec['priority']}]"):
            st.markdown(f"**Action:** {rec['action']}")
            st.markdown(f"**Impact:** {rec['impact']}")
    
    # Action Plan
    st.subheader("📋 30-60-90 Day Action Plan")
    action_plan = generate_action_plan(input_features, failure_prob)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🔴 30 Days (Critical)**")
        for action in action_plan['30_days']:
            st.markdown(f"- {action}")
    
    with col2:
        st.markdown("**🟡 60 Days (Important)**")
        for action in action_plan['60_days'][:5]:
            st.markdown(f"- {action}")
    
    with col3:
        st.markdown("**🟢 90 Days (Strategic)**")
        for action in action_plan['90_days'][:5]:
            st.markdown(f"- {action}")


def main():
    """Main application"""
    initialize_session_state()
    display_header()
    
    st.markdown("---")
    
    # Model Training
    train_model_section()
    
    st.markdown("---")
    
    # Prediction
    prediction_section()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p>🚀 <strong>AI Startup Survival Prediction Platform</strong> | Built with Streamlit, XGBoost & SHAP</p>
        <p>Like Tesla Autopilot for Startups - Predict failures, prevent disasters 💎</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
