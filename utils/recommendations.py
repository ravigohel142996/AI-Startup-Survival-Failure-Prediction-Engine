"""
Recommendation engine for startup survival
"""
from typing import List, Dict
import pandas as pd


def generate_recommendations(df: pd.DataFrame, failure_prob: float, 
                            feature_importance: Dict) -> List[Dict]:
    """
    Generate actionable recommendations based on prediction and feature importance
    """
    recommendations = []
    
    # Get key metrics
    runway_months = df['runway_months'].iloc[0]
    revenue_to_cost = df['revenue_to_cost_ratio'].iloc[0]
    burn_rate = df['burn_rate'].iloc[0]
    revenue = df['revenue'].iloc[0]
    growth_rate = df['monthly_growth_rate'].iloc[0]
    team_size = df['team_size'].iloc[0]
    customer_count = df['customer_count'].iloc[0]
    market_competition = df['market_competition'].iloc[0]
    
    # Critical: Runway Analysis
    if runway_months < 6:
        recommendations.append({
            'category': '🚨 CRITICAL',
            'priority': 'HIGH',
            'issue': 'Cash Runway Critically Low',
            'action': f'Your runway is only {runway_months:.1f} months. Immediately raise funds or reduce burn rate by at least 50%.',
            'impact': 'Survival Risk'
        })
    elif runway_months < 12:
        recommendations.append({
            'category': '⚠️ WARNING',
            'priority': 'HIGH',
            'issue': 'Low Cash Runway',
            'action': f'Runway is {runway_months:.1f} months. Start fundraising now or optimize expenses.',
            'impact': 'Financial Stability'
        })
    
    # Revenue vs Cost Analysis
    if revenue_to_cost < 0.3:
        recommendations.append({
            'category': '🚨 CRITICAL',
            'priority': 'HIGH',
            'issue': 'Revenue Far Below Costs',
            'action': f'Revenue covers only {revenue_to_cost*100:.1f}% of costs. Focus on sales or reduce burn rate immediately.',
            'impact': 'Business Model'
        })
    elif revenue_to_cost < 0.7:
        recommendations.append({
            'category': '⚠️ WARNING',
            'priority': 'MEDIUM',
            'issue': 'Revenue Below Costs',
            'action': 'Accelerate sales, improve pricing, or optimize unit economics.',
            'impact': 'Profitability Path'
        })
    
    # Growth Analysis
    if growth_rate < 0:
        recommendations.append({
            'category': '🚨 CRITICAL',
            'priority': 'HIGH',
            'issue': 'Negative Growth',
            'action': 'Growth is declining. Re-evaluate product-market fit, marketing strategy, or consider pivot.',
            'impact': 'Market Traction'
        })
    elif growth_rate < 10:
        recommendations.append({
            'category': '⚠️ WARNING',
            'priority': 'MEDIUM',
            'issue': 'Low Growth Rate',
            'action': 'Growth is below 10% MoM. Invest in customer acquisition and retention strategies.',
            'impact': 'Scalability'
        })
    
    # Team Efficiency
    revenue_per_employee = revenue / (team_size + 1)
    if revenue_per_employee < 10000 and revenue > 0:
        recommendations.append({
            'category': '💡 OPTIMIZATION',
            'priority': 'MEDIUM',
            'issue': 'Low Revenue per Employee',
            'action': f'${revenue_per_employee:.0f} per employee. Consider team optimization or sales enablement.',
            'impact': 'Operational Efficiency'
        })
    
    # Customer Base
    if customer_count < 100:
        recommendations.append({
            'category': '⚠️ WARNING',
            'priority': 'MEDIUM',
            'issue': 'Small Customer Base',
            'action': f'Only {customer_count} customers. Scale customer acquisition to validate product-market fit.',
            'impact': 'Market Validation'
        })
    
    # Market Competition
    if market_competition > 7:
        recommendations.append({
            'category': '💡 OPTIMIZATION',
            'priority': 'LOW',
            'issue': 'High Market Competition',
            'action': 'Market is highly competitive. Develop unique differentiation or find a niche.',
            'impact': 'Competitive Advantage'
        })
    
    # Overall Risk Assessment
    if failure_prob > 0.7:
        recommendations.append({
            'category': '🚨 CRITICAL',
            'priority': 'HIGH',
            'issue': 'Critical Failure Risk',
            'action': 'Multiple red flags detected. Consider strategic pivot, aggressive fundraising, or cost restructuring.',
            'impact': 'Immediate Survival'
        })
    
    # Positive Reinforcement
    if failure_prob < 0.3:
        recommendations.append({
            'category': '✅ STRENGTH',
            'priority': 'INFO',
            'issue': 'Strong Foundation',
            'action': 'Your startup shows healthy metrics. Focus on scaling while maintaining financial discipline.',
            'impact': 'Growth Opportunity'
        })
    
    return sorted(recommendations, key=lambda x: {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2, 'INFO': 3}[x['priority']])


def generate_action_plan(df: pd.DataFrame, failure_prob: float) -> Dict:
    """
    Generate 30-60-90 day action plan
    """
    action_plan = {
        '30_days': [],
        '60_days': [],
        '90_days': []
    }
    
    runway_months = df['runway_months'].iloc[0]
    revenue_to_cost = df['revenue_to_cost_ratio'].iloc[0]
    growth_rate = df['monthly_growth_rate'].iloc[0]
    
    # 30-day priorities (Critical)
    if runway_months < 6:
        action_plan['30_days'].extend([
            'Start emergency fundraising conversations',
            'Cut all non-essential expenses',
            'Negotiate extended payment terms with vendors'
        ])
    
    if revenue_to_cost < 0.5:
        action_plan['30_days'].extend([
            'Launch aggressive sales campaign',
            'Implement customer success program to reduce churn',
            'Review and optimize pricing strategy'
        ])
    
    if growth_rate < 5:
        action_plan['30_days'].extend([
            'Conduct customer interviews to understand pain points',
            'Test new marketing channels',
            'Implement referral program'
        ])
    
    # 60-day priorities (Important)
    action_plan['60_days'].extend([
        'Build strategic partnership pipeline',
        'Develop customer retention metrics and dashboard',
        'Implement automated sales processes',
        'Create content marketing strategy',
        'Establish advisory board with industry experts'
    ])
    
    # 90-day priorities (Strategic)
    action_plan['90_days'].extend([
        'Develop new revenue streams or product features',
        'Plan Series A/next fundraising round',
        'Build scalable growth infrastructure',
        'Expand to adjacent markets or segments',
        'Implement comprehensive analytics and KPI tracking'
    ])
    
    return action_plan


def get_risk_indicators(df: pd.DataFrame) -> Dict:
    """
    Calculate detailed risk indicators
    """
    indicators = {}
    
    # Financial Health Score (0-100)
    runway_score = min(df['runway_months'].iloc[0] / 24 * 40, 40)
    revenue_score = min(df['revenue_to_cost_ratio'].iloc[0] * 30, 30)
    funding_score = min(df['funding_adequacy'].iloc[0] / 2 * 30, 30)
    indicators['financial_health_score'] = round(runway_score + revenue_score + funding_score, 1)
    
    # Growth Health Score (0-100)
    growth_score = min(max(df['monthly_growth_rate'].iloc[0], 0) / 30 * 50, 50)
    customer_score = min(df['customer_count'].iloc[0] / 1000 * 50, 50)
    indicators['growth_health_score'] = round(growth_score + customer_score, 1)
    
    # Team Health Score (0-100)
    team_exp_score = min(df['team_experience'].iloc[0] / 15 * 60, 60)
    team_size_score = min(df['team_size'].iloc[0] / 30 * 40, 40)
    indicators['team_health_score'] = round(team_exp_score + team_size_score, 1)
    
    # Market Risk Score (0-100, lower is better)
    competition_score = df['market_competition'].iloc[0] / 10 * 60
    pivot_score = df['pivots_count'].iloc[0] / 5 * 40
    indicators['market_risk_score'] = round(min(competition_score + pivot_score, 100), 1)
    
    return indicators
