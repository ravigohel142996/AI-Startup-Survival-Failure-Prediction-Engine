"""
Visualization utilities for startup survival dashboard
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import Dict, List


def create_gauge_chart(value: float, title: str, color_scheme: str = 'probability') -> go.Figure:
    """
    Create a gauge chart for probability or score
    
    Args:
        value: Value between 0-100 (will convert if between 0-1)
        title: Chart title
        color_scheme: 'probability' or 'score'
    """
    # Normalize to 0-100 range if value is between 0-1
    if value <= 1.0:
        value = value * 100
    
    if color_scheme == 'probability':
        # For failure probability (high is bad)
        if value < 30:
            color = 'green'
        elif value < 50:
            color = 'yellow'
        elif value < 70:
            color = 'orange'
        else:
            color = 'red'
    else:
        # For scores (high is good)
        if value > 70:
            color = 'green'
        elif value > 50:
            color = 'yellow'
        elif value > 30:
            color = 'orange'
        else:
            color = 'red'
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title, 'font': {'size': 20}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 30], 'color': 'lightgray'},
                {'range': [30, 70], 'color': 'gray'}
            ],
            'threshold': {
                'line': {'color': 'red', 'width': 4},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))
    
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20))
    return fig


def create_feature_importance_chart(feature_importance: Dict) -> go.Figure:
    """
    Create horizontal bar chart for feature importance
    """
    sorted_features = dict(sorted(feature_importance.items(), 
                                 key=lambda x: abs(x[1]), 
                                 reverse=True)[:10])
    
    colors = ['red' if v > 0 else 'green' for v in sorted_features.values()]
    
    fig = go.Figure(go.Bar(
        x=list(sorted_features.values()),
        y=list(sorted_features.keys()),
        orientation='h',
        marker=dict(color=colors),
        text=[f"{v:.3f}" for v in sorted_features.values()],
        textposition='auto',
    ))
    
    fig.update_layout(
        title='Top 10 Risk Factors (Red = Increases Risk)',
        xaxis_title='Impact on Failure Risk',
        yaxis_title='Feature',
        height=400,
        margin=dict(l=150, r=20, t=50, b=50)
    )
    
    return fig


def create_metrics_comparison(df: pd.DataFrame) -> go.Figure:
    """
    Create comparison chart of key metrics
    """
    metrics = {
        'Runway': df['runway_months'].iloc[0],
        'Revenue/Cost': df['revenue_to_cost_ratio'].iloc[0] * 100,
        'Growth Rate': df['monthly_growth_rate'].iloc[0],
        'Team Size': df['team_size'].iloc[0],
        'Customers': df['customer_count'].iloc[0] / 10
    }
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=list(metrics.keys()),
        y=list(metrics.values()),
        marker_color=['blue', 'green', 'orange', 'purple', 'red'],
        text=[f"{v:.1f}" for v in metrics.values()],
        textposition='auto',
    ))
    
    fig.update_layout(
        title='Key Metrics Overview',
        yaxis_title='Value',
        height=350,
        margin=dict(l=20, r=20, t=50, b=50)
    )
    
    return fig


def create_risk_radar(indicators: Dict) -> go.Figure:
    """
    Create radar chart for risk indicators
    """
    categories = ['Financial Health', 'Growth Health', 'Team Health', 'Market Risk (inverted)']
    values = [
        indicators['financial_health_score'],
        indicators['growth_health_score'],
        indicators['team_health_score'],
        100 - indicators['market_risk_score']  # Invert so high is good
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Your Startup',
        line=dict(color='blue', width=2)
    ))
    
    # Add benchmark (ideal startup)
    fig.add_trace(go.Scatterpolar(
        r=[80, 80, 80, 80],
        theta=categories,
        fill='toself',
        name='Healthy Benchmark',
        line=dict(color='green', width=2, dash='dash'),
        opacity=0.3
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100])
        ),
        showlegend=True,
        title='Health Score Radar',
        height=400
    )
    
    return fig


def create_timeline_chart(timeline_data: Dict) -> go.Figure:
    """
    Create timeline visualization
    """
    months = list(range(0, int(timeline_data['estimated_survival_months']) + 6))
    runway = [timeline_data['runway_months']] * len(months)
    estimated = [timeline_data['estimated_survival_months']] * len(months)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=months,
        y=runway,
        mode='lines',
        name='Current Runway',
        line=dict(color='blue', width=3, dash='dash')
    ))
    
    fig.add_trace(go.Scatter(
        x=months,
        y=estimated,
        mode='lines',
        name='Predicted Survival',
        line=dict(color='red', width=3)
    ))
    
    # Add safety threshold
    fig.add_hline(y=12, line_dash="dot", line_color="green",
                  annotation_text="Safe Runway (12 months)")
    
    fig.update_layout(
        title='Survival Timeline Projection',
        xaxis_title='Months from Now',
        yaxis_title='Months of Runway',
        height=350,
        margin=dict(l=20, r=20, t=50, b=50)
    )
    
    return fig


def create_shap_waterfall(shap_values: np.ndarray, features: pd.DataFrame, 
                         feature_names: List[str], base_value: float) -> go.Figure:
    """
    Create SHAP waterfall chart
    """
    # Get top features by absolute SHAP value
    indices = np.argsort(np.abs(shap_values))[-10:][::-1]
    
    values = shap_values[indices]
    names = [feature_names[i] for i in indices]
    feature_vals = [features.iloc[0, i] for i in indices]
    
    cumulative = [base_value]
    for val in values:
        cumulative.append(cumulative[-1] + val)
    
    fig = go.Figure()
    
    # Create waterfall effect
    for i, (name, val, feat_val) in enumerate(zip(names, values, feature_vals)):
        color = 'red' if val > 0 else 'green'
        fig.add_trace(go.Bar(
            x=[i],
            y=[abs(val)],
            base=min(cumulative[i], cumulative[i+1]),
            marker=dict(color=color),
            name=f"{name}={feat_val:.1f}",
            text=f"{val:.3f}",
            textposition='auto',
            showlegend=False
        ))
    
    fig.update_layout(
        title='SHAP Impact Analysis (How each feature affects prediction)',
        xaxis=dict(ticktext=names, tickvals=list(range(len(names))), tickangle=-45),
        yaxis_title='SHAP Value (Impact on Risk)',
        height=450,
        margin=dict(l=20, r=20, t=50, b=150)
    )
    
    return fig
