"""
Data processing utilities for startup survival prediction
"""
import pandas as pd
import numpy as np
from typing import Dict, Tuple, List
import warnings
warnings.filterwarnings('ignore')


def generate_sample_data(n_samples: int = 100) -> pd.DataFrame:
    """
    Generate sample startup data for demonstration
    """
    np.random.seed(42)
    
    data = {
        'startup_id': range(1, n_samples + 1),
        'burn_rate': np.random.uniform(10000, 500000, n_samples),
        'revenue': np.random.uniform(0, 1000000, n_samples),
        'funding_raised': np.random.uniform(50000, 5000000, n_samples),
        'team_size': np.random.randint(2, 50, n_samples),
        'months_since_founding': np.random.randint(1, 60, n_samples),
        'monthly_growth_rate': np.random.uniform(-10, 50, n_samples),
        'customer_count': np.random.randint(0, 10000, n_samples),
        'market_competition': np.random.randint(1, 10, n_samples),
        'team_experience': np.random.randint(1, 20, n_samples),
        'pivots_count': np.random.randint(0, 5, n_samples),
        'investor_count': np.random.randint(0, 10, n_samples),
    }
    
    df = pd.DataFrame(data)
    
    # Create target based on logical rules
    df['runway_months'] = df['funding_raised'] / (df['burn_rate'] + 1)
    df['revenue_to_cost_ratio'] = df['revenue'] / (df['burn_rate'] + 1)
    df['customer_per_team'] = df['customer_count'] / (df['team_size'] + 1)
    
    # Survival logic
    survival_score = (
        (df['runway_months'] > 12).astype(int) * 3 +
        (df['revenue_to_cost_ratio'] > 0.5).astype(int) * 2 +
        (df['monthly_growth_rate'] > 10).astype(int) * 2 +
        (df['team_experience'] > 5).astype(int) * 1 +
        (df['investor_count'] > 2).astype(int) * 1 +
        (df['market_competition'] < 7).astype(int) * 1
    )
    
    # Add some randomness
    survival_score += np.random.randint(-2, 3, n_samples)
    
    # Create binary target
    df['survived'] = (survival_score > 5).astype(int)
    
    return df


def validate_data(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """
    Validate uploaded data
    """
    errors = []
    required_columns = [
        'burn_rate', 'revenue', 'funding_raised', 'team_size',
        'months_since_founding', 'monthly_growth_rate', 'customer_count',
        'market_competition', 'team_experience', 'pivots_count', 'investor_count'
    ]
    
    # Check required columns
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        errors.append(f"Missing required columns: {', '.join(missing_cols)}")
    
    # Check for negative values where not allowed
    numeric_cols = ['burn_rate', 'revenue', 'funding_raised', 'team_size', 
                    'months_since_founding', 'customer_count', 'team_experience']
    
    for col in numeric_cols:
        if col in df.columns and (df[col] < 0).any():
            errors.append(f"Column '{col}' contains negative values")
    
    # Check data types
    for col in required_columns:
        if col in df.columns and not pd.api.types.is_numeric_dtype(df[col]):
            errors.append(f"Column '{col}' must be numeric")
    
    return len(errors) == 0, errors


def calculate_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate derived features for prediction
    """
    df = df.copy()
    
    # Financial health features
    df['runway_months'] = df['funding_raised'] / (df['burn_rate'] + 1)
    df['revenue_to_cost_ratio'] = df['revenue'] / (df['burn_rate'] + 1)
    df['burn_rate_per_employee'] = df['burn_rate'] / (df['team_size'] + 1)
    df['revenue_per_employee'] = df['revenue'] / (df['team_size'] + 1)
    
    # Growth features
    df['customer_per_team'] = df['customer_count'] / (df['team_size'] + 1)
    df['customer_growth_potential'] = df['customer_count'] * (df['monthly_growth_rate'] + 1) / 100
    
    # Risk features
    df['competition_risk'] = df['market_competition'] / 10
    df['pivot_risk'] = np.minimum(df['pivots_count'] / 5, 1)
    df['funding_adequacy'] = df['funding_raised'] / (df['burn_rate'] * 12 + 1)
    
    # Experience features
    df['avg_team_experience'] = df['team_experience'] / (df['team_size'] + 1)
    df['investor_confidence'] = df['investor_count'] / 10
    
    return df


def get_feature_columns() -> List[str]:
    """
    Get list of feature columns for modeling
    """
    return [
        'burn_rate', 'revenue', 'funding_raised', 'team_size',
        'months_since_founding', 'monthly_growth_rate', 'customer_count',
        'market_competition', 'team_experience', 'pivots_count', 'investor_count',
        'runway_months', 'revenue_to_cost_ratio', 'burn_rate_per_employee',
        'revenue_per_employee', 'customer_per_team', 'customer_growth_potential',
        'competition_risk', 'pivot_risk', 'funding_adequacy',
        'avg_team_experience', 'investor_confidence'
    ]


def get_risk_level(probability: float) -> Tuple[str, str]:
    """
    Get risk level and color based on failure probability
    """
    if probability < 0.3:
        return "Low Risk", "green"
    elif probability < 0.5:
        return "Medium Risk", "orange"
    elif probability < 0.7:
        return "High Risk", "red"
    else:
        return "Critical Risk", "darkred"


def calculate_survival_timeline(df: pd.DataFrame, prediction: float) -> Dict:
    """
    Calculate estimated survival timeline
    """
    runway = df['runway_months'].iloc[0]
    growth_rate = df['monthly_growth_rate'].iloc[0]
    
    if prediction > 0.7:  # High risk
        estimated_months = min(runway * 0.5, 6)
    elif prediction > 0.5:  # Medium-high risk
        estimated_months = min(runway * 0.7, 12)
    elif prediction > 0.3:  # Medium-low risk
        estimated_months = runway
    else:  # Low risk
        estimated_months = max(runway, 24)
    
    return {
        'estimated_survival_months': round(estimated_months, 1),
        'runway_months': round(runway, 1),
        'growth_adjusted': growth_rate > 0
    }
