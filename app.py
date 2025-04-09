import streamlit as st

# Page configuration - MUST be the first Streamlit command
st.set_page_config(
    page_title="Athlete Biometrics Platform",
    page_icon="🏃",
    layout="wide",
    initial_sidebar_state="expanded"
)

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_extras.app_logo import add_logo
from streamlit_extras.colored_header import colored_header
from streamlit_extras.metric_cards import style_metric_cards
import utils
from data_processor import DataProcessor
from prediction_model import PredictionModel
from body_diagram import create_body_diagram

# Initialize session state variables if they don't exist
if 'language' not in st.session_state:
    st.session_state.language = 'English'
if 'risk_threshold' not in st.session_state:
    st.session_state.risk_threshold = 75  # Default threshold value

# Text dictionary for multi-language support
text = utils.get_text_dict(st.session_state.language)

# Initialize data processor and prediction model
data_processor = DataProcessor()
prediction_model = PredictionModel()

# Sidebar for navigation and settings
with st.sidebar:
    st.title(text["app_title"])

    # Language selector
    language_options = ["English", "Arabic"]
    selected_language = st.selectbox(
        text["select_language"],
        options=language_options,
        index=language_options.index(st.session_state.language)
    )

    if selected_language != st.session_state.language:
        st.session_state.language = selected_language
        text = utils.get_text_dict(st.session_state.language)
        st.rerun()

    # Navigation options
    st.subheader(text["navigation"])
    page = st.radio(
        label=text["select_page"],
        options=[
            text["dashboard"],
            text["athlete_profiles"],
            text["team_overview"],
            text["historical_data"],
            text["settings"]
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.caption(text["app_description"])

# Main content
if page == text["dashboard"]:
    # Dashboard title
    colored_header(
        label=text["dashboard_title"],
        description=text["dashboard_description"],
        color_name="blue-70"
    )

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(label=text["total_athletes"], value="24")
    with col2:
        st.metric(label=text["high_risk_athletes"], value="3", delta="-1")
    with col3:
        st.metric(label=text["medium_risk_athletes"], value="8", delta="+2")
    with col4:
        st.metric(label=text["team_avg_risk"], value="32%", delta="-5%")

    style_metric_cards()

    # Add monitoring header
    st.header("Injsense")
    st.subheader("👁️ " + text.get("athlete_monitoring", "Athlete Monitoring"))
    st.markdown("_" + text.get("live_monitoring", "Live monitoring of athlete status") + "_")

    # Add session state for athlete detail view if not exists
    if 'selected_athlete_id' not in st.session_state:
        st.session_state.selected_athlete_id = None
    if 'selected_risk_factor' not in st.session_state:
        st.session_state.selected_risk_factor = None

    # Check if an athlete is selected for detailed view
    if st.session_state.selected_athlete_id is not None:
        # Get the athlete data
        athlete_data = data_processor.get_athlete_data(st.session_state.selected_athlete_id)

        # Back button
        if st.button("← Back to Monitoring View"):
            st.session_state.selected_athlete_id = None
            st.session_state.selected_risk_factor = None
            st.rerun()

        # Display athlete detail view with improved styling
        st.markdown(f"""
        <div style="display: flex; align-items: center; margin-bottom: 15px;">
            <img src="assets/player_photos/player_silhouette.svg" 
                style="width: 60px; height: 60px; border-radius: 50%; margin-right: 15px; border: 2px solid #2563EB;">
            <h1 style="margin: 0; color: #2563EB; font-size: 2em;">{athlete_data['name']}</h1>
        </div>
        <hr style="margin: 0 0 20px 0; border-color: #f0f0f0;">
        """, unsafe_allow_html=True)

        # Create 3-column layout for better space usage
        col1, col2, col3 = st.columns([1, 2, 1])

        with col1:
            # Styled personal info
            st.markdown(f"""
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                <h3 style="margin-top: 0; color: #1E3A8A; border-bottom: 2px solid #2563EB; padding-bottom: 8px;">
                    {text['personal_info']}
                </h3>
                <table style="width: 100%;">
                    <tr>
                        <td style="padding: 5px; font-weight: bold;">👤 {text['age']}:</td>
                        <td style="padding: 5px;">{athlete_data['age']} {text['years']}</td>
                    </tr>
                    <tr>
                        <td style="padding: 5px; font-weight: bold;">📏 {text['height']}:</td>
                        <td style="padding: 5px;">{athlete_data['height']} cm</td>
                    </tr>
                    <tr>
                        <td style="padding: 5px; font-weight: bold;">⚖️ {text['weight']}:</td>
                        <td style="padding: 5px;">{athlete_data['weight']} kg</td>
                    </tr>
                    <tr>
                        <td style="padding: 5px; font-weight: bold;">🏆 {text['team']}:</td>
                        <td style="padding: 5px;">{athlete_data['team']}</td>
                    </tr>
                    <tr>
                        <td style="padding: 5px; font-weight: bold;">🏃 {text['position']}:</td>
                        <td style="padding: 5px;">{athlete_data['position']}</td>
                    </tr>
                </table>
            </div>
            """, unsafe_allow_html=True)

            # Injury history in a styled box
            st.markdown(f"""
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                <h3 style="margin-top: 0; color: #1E3A8A; border-bottom: 2px solid #2563EB; padding-bottom: 8px;">
                    {text['injury_history']}
                </h3>
                <ul style="margin-bottom: 0; padding-left: 20px;">
            """, unsafe_allow_html=True)

            if athlete_data.get('injury_history'):
                for injury in athlete_data['injury_history']:
                    st.markdown(f"<li>{injury}</li>", unsafe_allow_html=True)
            else:
                st.markdown(f"<li><em>{text.get('no_injury_history', 'No injury history recorded')}</em></li>", unsafe_allow_html=True)

            st.markdown("</ul></div>", unsafe_allow_html=True)

            # Risk score display with enhanced styling
            risk_score = athlete_data['risk_score']
            risk_color = utils.risk_color(risk_score)

            # Determine risk category text
            if risk_score >= 70:
                risk_category = text.get('high_risk', 'High Risk')
                risk_icon = "🔴"
            elif risk_score >= 40:
                risk_category = text.get('medium_risk', 'Medium Risk')
                risk_icon = "🟡"
            else:
                risk_category = text.get('low_risk', 'Low Risk')
                risk_icon = "🟢"

            st.markdown(f"""
            <div style="background-color: {risk_color}; color: white; border-radius: 10px; padding: 15px; text-align: center;">
                <h4 style="margin-top: 0; margin-bottom: 5px;">{text.get('risk_analysis', 'Risk Analysis')}</h4>
                <div style="font-size: 3em; font-weight: bold; margin: 10px 0;">{risk_score}</div>
                <div style="font-size: 1.2em;">{risk_icon} {risk_category}</div>
            </div>
            """, unsafe_allow_html=True)

        # Add third column with detailed monitoring data
        with col3:
            # Training load
            st.markdown(f"""
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                <h3 style="margin-top: 0; color: #1E3A8A; border-bottom: 2px solid #2563EB; padding-bottom: 8px;">
                    {text.get('training_load', 'Training Load')}
                </h3>
                <div style="text-align: center; font-size: 2.5em; font-weight: bold; color: #2563EB;">
                    {athlete_data.get('training_load', 820)}
                </div>
                <div style="text-align: center; font-size: 0.9em; color: #666;">
                    {text.get('weekly_load_units', 'Weekly load units')}
                </div>
                <div style="margin-top: 10px; height: 8px; background-color: #e0e0e0; border-radius: 4px;">
                    <div style="height: 100%; width: 75%; background-color: #2563EB; border-radius: 4px;"></div>
                </div>
                <div style="display: flex; justify-content: space-between; margin-top: 5px; font-size: 0.8em; color: #666;">
                    <span>{text.get('optimal_range', 'Optimal range')}</span>
                    <span>1100</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Recovery status gauge
            recovery = athlete_data.get('recovery_status', 72)
            if recovery >= 70:
                recovery_color = "#4CAF50"  # Green
                recovery_status = text.get('good', 'Good')
            elif recovery >= 40:
                recovery_color = "#FFC107"  # Yellow
                recovery_status = text.get('moderate', 'Moderate')
            else:
                recovery_color = "#F44336"  # Red
                recovery_status = text.get('poor', 'Poor')

            st.markdown(f"""
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                <h3 style="margin-top: 0; color: #1E3A8A; border-bottom: 2px solid #2563EB; padding-bottom: 8px;">
                    {text.get('recovery_status', 'Recovery Status')}
                </h3>
                <div style="position: relative; width: 100%; height: 130px;">
                    <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center;">
                        <div style="font-size: 2.5em; font-weight: bold; color: {recovery_color};">{recovery}%</div>
                        <div style="font-size: 1.1em; color: #333;">{recovery_status}</div>
                    </div>
                    <svg width="100%" height="100%" viewBox="0 0 100 50">
                        <!-- Background arc -->
                        <path d="M 10 50 A 40 40 0 0 1 90 50" fill="none" stroke="#e0e0e0" stroke-width="8" />
                        <!-- Colored arc representing recovery level -->
                        <path d="M 10 50 A 40 40 0 0 1 {10 + (recovery/100)*80} 50" fill="none" stroke="{recovery_color}" stroke-width="8" stroke-linecap="round" />
                    </svg>
                </div>
                <div style="display: flex; justify-content: space-between; margin-top: 5px; font-size: 0.9em; color: #666;">
                    <span style="color: #F44336;">0%</span>
                    <span style="color: #FFC107;">50%</span>
                    <span style="color: #4CAF50;">100%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Recent activity summary
            st.markdown(f"""
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px;">
                <h3 style="margin-top: 0; color: #1E3A8A; border-bottom: 2px solid #2563EB; padding-bottom: 8px;">
                    {text.get('recent_activity', 'Recent Activity')}
                </h3>
                <ul style="margin-bottom: 0; padding-left: 20px;">
                    <li style="margin-bottom: 10px;">
                        <div style="font-weight: bold;">{text.get('yesterday', 'Yesterday')}</div>
                        <div>{text.get('strength_training', 'Strength Training')} - 60 {text.get('minutes', 'min')}</div>
                    </li>
                    <li style="margin-bottom: 10px;">
                        <div style="font-weight: bold;">24/03/2025</div>
                        <div>{text.get('team_practice', 'Team Practice')} - 90 {text.get('minutes', 'min')}</div>
                    </li>
                    <li>
                        <div style="font-weight: bold;">22/03/2025</div>
                        <div>{text.get('recovery_session', 'Recovery Session')} - 45 {text.get('minutes', 'min')}</div>
                    </li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            # If a specific risk factor is selected, show relevant chart
            if st.session_state.selected_risk_factor is not None:
                risk_factor = st.session_state.selected_risk_factor
                st.subheader(f"{text.get(risk_factor, risk_factor.replace('_', ' ').title())} {text.get('analysis', 'Analysis')}")

                # Display relevant chart based on selected risk factor
                if risk_factor == "hamstring":
                    # Show hamstring specific data
                    time = np.linspace(0, 10, 500)
                    semg_signal = 0.2 * np.sin(2 * np.pi * 2 * time) + 0.1 * np.random.randn(500)

                    if athlete_data['risk_score'] > 60:
                        # Add artifacts for high-risk athletes
                        semg_signal[250:300] += 0.3 * (np.random.rand(50) + 0.5)

                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=time, 
                        y=semg_signal, 
                        mode='lines', 
                        name=text["hamstring"]
                    ))

                    fig.update_layout(
                        title=f"{text['hamstring']} {text.get('semg_signals', 'sEMG Signals')}",
                        xaxis_title=text["time_seconds"],
                        yaxis_title=text["amplitude_mv"]
                    )

                    st.plotly_chart(fig, use_container_width=True)

                elif risk_factor == "quadriceps":
                    # Quadriceps specific data
                    days = np.arange(30)
                    quad_strain = 30 + days * 0.8 + np.random.randn(30) * 3

                    fig = px.line(
                        x=days, 
                        y=quad_strain, 
                        title=f"{text['quadriceps']} {text.get('strain_over_time', 'Strain Over Time')}"
                    )

                    fig.update_layout(
                        xaxis_title=text["days"],
                        yaxis_title=text.get('strain_level', 'Strain Level')
                    )

                    st.plotly_chart(fig, use_container_width=True)

                else:
                    # Generic risk history
                    risk_history = data_processor.get_historical_data(
                        st.session_state.selected_athlete_id, 
                        "risk_score",
                        days=30
                    )

                    fig = px.line(
                        risk_history,
                        x='date',
                        y='value',
                        title=text["risk_progression"]
                    )

                    fig.update_layout(
                        xaxis_title=text["days"],
                        yaxis_title=text["risk_score"]
                    )

                    st.plotly_chart(fig, use_container_width=True)

                if st.button("← Back to Athlete Overview"):
                    st.session_state.selected_risk_factor = None
                    st.rerun()

            else:
                # Display body diagram with muscle risks
                st.markdown(f"### {text['body_diagram']}")
                body_fig = create_body_diagram(athlete_data, text)
                st.plotly_chart(body_fig, use_container_width=True)

                # Display risk factors with enhanced styling
                st.markdown(f"""
                <h3 style="color: #1E3A8A; margin-top: 20px; border-bottom: 2px solid #2563EB; padding-bottom: 8px;">
                    {text.get('risk_factors', 'Risk Factors')}
                </h3>
                <p style="font-size: 0.9em; color: #666; margin-bottom: 15px;">
                    {text.get('click_risk_factor', 'Click on a muscle group to see detailed analysis')}
                </p>
                """, unsafe_allow_html=True)

                # Create modern, more attractive risk factor cards
                for muscle, risk in athlete_data['muscle_risks'].items():
                    risk_color = utils.risk_color(risk)
                    muscle_name = text.get(muscle, muscle.replace('_', ' ').title())

                    # Risk level indicator
                    if risk >= 70:
                        risk_indicator = "🔴 " + text.get('high_risk', 'High Risk')
                    elif risk >= 40:
                        risk_indicator = "🟡 " + text.get('medium_risk', 'Medium Risk')
                    else:
                        risk_indicator = "🟢 " + text.get('low_risk', 'Low Risk')

                    # Create modern card with hover effects
                    st.markdown(f"""
                    <div onclick="parent.postMessage({{cmd: 'streamlitSelectRiskFactor', factor: '{muscle}'}}, '*')" 
                         style="cursor: pointer; border-radius: 10px; padding: 15px; margin-bottom: 12px; 
                                background: linear-gradient(to right, {risk_color}, {risk_color}CC); 
                                color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                                transition: transform 0.2s, box-shadow 0.2s;"
                         onmouseover="this.style.transform='translateY(-3px)';this.style.boxShadow='0 6px 10px rgba(0,0,0,0.2)';"
                         onmouseout="this.style.transform='translateY(0)';this.style.boxShadow='0 4px 6px rgba(0,0,0,0.1)';">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h4 style="margin: 0; font-size: 1.1em;">{muscle_name}</h4>
                            <span style="font-size: 0.8em; padding: 3px 6px; background-color: rgba(0,0,0,0.2); 
                                         border-radius: 4px;">{risk_indicator}</span>
                        </div>
                        <div style="margin-top: 10px; display: flex; align-items: center;">
                            <div style="flex-grow: 1; height: 8px; background-color: rgba(255,255,255,0.2); border-radius: 4px; overflow: hidden;">
                                <div style="height: 100%; width: {risk}%; background-color: white; border-radius: 4px;"></div>
                            </div>
                            <span style="margin-left: 10px; font-weight: bold; font-size: 1.2em;">{risk}%</span>
                        </div>
                        <div style="text-align: right; margin-top: 5px; font-size: 0.8em;">
                            {text.get('click_for_details', 'Click for details')} →
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # JavaScript to handle the click event
                st.markdown("""
                <script>
                window.addEventListener('message', function(e) {
                    if (e.data.cmd === 'streamlitSelectRiskFactor') {
                        window.parent.postMessage({
                            type: 'streamlit:setComponentValue',
                            value: e.data.factor
                        }, '*');
                    }
                });
                </script>
                """, unsafe_allow_html=True)

                # Use a hidden button to capture the JavaScript click
                clicked_risk = st.text_input("Selected Risk Factor", key="risk_factor_input", label_visibility="collapsed")
                if clicked_risk and clicked_risk != st.session_state.selected_risk_factor:
                    st.session_state.selected_risk_factor = clicked_risk
                    st.rerun()
    else:
        # CCTV-style monitoring for all athletes at once
        # Add title for the CCTV view
        st.subheader("📹 Athlete Monitoring")
        st.caption("Real-time monitoring of all athletes")

        # Get all athletes
        athletes = data_processor.get_athletes_list()

        # Create 3 columns for the grid layout
        cols = st.columns(3)

        # Loop through all athletes to create CCTV-like cards
        for i, athlete in enumerate(athletes):
            # Get detailed data for this athlete
            athlete_data = data_processor.get_athlete_data(athlete['id'])

            # Determine risk level styling
            risk_score = athlete_data['risk_score']
            risk_color = utils.risk_color(risk_score)

            if risk_score >= 70:
                alert_icon = "🔴"
                risk_level = text.get('high_risk', 'High Risk')
            elif risk_score >= 40:
                alert_icon = "🟡"
                risk_level = text.get('medium_risk', 'Medium Risk')
            else:
                alert_icon = "🟢"
                risk_level = text.get('low_risk', 'Low Risk')

            with cols[i % len(cols)]:
                # Create a card container with a border
                st.markdown(f"""
                <div style="border: 2px solid #333; border-radius: 10px; margin-bottom: 15px; overflow: hidden;">
                    <div style="background: linear-gradient(90deg, #1E3A8A 0%, #2563EB 100%); color: white; padding: 8px 15px; display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: bold;">{athlete['name']}</span>
                        <span style="font-size: 0.8em;">CAM {i+1:02d} <span style="background-color: rgba(0,0,0,0.5); padding: 2px 6px; border-radius: 4px; font-size: 0.9em;">LIVE</span></span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Add player photo and info
                col_left, col_right = st.columns([1, 2])

                with col_left:
                    st.image("assets/player_photos/player_silhouette.svg", width=80)

                with col_right:
                    st.markdown(f"""
                    **Team:** {athlete['team']}  
                    **Position:** {athlete['position']}
                    """)

                    # Display the risk level with appropriate color
                    st.markdown(f"""
                    <div style="background-color: {risk_color}; color: white; padding: 5px 10px; border-radius: 5px; text-align: center; margin-top: 5px;">
                        <span>{alert_icon} {risk_level}: {risk_score}</span>
                    </div>
                    """, unsafe_allow_html=True)

                # Display vital stats in 3 small columns
                v_col1, v_col2, v_col3 = st.columns(3)
                with v_col1:
                    st.metric("HR", f"{athlete_data.get('heart_rate', 72)}")
                with v_col2:
                    st.metric("Temp", f"{athlete_data.get('temperature', 36.5)}°")
                with v_col3:
                    st.metric("Load", f"{athlete_data.get('current_load', 65)}%")

                # Create compact body diagram
                body_fig = create_body_diagram(athlete_data, text, compact=True)
                st.plotly_chart(body_fig, use_container_width=True, config={'displayModeBar': False})

                # View details button
                if st.button(f"View Details", key=f"view_{athlete['id']}"):
                    st.session_state.selected_athlete_id = athlete['id']
                    st.rerun()

    # Risk distribution chart
    st.subheader(text["risk_distribution"])

    # Generate sample data for demonstration
    risk_data = {
        'Muscle Group': ['Hamstring', 'Quadriceps', 'Calf', 'Lower Back', 'Shoulder'],
        'Average Risk': [45, 32, 67, 22, 18]
    }

    risk_df = pd.DataFrame(risk_data)

    # Create color scale for risk levels
    risk_df['Color'] = risk_df['Average Risk'].apply(
        lambda x: 'green' if x < 30 else ('yellow' if x < 60 else 'red')
    )

    fig = px.bar(
        risk_df,
        x='Muscle Group',
        y='Average Risk',
        color='Color',
        color_discrete_map={'green': '#4CAF50', 'yellow': '#FFC107', 'red': '#F44336'},
        title=text["team_risk_by_muscle"]
    )

    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    # Recent alerts
    st.subheader(text["recent_alerts"])

    alert_data = [
        {"athlete": "Khalid Ahmed", "alert": text["high_risk_hamstring"], "time": "25 min ago", "severity": "High"},
        {"athlete": "Sarah Wilson", "alert": text["elevated_temperature"], "time": "1 hour ago", "severity": "Medium"},
        {"athlete": "Ahmed Hassan", "alert": text["emg_irregularity"], "time": "3 hours ago", "severity": "Medium"}
    ]

    cols = st.columns(3)
    for i, alert in enumerate(alert_data):
        with cols[i]:
            color = "#F44336" if alert["severity"] == "High" else "#FFC107"
            st.markdown(f"""
            <div style='border-left: 4px solid {color}; padding-left: 10px;'>
                <h4>{alert["athlete"]}</h4>
                <p>{alert["alert"]}</p>
                <p><small>{alert["time"]}</small></p>
            </div>
            """, unsafe_allow_html=True)

    # sEMG Signal Visualization
    st.subheader(text["semg_visualization"])

    # Create tabs for different signal visualizations
    tab1, tab2 = st.tabs([text["real_time_signals"], text["avg_activation"]])

    with tab1:
        # Generate mock time series data for sEMG signals
        time = np.linspace(0, 10, 500)
        semg_signal_1 = np.sin(2 * np.pi * 1 * time) * np.exp(-0.1 * time) + 0.1 * np.random.randn(len(time))
        semg_signal_2 = np.sin(2 * np.pi * 0.5 * time) * np.exp(-0.05 * time) + 0.1 * np.random.randn(len(time))

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=time, y=semg_signal_1, mode='lines', name=text["hamstring"]))
        fig.add_trace(go.Scatter(x=time, y=semg_signal_2, mode='lines', name=text["quadriceps"]))

        fig.update_layout(
            title=text["semg_signals_title"],
            xaxis_title=text["time_seconds"],
            yaxis_title=text["amplitude_mv"],
            legend_title=text["muscle_group"]
        )

        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        # Average activation by muscle group
        activation_data = {
            'Muscle Group': ['Hamstring', 'Quadriceps', 'Calf', 'Lower Back', 'Shoulder'],
            'Left Side': [78, 65, 82, 42, 55],
            'Right Side': [75, 68, 79, 45, 53]
        }

        activation_df = pd.DataFrame(activation_data)

        fig = go.Figure(data=[
            go.Bar(name=text["left_side"], x=activation_df['Muscle Group'], y=activation_df['Left Side']),
            go.Bar(name=text["right_side"], x=activation_df['Muscle Group'], y=activation_df['Right Side'])
        ])

        fig.update_layout(
            barmode='group',
            title=text["avg_muscle_activation"],
            xaxis_title=text["muscle_group"],
            yaxis_title=text["activation_percentage"]
        )

        st.plotly_chart(fig, use_container_width=True)

    # Temperature Readings
    st.subheader(text["temperature_readings"])

    temp_data = {
        'Athlete': ['Khalid Ahmed', 'Sarah Wilson', 'Ahmed Hassan', 'Maria Rodriguez', 'James Smith'],
        'Hamstring': [36.2, 36.7, 36.5, 36.3, 36.4],
        'Quadriceps': [36.5, 36.8, 36.3, 36.4, 36.6],
        'Calf': [36.4, 36.5, 36.7, 36.2, 36.3],
        'Lower Back': [36.9, 36.6, 36.8, 36.5, 36.7]
    }

    temp_df = pd.DataFrame(temp_data)

    # Convert to long format for heatmap
    temp_long = pd.melt(
        temp_df, 
        id_vars=['Athlete'], 
        value_vars=['Hamstring', 'Quadriceps', 'Calf', 'Lower Back'],
        var_name='Muscle Group',
        value_name='Temperature'
    )

    fig = px.density_heatmap(
        temp_long,
        x='Muscle Group',
        y='Athlete',
        z='Temperature',
        color_continuous_scale='Viridis',
        title=text["skin_temperature"]
    )

    fig.update_layout(
        xaxis_title=text["muscle_group"],
        yaxis_title=text["athlete"],
        coloraxis_colorbar_title=text["temperature_c"]
    )

    st.plotly_chart(fig, use_container_width=True)

    # Injury prediction model section
    st.subheader(text["injury_prediction"])

    col1, col2 = st.columns(2)

    with col1:
        # Risk progression over time
        days = np.arange(30)
        risk_trend_1 = 30 + days * 1.5 + np.random.randn(30) * 5
        risk_trend_2 = 25 + np.sin(days/5) * 10 + np.random.randn(30) * 3

        risk_trend_df = pd.DataFrame({
            'Day': days,
            'Khalid Ahmed': risk_trend_1,
            'Sarah Wilson': risk_trend_2
        })

        risk_trend_long = pd.melt(
            risk_trend_df,
            id_vars=['Day'],
            value_vars=['Khalid Ahmed', 'Sarah Wilson'],
            var_name='Athlete',
            value_name='Risk Score'
        )

        fig = px.line(
            risk_trend_long,
            x='Day',
            y='Risk Score',
            color='Athlete',
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

    with col2:
        # Risk factors contribution
        risk_factors = {
            'Factor': [
                text["semg_imbalance"], 
                text["training_load"], 
                text["recovery_time"],
                text["previous_injury"],
                text["temperature_variation"]
            ],
            'Contribution': [32, 25, 18, 15, 10]
        }

        risk_factors_df = pd.DataFrame(risk_factors)

        fig = px.pie(
            risk_factors_df,
            values='Contribution',
            names='Factor',
            title=text["risk_factors"]
        )

        fig.update_traces(textposition='inside', textinfo='percent+label')

        st.plotly_chart(fig, use_container_width=True)

    # Export section
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            label=text["export_dashboard"],
            data=utils.generate_report(),
            file_name="athlete_biometrics_report.csv",
            mime="text/csv"
        )

    with col2:
        st.markdown(f"**{text['last_updated']}:** {utils.get_current_time()}")

elif page == text["athlete_profiles"]:
    # Use streamlit pages feature to load the athlete profiles page
    import pages.athlete_profiles

elif page == text["team_overview"]:
    # Use streamlit pages feature to load the team overview page
    import pages.team_overview

elif page == text["historical_data"]:
    # Use streamlit pages feature to load the historical data page
    import pages.historical_data

elif page == text["settings"]:
    # Use streamlit pages feature to load the settings page
    import pages.settings