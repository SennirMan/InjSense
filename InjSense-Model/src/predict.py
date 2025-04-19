import joblib
import numpy as np
from src.feature_extraction import extract_all_features

# Load the trained model
model = joblib.load("models/risk_model.pkl")

def predict_risk(emg_window, hr_window, temp_window):
    """
    Predict injury risk given EMG, heart rate, and temperature data.
    """
    features = extract_all_features(emg_window, hr_window, temp_window)
    features = np.array(features).reshape(1, -1)  # Reshape for the model
    risk = model.predict(features)[0]  # Predict injury risk
    return round(risk, 2)

# Example usage
if __name__ == "__main__":
    emg_example = np.random.randn(250, 3)  # Simulated 1 second of EMG data (250Hz, 3 channels)
    hr_example = [85, 87, 86, 90, 88]      # 5 second HR readings
    temp_example = [36.5, 36.6, 36.7, 36.8, 36.9]  # 5 second temperature readings

    risk_score = predict_risk(emg_example, hr_example, temp_example)
    print(f"Predicted Injury Risk: {risk_score}%")
