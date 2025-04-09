import numpy as np
import pandas as pd
from scipy import signal
import random
from datetime import datetime, timedelta

class DataProcessor:
    """
    Class for processing biometric data from athletes
    """
    
    def __init__(self):
        """Initialize the DataProcessor class"""
        self.sample_rate = 1000  # Hz, typical for sEMG signals
        self.butterworth_order = 4
        self.lowcut = 20  # Hz, high-pass filter cut-off
        self.highcut = 450  # Hz, low-pass filter cut-off
    
    def filter_semg(self, semg_data):
        """
        Apply a bandpass Butterworth filter to sEMG data
        
        Args:
            semg_data (numpy.ndarray): Raw sEMG data
            
        Returns:
            numpy.ndarray: Filtered sEMG data
        """
        nyquist = 0.5 * self.sample_rate
        low = self.lowcut / nyquist
        high = self.highcut / nyquist
        
        b, a = signal.butter(
            self.butterworth_order, 
            [low, high], 
            btype='band'
        )
        
        filtered_data = signal.filtfilt(b, a, semg_data)
        return filtered_data
    
    def calculate_rms(self, semg_data, window_size=100):
        """
        Calculate the root mean square (RMS) of sEMG data
        
        Args:
            semg_data (numpy.ndarray): Filtered sEMG data
            window_size (int, optional): Window size for RMS calculation. Defaults to 100.
            
        Returns:
            numpy.ndarray: RMS values
        """
        squared = np.square(semg_data)
        windows = np.lib.stride_tricks.sliding_window_view(squared, window_size)
        rms = np.sqrt(np.mean(windows, axis=1))
        return rms
    
    def calculate_muscle_fatigue(self, semg_data):
        """
        Estimate muscle fatigue based on median frequency shift in sEMG data
        
        Args:
            semg_data (numpy.ndarray): Filtered sEMG data
            
        Returns:
            float: Fatigue index (0-100)
        """
        # Calculate power spectrum
        f, Pxx = signal.welch(semg_data, fs=self.sample_rate, nperseg=256)
        
        # Calculate median frequency
        total_power = np.sum(Pxx)
        cumulative_power = np.cumsum(Pxx)
        median_freq_idx = np.argmax(cumulative_power >= total_power / 2)
        median_freq = f[median_freq_idx]
        
        # Normalize to get fatigue index (lower median frequency means higher fatigue)
        # Typical median frequency range for healthy muscle is 50-120 Hz
        fatigue_index = 100 * (1 - (median_freq - 30) / 90)
        fatigue_index = max(0, min(100, fatigue_index))  # Clamp between 0-100
        
        return fatigue_index
    
    def calculate_muscle_imbalance(self, left_semg, right_semg):
        """
        Calculate muscle imbalance between left and right sides
        
        Args:
            left_semg (numpy.ndarray): Filtered sEMG data from left side
            right_semg (numpy.ndarray): Filtered sEMG data from right side
            
        Returns:
            float: Imbalance percentage (0-100)
        """
        left_rms = np.mean(self.calculate_rms(left_semg))
        right_rms = np.mean(self.calculate_rms(right_semg))
        
        # Calculate imbalance as percentage difference
        total = left_rms + right_rms
        if total > 0:
            imbalance = 100 * abs(left_rms - right_rms) / total
        else:
            imbalance = 0
            
        return imbalance
    
    def analyze_temperature(self, temp_data):
        """
        Analyze temperature data to detect abnormalities
        
        Args:
            temp_data (numpy.ndarray): Temperature readings in Celsius
            
        Returns:
            dict: Analysis results including average, max, min, and abnormality flag
        """
        avg_temp = np.mean(temp_data)
        max_temp = np.max(temp_data)
        min_temp = np.min(temp_data)
        std_temp = np.std(temp_data)
        
        # Flag if temperature variation is high or temp is elevated
        abnormal = (std_temp > 0.5) or (max_temp > 38.0)
        
        return {
            "average": avg_temp,
            "maximum": max_temp,
            "minimum": min_temp,
            "std_deviation": std_temp,
            "abnormal": abnormal
        }
    
    def get_athletes_list(self):
        """
        Get a list of all athletes in the system
        
        Returns:
            list: List of athlete dictionaries with name and ID
        """
        # In a real application, this would fetch from a database
        athletes = [
            {"id": 1, "name": "Khalid Ahmed", "team": "Team A", "position": "Forward"},
            {"id": 2, "name": "Sarah Wilson", "team": "Team A", "position": "Midfielder"},
            {"id": 3, "name": "Ahmed Hassan", "team": "Team B", "position": "Defender"},
            {"id": 4, "name": "Maria Rodriguez", "team": "Team B", "position": "Forward"},
            {"id": 5, "name": "James Smith", "team": "Team A", "position": "Goalkeeper"},
            {"id": 6, "name": "Layla Mahmoud", "team": "Team C", "position": "Midfielder"},
            {"id": 7, "name": "David Chen", "team": "Team C", "position": "Defender"}
        ]
        return athletes
    
    def get_athlete_data(self, athlete_id):
        """
        Get detailed data for a specific athlete
        
        Args:
            athlete_id (int): Athlete ID
            
        Returns:
            dict: Athlete data including personal info and latest readings
        """
        # In a real application, this would fetch from a database
        athletes = self.get_athletes_list()
        athlete = next((a for a in athletes if a["id"] == athlete_id), None)
        
        if not athlete:
            return None
        
        # Add more detailed information
        athlete_data = athlete.copy()
        
        # Generate consistent data based on athlete_id to ensure the same athlete
        # gets the same data each time
        random.seed(athlete_id)
        
        risk_score = random.randint(10, 90)
        
        athlete_data.update({
            "age": random.randint(18, 35),
            "height": random.randint(160, 200),
            "weight": random.randint(60, 100),
            "injury_history": ["Hamstring strain (2021)", "Ankle sprain (2020)"] if random.random() > 0.5 else [],
            "risk_score": risk_score
        })
        
        # Calculate risk color based on score
        if athlete_data["risk_score"] < 30:
            athlete_data["risk_color"] = "green"
        elif athlete_data["risk_score"] < 60:
            athlete_data["risk_color"] = "yellow"
        else:
            athlete_data["risk_color"] = "red"
        
        # Add muscle-specific risk data
        if risk_score > 60:
            # High-risk athlete will have higher risks for specific muscles
            athlete_data["muscle_risks"] = {
                "hamstring": min(95, risk_score + random.randint(0, 10)),  # Higher risk for hamstring
                "quadriceps": max(30, risk_score - random.randint(10, 25)),
                "calf": max(20, risk_score - random.randint(15, 30)),
                "lower_back": max(35, risk_score - random.randint(5, 15)),
                "shoulder": max(15, risk_score - random.randint(20, 40))
            }
        else:
            # Lower overall risk profile but with some variety
            athlete_data["muscle_risks"] = {
                "hamstring": min(75, risk_score + random.randint(-10, 15)),
                "quadriceps": max(10, risk_score + random.randint(-15, 10)),
                "calf": max(10, risk_score + random.randint(-20, 5)),
                "lower_back": max(10, risk_score + random.randint(-15, 10)),
                "shoulder": max(5, risk_score + random.randint(-25, 0))
            }
        
        # Reset random seed after generating athlete data
        random.seed()
            
        return athlete_data
    
    def get_historical_data(self, athlete_id, metric, days=30):
        """
        Get historical data for a specific athlete and metric
        
        Args:
            athlete_id (int): Athlete ID
            metric (str): Metric name (e.g., "risk_score", "semg_imbalance")
            days (int, optional): Number of days of history. Defaults to 30.
            
        Returns:
            pandas.DataFrame: Historical data with dates and values
        """
        # Generate dates
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        dates = [start_date + timedelta(days=i) for i in range(days)]
        
        # Generate synthetic data based on metric type
        if metric == "risk_score":
            # Random walk with upward trend
            base = random.randint(20, 40)
            values = [base]
            for i in range(1, days):
                new_val = values[-1] + random.uniform(-5, 7)
                # Ensure within bounds
                new_val = max(5, min(95, new_val))
                values.append(new_val)
                
        elif metric == "semg_imbalance":
            # Fluctuating with occasional spikes
            values = [random.uniform(5, 20) for _ in range(days)]
            # Add some spikes
            for _ in range(3):
                spike_idx = random.randint(0, days-1)
                values[spike_idx] = random.uniform(25, 40)
                
        elif metric == "temperature":
            # Normally stable with small variations
            base_temp = 36.5 + random.uniform(-0.2, 0.2)
            values = [base_temp + random.uniform(-0.3, 0.3) for _ in range(days)]
            # Add fever event if risk score is high
            if self.get_athlete_data(athlete_id)["risk_score"] > 70:
                fever_start = random.randint(0, days-5)
                for i in range(fever_start, min(fever_start+3, days)):
                    values[i] = base_temp + random.uniform(1.0, 1.5)
                    
        elif metric == "training_load":
            # Weekly pattern with rest days
            values = []
            for i in range(days):
                # Lower values on day 0 and 6 (weekends)
                if i % 7 in [0, 6]:
                    values.append(random.uniform(10, 30))
                else:
                    values.append(random.uniform(50, 90))
        
        else:
            # Default random data
            values = [random.uniform(0, 100) for _ in range(days)]
            
        # Create DataFrame
        df = pd.DataFrame({
            'date': dates,
            'value': values
        })
        
        return df
    
    def get_team_summary(self):
        """
        Get summary metrics for the entire team
        
        Returns:
            dict: Team summary metrics
        """
        athletes = self.get_athletes_list()
        athlete_data = [self.get_athlete_data(athlete["id"]) for athlete in athletes]
        
        # Calculate metrics
        risk_scores = [athlete["risk_score"] for athlete in athlete_data]
        
        return {
            "total_athletes": len(athletes),
            "avg_risk_score": np.mean(risk_scores),
            "high_risk_count": sum(1 for score in risk_scores if score >= 60),
            "medium_risk_count": sum(1 for score in risk_scores if 30 <= score < 60),
            "low_risk_count": sum(1 for score in risk_scores if score < 30),
            "teams": list(set(athlete["team"] for athlete in athletes))
        }
