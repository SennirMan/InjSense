import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import xgboost as xgb
import joblib

# Load dataset
df = pd.read_csv("data/example_data.csv")

# Split features and labels
X = df.drop(columns=["injury_risk", "fatigue_level"])
y_risk = df["injury_risk"]
y_fatigue = df["fatigue_level"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y_risk, test_size=0.2, random_state=42)

# Train XGBoost model
model = xgb.XGBRegressor(n_estimators=100, max_depth=5, learning_rate=0.05)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
rmse = mean_squared_error(y_test, y_pred, squared=False)
print(f"Validation RMSE (Injury Risk): {rmse:.2f}")

# Save model
joblib.dump(model, "models/risk_model.pkl")
print("Model saved to models/risk_model.pkl")
