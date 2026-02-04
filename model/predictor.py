"""
ML Model for startup survival prediction
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from xgboost import XGBClassifier
import joblib
import shap
from typing import Dict, Tuple, Optional
import os
import warnings
warnings.filterwarnings('ignore')


class StartupSurvivalModel:
    """
    Ensemble model for predicting startup survival
    """
    
    def __init__(self, model_type: str = 'xgboost'):
        """
        Initialize the model
        
        Args:
            model_type: 'xgboost' or 'random_forest'
        """
        self.model_type = model_type
        self.model = None
        self.feature_names = None
        self.explainer = None
        
        if model_type == 'xgboost':
            self.model = XGBClassifier(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42,
                eval_metric='logloss'
            )
        else:
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            )
    
    def train(self, X: pd.DataFrame, y: pd.Series, test_size: float = 0.2) -> Dict:
        """
        Train the model
        
        Args:
            X: Feature dataframe
            y: Target variable (1 = survived, 0 = failed)
            test_size: Test set size
            
        Returns:
            Dictionary with training metrics
        """
        self.feature_names = X.columns.tolist()
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        # Train model
        self.model.fit(X_train, y_train)
        
        # Predictions
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]
        
        # Calculate metrics
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1_score': f1_score(y_test, y_pred),
            'roc_auc': roc_auc_score(y_test, y_pred_proba),
            'train_samples': len(X_train),
            'test_samples': len(X_test)
        }
        
        # Initialize SHAP explainer
        try:
            if self.model_type == 'xgboost':
                self.explainer = shap.TreeExplainer(self.model)
            else:
                # Use a sample for faster computation
                sample_size = min(100, len(X_train))
                background = shap.sample(X_train, sample_size)
                self.explainer = shap.TreeExplainer(self.model, background)
        except Exception as e:
            print(f"Warning: Could not initialize SHAP explainer: {e}")
            self.explainer = None
        
        return metrics
    
    def predict(self, X: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """
        Make predictions
        
        Args:
            X: Feature dataframe
            
        Returns:
            Tuple of (predictions, probabilities)
        """
        if self.model is None:
            raise ValueError("Model not trained yet")
        
        predictions = self.model.predict(X)
        probabilities = self.model.predict_proba(X)
        
        return predictions, probabilities
    
    def predict_single(self, X: pd.DataFrame) -> Dict:
        """
        Predict for a single startup with detailed output
        
        Args:
            X: Single row feature dataframe
            
        Returns:
            Dictionary with prediction details
        """
        predictions, probabilities = self.predict(X)
        
        # Probability of failure (class 0)
        failure_prob = probabilities[0][0]
        survival_prob = probabilities[0][1]
        
        result = {
            'prediction': 'SURVIVE' if predictions[0] == 1 else 'FAIL',
            'failure_probability': float(failure_prob),
            'survival_probability': float(survival_prob),
            'confidence': float(max(failure_prob, survival_prob))
        }
        
        return result
    
    def get_feature_importance(self, X: Optional[pd.DataFrame] = None) -> Dict[str, float]:
        """
        Get feature importance
        
        Args:
            X: Optional dataframe for SHAP values
            
        Returns:
            Dictionary of feature importances
        """
        if self.model is None:
            raise ValueError("Model not trained yet")
        
        # Use model's native feature importance
        if hasattr(self.model, 'feature_importances_'):
            importances = self.model.feature_importances_
            feature_importance = dict(zip(self.feature_names, importances))
            return dict(sorted(feature_importance.items(), 
                             key=lambda x: x[1], 
                             reverse=True))
        
        return {}
    
    def explain_prediction(self, X: pd.DataFrame) -> Dict:
        """
        Explain prediction using SHAP values
        
        Args:
            X: Single row feature dataframe
            
        Returns:
            Dictionary with SHAP values and base value
        """
        if self.explainer is None:
            return {
                'shap_values': None,
                'base_value': None,
                'feature_values': X.iloc[0].to_dict(),
                'error': 'SHAP explainer not available'
            }
        
        try:
            # Calculate SHAP values
            shap_values = self.explainer.shap_values(X)
            
            # Handle different SHAP output formats
            if isinstance(shap_values, list):
                # For binary classification, use failure class (index 0)
                shap_values_array = shap_values[0][0]
            else:
                shap_values_array = shap_values[0]
            
            base_value = self.explainer.expected_value
            if isinstance(base_value, (list, np.ndarray)):
                base_value = base_value[0]
            
            # Create feature importance dictionary
            feature_importance = {}
            for i, feature in enumerate(self.feature_names):
                feature_importance[feature] = float(shap_values_array[i])
            
            return {
                'shap_values': shap_values_array,
                'base_value': float(base_value),
                'feature_importance': feature_importance,
                'feature_values': X.iloc[0].to_dict()
            }
        except Exception as e:
            return {
                'shap_values': None,
                'base_value': None,
                'feature_values': X.iloc[0].to_dict(),
                'error': f'Error calculating SHAP values: {str(e)}'
            }
    
    def save(self, filepath: str):
        """
        Save model to disk
        """
        model_data = {
            'model': self.model,
            'model_type': self.model_type,
            'feature_names': self.feature_names,
            'explainer': self.explainer
        }
        joblib.dump(model_data, filepath)
    
    @classmethod
    def load(cls, filepath: str) -> 'StartupSurvivalModel':
        """
        Load model from disk
        """
        model_data = joblib.load(filepath)
        
        instance = cls(model_type=model_data['model_type'])
        instance.model = model_data['model']
        instance.feature_names = model_data['feature_names']
        instance.explainer = model_data.get('explainer')
        
        return instance


def train_model_from_data(df: pd.DataFrame, target_column: str = 'survived',
                          model_type: str = 'xgboost') -> Tuple[StartupSurvivalModel, Dict]:
    """
    Train model from dataframe
    
    Args:
        df: Dataframe with features and target
        target_column: Name of target column
        model_type: Type of model to train
        
    Returns:
        Tuple of (trained model, metrics)
    """
    from utils.data_processing import calculate_features, get_feature_columns
    
    # Calculate features
    df_features = calculate_features(df)
    
    # Prepare data
    feature_cols = get_feature_columns()
    X = df_features[feature_cols]
    y = df[target_column]
    
    # Train model
    model = StartupSurvivalModel(model_type=model_type)
    metrics = model.train(X, y)
    
    return model, metrics
