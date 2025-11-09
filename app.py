"""
AutoKPI - Streamlit Application
Main UI for the AutoKPI analytics application
"""

import streamlit as st
import pandas as pd
import io
from datetime import datetime
import sys
import os
from typing import Dict, List, Any

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from autokpi.schema_inference import infer_schema, get_schema_summary
from autokpi.kpi_rules import generate_kpis
from autokpi.sql_generator import generate_sql_queries
from autokpi.viz_suggestions import suggest_chart_type, generate_chart
from autokpi.chart_explanations import generate_chart_explanation
# LLM refinement removed - using rule-based KPI generation only
from autokpi.exporter import export_to_json, export_to_markdown, export_to_dashboard_spec
from autokpi.data_quality import check_data_quality
from autokpi.advanced_analytics import (
    calculate_correlations, detect_outliers, calculate_distribution_stats,
    detect_trends, calculate_growth_rates, generate_statistical_summary
)
from autokpi.auto_insights import generate_insights, format_insights_for_display
import altair as alt

# Page configuration
st.set_page_config(
    page_title="AutoKPI - AI-Assisted Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful, modern dark theme styling
st.markdown("""
    <style>
    /* Global styling - DARK THEME with black background */
    .stApp {
        background: #000000 !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    }
    
    /* Main content area - dark */
    .main .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 1200px;
        background: #000000 !important;
        color: #ffffff !important;
    }
    
    /* Make all text visible on black */
    .element-container {
        margin-bottom: 1.5rem;
        background: transparent !important;
    }
    
    /* Dark theme for main content */
    .main {
        background: #000000 !important;
        color: #ffffff !important;
    }
    
    /* All text should be light on black */
    p, li, div, span {
        color: #e5e7eb !important;
    }
    
    /* Make buttons more prominent - DARK THEME */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%) !important;
        color: #ffffff !important;
        border: 2px solid rgba(139, 92, 246, 0.5) !important;
        border-radius: 12px !important;
        padding: 1rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 6px 20px rgba(139, 92, 246, 0.5), 0 0 30px rgba(139, 92, 246, 0.3) !important;
        margin: 0.5rem 0 !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 10px 40px rgba(139, 92, 246, 0.7), 0 0 50px rgba(139, 92, 246, 0.4) !important;
        background: linear-gradient(135deg, #ec4899 0%, #8b5cf6 100%) !important;
        border-color: rgba(236, 72, 153, 0.7) !important;
    }
    
    /* Make file uploader more visible - DARK THEME */
    [data-testid="stFileUploader"] {
        border: 3px dashed #8b5cf6 !important;
        border-radius: 20px !important;
        padding: 3rem !important;
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(236, 72, 153, 0.1) 100%) !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 0 30px rgba(139, 92, 246, 0.2) !important;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #ec4899 !important;
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(236, 72, 153, 0.2) 100%) !important;
        transform: scale(1.01);
        box-shadow: 0 0 40px rgba(139, 92, 246, 0.4) !important;
    }
    
    /* Make text more readable - DARK THEME */
    p, li, div, span {
        color: #e5e7eb !important;
        font-size: 1.05rem !important;
        line-height: 1.7 !important;
    }
    
    /* Make headings more prominent - DARK THEME */
    h1, h2, h3, h4, h5, h6 {
        color: #f3f4f6 !important;
        font-weight: 800 !important;
    }
    
    /* Main header - stunning gradient on black */
    .main-header {
        font-size: 4rem;
        font-weight: 900;
        background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 50%, #f59e0b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -2px;
        text-shadow: 0 0 40px rgba(139, 92, 246, 0.5);
        animation: gradient-shift 3s ease infinite;
        background-size: 200% 200%;
        filter: drop-shadow(0 0 20px rgba(139, 92, 246, 0.3));
    }
    
    @keyframes gradient-shift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .sub-header {
        font-size: 1.4rem;
        color: #a78bfa !important;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 300;
        letter-spacing: 0.5px;
        text-shadow: 0 0 10px rgba(167, 139, 250, 0.3);
    }
    
    /* Beautiful card styling - DARK THEME */
    .insight-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #0f0f0f 100%) !important;
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 10px 40px rgba(139, 92, 246, 0.3), 0 2px 8px rgba(0, 0, 0, 0.8);
        border: 1px solid rgba(139, 92, 246, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        color: #e5e7eb !important;
    }
    
    .insight-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, #8b5cf6 0%, #ec4899 100%);
        box-shadow: 0 0 10px rgba(139, 92, 246, 0.5);
    }
    
    .insight-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 60px rgba(139, 92, 246, 0.4), 0 4px 12px rgba(0, 0, 0, 0.9);
        border-color: rgba(139, 92, 246, 0.5);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #0f0f0f 100%) !important;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(139, 92, 246, 0.2);
        border: 1px solid rgba(139, 92, 246, 0.2);
        transition: all 0.3s ease;
        color: #e5e7eb !important;
    }
    
    .metric-card:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 12px 40px rgba(139, 92, 246, 0.4);
        border-color: rgba(139, 92, 246, 0.5);
    }
    
    /* Beautiful story section - DARK THEME */
    .story-section {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(236, 72, 153, 0.15) 100%) !important;
        border-radius: 24px;
        padding: 2.5rem;
        margin: 2.5rem 0;
        border: 1px solid rgba(139, 92, 246, 0.3);
        box-shadow: 0 8px 32px rgba(139, 92, 246, 0.2);
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
        color: #e5e7eb !important;
    }
    
    .story-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #8b5cf6 0%, #ec4899 50%, #f59e0b 100%);
        box-shadow: 0 0 20px rgba(139, 92, 246, 0.5);
    }
    
    .story-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #f3f4f6 !important;
        margin-bottom: 1rem;
        text-shadow: 0 0 10px rgba(139, 92, 246, 0.3);
    }
    
    .story-text {
        font-size: 1.1rem;
        line-height: 1.8;
        color: #d1d5db !important;
        margin-bottom: 1rem;
    }
    
    /* Badge styling */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.875rem;
        font-weight: 600;
        margin: 0.25rem;
    }
    
    .badge-success {
        background-color: #10b981;
        color: white;
    }
    
    .badge-warning {
        background-color: #f59e0b;
        color: white;
    }
    
    .badge-danger {
        background-color: #ef4444;
        color: white;
    }
    
    .badge-info {
        background-color: #3b82f6;
        color: white;
    }
    
    /* Beautiful step styling - DARK THEME */
    .step-number {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 48px;
        height: 48px;
        border-radius: 50%;
        background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%);
        color: white;
        font-weight: 800;
        font-size: 1.3rem;
        margin-right: 1rem;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.5), 0 0 20px rgba(139, 92, 246, 0.3);
        transition: all 0.3s ease;
    }
    
    .step-number:hover {
        transform: scale(1.1) rotate(5deg);
        box-shadow: 0 6px 25px rgba(139, 92, 246, 0.7), 0 0 30px rgba(139, 92, 246, 0.5);
    }
    
    
    /* Beautiful file uploader - DARK THEME */
    .uploadedFile {
        border-radius: 16px;
        border: 2px dashed rgba(139, 92, 246, 0.4);
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(236, 72, 153, 0.1) 100%);
        padding: 2rem;
        transition: all 0.3s ease;
        box-shadow: 0 0 20px rgba(139, 92, 246, 0.2);
    }
    
    .uploadedFile:hover {
        border-color: rgba(139, 92, 246, 0.7);
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(236, 72, 153, 0.2) 100%);
        box-shadow: 0 0 30px rgba(139, 92, 246, 0.4);
    }
    
    /* Beautiful expanders - DARK THEME */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(236, 72, 153, 0.15) 100%) !important;
        border-radius: 12px;
        padding: 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        color: #f3f4f6 !important;
        border: 1px solid rgba(139, 92, 246, 0.3) !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.25) 0%, rgba(236, 72, 153, 0.25) 100%) !important;
        border-color: rgba(139, 92, 246, 0.5) !important;
        box-shadow: 0 0 20px rgba(139, 92, 246, 0.3);
    }
    
    /* Expander content - dark */
    .streamlit-expanderContent {
        background: #1a1a1a !important;
        color: #e5e7eb !important;
        border: 1px solid rgba(139, 92, 246, 0.2) !important;
        border-radius: 12px;
        margin-top: 0.5rem;
    }
    
    /* Beautiful metrics - DARK THEME */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #a78bfa 0%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 0 5px rgba(167, 139, 250, 0.4));
    }
    
    [data-testid="stMetricLabel"] {
        color: #d1d5db !important;
    }
    
    [data-testid="stMetricDelta"] {
        color: #a78bfa !important;
    }
    
    /* Beautiful info boxes - DARK THEME */
    .stAlert {
        border-radius: 16px;
        border-left: 4px solid;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
        background: #1a1a1a !important;
        color: #e5e7eb !important;
    }
    
    /* Beautiful section headers - DARK THEME */
    h2 {
        background: linear-gradient(135deg, #a78bfa 0%, #f472b6 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        font-weight: 800 !important;
        font-size: 2.2rem !important;
        margin-top: 2rem !important;
        margin-bottom: 1.5rem !important;
        display: block !important;
        filter: drop-shadow(0 0 10px rgba(167, 139, 250, 0.4));
    }
    
    h3 {
        color: #f3f4f6 !important;
        font-weight: 700 !important;
        font-size: 1.6rem !important;
        margin-top: 1.5rem !important;
        margin-bottom: 1rem !important;
        display: block !important;
        text-shadow: 0 0 10px rgba(139, 92, 246, 0.3);
    }
    
    h4 {
        color: #e5e7eb !important;
        font-weight: 600 !important;
    }
    
    /* Hide Streamlit default elements but keep content visible */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    /* Make header transparent but keep functionality */
    header {background: rgba(255,255,255,0.1) !important;}
    
    /* Ensure all content is visible */
    .main .block-container {
        visibility: visible !important;
        opacity: 1 !important;
        display: block !important;
    }
    
    /* Ensure all markdown content is visible - DARK THEME */
    .stMarkdown {
        visibility: visible !important;
        opacity: 1 !important;
        color: #e5e7eb !important;
    }
    
    .stMarkdown * {
        visibility: visible !important;
        opacity: 1 !important;
        color: #e5e7eb !important;
    }
    
    .stMarkdown strong {
        color: #f3f4f6 !important;
    }
    
    .stMarkdown em {
        color: #d1d5db !important;
    }
    
    /* Make columns visible */
    [data-testid="column"] {
        visibility: visible !important;
        opacity: 1 !important;
        background: transparent !important;
    }
    
    /* Make buttons super visible */
    button {
        visibility: visible !important;
        opacity: 1 !important;
    }
    
    /* Dataframes - dark theme */
    .dataframe {
        background: #1a1a1a !important;
        color: #e5e7eb !important;
    }
    
    /* Captions and labels */
    .stCaption {
        color: #9ca3af !important;
    }
    
    /* Code blocks - dark theme */
    code {
        background: #1a1a1a !important;
        color: #a78bfa !important;
        border: 1px solid rgba(139, 92, 246, 0.3) !important;
        padding: 0.25rem 0.5rem !important;
        border-radius: 4px !important;
    }
    
    pre {
        background: #1a1a1a !important;
        color: #e5e7eb !important;
        border: 1px solid rgba(139, 92, 246, 0.3) !important;
        border-radius: 8px !important;
    }
    
    /* Dividers */
    hr {
        border-color: rgba(139, 92, 246, 0.3) !important;
    }
    
    /* Tables */
    table {
        background: #1a1a1a !important;
        color: #e5e7eb !important;
        border: 1px solid rgba(139, 92, 246, 0.3) !important;
    }
    
    th {
        background: rgba(139, 92, 246, 0.2) !important;
        color: #f3f4f6 !important;
        border: 1px solid rgba(139, 92, 246, 0.3) !important;
    }
    
    td {
        border: 1px solid rgba(139, 92, 246, 0.2) !important;
        color: #e5e7eb !important;
    }
    
    /* Sidebar styling - DARK THEME */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0a0a 0%, #000000 100%) !important;
        border-right: 2px solid rgba(139, 92, 246, 0.3) !important;
        color: #e5e7eb !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #e5e7eb !important;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4 {
        color: #f3f4f6 !important;
    }
    
    /* Make all Streamlit widgets visible - DARK THEME */
    .stSelectbox, .stTextInput, .stTextArea, .stCheckbox, .stRadio {
        visibility: visible !important;
        opacity: 1 !important;
        background: #1a1a1a !important;
        color: #e5e7eb !important;
        border: 1px solid rgba(139, 92, 246, 0.3) !important;
    }
    
    /* Beautiful success/info/warning boxes - DARK THEME */
    .stSuccess {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(5, 150, 105, 0.2) 100%) !important;
        border-left: 4px solid #10b981 !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        color: #d1fae5 !important;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.3);
    }
    
    .stInfo {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(236, 72, 153, 0.2) 100%) !important;
        border-left: 4px solid #8b5cf6 !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        color: #e9d5ff !important;
        box-shadow: 0 0 20px rgba(139, 92, 246, 0.3);
    }
    
    .stWarning {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.2) 0%, rgba(217, 119, 6, 0.2) 100%) !important;
        border-left: 4px solid #f59e0b !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        color: #fef3c7 !important;
        box-shadow: 0 0 20px rgba(245, 158, 11, 0.3);
    }
    
    .stError {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(220, 38, 38, 0.2) 100%) !important;
        border-left: 4px solid #ef4444 !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        color: #fee2e2 !important;
        box-shadow: 0 0 20px rgba(239, 68, 68, 0.3);
    }
    
    /* Markdown text in sidebar */
    [data-testid="stSidebar"] .stMarkdown {
        color: #d1d5db !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown strong {
        color: #f3f4f6 !important;
    }
    </style>
    """, unsafe_allow_html=True)


def create_story_section(title: str, content: str, icon: str = "📊"):
    """Create a beautifully styled story section."""
    st.markdown(f"""
    <div class="story-section">
        <div class="story-title">{icon} {title}</div>
        <div class="story-text">{content}</div>
    </div>
    """, unsafe_allow_html=True)


def create_info_box(content: str, type: str = "info"):
    """Create an info box with different types."""
    if type == "info":
        st.info(f"💡 {content}")
    elif type == "success":
        st.success(f"✅ {content}")
    elif type == "warning":
        st.warning(f"⚠️ {content}")
    elif type == "error":
        st.error(f"❌ {content}")


def format_quality_score_explanation(score: float) -> str:
    """Generate a narrative explanation of the quality score."""
    if score >= 90:
        return f"🎉 **Excellent!** Your dataset has a quality score of {score:.1f}/100. This means your data is in great shape and ready for analysis. You can proceed with confidence knowing that the data is complete, consistent, and accurate."
    elif score >= 80:
        return f"✅ **Good!** Your dataset has a quality score of {score:.1f}/100. The data is generally reliable, but there are some minor issues that could be addressed to improve analysis accuracy. Review the recommendations below for optimization."
    elif score >= 60:
        return f"⚠️ **Fair.** Your dataset has a quality score of {score:.1f}/100. While the data is usable, there are several issues that should be addressed before performing detailed analysis. The recommendations below will help you improve data quality."
    else:
        return f"🔴 **Needs Attention.** Your dataset has a quality score of {score:.1f}/100. There are significant data quality issues that should be resolved before analysis. Please review the issues and recommendations carefully."


def create_data_story_summary(df: pd.DataFrame, schema: Dict[str, Any], 
                              quality_report: Dict[str, Any], 
                              insights: List[Dict[str, Any]]) -> str:
    """Create a narrative summary of the data story."""
    story_parts = []
    
    # Introduction
    story_parts.append(f"## 📖 Your Data Story\n\n")
    story_parts.append(f"Welcome to your data analysis journey! Let's explore what your dataset tells us.\n\n")
    
    # Dataset overview
    story_parts.append(f"### 📊 Dataset Overview\n\n")
    story_parts.append(f"Your dataset contains **{len(df):,} records** across **{len(df.columns)} different attributes**. ")
    
    # Schema story
    id_cols = len(schema.get('id_columns', []))
    num_cols = len(schema.get('numeric_columns', []))
    cat_cols = len(schema.get('categorical_columns', []))
    date_cols = len(schema.get('datetime_columns', []))
    
    story_parts.append(f"We've identified {id_cols} identifier columns, {num_cols} numeric metrics, {cat_cols} categorical dimensions, and {date_cols} time-based columns. ")
    
    # Quality story
    quality_score = quality_report.get('overall_score', 0)
    story_parts.append(f"\n### 🔍 Data Quality Assessment\n\n")
    story_parts.append(format_quality_score_explanation(quality_score))
    story_parts.append("\n\n")
    
    # Key insights story
    high_priority_insights = [i for i in insights if i.get('priority', 0) >= 7]
    if high_priority_insights:
        story_parts.append(f"### 💡 Key Discoveries\n\n")
        story_parts.append(f"We've uncovered **{len(high_priority_insights)} critical insights** that deserve your attention:\n\n")
        for i, insight in enumerate(high_priority_insights[:5], 1):
            story_parts.append(f"{i}. **{insight.get('title', 'Insight')}**: {insight.get('message', '')}\n\n")
    
    # Recommendations
    recommendations = quality_report.get('recommendations', [])
    if recommendations:
        story_parts.append(f"### 🎯 Next Steps\n\n")
        story_parts.append("Based on our analysis, here are the recommended actions:\n\n")
        for i, rec in enumerate(recommendations[:5], 1):
            story_parts.append(f"{i}. {rec}\n\n")
    
    return "".join(story_parts)


def create_insight_card(insight: Dict[str, Any]):
    """Create a beautiful insight card using Streamlit components - DARK THEME."""
    severity = insight.get('severity', 'low')
    title = insight.get('title', 'Insight')
    message = insight.get('message', '')
    metric_value = insight.get('metric_value', '')
    recommendations = insight.get('recommendations', [])
    
    # Choose icon and colors based on severity - DARK THEME
    if severity == 'high':
        icon = "🔴"
        color = "#ef4444"
        bg_color = "rgba(239, 68, 68, 0.2)"
        text_color = "#fee2e2"
        border_glow = "0 0 20px rgba(239, 68, 68, 0.4)"
    elif severity == 'medium':
        icon = "🟡"
        color = "#f59e0b"
        bg_color = "rgba(245, 158, 11, 0.2)"
        text_color = "#fef3c7"
        border_glow = "0 0 20px rgba(245, 158, 11, 0.4)"
    else:
        icon = "🟢"
        color = "#10b981"
        bg_color = "rgba(16, 185, 129, 0.2)"
        text_color = "#d1fae5"
        border_glow = "0 0 20px rgba(16, 185, 129, 0.4)"
    
    # Create card using Streamlit columns and markdown - DARK THEME
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {bg_color} 0%, rgba(26, 26, 26, 0.8) 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.6), {border_glow};
        border-left: 4px solid {color};
        border: 2px solid {color}33;
    ">
        <h4 style="color: {text_color}; margin-bottom: 0.5rem; text-shadow: 0 0 10px {color}66;">{icon} {title}</h4>
        <p style="color: #e5e7eb; line-height: 1.6; margin-bottom: 0.5rem;">{message}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show metric value if available
    if metric_value:
        st.markdown(f"<p style='color: #9ca3af; font-size: 0.9rem;'><strong>Metric:</strong> {metric_value}</p>", unsafe_allow_html=True)
    
    # Show recommendations as bullet points using Streamlit
    if recommendations:
        st.markdown("**Recommendations:**")
        for rec in recommendations:
            st.markdown(f"• {rec}")


def main():
    # Header with gradient
    st.markdown('<h1 class="main-header">🚀 AutoKPI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Transform Your Data into Compelling Stories & Actionable Insights</p>', 
                unsafe_allow_html=True)
    
    # Welcome message
    create_story_section(
        "Welcome to Your Data Journey",
        "AutoKPI doesn't just analyze your data—it tells its story. We'll guide you through understanding your data's quality, discovering hidden patterns, and uncovering insights that drive decisions. Every number has a story, and we're here to help you understand what your data is trying to tell you.",
        "🎯"
    )
    
    # Sidebar with beautiful dark theme styling
    with st.sidebar:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.3) 0%, rgba(236, 72, 153, 0.3) 100%);
            padding: 2rem;
            border-radius: 20px;
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: 0 8px 32px rgba(139, 92, 246, 0.4), 0 0 40px rgba(139, 92, 246, 0.2);
            border: 2px solid rgba(139, 92, 246, 0.5);
        ">
            <h2 style="color: #f3f4f6; margin: 0; font-size: 1.8rem; font-weight: 800; text-shadow: 0 0 10px rgba(167, 139, 250, 0.5);">⚙️ Control Panel</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Reset button
        if st.button("🔄 Reset All Data", use_container_width=True, type="secondary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        st.markdown("---")
        
        st.markdown("### 📚 About")
        st.markdown("""
        **AutoKPI** is a comprehensive analytics toolkit that provides:
        
        🔍 **Data Quality Assessment**
        - Completeness, uniqueness, consistency checks
        - Data quality scoring
        
        📊 **Advanced Analytics**
        - Statistical analysis & distributions
        - Correlation analysis
        - Trend detection
        - Outlier detection
        
        🎯 **Auto-Generated KPIs**
        - Aggregation, time-series, category breakdowns
        - Advanced metrics (percentiles, ratios, growth rates)
        
        💡 **Auto-Insights**
        - Natural language insights
        - Recommendations
        - Key findings
        
        📈 **Visualizations**
        - Interactive charts
        - Correlation heatmaps
        - Distribution plots
        
        💾 **Exports**
        - JSON, Markdown, Dashboard Spec
        """)
    
    # File upload with beautiful design
    st.markdown("---")
    st.markdown("## 📤 Step 1: Upload Your Dataset")
    
    create_story_section(
        "Start Your Analysis Journey",
        "Upload your dataset to begin. We support CSV and Excel files. Once uploaded, we'll automatically analyze your data structure, assess quality, discover patterns, and generate comprehensive insights—all in seconds!",
        "🚀"
    )
    
    # Example datasets section - DARK THEME
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(236, 72, 153, 0.2) 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        border: 2px solid rgba(139, 92, 246, 0.4);
        box-shadow: 0 8px 32px rgba(139, 92, 246, 0.3), 0 0 40px rgba(139, 92, 246, 0.2);
    ">
        <h3 style="color: #a78bfa; font-size: 1.8rem; margin-bottom: 1rem; text-align: center; text-shadow: 0 0 10px rgba(167, 139, 250, 0.5);">
            🎯 Try Example Datasets
        </h3>
        <p style="text-align: center; font-size: 1.1rem; color: #d1d5db; margin-bottom: 1.5rem;">
            Want to see AutoKPI in action? Click any dataset below to get started instantly!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    example_col1, example_col2, example_col3 = st.columns(3)
    
    with example_col1:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h4 style="color: #f3f4f6; margin-bottom: 0.5rem; text-shadow: 0 0 5px rgba(167, 139, 250, 0.3);">🚗 BMW Sales</h4>
            <p style="color: #9ca3af; font-size: 0.9rem; margin-bottom: 1rem;">Sales data 2010-2024</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚗 Load BMW Sales Data", use_container_width=True, type="primary", key="bmw_button"):
            example_path = "example_data/BMW sales data (2010-2024).csv"
            if os.path.exists(example_path):
                df_temp = pd.read_csv(example_path)
                st.session_state['df'] = df_temp
                st.session_state['file_name'] = "BMW sales data (2010-2024).csv"
                # Clear previous analysis
                for key in ['schema', 'quality_report', 'statistical_summary', 'insights', 'kpis', 'sql_queries', 'grouped_insights']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
    
    with example_col2:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h4 style="color: #f3f4f6; margin-bottom: 0.5rem; text-shadow: 0 0 5px rgba(167, 139, 250, 0.3);">🎓 Students Performance</h4>
            <p style="color: #9ca3af; font-size: 0.9rem; margin-bottom: 1rem;">Test scores & demographics</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🎓 Load Students Data", use_container_width=True, type="primary", key="students_button"):
            example_path = "example_data/StudentsPerformance.csv"
            if os.path.exists(example_path):
                df_temp = pd.read_csv(example_path)
                st.session_state['df'] = df_temp
                st.session_state['file_name'] = "StudentsPerformance.csv"
                # Clear previous analysis
                for key in ['schema', 'quality_report', 'statistical_summary', 'insights', 'kpis', 'sql_queries', 'grouped_insights']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
    
    with example_col3:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h4 style="color: #f3f4f6; margin-bottom: 0.5rem; text-shadow: 0 0 5px rgba(167, 139, 250, 0.3);">📦 Sample Orders</h4>
            <p style="color: #9ca3af; font-size: 0.9rem; margin-bottom: 1rem;">E-commerce order data</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📦 Load Orders Data", use_container_width=True, type="primary", key="orders_button"):
            example_path = "example_data/orders.csv"
            if os.path.exists(example_path):
                df_temp = pd.read_csv(example_path)
                st.session_state['df'] = df_temp
                st.session_state['file_name'] = "orders.csv"
                # Clear previous analysis
                for key in ['schema', 'quality_report', 'statistical_summary', 'insights', 'kpis', 'sql_queries', 'grouped_insights']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1rem; margin: 2rem 0;">
        <h3 style="color: #a78bfa; font-size: 1.5rem; margin-bottom: 0.5rem; text-shadow: 0 0 10px rgba(167, 139, 250, 0.4);">OR</h3>
        <p style="color: #9ca3af; font-size: 1rem;">Upload your own dataset below</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "📁 Upload Your Own CSV or Excel File",
        type=['csv', 'xlsx', 'xls'],
        help="💡 Supported formats: CSV, Excel (.xlsx, .xls). Maximum file size: 200MB"
    )
    
    # Check if we have a dataset in session state (from example buttons)
    if 'df' in st.session_state and 'file_name' in st.session_state:
        # We have a dataset loaded from example button
        df = st.session_state['df']
        uploaded_file = type('obj', (object,), {'name': st.session_state['file_name']})()
    elif uploaded_file is None:
        st.markdown("### 👆 Ready to Get Started?")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### 📋 What You Can Analyze
            
            AutoKPI works with any dataset containing:
            - **Identifiers**: user_id, order_id, customer_id
            - **Dates**: order_date, created_at, timestamp
            - **Categories**: country, status, product_type
            - **Metrics**: revenue, quantity, price, score
            
            #### 💡 Example Use Cases
            - Sales and revenue analysis
            - Customer behavior insights
            - Product performance metrics
            - Marketing campaign analysis
            - Operational KPIs
            """)
        
        with col2:
            st.markdown("""
            #### 🎯 What You'll Get
            
            After uploading, you'll receive:
            - **Data Quality Score**: Health assessment
            - **Correlation Analysis**: Variable relationships
            - **Auto-Generated Insights**: Key discoveries
            - **30-100+ KPIs**: Comprehensive metrics
            - **SQL Queries**: Ready-to-use code
            - **Visualizations**: Interactive charts
            - **Export Options**: JSON, Markdown, Dashboard Spec
            
            #### 📊 Try It Now!
            
            Upload your dataset above to see the magic happen! 🪄
            """)
        
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(236, 72, 153, 0.2) 100%);
            padding: 2rem;
            border-radius: 16px;
            border-left: 4px solid #8b5cf6;
            margin: 2rem 0;
            box-shadow: 0 0 30px rgba(139, 92, 246, 0.3);
        ">
            <h4 style="color: #a78bfa; margin-bottom: 1rem; text-shadow: 0 0 10px rgba(167, 139, 250, 0.4);">💡 Quick Start Tips</h4>
            <ul style="color: #d1d5db; line-height: 2;">
                <li>Click any example dataset above to see AutoKPI in action instantly</li>
                <li>Or upload your own CSV/Excel file to analyze your data</li>
                <li>AutoKPI will automatically detect patterns, generate KPIs, and provide insights</li>
                <li>Use the Reset button in the sidebar to clear and start over</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Load dataset (if not already loaded from example button)
    if 'df' not in st.session_state or (hasattr(uploaded_file, 'name') and uploaded_file.name != st.session_state.get('file_name', '')):
        try:
            if hasattr(uploaded_file, 'read'):
                # It's a file uploader object
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
            else:
                # It's from session state, already loaded
                df = st.session_state.get('df')
                if df is None:
                    st.error("❌ Error: Dataset not found. Please upload a file or select an example dataset.")
                    return
            
            # Store in session state
            # Clear previous analysis when new file is uploaded
            for key in ['schema', 'quality_report', 'statistical_summary', 'insights', 'kpis', 'sql_queries', 'grouped_insights']:
                if key in st.session_state:
                    del st.session_state[key]
            
            st.session_state['df'] = df
            if hasattr(uploaded_file, 'name'):
                st.session_state['file_name'] = uploaded_file.name
            
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, rgba(16, 185, 129, 0.25) 0%, rgba(5, 150, 105, 0.25) 100%);
                padding: 1.5rem;
                border-radius: 16px;
                border-left: 4px solid #10b981;
                margin: 1.5rem 0;
                box-shadow: 0 4px 20px rgba(16, 185, 129, 0.4), 0 0 30px rgba(16, 185, 129, 0.2);
                border: 2px solid rgba(16, 185, 129, 0.3);
            ">
                <h3 style="color: #6ee7b7; margin: 0; font-size: 1.5rem; font-weight: 700; text-shadow: 0 0 10px rgba(16, 185, 129, 0.5);">
                    ✅ Dataset Loaded Successfully!
                </h3>
                <p style="color: #a7f3d0; margin: 0.5rem 0 0 0; font-size: 1.1rem; font-weight: 600;">
                    📊 {len(df):,} rows × {len(df.columns)} columns
                </p>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"❌ Error loading dataset: {str(e)}")
            return
    else:
        df = st.session_state['df']
    
    # Data preview
    with st.expander("📋 Data Preview (Top 50 rows)", expanded=False):
        st.dataframe(df.head(50), use_container_width=True)
    
    # Schema inference with storytelling
    st.markdown("---")
    st.markdown("## 🔍 Step 2: Understanding Your Data Structure")
    
    create_story_section(
        "Getting to Know Your Data",
        "Every dataset tells a story, and the first step is understanding its structure. We automatically analyze your columns to identify identifiers, dates, categories, numbers, and text. This helps us generate the right types of insights and KPIs for your specific data.",
        "📚"
    )
    
    if 'schema' not in st.session_state or st.session_state.get('file_name') != uploaded_file.name:
        with st.spinner("🔍 Analyzing your data structure and column types..."):
            schema = infer_schema(df)
            schema_summary = get_schema_summary(df, schema)
            st.session_state['schema'] = schema
            st.session_state['schema_summary'] = schema_summary
    
    schema = st.session_state['schema']
    schema_summary = st.session_state['schema_summary']
    
    # Display schema with narrative
    st.markdown("### 📊 Your Data Structure")
    st.markdown("Here's what we discovered about your dataset:")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        id_count = len(schema['id_columns'])
        st.metric("ID Columns", id_count, 
                 help="Unique identifiers like user_id, order_id, etc.")
    
    with col2:
        date_count = len(schema['datetime_columns'])
        st.metric("Date Columns", date_count,
                 help="Time-based columns for trend analysis")
    
    with col3:
        cat_count = len(schema['categorical_columns'])
        st.metric("Categories", cat_count,
                 help="Grouping dimensions like country, status, etc.")
    
    with col4:
        num_count = len(schema['numeric_columns'])
        st.metric("Metrics", num_count,
                 help="Numbers we can measure and analyze")
    
    with col5:
        text_count = len(schema['text_columns'])
        st.metric("Text Columns", text_count,
                 help="Descriptive text fields")
    
    # Narrative explanation
    if num_count > 0 and cat_count > 0:
        st.success(f"✨ Great! We found {num_count} metric columns and {cat_count} category columns. This means we can analyze how metrics vary across different categories—perfect for insights!")
    elif num_count > 0:
        st.info(f"💡 We found {num_count} metric columns. We can analyze trends, averages, and distributions for these metrics.")
    elif cat_count > 0:
        st.info(f"💡 We found {cat_count} category columns. We can analyze distributions and patterns across these categories.")
    
    # Detailed schema view
    with st.expander("📊 Detailed Schema", expanded=False):
        if schema['id_columns']:
            st.subheader("🆔 ID Columns")
            for col_info in schema_summary['id_columns']:
                st.write(f"**{col_info['name']}**: {col_info['dtype']} ({col_info['unique_count']} unique values)")
        
        if schema['datetime_columns']:
            st.subheader("📅 Datetime Columns")
            for col_info in schema_summary['datetime_columns']:
                st.write(f"**{col_info['name']}**: {col_info['dtype']}")
                if col_info.get('min') and col_info.get('max'):
                    st.write(f"  Range: {col_info['min']} to {col_info['max']}")
        
        if schema['categorical_columns']:
            st.subheader("🏷️ Categorical Columns")
            for col_info in schema_summary['categorical_columns']:
                st.write(f"**{col_info['name']}**: {col_info['dtype']} ({col_info['unique_count']} unique values)")
                if col_info.get('top_values'):
                    st.write(f"  Top values: {', '.join(list(col_info['top_values'].keys())[:5])}")
        
        if schema['numeric_columns']:
            st.subheader("🔢 Numeric Columns")
            for col_info in schema_summary['numeric_columns']:
                st.write(f"**{col_info['name']}**: {col_info['dtype']}")
                if col_info.get('min') is not None and col_info.get('max') is not None:
                    st.write(f"  Range: {col_info['min']:.2f} to {col_info['max']:.2f}, Mean: {col_info.get('mean', 0):.2f}")
        
        if schema['text_columns']:
            st.subheader("📝 Text Columns")
            for col_info in schema_summary['text_columns']:
                st.write(f"**{col_info['name']}**: {col_info['dtype']} (avg length: {col_info.get('avg_length', 0):.1f} chars)")
    
    # Data Quality Assessment with Storytelling
    st.markdown("---")
    st.markdown("## 🔍 Step 3: Understanding Your Data's Health")
    
    create_story_section(
        "Why Data Quality Matters",
        "Before we dive into insights, let's understand the health of your data. Just like a doctor checks vital signs, we assess your data's completeness, uniqueness, consistency, and accuracy. This helps us understand how reliable our findings will be.",
        "🏥"
    )
    
    if 'quality_report' not in st.session_state or st.session_state.get('file_name') != uploaded_file.name:
        with st.spinner("🔍 Analyzing your data's health and quality..."):
            quality_report = check_data_quality(df, schema)
            st.session_state['quality_report'] = quality_report
    
    quality_report = st.session_state['quality_report']
    
    # Quality Score with narrative
    overall_score = quality_report.get('overall_score', 0)
    st.markdown("### 📊 Overall Data Quality Score")
    
    # Create a visual score display
    col1, col2 = st.columns([1, 2])
    with col1:
        score_color = "🟢" if overall_score >= 80 else "🟡" if overall_score >= 60 else "🔴"
        st.metric("Quality Score", f"{score_color} {overall_score:.1f}/100", 
                 delta=f"{'Excellent' if overall_score >= 90 else 'Good' if overall_score >= 80 else 'Fair' if overall_score >= 60 else 'Needs Work'}")
    
    with col2:
        st.markdown(format_quality_score_explanation(overall_score))
    
    # Quality Dimensions with explanations
    st.markdown("### 📈 Quality Dimensions Breakdown")
    st.markdown("Let's break down what makes up your quality score:")
    
    dimensions = quality_report.get('dimensions', {})
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        completeness = dimensions.get('completeness', {}).get('score', 0)
        st.metric("Completeness", f"{completeness:.1f}%", 
                 help="Measures how much of your data is complete (no missing values)")
    
    with col2:
        uniqueness = dimensions.get('uniqueness', {}).get('score', 0)
        st.metric("Uniqueness", f"{uniqueness:.1f}%",
                 help="Measures how unique your records are (no duplicates)")
    
    with col3:
        consistency = dimensions.get('consistency', {}).get('score', 0)
        st.metric("Consistency", f"{consistency:.1f}%",
                 help="Measures data type and format consistency")
    
    with col4:
        validity = dimensions.get('validity', {}).get('score', 0)
        st.metric("Validity", f"{validity:.1f}%",
                 help="Measures if data values are within expected ranges")
    
    with col5:
        accuracy = dimensions.get('accuracy', {}).get('score', 0)
        st.metric("Accuracy", f"{accuracy:.1f}%",
                 help="Measures data accuracy (outlier detection)")
    
    # Quality Issues and Recommendations with storytelling
    st.markdown("### 🔎 Detailed Quality Assessment")
    
    issues = quality_report.get('issues', [])
    if issues:
        create_story_section(
            "Issues We Found",
            f"We discovered {len(issues)} data quality issues in your dataset. Don't worry—these are common and can often be addressed. Let's review them:",
            "⚠️"
        )
        
        high_issues = [i for i in issues if i.get('severity') == 'high']
        medium_issues = [i for i in issues if i.get('severity') == 'medium']
        low_issues = [i for i in issues if i.get('severity') == 'low']
        
        if high_issues:
            st.markdown("#### 🔴 High Priority Issues")
            for issue in high_issues[:5]:
                st.error(f"**{issue.get('type', 'Unknown')}**: {issue.get('message', '')}")
        
        if medium_issues:
            st.markdown("#### 🟡 Medium Priority Issues")
            for issue in medium_issues[:5]:
                st.warning(f"**{issue.get('type', 'Unknown')}**: {issue.get('message', '')}")
        
        if low_issues:
            with st.expander("🟢 Low Priority Issues", expanded=False):
                for issue in low_issues[:5]:
                    st.info(f"**{issue.get('type', 'Unknown')}**: {issue.get('message', '')}")
    
    recommendations = quality_report.get('recommendations', [])
    if recommendations:
        create_story_section(
            "💡 How to Improve Your Data",
            "Based on our analysis, here are actionable steps you can take to improve your data quality:",
            "🚀"
        )
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"{i}. {rec}")
    
    # Advanced Analytics with storytelling
    st.markdown("---")
    st.markdown("## 📊 Step 4: Discovering Hidden Patterns")
    
    create_story_section(
        "Finding Connections in Your Data",
        "Now comes the exciting part—uncovering hidden patterns and relationships. We'll analyze correlations between variables, detect trends over time, and identify statistical patterns. These insights help you understand not just what your data says, but why it matters.",
        "🔬"
    )
    
    if 'statistical_summary' not in st.session_state or st.session_state.get('file_name') != uploaded_file.name:
        with st.spinner("🔬 Analyzing patterns, correlations, and statistical relationships..."):
            statistical_summary = generate_statistical_summary(df, schema)
            st.session_state['statistical_summary'] = statistical_summary
    
    statistical_summary = st.session_state['statistical_summary']
    
    # Correlation Analysis with narrative
    numeric_cols = schema.get('numeric_columns', [])
    if len(numeric_cols) >= 2:
        st.markdown("### 🔗 Correlation Analysis")
        st.markdown("Correlations reveal how variables move together. Strong correlations (close to +1 or -1) indicate that when one variable changes, the other tends to change in a predictable way. This can reveal hidden relationships and help you understand what drives your metrics.")
        
        corr_matrix = calculate_correlations(df, numeric_cols)
        if not corr_matrix.empty:
            # Create correlation heatmap - only show upper triangle to avoid redundancy
            corr_data = []
            for i, col1 in enumerate(corr_matrix.index):
                for j, col2 in enumerate(corr_matrix.columns):
                    # Only include upper triangle (including diagonal)
                    if i <= j:
                        corr_value = corr_matrix.loc[col1, col2]
                        corr_data.append({
                            'Variable 1': col1,
                            'Variable 2': col2,
                            'Correlation': corr_value
                        })
            
            corr_df = pd.DataFrame(corr_data)
            
            if len(corr_df) > 0:
                # Create a proper symmetric heatmap
                heatmap = alt.Chart(corr_df).mark_rect(stroke='white', strokeWidth=1).encode(
                    x=alt.X('Variable 1:O', title='', sort=alt.SortField(field='Variable 1', order='ascending')),
                    y=alt.Y('Variable 2:O', title='', sort=alt.SortField(field='Variable 2', order='ascending')),
                    color=alt.Color('Correlation:Q', 
                                  scale=alt.Scale(scheme='redblue', domain=[-1, 1]), 
                                  title='Correlation',
                                  legend=alt.Legend(title="Correlation", orient="right")),
                    tooltip=[
                        alt.Tooltip('Variable 1', title='Variable 1'),
                        alt.Tooltip('Variable 2', title='Variable 2'), 
                        alt.Tooltip('Correlation:Q', format='.3f', title='Correlation')
                    ]
                ).properties(
                    width=min(700, len(numeric_cols) * 100),
                    height=min(600, len(numeric_cols) * 100),
                    title='Correlation Heatmap - How Variables Move Together'
                )
                
                # Add text labels for correlation values
                text = heatmap.mark_text(baseline='middle', fontSize=10, fontWeight='bold').encode(
                    text=alt.Text('Correlation:Q', format='.2f'),
                    color=alt.condition(
                        alt.datum.Correlation > 0.5,
                        alt.value('white'),
                        alt.value('black')
                    )
                )
                
                st.altair_chart(heatmap + text, use_container_width=True)
            
            # Strong correlations
            strong_corrs = []
            for i, col1 in enumerate(numeric_cols):
                for col2 in numeric_cols[i+1:]:
                    if col1 in corr_matrix.index and col2 in corr_matrix.columns:
                        corr_value = corr_matrix.loc[col1, col2]
                        if abs(corr_value) > 0.7:
                            strong_corrs.append({
                                'Variables': f"{col1} ↔ {col2}",
                                'Correlation': f"{corr_value:.3f}",
                                'Strength': 'Strong' if abs(corr_value) > 0.8 else 'Moderate'
                            })
            
            if strong_corrs:
                st.write("**Strong Correlations (>0.7):**")
                st.dataframe(pd.DataFrame(strong_corrs), use_container_width=True)
    
    # Trend Analysis (if datetime columns exist)
    datetime_cols = schema.get('datetime_columns', [])
    if datetime_cols and numeric_cols:
        st.subheader("📈 Trend Analysis")
        datetime_col = datetime_cols[0]
        for num_col in numeric_cols[:2]:  # Analyze top 2 numeric columns
            trend = detect_trends(df, num_col, datetime_col)
            if trend:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(f"{num_col} Trend", trend.get('trend_direction', 'Unknown').title())
                with col2:
                    st.metric("R² Value", f"{trend.get('r_squared', 0):.3f}")
                with col3:
                    st.metric("Significance", "✅ Significant" if trend.get('is_significant') else "❌ Not Significant")
    
    # Auto-Insights with storytelling
    st.markdown("---")
    st.markdown("## 💡 Step 5: Key Insights & Discoveries")
    
    create_story_section(
        "What Your Data Is Telling You",
        "Based on our comprehensive analysis, we've uncovered key insights that matter. These aren't just numbers—they're actionable findings that can help you make better decisions. We've prioritized them so you can focus on what's most important.",
        "🎯"
    )
    
    if 'insights' not in st.session_state or st.session_state.get('file_name') != uploaded_file.name:
        with st.spinner("💡 Generating insights and discovering key patterns..."):
            # Generate KPIs first (needed for insights)
            if 'kpis' not in st.session_state:
                kpis = generate_kpis(schema, df)
                st.session_state['kpis'] = kpis
                # Also generate SQL queries
                sql_queries = generate_sql_queries(kpis, "your_table")
                st.session_state['sql_queries'] = sql_queries
                st.session_state['table_name'] = "your_table"
            else:
                kpis = st.session_state['kpis']
            
            insights = generate_insights(df, schema, kpis, quality_report, statistical_summary)
            grouped_insights = format_insights_for_display(insights)
            st.session_state['insights'] = insights
            st.session_state['grouped_insights'] = grouped_insights
    
    insights = st.session_state.get('insights', [])
    grouped_insights = st.session_state.get('grouped_insights', {})
    
    # Display high priority insights with beautiful cards
    high_priority = grouped_insights.get('high_priority', [])
    if high_priority:
        st.markdown("### 🎯 High Priority Insights")
        st.markdown(f"We've identified **{len(high_priority)} high-priority insights** that deserve your immediate attention:")
        
        for insight in high_priority[:5]:
            create_insight_card(insight)
    
    # Data Story Summary
    if insights:
        st.markdown("---")
        st.markdown("## 📖 Your Complete Data Story")
        data_story = create_data_story_summary(df, schema, quality_report, insights)
        st.markdown(data_story)
    
    # Display all insights by category
    with st.expander("📚 All Insights by Category", expanded=False):
        tab1, tab2, tab3 = st.tabs(["Quality", "Statistical", "Business"])
        
        with tab1:
            quality_insights = grouped_insights.get('quality', [])
            for insight in quality_insights:
                st.write(f"**{insight.get('title')}**")
                st.write(insight.get('message'))
                st.divider()
        
        with tab2:
            statistical_insights = grouped_insights.get('statistical', [])
            for insight in statistical_insights:
                st.write(f"**{insight.get('title')}**")
                st.write(insight.get('message'))
                if insight.get('metric_value'):
                    st.caption(f"Metric: {insight['metric_value']}")
                st.divider()
        
        with tab3:
            business_insights = grouped_insights.get('business', [])
            for insight in business_insights:
                st.write(f"**{insight.get('title')}**")
                st.write(insight.get('message'))
                if insight.get('recommendations'):
                    st.write("**Recommendations:**")
                    for rec in insight['recommendations']:
                        st.write(f"• {rec}")
                st.divider()
    
    # KPI generation with storytelling
    st.markdown("---")
    st.markdown("## 🎯 Step 6: Generate Key Performance Indicators")
    
    create_story_section(
        "Metrics That Matter",
        "KPIs (Key Performance Indicators) are the metrics that help you measure success. We automatically generate comprehensive KPIs tailored to your data, including aggregations, trends, category breakdowns, and advanced statistical metrics. Each KPI comes with SQL queries and visualizations ready to use.",
        "📈"
    )
    
    if st.button("🚀 Generate Comprehensive KPIs", type="primary", use_container_width=True):
        with st.spinner("Generating comprehensive KPIs and analytics..."):
            # Generate KPIs
            kpis = generate_kpis(schema, df)
            
            # Generate SQL queries
            sql_queries = generate_sql_queries(kpis, "your_table")
            
            # Store in session state
            st.session_state['kpis'] = kpis
            st.session_state['sql_queries'] = sql_queries
            st.session_state['table_name'] = "your_table"
        
        st.success(f"✅ Generated {len(kpis)} comprehensive KPIs!")
    
    # Display KPIs
    if 'kpis' in st.session_state:
        kpis = st.session_state['kpis']
        # Generate SQL queries if they don't exist
        if 'sql_queries' not in st.session_state:
            sql_queries = generate_sql_queries(kpis, "your_table")
            st.session_state['sql_queries'] = sql_queries
            st.session_state['table_name'] = "your_table"
        else:
            sql_queries = st.session_state['sql_queries']
        table_name = st.session_state.get('table_name', "your_table")
        
        st.markdown("---")
        st.markdown("## 📈 Step 7: Explore Your KPIs")
        
        create_story_section(
            "Your Performance Metrics",
            f"Excellent! We've generated **{len(kpis)} comprehensive KPIs** for your dataset. Each KPI tells part of your data's story. Click on any KPI to explore its SQL query, see a visualization, and understand what it means for your analysis.",
            "📊"
        )
        
        # KPI Summary with creative highlights
        kpi_categories = {}
        creative_kpis_list = []
        creative_categories = ['anomaly_detection', 'pattern_detection', 'comparative_analysis', 
                              'distribution_analysis', 'trend_analysis']
        
        for kpi in kpis:
            cat = kpi.get('category', 'other')
            kpi_categories[cat] = kpi_categories.get(cat, 0) + 1
            if cat in creative_categories:
                creative_kpis_list.append(kpi)
        
        # Creative KPIs Highlights
        if creative_kpis_list:
            st.markdown("### 🌟 Creative KPIs Highlights")
            create_story_section(
                "Discover Hidden Patterns",
                f"We've found **{len(creative_kpis_list)} creative KPIs** that reveal hidden patterns, anomalies, seasonality, and comparative insights in your data. These go beyond basic metrics to show you what's really happening in your dataset.",
                "🎯"
            )
            
            # Show top 3 creative KPIs as highlights
            for kpi in creative_kpis_list[:3]:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.markdown(f"**🌟 {kpi.get('name', 'KPI')}**")
                    st.markdown(f"*{kpi.get('description', '')[:150]}...*")
                    if kpi.get('insight'):
                        st.caption(f"💡 {kpi['insight']}")
                with col2:
                    if 'anomaly_percentage' in kpi:
                        st.metric("Anomaly Rate", f"{kpi['anomaly_percentage']:.1f}%")
                    elif 'top_performance_pct' in kpi:
                        st.metric("vs Avg", f"{kpi['top_performance_pct']:+.1f}%")
                    elif 'concentration_percentage' in kpi:
                        st.metric("Concentration", f"{kpi['concentration_percentage']:.1f}%")
                with col3:
                    st.markdown(f"**{kpi.get('category', 'unknown').replace('_', ' ').title()}**")
                st.divider()
        
        # KPI Overview
        st.markdown("### 📊 Complete KPI Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total KPIs", len(kpis), help="Total number of KPIs generated")
        with col2:
            st.metric("Creative KPIs", len(creative_kpis_list), 
                     delta=f"{len(creative_kpis_list)} pattern insights",
                     help="KPIs that reveal hidden patterns and insights")
        with col3:
            standard_kpis = len(kpis) - len(creative_kpis_list)
            st.metric("Standard KPIs", standard_kpis, help="Basic aggregation and breakdown KPIs")
        with col4:
            st.metric("Categories", len(kpi_categories), help="Number of KPI categories")
        
        # Category breakdown
        st.markdown("#### 📋 KPIs by Category")
        category_cols = st.columns(min(4, len(kpi_categories)))
        for idx, (cat, count) in enumerate(sorted(kpi_categories.items(), key=lambda x: x[1], reverse=True)):
            with category_cols[idx % len(category_cols)]:
                is_creative = cat in creative_categories
                icon = "🌟" if is_creative else "📊"
                st.markdown(f"{icon} **{cat.replace('_', ' ').title()}**: {count}")
        
        st.info(f"💡 **Pro Tip**: Creative KPIs (marked with 🌟) are auto-expanded and reveal hidden patterns. They help you discover insights you might not have noticed!")
        
        # Creative Ideas Section
        if creative_kpis_list:
            st.markdown("---")
            st.markdown("## 💡 Creative Ideas & Recommendations")
            
            create_story_section(
                "Turning Insights into Action",
                "Based on the creative KPIs we've discovered, here are actionable ideas and recommendations to help you make the most of your data insights:",
                "🚀"
            )
            
            try:
                from autokpi.creative_insights import generate_creative_ideas
                creative_ideas = generate_creative_ideas(kpis, df, schema)
                
                if creative_ideas:
                    for idea in creative_ideas[:5]:
                        priority_color = "🔴" if idea.get('priority') == 'high' else "🟡" if idea.get('priority') == 'medium' else "🟢"
                        st.markdown(f"### {priority_color} {idea.get('title', 'Idea')}")
                        st.markdown(idea.get('description', ''))
                        st.markdown(f"**💡 Action**: {idea.get('action', '')}")
                        st.divider()
            except Exception as e:
                pass
        
        # Group KPIs by category
        kpis_by_category = {}
        for kpi in kpis:
            category = kpi.get('category', 'other')
            if category not in kpis_by_category:
                kpis_by_category[category] = []
            kpis_by_category[category].append(kpi)
        
        # Display KPIs by category with enhanced visuals
        for category, category_kpis in kpis_by_category.items():
            # Special styling for creative KPI categories
            category_icons = {
                'anomaly_detection': '🔍',
                'pattern_detection': '📈',
                'comparative_analysis': '⚖️',
                'distribution_analysis': '📊',
                'trend_analysis': '📉',
                'aggregation': '🔢',
                'time_series': '⏰',
                'category_breakdown': '🏷️',
                'conversion': '🔄',
                'statistical': '📐',
                'ratio': '📏',
                'growth': '📈'
            }
            
            category_icon = category_icons.get(category, '📊')
            category_title = category.replace('_', ' ').title()
            
            # Special header for creative categories
            if category in ['anomaly_detection', 'pattern_detection', 'comparative_analysis', 
                           'distribution_analysis', 'trend_analysis']:
                st.markdown(f"### {category_icon} {category_title} KPIs - 🎯 Creative Insights")
                st.markdown(f"*These KPIs reveal hidden patterns, anomalies, and comparative insights that help you understand your data at a deeper level.*")
            else:
                st.markdown(f"### {category_icon} {category_title} KPIs")
            
            for i, kpi in enumerate(category_kpis):
                kpi_name = kpi.get('name', f'KPI {i+1}')
                kpi_description = kpi.get('description', '')
                chart_type = suggest_chart_type(kpi)
                sql_query = sql_queries.get(kpi_name, '')
                columns_used = kpi.get('columns_used', [])
                difficulty = kpi.get('difficulty', 'easy')
                refined_by_llm = kpi.get('refined_by_llm', False)
                insight = kpi.get('insight', '')
                
                # Determine if this is a creative/insightful KPI
                is_creative = category in ['anomaly_detection', 'pattern_detection', 
                                          'comparative_analysis', 'distribution_analysis', 'trend_analysis']
                
                # Create a more prominent expander for creative KPIs
                expander_title = f"{'🌟' if is_creative else '🔹'} {kpi_name}"
                if is_creative:
                    expander_title += " 🎯"
                
                with st.expander(expander_title, expanded=is_creative):  # Auto-expand creative KPIs
                    # Main content area - graph is most important
                    st.markdown(f"### {kpi_name}")
                    st.markdown(f"*{kpi_description}*")
                    
                    # Generate chart first (most important)
                    chart_col1, chart_col2 = st.columns([2, 1])
                    
                    # Initialize chart_explanation variable
                    chart_explanation = ""
                    
                    with chart_col1:
                        # Generate and show chart
                        chart = generate_chart(kpi, df, table_name)
                        if chart is not None:
                            st.altair_chart(chart, use_container_width=True)
                            
                            # Generate and display comprehensive chart explanation
                            try:
                                chart_explanation = generate_chart_explanation(kpi, df)
                                if chart_explanation:
                                    st.markdown("---")
                                    # Display the explanation with proper formatting
                                    st.markdown(chart_explanation)
                            except Exception as e:
                                # Fallback if explanation generation fails - show basic info
                                chart_explanation = ""
                                column = kpi.get('column')
                                group_by = kpi.get('group_by')
                                if column and column in df.columns:
                                    if group_by and group_by in df.columns:
                                        st.info(f"📊 This chart shows {column.replace('_', ' ').title()} grouped by {group_by.replace('_', ' ').title()}. Compare the bars to see which categories perform best.")
                                    else:
                                        st.info(f"📊 This chart displays the distribution of {column.replace('_', ' ').title()} values across your dataset.")
                        else:
                            # Fallback: try simple visualization
                            column = kpi.get('column')
                            if column and column in df.columns:
                                try:
                                    # Show metric value with context
                                    sql_function = kpi.get('sql_function', 'AVG')
                                    if sql_function == 'AVG':
                                        value = df[column].mean()
                                        st.metric(f"Average {column.replace('_', ' ').title()}", f"{value:,.2f}")
                                        st.caption(f"Range: {df[column].min():,.2f} - {df[column].max():,.2f}")
                                    
                                    # Try to create breakdown chart
                                    categorical_cols = [col for col in df.columns if col != column and (df[col].dtype == 'object' or df[col].dtype.name == 'category')]
                                    if categorical_cols:
                                        group_col = categorical_cols[0]
                                        chart_df = df.groupby(group_col)[column].mean().reset_index()
                                        chart_df.columns = [group_col, 'average']
                                        chart_df = chart_df.sort_values('average', ascending=False).head(10)
                                        
                                        simple_chart = alt.Chart(chart_df).mark_bar(color='#667eea').encode(
                                            x=alt.X('average:Q', title=f'Average {column.replace("_", " ").title()}'),
                                            y=alt.Y(f'{group_col}:N', title=group_col.replace('_', ' ').title(), sort='-x'),
                                            tooltip=[group_col, alt.Tooltip('average:Q', format='.2f')]
                                        ).properties(
                                            title=f'Average {column.replace("_", " ").title()} by {group_col.replace("_", " ").title()}',
                                            width=600,
                                            height=300
                                        )
                                        st.altair_chart(simple_chart, use_container_width=True)
                                        
                                        # Show data in writing
                                        st.info(f"📊 **Breakdown by {group_col.replace('_', ' ').title()}**: Top = {chart_df.iloc[0][group_col]} ({chart_df.iloc[0]['average']:,.2f}), Bottom = {chart_df.iloc[-1][group_col]} ({chart_df.iloc[-1]['average']:,.2f})")
                                except:
                                    st.info("📊 Chart preview generating...")
                    
                    with chart_col2:
                        # Show key metrics in sidebar
                        if is_creative:
                            if 'anomaly_percentage' in kpi:
                                st.metric("Anomaly Rate", f"{kpi['anomaly_percentage']:.1f}%")
                            if 'top_performance_pct' in kpi:
                                st.metric("vs Average", f"{kpi['top_performance_pct']:+.1f}%")
                            if 'gap_percentage' in kpi:
                                st.metric("Gap", f"{kpi['gap_percentage']:.1f}%")
                            if 'best_day' in kpi:
                                st.success(f"🏆 {kpi['best_day']}")
                            if 'concentration_percentage' in kpi:
                                st.warning(f"📊 {kpi['concentration_percentage']:.1f}%")
                            if 'change_percentage' in kpi:
                                change_icon = "📈" if kpi['change_percentage'] > 0 else "📉"
                                st.metric("Trend", f"{change_icon} {abs(kpi['change_percentage']):.1f}%")
                    
                    # Detailed insights section (only if chart explanation wasn't shown)
                    # Chart explanation already includes comprehensive details, so this section is for additional insights
                    if not chart_explanation or len(chart_explanation) < 100:
                        st.markdown("---")
                        st.markdown("#### 📖 Additional Insights")
                        
                        # Show insight if available
                        if insight:
                            st.info(f"💡 {insight}")
                        
                        # Generate and show creative insights
                        if is_creative:
                            try:
                                from autokpi.creative_insights import generate_kpi_insights
                                kpi_insights = generate_kpi_insights(kpi, df)
                                if kpi_insights:
                                    for insight_text in kpi_insights:
                                        st.markdown(insight_text)
                            except:
                                pass
                    else:
                        # Chart explanation was comprehensive, show additional creative insights if available
                        if is_creative:
                            st.markdown("---")
                            st.markdown("#### 💡 Actionable Recommendations")
                            try:
                                from autokpi.creative_insights import generate_kpi_insights
                                kpi_insights = generate_kpi_insights(kpi, df)
                                if kpi_insights:
                                    # Show only the action parts if available
                                    for insight_text in kpi_insights:
                                        if "💡 **The Action**" in insight_text or "Action" in insight_text:
                                            st.markdown(insight_text)
                            except:
                                pass
                    
                    # Technical details (collapsed)
                    with st.expander("🔧 Technical Details", expanded=False):
                        st.markdown(f"**Category:** {category_title}")
                        if columns_used:
                            st.markdown(f"**Columns Used:** {', '.join(columns_used)}")
                        st.markdown(f"**Chart Type:** {chart_type.replace('_', ' ').title()}")
                        if refined_by_llm:
                            st.success("✨ Refined by GPT-4")
                        
                        # SQL Query (hidden by default)
                        st.markdown("**SQL Query:**")
                        st.markdown("*Copy this SQL query to use in your database or BI tool:*")
                        st.code(sql_query, language='sql')
                    
                    # Next steps for creative KPIs
                    if is_creative:
                        st.markdown("---")
                        st.markdown("#### 🎯 Recommended Actions")
                        if category == 'anomaly_detection':
                            st.markdown("- Investigate outlier records to understand why they're different")
                            st.markdown("- Determine if outliers represent errors or exceptional cases")
                            st.markdown("- Consider creating separate analysis segments for outliers")
                        elif category == 'pattern_detection':
                            st.markdown("- Adjust scheduling and campaigns based on seasonal patterns")
                            st.markdown("- Allocate resources to peak periods")
                            st.markdown("- Plan inventory and staffing around identified patterns")
                        elif category == 'comparative_analysis':
                            st.markdown("- Study top performers to identify success factors")
                            st.markdown("- Develop strategies to improve underperformers")
                            st.markdown("- Create best practice guides from top performers")
                        elif category == 'distribution_analysis':
                            st.markdown("- Focus resources on high-value segments (Pareto principle)")
                            st.markdown("- Consider segmentation strategies for different tiers")
                            st.markdown("- Analyze what makes top performers different")
                        elif category == 'trend_analysis':
                            st.markdown("- Monitor trend direction and take action if declining")
                            st.markdown("- Scale successful strategies if trend is positive")
                            st.markdown("- Set up alerts for significant trend changes")
                    
                    st.divider()
        
        # Export section with storytelling
        st.markdown("---")
        st.markdown("## 💾 Step 8: Export Your Results")
        
        create_story_section(
            "Take Your Insights With You",
            "Export your analysis in multiple formats to use in other tools, share with your team, or integrate into your workflows. Choose the format that works best for your needs.",
            "📦"
        )
        
        st.markdown("### 📥 Export Options")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 📄 JSON Format")
            st.markdown("Perfect for developers and API integrations. Contains all KPI definitions, SQL queries, and metadata in a structured format.")
            json_export = export_to_json(kpis, schema, table_name)
            st.download_button(
                label="📄 Download JSON",
                data=json_export,
                file_name=f"kpis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col2:
            st.markdown("#### 📝 Markdown Format")
            st.markdown("Ideal for documentation and reports. Includes formatted KPI descriptions, SQL queries, and can be used in GitHub, Confluence, or documentation tools.")
            dataset_name = uploaded_file.name.replace('.csv', '').replace('.xlsx', '').replace('.xls', '')
            md_export = export_to_markdown(kpis, schema, table_name, dataset_name)
            st.download_button(
                label="📝 Download Markdown",
                data=md_export,
                file_name=f"kpis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown",
                use_container_width=True
            )
        
        with col3:
            st.markdown("#### 📊 Dashboard Spec")
            st.markdown("Ready-to-use configuration for BI tools like Power BI, Tableau, or Looker. Import this spec to quickly build dashboards with your KPIs.")
            dashboard_export = export_to_dashboard_spec(kpis, schema, table_name)
            st.download_button(
                label="📊 Download Dashboard Spec",
                data=dashboard_export,
                file_name=f"dashboard_spec_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Built with ❤️ using Streamlit | AutoKPI v1.0.0</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

