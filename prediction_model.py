import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline
import joblib
import os
import random

class PredictionModel:
    """
    Class for injury risk prediction model
    """
    
    def __init__(self):
        """Initialize the PredictionModel class"""
        self.model = None
        self.feature_names = [
            'semg_imbalance', 'muscle_fatigue', 'training_load',
            'recovery_time', 'previous_injuries', 'temperature_variation',
            'age', 'consecutive_games'
        ]
        self.target = 'injury_risk'
        
        # Try to load existing model if available, otherwise create a new one
        try:
            self.load_model()
            print("Loaded existing prediction model")
        except:
            print("Creating new prediction model")
            self.train_model()
    
    def train_model(self):
        """
        Train a new injury prediction model
        
        Note: In a real-world application, this would use actual historical data
        """
        # Generate synthetic training data (in a real app, this would be loaded from a database)
        # We're generating synthetic data to demonstrate the model functionality
        np.random.seed(42)
        n_samples = 1000
        
        X = np.zeros((n_samples, len(self.feature_names)))
        y = np.zeros(n_samples)
        
        # Generate feature data with realistic correlations to the target
        for i in range(n_samples):
            # sEMG imbalance (0-50%)
            X[i, 0] = np.random.uniform(0, 50)
            
            # Muscle fatigue (0-100)
            X[i, 1] = np.random.uniform(0, 100)
            
            # Training load (arbitrary units, 0-100)
            X[i, 2] = np.random.uniform(0, 100)
            
            # Recovery time (hours, 0-72)
            X[i, 3] = np.random.uniform(0, 72)
            
            # Previous injuries count (0-5)
            X[i, 4] = np.random.randint(0, 6)
            
            # Temperature variation (degrees C, 0-3)
            X[i, 5] = np.random.uniform(0, 3)
            
            # Age (years, 18-35)
            X[i, 6] = np.random.randint(18, 36)
            
            # Consecutive games played (0-15)
            X[i, 7] = np.random.randint(0, 16)
            
            # Calculate injury risk based on a weighted formula of features
            # This simulates the complex relationship between features and injury risk
            risk = (
                0.3 * X[i, 0] +       # semg_imbalance
                0.2 * X[i, 1] / 100 + # muscle_fatigue (normalized)
                0.15 * X[i, 2] / 100 + # training_load (normalized)
                0.15 * (72 - X[i, 3]) / 72 + # recovery_time (inverted and normalized)
                0.1 * X[i, 4] / 5 +   # previous_injuries (normalized)
                0.05 * X[i, 5] / 3 +  # temperature_variation (normalized)
                0.025 * (X[i, 6] - 18) / 17 + # age (normalized)
                0.025 * X[i, 7] / 15  # consecutive_games (normalized)
            )
            
            # Add some noise to make the model more realistic
            risk += np.random.normal(0, 0.1)
            
            # Clamp between 0 and 1
            risk = max(0, min(1, risk))
            
            # Convert to binary label (high risk = 1, low risk = 0)
            # using a threshold of 0.5
            y[i] = 1 if risk > 0.5 else 0
        
        # Create a DataFrame for clarity
        X_df = pd.DataFrame(X, columns=self.feature_names)
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X_df, y, test_size=0.2, random_state=42
        )
        
        # Create a pipeline with preprocessing and model
        self.model = Pipeline([
            ('scaler', StandardScaler()),
            ('classifier', RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42
            ))
        ])
        
        # Train the model
        self.model.fit(X_train, y_train)
        
        # Evaluate the model
        y_pred = self.model.predict(X_test)
        print(classification_report(y_test, y_pred))
        
        # Save the model
        self.save_model()
    
    def predict_risk(self, athlete_data):
        """
        Predict injury risk for an athlete
        
        Args:
            athlete_data (dict): Dictionary containing athlete metrics
            
        Returns:
            dict: Risk prediction results
        """
        # Extract features from athlete data
        # In a real application, this would extract actual values
        # Here we're creating synthetic data for demonstration
        
        features = np.zeros(len(self.feature_names))
        
        # Fill in available features from athlete_data
        for i, feature in enumerate(self.feature_names):
            if feature in athlete_data:
                features[i] = athlete_data[feature]
            else:
                # Generate realistic values for missing features
                if feature == 'semg_imbalance':
                    features[i] = random.uniform(5, 30)
                elif feature == 'muscle_fatigue':
                    features[i] = random.uniform(20, 80)
                elif feature == 'training_load':
                    features[i] = random.uniform(30, 90)
                elif feature == 'recovery_time':
                    features[i] = random.uniform(12, 48)
                elif feature == 'previous_injuries':
                    features[i] = len(athlete_data.get('injury_history', []))
                elif feature == 'temperature_variation':
                    features[i] = random.uniform(0.1, 1.5)
                elif feature == 'age':
                    features[i] = athlete_data.get('age', random.randint(18, 35))
                elif feature == 'consecutive_games':
                    features[i] = random.randint(0, 10)
        
        # Convert to DataFrame for prediction
        X = pd.DataFrame([features], columns=self.feature_names)
        
        # Make prediction
        probability = self.model.predict_proba(X)[0, 1]  # Probability of high risk
        risk_score = int(probability * 100)  # Convert to 0-100 scale
        risk_label = "High" if risk_score >= 60 else ("Medium" if risk_score >= 30 else "Low")
        
        # Get feature importances for this prediction
        importances = self.get_feature_importance()
        
        return {
            "risk_score": risk_score,
            "risk_label": risk_label,
            "risk_factors": importances,
            "prediction_confidence": int((1 - abs(probability - 0.5) * 2) * 100)  # Higher near 0.5
        }
    
    def get_feature_importance(self):
        """
        Get the importance of each feature in the model
        
        Returns:
            dict: Feature names and their importance values
        """
        if self.model is None:
            self.train_model()
            
        # Extract the feature importances from the Random Forest model
        importances = self.model.named_steps['classifier'].feature_importances_
        
        # Create a dictionary of feature names and their importance values
        importance_dict = {
            name: float(importance) 
            for name, importance in zip(self.feature_names, importances)
        }
        
        # Sort by importance (descending)
        sorted_importances = sorted(
            importance_dict.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        return dict(sorted_importances)
    
    def save_model(self, filename='injury_prediction_model.joblib'):
        """
        Save the model to disk
        
        Args:
            filename (str, optional): Filename to save the model. Defaults to 'injury_prediction_model.joblib'.
        """
        if self.model is not None:
            try:
                joblib.dump(self.model, filename)
                print(f"Model saved to {filename}")
            except Exception as e:
                print(f"Error saving model: {e}")
    
    def load_model(self, filename='injury_prediction_model.joblib'):
        """
        Load the model from disk
        
        Args:
            filename (str, optional): Filename to load the model from. Defaults to 'injury_prediction_model.joblib'.
            
        Raises:
            FileNotFoundError: If the model file doesn't exist
        """
        if os.path.exists(filename):
            self.model = joblib.load(filename)
        else:
            raise FileNotFoundError(f"Model file {filename} not found")
