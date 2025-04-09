import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_extras.colored_header import colored_header

import sys
import os

# Add the root directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import utils
from data_processor import DataProcessor
from prediction_model import PredictionModel

# Get text based on selected language
text = utils.get_text_dict(st.session_state.language)

# Initialize data processor and prediction model
data_processor = DataProcessor()
prediction_model = PredictionModel()

# Page title
colored_header(
    label=text["settings"],
    description=text["risk_settings"],
    color_name="blue-70"
)

# Risk threshold setting
st.subheader(text["risk_threshold_setting"])

risk_threshold = st.slider(
    text["risk_threshold"],
    min_value=10,
    max_value=90,
    value=st.session_state.risk_threshold,
    step=5
)

# Save settings button
if st.button(text["save_settings"]):
    st.session_state.risk_threshold = risk_threshold
    st.success(text["settings_saved"])
    
    # Show what the risk threshold means
    st.info(f"Athletes with risk scores above {risk_threshold} will be flagged as high risk.")

# Language settings (already in sidebar)
st.subheader(text["select_language"])
st.info(f"Language settings can be changed in the sidebar. Current language: {st.session_state.language}")

# Display a visual representation of risk thresholds
st.subheader("Risk Level Visualization")

# Create a dataframe for visualization
risk_levels = pd.DataFrame({
    'Risk Level': ['Low Risk', 'Medium Risk', 'High Risk'],
    'Min Value': [0, 30, 60],
    'Max Value': [29, 59, 100],
    'Color': ['#4CAF50', '#FFC107', '#F44336']
})

# Create a bar chart to visualize risk levels
fig = go.Figure()

for i, row in risk_levels.iterrows():
    fig.add_trace(go.Bar(
        x=[row['Max Value'] - row['Min Value']],
        y=[row['Risk Level']],
        orientation='h',
        marker=dict(
            color=row['Color']
        ),
        base=row['Min Value'],
        name=row['Risk Level']
    ))

# Add threshold marker
fig.add_vline(
    x=risk_threshold,
    line_dash="dash",
    line_color="black",
    line_width=2,
    annotation_text="Current Threshold",
    annotation_position="top"
)

fig.update_layout(
    barmode='stack',
    title="Risk Level Thresholds",
    xaxis_title="Risk Score",
    yaxis_title="Risk Level",
    showlegend=False,
    height=300
)

st.plotly_chart(fig, use_container_width=True)

# About the system
st.subheader("About the System")

st.markdown("""
### Athlete Biometric Monitoring Platform

This platform is designed to monitor athlete biometric signals and predict injury risks using machine learning. The system collects and analyzes multiple data points including:

- sEMG signals from key muscle groups
- Skin temperature readings
- Training load metrics
- Recovery time
- Historical injury data

### Risk Score Calculation

The risk score is calculated using a machine learning model that considers multiple factors with varying weights:

1. **sEMG Imbalance** - Differences between left and right muscle activation
2. **Training Load** - Volume and intensity of recent training
3. **Recovery Time** - Hours of recovery between sessions
4. **Previous Injuries** - History and frequency of past injuries
5. **Temperature Variation** - Abnormal skin temperature patterns

### Data Security

All athlete data is securely stored and processed in compliance with data protection regulations.
""")

# Export system settings button
if st.button("Export System Settings"):
    # Create settings dictionary
    settings = {
        "risk_threshold": st.session_state.risk_threshold,
        "language": st.session_state.language,
        "export_time": utils.get_current_time()
    }
    
    # Convert to CSV
    settings_df = pd.DataFrame([settings])
    csv = settings_df.to_csv(index=False).encode('utf-8')
    
    # Download button
    st.download_button(
        "Download Settings",
        csv,
        "system_settings.csv",
        "text/csv",
        key="settings_export_button"
    )
