import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import xgboost as xgb
import joblib
from src.feature_extraction import extract_all_features

# Load your dataset
df = pd.read_csv("data/example_data.csv")

# Assuming the data format is already in suitable format for model
# Features (EMG, HR, Temp columns) and labels (injury risk, fatigue level)
X = df.drop(columns=["injury_risk", "fatigue_level"])
y_risk = df["injury_risk"]
y_fatigue = df["fatigue_level"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y_risk, test_size=0.2, random_state=42)

# Train XGBoost model
model = xgb.XGBRegressor(n_estimators=100, max_depth=5, learning_rate=0.05)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
rmse = mean_squared_error(y_test, y_pred, squared=False)
print(f"Validation RMSE (Injury Risk): {rmse}")

# Save the trained model
joblib.dump(model, "models/risk_model.pkl")
print("Model saved as models/risk_model.pkl")
