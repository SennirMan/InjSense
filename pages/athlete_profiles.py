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
from body_diagram import create_mobile_body_diagram_section

# Get text based on selected language
text = utils.get_text_dict(st.session_state.language)

# Initialize data processor and prediction model
data_processor = DataProcessor()
prediction_model = PredictionModel()

# Page title
colored_header(
    label=text["athlete_profiles"],
    description=text["athlete_details"],
    color_name="blue-70"
)

# Get list of athletes
athletes = data_processor.get_athletes_list()
athlete_options = [f"{athlete['name']} ({athlete['team']})" for athlete in athletes]

# Athlete selector
selected_athlete_name = st.selectbox(
    text["select_athlete"],
    options=athlete_options
)

# Find the selected athlete
selected_athlete_id = None
for athlete in athletes:
    if f"{athlete['name']} ({athlete['team']})" == selected_athlete_name:
        selected_athlete_id = athlete['id']
        break

if selected_athlete_id:
    # Get detailed athlete data
    athlete_data = data_processor.get_athlete_data(selected_athlete_id)
    
    # Make prediction for this athlete
    risk_prediction = prediction_model.predict_risk(athlete_data)
    
    # Update athlete data with prediction
    athlete_data['risk_score'] = risk_prediction['risk_score']
    athlete_data['risk_label'] = risk_prediction['risk_label']
    
    # Display athlete information
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader(athlete_data['name'])
        
        # Personal information card
        st.markdown(f"### {text['personal_info']}")
        
        info_markdown = f"""
        **{text['age']}:** {athlete_data['age']} {text['years']}  
        **{text['height']}:** {athlete_data['height']} cm  
        **{text['weight']}:** {athlete_data['weight']} kg  
        **{text['team']}:** {athlete_data['team']}  
        **{text['position']}:** {athlete_data['position']}
        """
        
        st.markdown(info_markdown)
        
        # Injury history
        st.markdown(f"### {text['injury_history']}")
        
        if athlete_data['injury_history']:
            for injury in athlete_data['injury_history']:
                st.markdown(f"- {injury}")
        else:
            st.markdown(f"*{text['no_injury_history']}*")
        
        # Risk score
        st.markdown(f"### {text['risk_analysis']}")
        
        risk_color = utils.risk_color(athlete_data['risk_score'])
        
        st.markdown(f"""
        <div style="border-radius: 10px; padding: 10px; background-color: {risk_color}; color: white;">
            <h2 style="margin: 0; text-align: center;">{athlete_data['risk_score']}</h2>
            <p style="margin: 0; text-align: center;">{athlete_data['risk_label']} {text['risk']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Risk factors
        st.markdown("#### Top Risk Factors")
        
        risk_factors = risk_prediction['risk_factors']
        top_factors = list(risk_factors.items())[:3]
        
        for factor, importance in top_factors:
            factor_label = text.get(factor, factor.replace('_', ' ').title())
            st.markdown(f"- {factor_label}: {int(importance * 100)}%")
    
    with col2:
        # Tabs for different visualizations
        tab1, tab2, tab3, tab4 = st.tabs([
            text["biometric_signals"], 
            text["risk_progression"], 
            text["muscle_activation"],
            text["body_diagram"]
        ])
        
        with tab1:
            # sEMG signal visualization
            st.subheader(text["semg_signals_title"])
            
            # Generate sample EMG data for visualization
            time = np.linspace(0, 5, 500)
            hamstring_signal = 0.2 * np.sin(2 * np.pi * 2 * time) + 0.1 * np.random.randn(500)
            quad_signal = 0.15 * np.sin(2 * np.pi * 2.2 * time) + 0.1 * np.random.randn(500)
            
            if athlete_data['risk_score'] > 60:
                # Add artifacts for high-risk athletes
                hamstring_signal[250:300] += 0.3 * (np.random.rand(50) + 0.5)
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=time, 
                y=hamstring_signal, 
                mode='lines', 
                name=text["hamstring"]
            ))
            
            fig.add_trace(go.Scatter(
                x=time, 
                y=quad_signal, 
                mode='lines', 
                name=text["quadriceps"]
            ))
            
            fig.update_layout(
                title=text["semg_signals_title"],
                xaxis_title=text["time_seconds"],
                yaxis_title=text["amplitude_mv"],
                legend_title=text["muscle_group"]
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Temperature heatmap
            st.subheader(text["temperature_readings"])
            
            muscle_groups = [text["hamstring"], text["quadriceps"], text["calf"], text["lower_back"], text["shoulder"]]
            left_temps = [36.8, 36.5, 36.6, 36.9, 36.4]
            right_temps = [36.9, 36.4, 36.7, 36.8, 36.5]
            
            # Make left-right temperature differ more for high-risk athletes
            if athlete_data['risk_score'] > 60:
                # Increase difference in hamstring temperatures
                left_temps[0] += 0.4
            
            temp_data = pd.DataFrame({
                'Muscle Group': muscle_groups * 2,
                'Side': [text["left_side"]] * 5 + [text["right_side"]] * 5,
                'Temperature': left_temps + right_temps
            })
            
            fig = px.density_heatmap(
                temp_data,
                x='Muscle Group',
                y='Side',
                z='Temperature',
                color_continuous_scale='Viridis',
                title=text["skin_temperature"]
            )
            
            fig.update_layout(
                xaxis_title=text["muscle_group"],
                yaxis_title="",
                coloraxis_colorbar_title=text["temperature_c"]
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        with tab2:
            # Risk progression chart
            st.subheader(text["risk_progression"])
            
            # Get historical risk data
            risk_history = data_processor.get_historical_data(
                selected_athlete_id, 
                "risk_score",
                days=30
            )
            
            fig = px.line(
                risk_history,
                x='date',
                y='value',
                title=text["risk_progression"]
            )
            
            # Add threshold line
            fig.add_hline(
                y=st.session_state.risk_threshold,
                line_dash="dash",
                line_color="red",
                annotation_text=text["risk_threshold"],
                annotation_position="top right"
            )
            
            fig.update_layout(
                xaxis_title=text["days"],
                yaxis_title=text["risk_score"]
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Risk factor contribution
            st.subheader(text["risk_factors"])
            
            # Get top risk factors
            risk_factors = risk_prediction['risk_factors']
            factors_df = pd.DataFrame({
                'Factor': [text.get(k, k.replace('_', ' ').title()) for k in risk_factors.keys()],
                'Importance': [v * 100 for v in risk_factors.values()]
            }).head(6)  # Top 6 factors
            
            fig = px.bar(
                factors_df,
                y='Factor',
                x='Importance',
                orientation='h',
                title=text["risk_factors"]
            )
            
            fig.update_layout(
                xaxis_title="Contribution (%)",
                yaxis_title=""
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        with tab3:
            # Muscle activation comparison
            st.subheader(text["avg_muscle_activation"])
            
            muscle_groups = [text["hamstring"], text["quadriceps"], text["calf"], text["lower_back"], text["shoulder"]]
            left_activation = [78, 65, 82, 42, 55]
            right_activation = [75, 68, 79, 45, 53]
            
            # If high risk, create more imbalance
            if athlete_data['risk_score'] > 60:
                left_activation[0] = 85
                right_activation[0] = 65
            
            activation_data = pd.DataFrame({
                'Muscle Group': muscle_groups,
                text["left_side"]: left_activation,
                text["right_side"]: right_activation
            })
            
            fig = go.Figure(data=[
                go.Bar(name=text["left_side"], x=activation_data['Muscle Group'], y=activation_data[text["left_side"]]),
                go.Bar(name=text["right_side"], x=activation_data['Muscle Group'], y=activation_data[text["right_side"]])
            ])
            
            fig.update_layout(
                barmode='group',
                title=text["avg_muscle_activation"],
                xaxis_title=text["muscle_group"],
                yaxis_title=text["activation_percentage"]
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Muscle imbalance over time
            st.subheader("Muscle Imbalance Over Time")
            
            # Get historical imbalance data
            imbalance_history = data_processor.get_historical_data(
                selected_athlete_id, 
                "semg_imbalance",
                days=30
            )
            
            fig = px.line(
                imbalance_history,
                x='date',
                y='value',
                title="Muscle Imbalance Progression"
            )
            
            fig.update_layout(
                xaxis_title=text["days"],
                yaxis_title="Imbalance (%)"
            )
            
            # Add danger zone
            fig.add_hrect(
                y0=25, 
                y1=100,
                fillcolor="red", 
                opacity=0.2, 
                line_width=0,
                annotation_text="Danger Zone",
                annotation_position="top right"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        with tab4:
            # Create visual body diagram
            st.subheader(text["body_diagram"])
            
            # The muscle risk data is now coming directly from data_processor.py
            # and is already included in the athlete_data dictionary
            
            # Display interactive body diagram with risk visualization
            create_mobile_body_diagram_section(athlete_data, text)
            
else:
    st.warning("Please select an athlete to view their profile.")
