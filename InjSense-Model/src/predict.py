import joblib
import numpy as np
from src.feature_extraction import extract_all_features

# Load trained model
model = joblib.load("models/risk_model.pkl")

def predict_risk(emg_window, hr_window, temp_window):
    features = extract_all_features(emg_window, hr_window, temp_window)
    features = np.array(features).reshape(1, -1)
    risk = model.predict(features)[0]
    return round(risk, 2)

# Example usage
if __name__ == "__main__":
    emg_example = np.random.randn(250, 3)  # 250 samples, 3 channels
    hr_example = [85, 87, 86, 90, 88]
    temp_example = [36.5, 36.6, 36.7, 36.8, 36.9]

    risk_score = predict_risk(emg_example, hr_example, temp_example)
    print(f"Predicted Injury Risk: {risk_score}%")
