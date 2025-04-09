import streamlit as st
import plotly.graph_objects as go
import numpy as np

def create_body_diagram(athlete_data=None, text_dict=None, compact=False):
    """
    Create an interactive body diagram showing muscle risk levels
    
    Args:
        athlete_data (dict, optional): Athlete data containing risk scores. Defaults to None.
        text_dict (dict, optional): Text dictionary for translations. Defaults to None.
        compact (bool, optional): If True, creates a more compact version for dashboard. Defaults to False.
    
    Returns:
        plotly.graph_objects.Figure: Interactive body diagram
    """
    if text_dict is None:
        # Default English texts if not provided
        text_dict = {
            "body_diagram": "Body Diagram",
            "hamstring": "Hamstring",
            "quadriceps": "Quadriceps", 
            "calf": "Calf",
            "lower_back": "Lower Back",
            "shoulder": "Shoulder"
        }

    # Create a figure for the body diagram
    fig = go.Figure()
    
    # Define body outline coordinates
    # Using simple shapes to represent a human body in a more anatomical way
    # Head
    head_x = [0]
    head_y = [5]
    
    # Torso - more detailed shape
    torso_x = [-1.2, -1.4, -1.2, -0.8, 0, 0.8, 1.2, 1.4, 1.2, 0]
    torso_y = [3.8, 2.5, 1, 0, -0.5, 0, 1, 2.5, 3.8, 4]
    
    # Arms - more curved
    left_arm_x = [-1.4, -2, -2.3]
    left_arm_y = [3.2, 2.2, 1]
    
    right_arm_x = [1.4, 2, 2.3]
    right_arm_y = [3.2, 2.2, 1]
    
    # Legs - more anatomical
    left_leg_x = [-0.8, -1.1, -1, -0.9]
    left_leg_y = [-0.5, -2, -3.5, -5]
    
    right_leg_x = [0.8, 1.1, 1, 0.9]
    right_leg_y = [-0.5, -2, -3.5, -5]
    
    # Draw body outline with smoother lines and better colors
    # Use a skin-tone color for a more realistic look
    body_color = '#E0C2A2'
    outline_color = '#5D4037'
    
    # Draw body with filled shapes
    # Torso shape
    fig.add_trace(go.Scatter(
        x=torso_x, y=torso_y,
        fill="toself",
        fillcolor=body_color,
        line=dict(color=outline_color, width=1),
        name='Torso',
        hoverinfo='skip'
    ))
    
    # Left arm
    fig.add_trace(go.Scatter(
        x=left_arm_x, y=left_arm_y,
        mode='lines',
        line=dict(width=12, color=body_color),
        name='Left Arm',
        hoverinfo='skip'
    ))
    
    # Right arm
    fig.add_trace(go.Scatter(
        x=right_arm_x, y=right_arm_y,
        mode='lines',
        line=dict(width=12, color=body_color),
        name='Right Arm',
        hoverinfo='skip'
    ))
    
    # Left leg
    fig.add_trace(go.Scatter(
        x=left_leg_x, y=left_leg_y,
        mode='lines',
        line=dict(width=14, color=body_color),
        name='Left Leg',
        hoverinfo='skip'
    ))
    
    # Right leg
    fig.add_trace(go.Scatter(
        x=right_leg_x, y=right_leg_y,
        mode='lines',
        line=dict(width=14, color=body_color),
        name='Right Leg',
        hoverinfo='skip'
    ))
    
    # Head
    fig.add_trace(go.Scatter(
        x=head_x, y=head_y,
        mode='markers',
        marker=dict(size=24, color=body_color, line=dict(color=outline_color, width=1)),
        name='Head',
        hoverinfo='skip'
    ))
    
    # Define muscle group areas with colored circles
    # Default risk values if athlete_data is not provided
    default_risk = {
        "hamstring": 45,
        "quadriceps": 32,
        "calf": 25,
        "lower_back": 38,
        "shoulder": 20
    }
    
    risk_data = default_risk
    
    # If athlete data is provided, use their risk values
    if athlete_data and hasattr(athlete_data, "get"):
        # Try to extract risk values from athlete data
        muscle_risks = athlete_data.get("muscle_risks", {})
        if muscle_risks:
            risk_data = muscle_risks
    
    # Create hover text for muscle groups
    hamstring_text = f"{text_dict.get('hamstring', 'Hamstring')}<br>Risk: {risk_data['hamstring']}%"
    quad_text = f"{text_dict.get('quadriceps', 'Quadriceps')}<br>Risk: {risk_data['quadriceps']}%"
    calf_text = f"{text_dict.get('calf', 'Calf')}<br>Risk: {risk_data['calf']}%"
    back_text = f"{text_dict.get('lower_back', 'Lower Back')}<br>Risk: {risk_data['lower_back']}%"
    shoulder_text = f"{text_dict.get('shoulder', 'Shoulder')}<br>Risk: {risk_data['shoulder']}%"
    
    # Define color based on risk with better color scheme
    def get_color(risk):
        if risk < 30:
            return "#4CAF50"  # Green
        elif risk < 60:
            return "#FFC107"  # Yellow/Amber
        else:
            return "#F44336"  # Red
    
    # Add muscle groups as highlight areas with more anatomical placement
    # Hamstring (back of thigh)
    fig.add_trace(go.Scatter(
        x=[-1.05, 1.05], 
        y=[-2.5, -2.5],
        mode='markers',
        marker=dict(
            size=18 if compact else 25, 
            color=[get_color(risk_data['hamstring']), get_color(risk_data['hamstring'])],
            opacity=0.8,
            symbol='diamond',
            line=dict(color=outline_color, width=1)
        ),
        name=text_dict.get('hamstring', 'Hamstring'),
        text=[hamstring_text, hamstring_text],
        hoverinfo='text',
        customdata=[['hamstring'], ['hamstring']]  # Store muscle name for click events
    ))
    
    # Quadriceps (front of thigh)
    fig.add_trace(go.Scatter(
        x=[-1.05, 1.05], 
        y=[-1.5, -1.5],
        mode='markers',
        marker=dict(
            size=18 if compact else 25, 
            color=[get_color(risk_data['quadriceps']), get_color(risk_data['quadriceps'])],
            opacity=0.8,
            symbol='diamond',
            line=dict(color=outline_color, width=1)
        ),
        name=text_dict.get('quadriceps', 'Quadriceps'),
        text=[quad_text, quad_text],
        hoverinfo='text',
        customdata=[['quadriceps'], ['quadriceps']]
    ))
    
    # Calf muscles
    fig.add_trace(go.Scatter(
        x=[-0.95, 0.95], 
        y=[-4, -4],
        mode='markers',
        marker=dict(
            size=16 if compact else 22, 
            color=[get_color(risk_data['calf']), get_color(risk_data['calf'])],
            opacity=0.8,
            symbol='diamond',
            line=dict(color=outline_color, width=1)
        ),
        name=text_dict.get('calf', 'Calf'),
        text=[calf_text, calf_text],
        hoverinfo='text',
        customdata=[['calf'], ['calf']]
    ))
    
    # Lower back
    fig.add_trace(go.Scatter(
        x=[0], 
        y=[2],
        mode='markers',
        marker=dict(
            size=24 if compact else 35, 
            color=get_color(risk_data['lower_back']),
            opacity=0.8,
            symbol='diamond',
            line=dict(color=outline_color, width=1)
        ),
        name=text_dict.get('lower_back', 'Lower Back'),
        text=back_text,
        hoverinfo='text',
        customdata=[['lower_back']]
    ))
    
    # Shoulders
    fig.add_trace(go.Scatter(
        x=[-1.7, 1.7], 
        y=[3.2, 3.2],
        mode='markers',
        marker=dict(
            size=16 if compact else 22, 
            color=[get_color(risk_data['shoulder']), get_color(risk_data['shoulder'])],
            opacity=0.8,
            symbol='diamond',
            line=dict(color=outline_color, width=1)
        ),
        name=text_dict.get('shoulder', 'Shoulder'),
        text=[shoulder_text, shoulder_text],
        hoverinfo='text',
        customdata=[['shoulder'], ['shoulder']]
    ))
    
    # Add risk percentage labels directly on the diagram if not compact mode
    if not compact:
        # Hamstring label
        fig.add_annotation(
            x=-1.5, y=-2.5,
            text=f"{risk_data['hamstring']}%",
            showarrow=False,
            font=dict(size=10, color="white", family="Arial Black"),
            bgcolor=get_color(risk_data['hamstring']),
            bordercolor=outline_color,
            borderwidth=1,
            borderpad=3,
            opacity=0.8
        )
        
        # Quadriceps label
        fig.add_annotation(
            x=-1.5, y=-1.5,
            text=f"{risk_data['quadriceps']}%",
            showarrow=False,
            font=dict(size=10, color="white", family="Arial Black"),
            bgcolor=get_color(risk_data['quadriceps']),
            bordercolor=outline_color,
            borderwidth=1,
            borderpad=3,
            opacity=0.8
        )
        
        # Calf label
        fig.add_annotation(
            x=-1.5, y=-4,
            text=f"{risk_data['calf']}%",
            showarrow=False,
            font=dict(size=10, color="white", family="Arial Black"),
            bgcolor=get_color(risk_data['calf']),
            bordercolor=outline_color,
            borderwidth=1,
            borderpad=3,
            opacity=0.8
        )
        
        # Lower back label
        fig.add_annotation(
            x=0, y=1.3,
            text=f"{risk_data['lower_back']}%",
            showarrow=False,
            font=dict(size=10, color="white", family="Arial Black"),
            bgcolor=get_color(risk_data['lower_back']),
            bordercolor=outline_color,
            borderwidth=1,
            borderpad=3,
            opacity=0.8
        )
        
        # Shoulder label
        fig.add_annotation(
            x=2.3, y=3.2,
            text=f"{risk_data['shoulder']}%",
            showarrow=False,
            font=dict(size=10, color="white", family="Arial Black"),
            bgcolor=get_color(risk_data['shoulder']),
            bordercolor=outline_color,
            borderwidth=1,
            borderpad=3,
            opacity=0.8
        )
    
    # Update layout for better display
    title = text_dict.get('body_diagram', "Body Diagram") if not compact else None
    height = 300 if compact else 500
    
    fig.update_layout(
        title=title,
        showlegend=False,
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[-3.5, 3.5]
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[-5.5, 5.5],
            scaleanchor='x'
        ),
        margin=dict(l=0, r=0, t=30 if compact else 50, b=0),
        height=height,
        hovermode='closest',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    # Add instructions text if not in compact mode
    if not compact:
        fig.add_annotation(
            x=0, y=-5.5,
            text=text_dict.get('body_diagram_description', "Click on an area to see details"),
            showarrow=False,
            font=dict(size=12)
        )
    
    return fig

def create_mobile_body_diagram_section(athlete_data=None, text_dict=None):
    """
    Create a mobile-friendly body diagram section in Streamlit
    
    Args:
        athlete_data (dict, optional): Athlete data containing risk scores. Defaults to None.
        text_dict (dict, optional): Text dictionary for translations. Defaults to None.
    """
    # Create body diagram
    fig = create_body_diagram(athlete_data, text_dict)
    
    # Display in streamlit
    st.plotly_chart(fig, use_container_width=True, config={'responsive': True})
    
    # Display muscle group cards for mobile view
    # This gives an alternate way to view the data on small screens
    st.markdown("### " + text_dict.get('muscle_group', "Muscle Group") + " " + text_dict.get('risk_analysis', "Risk Analysis"))
    
    # Define default risk values if not provided
    default_risk = {
        "hamstring": 45,
        "quadriceps": 32,
        "calf": 25,
        "lower_back": 38,
        "shoulder": 20
    }
    
    risk_data = default_risk
    
    # If athlete data is provided, use their risk values
    if athlete_data and hasattr(athlete_data, "get"):
        # Try to extract risk values from athlete data
        muscle_risks = athlete_data.get("muscle_risks", {})
        if muscle_risks:
            risk_data = muscle_risks
    
    # Create columns for muscle groups
    col1, col2 = st.columns(2)
    
    # Function to get color based on risk
    def get_color_hex(risk):
        if risk < 30:
            return "#4CAF50"  # Green
        elif risk < 60:
            return "#FFC107"  # Yellow
        else:
            return "#F44336"  # Red
    
    # Display muscle group cards
    with col1:
        for muscle in ["hamstring", "quadriceps", "calf"]:
            risk = risk_data[muscle]
            st.markdown(f"""
            <div style="border-radius: 10px; padding: 10px; background-color: {get_color_hex(risk)}; 
                        color: white; margin-bottom: 10px; text-align: center;">
                <h4 style="margin: 0;">{text_dict.get(muscle, muscle.title())}</h4>
                <h2 style="margin: 5px 0;">{risk}%</h2>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        for muscle in ["lower_back", "shoulder"]:
            risk = risk_data[muscle]
            st.markdown(f"""
            <div style="border-radius: 10px; padding: 10px; background-color: {get_color_hex(risk)}; 
                        color: white; margin-bottom: 10px; text-align: center;">
                <h4 style="margin: 0;">{text_dict.get(muscle, muscle.title())}</h4>
                <h2 style="margin: 5px 0;">{risk}%</h2>
            </div>
            """, unsafe_allow_html=True)