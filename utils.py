import streamlit as st
import pandas as pd
import numpy as np
import io
from datetime import datetime
import pytz

def get_text_dict(language="English"):
    """
    Get text dictionary for the selected language
    
    Args:
        language (str, optional): Language code. Defaults to "English".
        
    Returns:
        dict: Dictionary containing UI text in the selected language
    """
    if language == "Arabic":
        return {
            "app_title": "منصة مراقبة البيانات الحيوية للرياضيين",
            "app_description": "منصة لمراقبة الإشارات الحيوية للرياضيين وتوقع مخاطر الإصابة",
            "select_language": "اختر اللغة",
            "navigation": "التنقل",
            "select_page": "اختر الصفحة",
            "dashboard": "لوحة المعلومات",
            "athlete_profiles": "ملفات الرياضيين",
            "team_overview": "نظرة عامة على الفريق",
            "historical_data": "البيانات التاريخية",
            "settings": "الإعدادات",
            "dashboard_title": "لوحة معلومات البيانات الحيوية للرياضيين",
            "dashboard_description": "مراقبة الإشارات الحيوية للرياضيين وتنبؤات مخاطر الإصابة",
            "total_athletes": "إجمالي الرياضيين",
            "high_risk_athletes": "الرياضيين ذوي المخاطر العالية",
            "medium_risk_athletes": "الرياضيين ذوي المخاطر المتوسطة",
            "team_avg_risk": "متوسط المخاطر للفريق",
            "avg_risk_score": "متوسط درجة المخاطر",
            "risk_distribution": "توزيع المخاطر",
            "team_risk_by_muscle": "مخاطر الفريق حسب مجموعة العضلات",
            "recent_alerts": "التنبيهات الأخيرة",
            "high_risk_hamstring": "ارتفاع مخاطر إصابة أوتار الركبة",
            "elevated_temperature": "ارتفاع درجة الحرارة فوق المتوسط",
            "emg_irregularity": "اضطراب في إشارة EMG للعضلات",
            "semg_visualization": "تصور إشارات sEMG",
            "real_time_signals": "الإشارات في الوقت الحقيقي",
            "avg_activation": "متوسط التنشيط",
            "semg_signals_title": "إشارات sEMG للعضلات",
            "time_seconds": "الوقت (ثواني)",
            "amplitude_mv": "السعة (ميلي فولت)",
            "muscle_group": "مجموعة العضلات",
            "select_muscle": "اختر مجموعة العضلات",
            "left_side": "الجانب الأيسر",
            "right_side": "الجانب الأيمن",
            "avg_muscle_activation": "متوسط تنشيط العضلات",
            "activation_percentage": "نسبة التنشيط (%)",
            "temperature_readings": "قراءات درجة الحرارة",
            "skin_temperature": "درجة حرارة الجلد فوق العضلات",
            "athlete": "الرياضي",
            "temperature_c": "درجة الحرارة (°C)",
            "injury_prediction": "توقع الإصابة",
            "risk_progression": "تطور المخاطر على مدار الوقت",
            "risk_threshold": "عتبة المخاطر",
            "days": "الأيام",
            "risk_score": "درجة المخاطر",
            "risk_factors": "عوامل المخاطر",
            "semg_imbalance": "عدم توازن إشارات sEMG",
            "training_load": "حمل التدريب",
            "recovery_time": "وقت التعافي",
            "previous_injury": "إصابة سابقة",
            "temperature_variation": "تباين درجة الحرارة",
            "export_dashboard": "تصدير بيانات لوحة المعلومات",
            "last_updated": "آخر تحديث",
            "select_athlete": "اختر الرياضي",
            "athlete_details": "تفاصيل الرياضي",
            "personal_info": "المعلومات الشخصية",
            "biometric_data": "البيانات الحيوية",
            "injury_history": "تاريخ الإصابات",
            "no_injury_history": "لا يوجد تاريخ إصابات مسجل",
            "age": "العمر",
            "years": "سنوات",
            "height": "الطول",
            "weight": "الوزن",
            "team": "الفريق",
            "position": "المركز",
            "risk_analysis": "تحليل المخاطر",
            "risk": "خطر",
            "biometric_signals": "الإشارات الحيوية",
            "hamstring": "أوتار الركبة",
            "quadriceps": "العضلة الرباعية",
            "calf": "عضلة السمانة",
            "lower_back": "أسفل الظهر",
            "shoulder": "الكتف",
            "filter_by_team": "تصفية حسب الفريق",
            "filter_by_risk": "تصفية حسب المخاطر",
            "all_teams": "جميع الفرق",
            "all_risk_levels": "جميع مستويات المخاطر",
            "high_risk": "مخاطر عالية",
            "medium_risk": "مخاطر متوسطة",
            "low_risk": "مخاطر منخفضة",
            "team_comparison": "مقارنة الفرق",
            "metrics_by_team": "المقاييس حسب الفريق",
            "risk_settings": "إعدادات المخاطر",
            "risk_threshold_setting": "تحديد عتبة المخاطر",
            "save_settings": "حفظ الإعدادات",
            "settings_saved": "تم حفظ الإعدادات بنجاح",
            "date_range": "النطاق الزمني",
            "date": "التاريخ",
            "select_metric": "اختر المقياس",
            "apply_filters": "تطبيق التصفية",
            "historical_view": "العرض التاريخي",
            "comparison_view": "عرض المقارنة",
            "select_athletes": "اختر الرياضيين",
            "compare": "مقارنة",
            "body_diagram": "مخطط الجسم",
            "body_diagram_description": "انقر على منطقة لعرض التفاصيل",
            "muscle_activation": "تنشيط العضلات",
            "athlete_monitoring": "مراقبة الرياضي",
            "live_monitoring": "المراقبة المباشرة لحالة الرياضي",
            "view_details": "عرض التفاصيل",
            "analysis": "تحليل",
            "semg_signals": "إشارات sEMG",
            "strain_over_time": "الإجهاد على مر الزمن",
            "strain_level": "مستوى الإجهاد"
        }
    else:  # Default to English
        return {
            "app_title": "Athlete Biometric Monitoring Platform",
            "app_description": "Platform for monitoring athlete biometric signals and predicting injury risks",
            "select_language": "Select Language",
            "navigation": "Navigation",
            "select_page": "Select Page",
            "dashboard": "Dashboard",
            "athlete_profiles": "Athlete Profiles",
            "team_overview": "Team Overview",
            "historical_data": "Historical Data",
            "settings": "Settings",
            "dashboard_title": "Athlete Biometric Dashboard",
            "dashboard_description": "Monitor athlete biometric signals and injury risk predictions",
            "total_athletes": "Total Athletes",
            "high_risk_athletes": "High Risk Athletes",
            "medium_risk_athletes": "Medium Risk Athletes",
            "team_avg_risk": "Team Avg. Risk",
            "avg_risk_score": "Average Risk Score",
            "risk_distribution": "Risk Distribution",
            "team_risk_by_muscle": "Team Risk by Muscle Group",
            "recent_alerts": "Recent Alerts",
            "high_risk_hamstring": "High hamstring injury risk",
            "elevated_temperature": "Elevated temperature above average",
            "emg_irregularity": "Muscle EMG signal irregularity",
            "semg_visualization": "sEMG Signal Visualization",
            "real_time_signals": "Real-time Signals",
            "avg_activation": "Average Activation",
            "semg_signals_title": "Muscle sEMG Signals",
            "time_seconds": "Time (seconds)",
            "amplitude_mv": "Amplitude (mV)",
            "muscle_group": "Muscle Group",
            "select_muscle": "Select Muscle Group",
            "left_side": "Left Side",
            "right_side": "Right Side",
            "avg_muscle_activation": "Average Muscle Activation",
            "activation_percentage": "Activation Percentage (%)",
            "temperature_readings": "Temperature Readings",
            "skin_temperature": "Skin Temperature Over Muscles",
            "athlete": "Athlete",
            "temperature_c": "Temperature (°C)",
            "injury_prediction": "Injury Prediction",
            "risk_progression": "Risk Progression Over Time",
            "risk_threshold": "Risk Threshold",
            "days": "Days",
            "risk_score": "Risk Score",
            "risk_factors": "Risk Factors",
            "semg_imbalance": "sEMG Imbalance",
            "training_load": "Training Load",
            "recovery_time": "Recovery Time",
            "previous_injury": "Previous Injury",
            "temperature_variation": "Temperature Variation",
            "export_dashboard": "Export Dashboard Data",
            "last_updated": "Last Updated",
            "select_athlete": "Select Athlete",
            "athlete_details": "Athlete Details",
            "personal_info": "Personal Info",
            "biometric_data": "Biometric Data",
            "injury_history": "Injury History",
            "no_injury_history": "No injury history recorded",
            "age": "Age",
            "years": "years",
            "height": "Height",
            "weight": "Weight",
            "team": "Team",
            "position": "Position",
            "risk_analysis": "Risk Analysis",
            "risk": "Risk", 
            "biometric_signals": "Biometric Signals",
            "hamstring": "Hamstring",
            "quadriceps": "Quadriceps",
            "calf": "Calf",
            "lower_back": "Lower Back",
            "shoulder": "Shoulder",
            "filter_by_team": "Filter by Team",
            "filter_by_risk": "Filter by Risk",
            "all_teams": "All Teams",
            "all_risk_levels": "All Risk Levels",
            "high_risk": "High Risk",
            "medium_risk": "Medium Risk",
            "low_risk": "Low Risk",
            "team_comparison": "Team Comparison",
            "metrics_by_team": "Metrics by Team",
            "risk_settings": "Risk Settings",
            "risk_threshold_setting": "Set Risk Threshold",
            "save_settings": "Save Settings",
            "settings_saved": "Settings saved successfully",
            "date_range": "Date Range",
            "date": "Date",
            "select_metric": "Select Metric",
            "apply_filters": "Apply Filters",
            "historical_view": "Historical View",
            "comparison_view": "Comparison View",
            "select_athletes": "Select Athletes",
            "compare": "Compare",
            "body_diagram": "Body Diagram",
            "body_diagram_description": "Click on an area to see details",
            "muscle_activation": "Muscle Activation",
            "athlete_monitoring": "Athlete Monitoring",
            "live_monitoring": "Live monitoring of athlete status",
            "view_details": "View Details",
            "analysis": "Analysis",
            "semg_signals": "sEMG Signals",
            "strain_over_time": "Strain Over Time",
            "strain_level": "Strain Level"
        }

def generate_report():
    """
    Generate a CSV report for export
    
    Returns:
        bytes: CSV data as bytes
    """
    # Create a DataFrame with sample data
    data = {
        'Athlete': ['Khalid Ahmed', 'Sarah Wilson', 'Ahmed Hassan', 'Maria Rodriguez', 'James Smith'],
        'Risk Score': [75, 45, 35, 20, 15],
        'Hamstring EMG (mV)': [0.45, 0.32, 0.38, 0.29, 0.34],
        'Quadriceps EMG (mV)': [0.42, 0.35, 0.33, 0.31, 0.36],
        'Muscle Imbalance (%)': [12.5, 8.2, 15.3, 6.7, 5.8],
        'Temperature (°C)': [36.8, 36.5, 36.7, 36.3, 36.4],
        'Fatigue Index': [65, 42, 38, 25, 30]
    }
    
    df = pd.DataFrame(data)
    
    # Convert DataFrame to CSV
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    
    return csv_buffer.getvalue().encode()

def get_current_time():
    """
    Get current time formatted as a string
    
    Returns:
        str: Current time string
    """
    now = datetime.now(pytz.timezone('UTC'))
    return now.strftime("%Y-%m-%d %H:%M:%S UTC")

def risk_color(risk_score):
    """
    Get color code based on risk score
    
    Args:
        risk_score (float): Risk score (0-100)
        
    Returns:
        str: Hex color code
    """
    if risk_score < 30:
        return "#4CAF50"  # Green
    elif risk_score < 60:
        return "#FFC107"  # Yellow
    else:
        return "#F44336"  # Red

def parse_date_range(date_range_str):
    """
    Parse date range string into start and end dates
    
    Args:
        date_range_str (str): Date range string (e.g., "2023-01-01 to 2023-01-31")
        
    Returns:
        tuple: (start_date, end_date) as datetime objects
    """
    try:
        start_str, end_str = date_range_str.split(" to ")
        start_date = datetime.strptime(start_str.strip(), "%Y-%m-%d")
        end_date = datetime.strptime(end_str.strip(), "%Y-%m-%d")
        return start_date, end_date
    except:
        # Default to last 30 days if parsing fails
        end_date = datetime.now()
        start_date = end_date - pd.Timedelta(days=30)
        return start_date, end_date
