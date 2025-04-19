import numpy as np

def extract_emg_features(emg_window):
    """
    Extract features from EMG data.
    """
    features = []
    for ch in range(emg_window.shape[1]):
        signal = emg_window[:, ch]

        rms = np.sqrt(np.mean(signal**2))       # Root Mean Square
        mav = np.mean(np.abs(signal))           # Mean Absolute Value
        iemg = np.sum(np.abs(signal))           # Integrated EMG
        wl = np.sum(np.abs(np.diff(signal)))    # Waveform Length
        zc = np.sum(np.diff(np.sign(signal)) != 0)  # Zero Crossings

        features.extend([rms, mav, iemg, wl, zc])
    return features

def extract_hr_features(hr_window):
    """
    Extract features from heart rate data.
    """
    hr_array = np.array(hr_window)
    mean_hr = np.mean(hr_array)
    std_hr = np.std(hr_array)
    delta_hr = hr_array[-1] - hr_array[0] if len(hr_array) > 1 else 0
    return [mean_hr, std_hr, delta_hr]

def extract_temp_features(temp_window):
    """
    Extract features from temperature data.
    """
    temp_array = np.array(temp_window)
    mean_temp = np.mean(temp_array)
    temp_rate = temp_array[-1] - temp_array[0] if len(temp_array) > 1 else 0
    return [mean_temp, temp_rate]

def extract_all_features(emg_window, hr_window, temp_window):
    """
    Extract all features (EMG + HR + Temp).
    """
    emg_feats = extract_emg_features(emg_window)
    hr_feats = extract_hr_features(hr_window)
    temp_feats = extract_temp_features(temp_window)
    return emg_feats + hr_feats + temp_feats
