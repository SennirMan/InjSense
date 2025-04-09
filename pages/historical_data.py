import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_extras.colored_header import colored_header
from datetime import datetime, timedelta

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
    label=text["historical_data"],
    description=text["historical_view"],
    color_name="blue-70"
)

# Create tabs for different views
tab1, tab2 = st.tabs([text["historical_view"], text["comparison_view"]])

with tab1:
    # Historical data for a single athlete
    
    # Get list of athletes
    athletes = data_processor.get_athletes_list()
    athlete_options = [f"{athlete['name']} ({athlete['team']})" for athlete in athletes]
    
    # Athlete selector
    selected_athlete_name = st.selectbox(
        text["select_athlete"],
        options=athlete_options,
        key="hist_athlete_select"
    )
    
    # Find the selected athlete
    selected_athlete_id = None
    for athlete in athletes:
        if f"{athlete['name']} ({athlete['team']})" == selected_athlete_name:
            selected_athlete_id = athlete['id']
            break
    
    # Date range selector
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    date_range = st.date_input(
        text["date_range"],
        value=(start_date.date(), end_date.date()),
        key="hist_date_range"
    )
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        days_diff = (end_date - start_date).days + 1
    else:
        days_diff = 30  # Default
    
    # Metric selector
    metric_options = [
        "risk_score", 
        "semg_imbalance",
        "temperature",
        "training_load"
    ]
    
    metric_labels = {
        "risk_score": text["risk_score"],
        "semg_imbalance": text["semg_imbalance"],
        "temperature": text["temperature_c"],
        "training_load": text["training_load"]
    }
    
    selected_metric = st.selectbox(
        text["select_metric"],
        options=[metric_labels[m] for m in metric_options],
        key="hist_metric_select"
    )
    
    # Map back to the internal metric name
    selected_metric_key = next(
        (k for k, v in metric_labels.items() if v == selected_metric),
        "risk_score"
    )
    
    # Apply filters button
    if st.button(text["apply_filters"], key="hist_apply"):
        if selected_athlete_id:
            # Get historical data
            hist_data = data_processor.get_historical_data(
                selected_athlete_id,
                selected_metric_key,
                days=days_diff
            )
            
            # Filter by date range
            hist_data = hist_data[
                (hist_data["date"].dt.date >= start_date) &
                (hist_data["date"].dt.date <= end_date)
            ]
            
            # Create visualization
            fig = px.line(
                hist_data,
                x="date",
                y="value",
                title=f"{selected_metric} - {selected_athlete_name}"
            )
            
            # Add threshold line for risk score
            if selected_metric_key == "risk_score":
                fig.add_hline(
                    y=st.session_state.risk_threshold,
                    line_dash="dash",
                    line_color="red",
                    annotation_text=text["risk_threshold"],
                    annotation_position="top right"
                )
            
            # Add danger zone for sEMG imbalance
            if selected_metric_key == "semg_imbalance":
                fig.add_hrect(
                    y0=15, 
                    y1=100,
                    fillcolor="red", 
                    opacity=0.1, 
                    line_width=0,
                    annotation_text="Danger Zone",
                    annotation_position="top right"
                )
            
            # Add fever line for temperature
            if selected_metric_key == "temperature":
                fig.add_hline(
                    y=37.5,
                    line_dash="dash",
                    line_color="red",
                    annotation_text="Fever Threshold",
                    annotation_position="top right"
                )
            
            # Update layout
            fig.update_layout(
                xaxis_title=text["date"],
                yaxis_title=selected_metric
            )
            
            # Display chart
            st.plotly_chart(fig, use_container_width=True)
            
            # Display statistics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Average",
                    f"{hist_data['value'].mean():.1f}"
                )
            
            with col2:
                st.metric(
                    "Maximum",
                    f"{hist_data['value'].max():.1f}"
                )
            
            with col3:
                st.metric(
                    "Minimum",
                    f"{hist_data['value'].min():.1f}"
                )
            
            with col4:
                st.metric(
                    "Standard Deviation",
                    f"{hist_data['value'].std():.2f}"
                )
            
            # Export data button
            csv = hist_data.to_csv(index=False).encode('utf-8')
            st.download_button(
                "Export Data",
                csv,
                f"{selected_athlete_name}_{selected_metric_key}.csv",
                "text/csv",
                key="hist_export_button"
            )

with tab2:
    # Comparison view for multiple athletes
    
    # Get list of athletes
    athletes = data_processor.get_athletes_list()
    athlete_options = [f"{athlete['name']} ({athlete['team']})" for athlete in athletes]
    
    # Multiple athlete selector
    selected_athletes = st.multiselect(
        text["select_athletes"],
        options=athlete_options,
        key="comp_athlete_select"
    )
    
    # Date range selector
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    date_range = st.date_input(
        text["date_range"],
        value=(start_date.date(), end_date.date()),
        key="comp_date_range"
    )
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        days_diff = (end_date - start_date).days + 1
    else:
        days_diff = 30  # Default
    
    # Metric selector
    metric_options = [
        "risk_score", 
        "semg_imbalance",
        "temperature",
        "training_load"
    ]
    
    metric_labels = {
        "risk_score": text["risk_score"],
        "semg_imbalance": text["semg_imbalance"],
        "temperature": text["temperature_c"],
        "training_load": text["training_load"]
    }
    
    selected_metric = st.selectbox(
        text["select_metric"],
        options=[metric_labels[m] for m in metric_options],
        key="comp_metric_select"
    )
    
    # Map back to the internal metric name
    selected_metric_key = next(
        (k for k, v in metric_labels.items() if v == selected_metric),
        "risk_score"
    )
    
    # Compare button
    if st.button(text["compare"], key="comp_compare"):
        if selected_athletes:
            # Create figure
            fig = go.Figure()
            
            # For each selected athlete
            for athlete_name in selected_athletes:
                # Find athlete ID
                athlete_id = None
                for athlete in athletes:
                    if f"{athlete['name']} ({athlete['team']})" == athlete_name:
                        athlete_id = athlete['id']
                        break
                
                if athlete_id:
                    # Get historical data
                    hist_data = data_processor.get_historical_data(
                        athlete_id,
                        selected_metric_key,
                        days=days_diff
                    )
                    
                    # Filter by date range
                    hist_data = hist_data[
                        (hist_data["date"].dt.date >= start_date) &
                        (hist_data["date"].dt.date <= end_date)
                    ]
                    
                    # Add to chart
                    fig.add_trace(go.Scatter(
                        x=hist_data["date"],
                        y=hist_data["value"],
                        mode="lines",
                        name=athlete_name
                    ))
            
            # Add threshold line for risk score
            if selected_metric_key == "risk_score":
                fig.add_hline(
                    y=st.session_state.risk_threshold,
                    line_dash="dash",
                    line_color="red",
                    annotation_text=text["risk_threshold"],
                    annotation_position="top right"
                )
            
            # Add danger zone for sEMG imbalance
            if selected_metric_key == "semg_imbalance":
                fig.add_hrect(
                    y0=15, 
                    y1=100,
                    fillcolor="red", 
                    opacity=0.1, 
                    line_width=0,
                    annotation_text="Danger Zone",
                    annotation_position="top right"
                )
            
            # Add fever line for temperature
            if selected_metric_key == "temperature":
                fig.add_hline(
                    y=37.5,
                    line_dash="dash",
                    line_color="red",
                    annotation_text="Fever Threshold",
                    annotation_position="top right"
                )
            
            # Update layout
            fig.update_layout(
                title=f"{selected_metric} - {text['comparison_view']}",
                xaxis_title=text["date"],
                yaxis_title=selected_metric
            )
            
            # Display chart
            st.plotly_chart(fig, use_container_width=True)
            
            # Create combined DataFrame for export
            combined_data = pd.DataFrame(columns=["date"])
            
            for athlete_name in selected_athletes:
                # Find athlete ID
                athlete_id = None
                for athlete in athletes:
                    if f"{athlete['name']} ({athlete['team']})" == athlete_name:
                        athlete_id = athlete['id']
                        break
                
                if athlete_id:
                    # Get data
                    hist_data = data_processor.get_historical_data(
                        athlete_id,
                        selected_metric_key,
                        days=days_diff
                    )
                    
                    # Filter by date range
                    hist_data = hist_data[
                        (hist_data["date"].dt.date >= start_date) &
                        (hist_data["date"].dt.date <= end_date)
                    ]
                    
                    # Rename value column to athlete name
                    hist_data = hist_data.rename(columns={"value": athlete_name})
                    
                    # Combine with main DataFrame
                    if combined_data.empty:
                        combined_data = hist_data[["date", athlete_name]]
                    else:
                        combined_data = pd.merge(
                            combined_data, 
                            hist_data[["date", athlete_name]], 
                            on="date", 
                            how="outer"
                        )
            
            # Export data button
            if not combined_data.empty:
                csv = combined_data.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "Export Comparison Data",
                    csv,
                    f"comparison_{selected_metric_key}.csv",
                    "text/csv",
                    key="comp_export_button"
                )
