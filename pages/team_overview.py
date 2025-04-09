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
    label=text["team_overview"],
    description=text["team_comparison"],
    color_name="blue-70"
)

# Get team summary data
team_summary = data_processor.get_team_summary()

# Filters section
st.sidebar.markdown(f"## {text['filter_by_team']}")
team_options = [text["all_teams"]] + team_summary["teams"]
selected_team = st.sidebar.selectbox(
    text["team"],
    options=team_options
)

st.sidebar.markdown(f"## {text['filter_by_risk']}")
risk_options = [
    text["all_risk_levels"],
    text["high_risk"],
    text["medium_risk"],
    text["low_risk"]
]
selected_risk = st.sidebar.selectbox(
    text["risk_score"],
    options=risk_options
)

# Summary metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label=text["total_athletes"], value=team_summary["total_athletes"])
with col2:
    st.metric(
        label=text["high_risk_athletes"], 
        value=team_summary["high_risk_count"],
        delta=None
    )
with col3:
    st.metric(
        label=text["medium_risk_athletes"], 
        value=team_summary["medium_risk_count"],
        delta=None
    )
with col4:
    st.metric(
        label=text["team_avg_risk"], 
        value=f"{team_summary['avg_risk_score']:.1f}%",
        delta=None
    )

# Team risk comparison
st.subheader(text["team_comparison"])

# Create data for team comparison
team_data = []
for team_name in team_summary["teams"]:
    risk_values = []
    for i in range(15):  # Simulate 15 athletes per team
        if team_name == "Team A":
            # Team A has higher risk
            base_risk = np.random.normal(45, 15)
        elif team_name == "Team B":
            # Team B has medium risk
            base_risk = np.random.normal(35, 12)
        else:
            # Team C has lower risk
            base_risk = np.random.normal(25, 10)
        
        # Clamp between 0-100
        risk = max(0, min(100, base_risk))
        risk_values.append(risk)
    
    team_data.append({
        "team": team_name,
        "mean_risk": np.mean(risk_values),
        "max_risk": np.max(risk_values),
        "min_risk": np.min(risk_values)
    })

team_df = pd.DataFrame(team_data)

# Team risk comparison chart
fig = go.Figure()

fig.add_trace(go.Bar(
    x=team_df["team"],
    y=team_df["mean_risk"],
    error_y=dict(
        type='data',
        symmetric=False,
        array=team_df["max_risk"] - team_df["mean_risk"],
        arrayminus=team_df["mean_risk"] - team_df["min_risk"]
    ),
    name=text["avg_risk_score"]
))

fig.update_layout(
    title=text["team_comparison"],
    xaxis_title=text["team"],
    yaxis_title=text["risk_score"]
)

# Add threshold line
fig.add_hline(
    y=st.session_state.risk_threshold,
    line_dash="dash",
    line_color="red",
    annotation_text=text["risk_threshold"],
    annotation_position="top right"
)

st.plotly_chart(fig, use_container_width=True)

# Athletes table with filtering
st.subheader(text["athlete_details"])

# Get all athletes
athletes = data_processor.get_athletes_list()
athlete_details = []

for athlete in athletes:
    # Get athlete data including risk score
    data = data_processor.get_athlete_data(athlete["id"])
    
    # Determine risk level
    if data["risk_score"] >= 60:
        risk_level = text["high_risk"]
    elif data["risk_score"] >= 30:
        risk_level = text["medium_risk"]
    else:
        risk_level = text["low_risk"]
    
    athlete_details.append({
        "id": athlete["id"],
        "name": athlete["name"],
        "team": athlete["team"],
        "position": athlete["position"],
        "risk_score": data["risk_score"],
        "risk_level": risk_level,
        "risk_color": utils.risk_color(data["risk_score"])
    })

# Create DataFrame
athletes_df = pd.DataFrame(athlete_details)

# Apply filters
filtered_df = athletes_df.copy()

if selected_team != text["all_teams"]:
    filtered_df = filtered_df[filtered_df["team"] == selected_team]
    
if selected_risk != text["all_risk_levels"]:
    filtered_df = filtered_df[filtered_df["risk_level"] == selected_risk]

# Display filtered athletes
if not filtered_df.empty:
    # Sort by risk score (descending)
    filtered_df = filtered_df.sort_values(by="risk_score", ascending=False)
    
    # Display as interactive table with colored risk scores
    for _, row in filtered_df.iterrows():
        col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 1])
        
        with col1:
            st.markdown(f"**{row['name']}**")
        with col2:
            st.markdown(f"{row['team']}")
        with col3:
            st.markdown(f"{row['position']}")
        with col4:
            st.markdown(f"{row['risk_level']}")
        with col5:
            st.markdown(
                f"""<div style="background-color: {row['risk_color']}; 
                            color: white; 
                            border-radius: 10px; 
                            padding: 5px; 
                            text-align: center">
                  {row['risk_score']}
                </div>""",
                unsafe_allow_html=True
            )
        
        st.markdown("---")
else:
    st.info("No athletes match the selected filters.")

# Team metrics by muscle group
st.subheader(text["metrics_by_team"])

# Create tabs for different metrics
tab1, tab2, tab3 = st.tabs([
    text["risk_distribution"], 
    text["avg_muscle_activation"], 
    text["temperature_readings"]
])

with tab1:
    # Risk by muscle group and team
    muscle_groups = [
        text["hamstring"], 
        text["quadriceps"], 
        text["calf"], 
        text["lower_back"], 
        text["shoulder"]
    ]
    
    risk_by_muscle_team = []
    
    for team in team_summary["teams"]:
        for muscle in muscle_groups:
            # Generate synthetic data with realistic patterns
            if muscle == text["hamstring"]:
                base_risk = 45  # Hamstrings typically have higher risk
            elif muscle == text["quadriceps"]:
                base_risk = 35
            elif muscle == text["calf"]:
                base_risk = 40
            elif muscle == text["lower_back"]:
                base_risk = 30
            else:  # shoulder
                base_risk = 25
            
            # Team variation
            if team == "Team A":
                team_factor = 1.2  # Higher risk for Team A
            elif team == "Team B":
                team_factor = 1.0  # Medium risk for Team B
            else:
                team_factor = 0.8  # Lower risk for Team C
            
            risk = base_risk * team_factor + np.random.normal(0, 5)
            risk = max(0, min(100, risk))  # Clamp between 0-100
            
            risk_by_muscle_team.append({
                "Team": team,
                "Muscle Group": muscle,
                "Risk Score": risk
            })
    
    risk_muscle_df = pd.DataFrame(risk_by_muscle_team)
    
    fig = px.bar(
        risk_muscle_df,
        x="Muscle Group",
        y="Risk Score",
        color="Team",
        barmode="group",
        title=text["risk_distribution"]
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
        xaxis_title=text["muscle_group"],
        yaxis_title=text["risk_score"]
    )
    
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    # Muscle activation by team
    activation_by_team = []
    
    for team in team_summary["teams"]:
        for muscle in muscle_groups:
            # Left side
            left_activation = np.random.normal(70, 10)
            left_activation = max(0, min(100, left_activation))
            
            # Right side
            if team == "Team A" and muscle == text["hamstring"]:
                # Team A has more imbalance in hamstrings
                right_activation = left_activation - np.random.normal(15, 5)
            else:
                # Small random imbalance
                right_activation = left_activation + np.random.normal(0, 7)
            
            right_activation = max(0, min(100, right_activation))
            
            # Calculate imbalance
            imbalance = abs(left_activation - right_activation)
            
            activation_by_team.append({
                "Team": team,
                "Muscle Group": muscle,
                "Left Activation": left_activation,
                "Right Activation": right_activation,
                "Imbalance": imbalance
            })
    
    activation_df = pd.DataFrame(activation_by_team)
    
    # Create visualization for muscle imbalance
    fig = px.scatter(
        activation_df,
        x="Muscle Group",
        y="Imbalance",
        color="Team",
        size="Imbalance",
        title="Muscle Activation Imbalance"
    )
    
    fig.update_layout(
        xaxis_title=text["muscle_group"],
        yaxis_title="Left-Right Imbalance (%)"
    )
    
    # Add danger zone
    fig.add_hrect(
        y0=15, 
        y1=100,
        fillcolor="red", 
        opacity=0.1, 
        line_width=0,
        annotation_text="Danger Zone",
        annotation_position="top right"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Activation comparison for one muscle group
    selected_muscle = st.selectbox(
        text["select_muscle"],
        options=muscle_groups
    )
    
    muscle_activation = activation_df[activation_df["Muscle Group"] == selected_muscle]
    
    fig = go.Figure()
    
    for team in team_summary["teams"]:
        team_data = muscle_activation[muscle_activation["Team"] == team]
        
        fig.add_trace(go.Bar(
            name=f"{team} - {text['left_side']}",
            x=[team],
            y=team_data["Left Activation"],
            marker_color="#1E88E5"
        ))
        
        fig.add_trace(go.Bar(
            name=f"{team} - {text['right_side']}",
            x=[team],
            y=team_data["Right Activation"],
            marker_color="#42A5F5"
        ))
    
    fig.update_layout(
        title=f"{selected_muscle} {text['avg_muscle_activation']}",
        xaxis_title=text["team"],
        yaxis_title=text["activation_percentage"],
        barmode="group"
    )
    
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    # Temperature readings by team
    temp_by_team = []
    
    for team in team_summary["teams"]:
        for muscle in muscle_groups:
            # Base temperature (normal is around 36.5°C)
            base_temp = 36.5
            
            # Team variation
            if team == "Team A":
                # Team A has slightly elevated temps
                team_factor = 0.3
            elif team == "Team B":
                team_factor = 0.1
            else:
                team_factor = 0.0
            
            # Muscle variation
            if muscle == text["hamstring"] and team == "Team A":
                # Team A has higher hamstring temps
                muscle_factor = 0.4
            elif muscle == text["lower_back"]:
                # Lower backs tend to be warmer
                muscle_factor = 0.2
            else:
                muscle_factor = 0.0
            
            # Calculate temperature with small random variation
            temp = base_temp + team_factor + muscle_factor + np.random.normal(0, 0.1)
            
            temp_by_team.append({
                "Team": team,
                "Muscle Group": muscle,
                "Temperature": temp
            })
    
    temp_df = pd.DataFrame(temp_by_team)
    
    fig = px.density_heatmap(
        temp_df,
        x="Muscle Group",
        y="Team",
        z="Temperature",
        color_continuous_scale="Viridis",
        title=text["temperature_readings"]
    )
    
    fig.update_layout(
        xaxis_title=text["muscle_group"],
        yaxis_title=text["team"],
        coloraxis_colorbar_title=text["temperature_c"]
    )
    
    st.plotly_chart(fig, use_container_width=True)
