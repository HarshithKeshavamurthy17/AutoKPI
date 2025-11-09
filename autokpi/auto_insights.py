"""
Auto Insights Generator
Generates natural language insights and recommendations from data analysis
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from .advanced_analytics import (
    calculate_correlations, detect_outliers, calculate_distribution_stats,
    detect_trends, calculate_growth_rates, analyze_categorical_relationships
)
from .data_quality import check_data_quality


def generate_insights(df: pd.DataFrame, schema: Dict[str, Any], 
                     kpis: List[Dict[str, Any]], 
                     quality_report: Optional[Dict[str, Any]] = None,
                     statistical_summary: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """
    Generate comprehensive auto-insights from the dataset.
    
    Args:
        df: DataFrame
        schema: Inferred schema
        kpis: List of generated KPIs
        quality_report: Optional data quality report
        statistical_summary: Optional statistical summary
        
    Returns:
        List of insight dictionaries
    """
    insights = []
    
    # 1. Data Quality Insights
    if quality_report:
        insights.extend(generate_quality_insights(quality_report))
    
    # 2. Statistical Insights
    insights.extend(generate_statistical_insights(df, schema, statistical_summary))
    
    # 3. Correlation Insights
    insights.extend(generate_correlation_insights(df, schema))
    
    # 4. Trend Insights
    insights.extend(generate_trend_insights(df, schema))
    
    # 5. Distribution Insights
    insights.extend(generate_distribution_insights(df, schema))
    
    # 6. Outlier Insights
    insights.extend(generate_outlier_insights(df, schema))
    
    # 7. Categorical Insights
    insights.extend(generate_categorical_insights(df, schema))
    
    # 8. KPI Insights
    insights.extend(generate_kpi_insights(kpis, df, schema))
    
    # 9. Business Insights
    insights.extend(generate_business_insights(df, schema))
    
    # Sort by importance/severity
    insights.sort(key=lambda x: x.get('priority', 0), reverse=True)
    
    return insights


def generate_quality_insights(quality_report: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Generate insights from data quality report.
    """
    insights = []
    overall_score = quality_report.get('overall_score', 100)
    
    if overall_score < 70:
        insights.append({
            'type': 'quality',
            'category': 'data_quality',
            'title': 'Data Quality Alert',
            'message': f'Overall data quality score is {overall_score:.1f}/100. Review quality issues before proceeding with analysis.',
            'priority': 9,
            'severity': 'high' if overall_score < 50 else 'medium',
            'recommendations': quality_report.get('recommendations', [])
        })
    
    # Completeness insights
    completeness = quality_report.get('dimensions', {}).get('completeness', {})
    missing_cols = completeness.get('problematic_columns', [])
    if missing_cols:
        insights.append({
            'type': 'quality',
            'category': 'completeness',
            'title': 'Missing Values Detected',
            'message': f'{len(missing_cols)} columns have significant missing values (>10%). Consider data imputation strategies.',
            'priority': 7,
            'severity': 'medium',
            'details': {col: f"{completeness.get('missing_percentage_by_column', {}).get(col, 0):.1f}% missing" 
                       for col in missing_cols[:5]}
        })
    
    # Duplicate insights
    uniqueness = quality_report.get('dimensions', {}).get('uniqueness', {})
    if uniqueness.get('duplicate_rows', 0) > 0:
        insights.append({
            'type': 'quality',
            'category': 'uniqueness',
            'title': 'Duplicate Rows Found',
            'message': f'{uniqueness["duplicate_rows"]} duplicate rows detected. Consider removing duplicates to improve data quality.',
            'priority': 6,
            'severity': 'medium'
        })
    
    return insights


def generate_statistical_insights(df: pd.DataFrame, schema: Dict[str, Any],
                                 statistical_summary: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Generate statistical insights.
    """
    insights = []
    numeric_cols = schema.get('numeric_columns', [])
    
    if not numeric_cols:
        return insights
    
    # Find columns with high variance
    for col in numeric_cols:
        if col in df.columns:
            std = df[col].std()
            mean = df[col].mean()
            cv = (std / mean * 100) if mean != 0 else 0
            
            if cv > 100:
                insights.append({
                    'type': 'statistical',
                    'category': 'variability',
                    'title': f'High Variability in {col}',
                    'message': f'{col} shows high variability (CV: {cv:.1f}%), indicating wide spread in values. Consider segmenting analysis.',
                    'priority': 5,
                    'severity': 'low',
                    'metric_value': f'CV: {cv:.1f}%'
                })
    
    return insights


def generate_correlation_insights(df: pd.DataFrame, schema: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Generate correlation insights.
    """
    insights = []
    numeric_cols = schema.get('numeric_columns', [])
    
    if len(numeric_cols) < 2:
        return insights
    
    corr_matrix = calculate_correlations(df, numeric_cols)
    
    if corr_matrix.empty:
        return insights
    
    # Find strong correlations
    for i, col1 in enumerate(numeric_cols):
        for col2 in numeric_cols[i+1:]:
            if col1 in corr_matrix.index and col2 in corr_matrix.columns:
                corr_value = corr_matrix.loc[col1, col2]
                
                if abs(corr_value) > 0.7:
                    insights.append({
                        'type': 'statistical',
                        'category': 'correlation',
                        'title': f'Strong Correlation: {col1} ↔ {col2}',
                        'message': f'Strong {"positive" if corr_value > 0 else "negative"} correlation ({corr_value:.2f}) between {col1} and {col2}. These variables move together.',
                        'priority': 7,
                        'severity': 'medium',
                        'metric_value': f'r = {corr_value:.2f}',
                        'implication': 'Consider multivariate analysis or dimension reduction techniques.'
                    })
                elif abs(corr_value) > 0.5:
                    insights.append({
                        'type': 'statistical',
                        'category': 'correlation',
                        'title': f'Moderate Correlation: {col1} ↔ {col2}',
                        'message': f'Moderate {"positive" if corr_value > 0 else "negative"} correlation ({corr_value:.2f}) detected.',
                        'priority': 4,
                        'severity': 'low',
                        'metric_value': f'r = {corr_value:.2f}'
                    })
    
    return insights


def generate_trend_insights(df: pd.DataFrame, schema: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Generate trend insights from time series data.
    """
    insights = []
    datetime_cols = schema.get('datetime_columns', [])
    numeric_cols = schema.get('numeric_columns', [])
    
    if not datetime_cols or not numeric_cols:
        return insights
    
    datetime_col = datetime_cols[0]
    
    for num_col in numeric_cols[:3]:  # Analyze top 3 numeric columns
        trend = detect_trends(df, num_col, datetime_col)
        if trend and trend.get('is_significant'):
            insights.append({
                'type': 'trend',
                'category': 'time_series',
                'title': f'{num_col} Trend Analysis',
                'message': f'{num_col} shows a {trend["trend_direction"]} trend with {trend["strength"]} correlation (R² = {trend["r_squared"]:.2f}).',
                'priority': 8,
                'severity': 'medium',
                'metric_value': f'Slope: {trend["slope"]:.2f}, R²: {trend["r_squared"]:.2f}',
                'implication': f'Consider forecasting or investigating factors driving the {trend["trend_direction"]} trend.'
            })
    
    return insights


def generate_distribution_insights(df: pd.DataFrame, schema: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Generate distribution insights.
    """
    insights = []
    numeric_cols = schema.get('numeric_columns', [])
    
    for col in numeric_cols[:3]:
        dist_stats = calculate_distribution_stats(df, col)
        if dist_stats:
            skewness = dist_stats.get('skewness', 0)
            is_normal = dist_stats.get('is_normal', False)
            
            if abs(skewness) > 1:
                insights.append({
                    'type': 'statistical',
                    'category': 'distribution',
                    'title': f'{col} Distribution Analysis',
                    'message': f'{col} is {"positively" if skewness > 0 else "negatively"} skewed (skewness: {skewness:.2f}), indicating non-normal distribution.',
                    'priority': 5,
                    'severity': 'low',
                    'metric_value': f'Skewness: {skewness:.2f}',
                    'implication': 'Consider log transformation or non-parametric tests for analysis.'
                })
            elif is_normal:
                insights.append({
                    'type': 'statistical',
                    'category': 'distribution',
                    'title': f'{col} is Normally Distributed',
                    'message': f'{col} follows a normal distribution, suitable for parametric statistical tests.',
                    'priority': 3,
                    'severity': 'low',
                    'metric_value': 'Normal distribution confirmed'
                })
    
    return insights


def generate_outlier_insights(df: pd.DataFrame, schema: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Generate outlier insights.
    """
    insights = []
    numeric_cols = schema.get('numeric_columns', [])
    
    for col in numeric_cols:
        outliers = detect_outliers(df, col)
        if outliers and outliers.get('outlier_percentage', 0) > 5:
            insights.append({
                'type': 'data_quality',
                'category': 'outliers',
                'title': f'Outliers Detected in {col}',
                'message': f'{col} contains {outliers["outlier_percentage"]:.1f}% outliers ({outliers["total_outliers"]} values). Review for data entry errors.',
                'priority': 6,
                'severity': 'medium',
                'metric_value': f'{outliers["total_outliers"]} outliers ({outliers["outlier_percentage"]:.1f}%)',
                'recommendations': [
                    'Review outlier values for data entry errors',
                    'Consider outlier treatment (removal, winsorization, or separate analysis)'
                ]
            })
    
    return insights


def generate_categorical_insights(df: pd.DataFrame, schema: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Generate categorical variable insights.
    """
    insights = []
    cat_cols = schema.get('categorical_columns', [])
    numeric_cols = schema.get('numeric_columns', [])
    
    # Analyze categorical distributions
    for col in cat_cols:
        value_counts = df[col].value_counts()
        top_value_pct = (value_counts.iloc[0] / len(df) * 100) if len(value_counts) > 0 else 0
        
        if top_value_pct > 80:
            insights.append({
                'type': 'statistical',
                'category': 'distribution',
                'title': f'Imbalanced Categories in {col}',
                'message': f'{col} is highly imbalanced - top category represents {top_value_pct:.1f}% of data.',
                'priority': 4,
                'severity': 'low',
                'metric_value': f'Top category: {top_value_pct:.1f}%',
                'implication': 'Consider stratified sampling or separate analysis for minority categories.'
            })
    
    # Analyze relationships
    relationships = analyze_categorical_relationships(df, cat_cols)
    for rel in relationships:
        if rel.get('is_significant'):
            insights.append({
                'type': 'statistical',
                'category': 'relationship',
                'title': f'Categorical Relationship: {rel["columns"][0]} ↔ {rel["columns"][1]}',
                'message': f'{rel["columns"][0]} and {rel["columns"][1]} are statistically dependent (p < 0.05).',
                'priority': 6,
                'severity': 'medium',
                'metric_value': f'Chi² = {rel["chi2_statistic"]:.2f}, p = {rel["p_value"]:.4f}'
            })
    
    return insights


def generate_kpi_insights(kpis: List[Dict[str, Any]], df: pd.DataFrame, 
                         schema: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Generate insights from KPIs.
    """
    insights = []
    
    # Find high-value KPIs
    aggregation_kpis = [kpi for kpi in kpis if kpi.get('category') == 'aggregation']
    
    if aggregation_kpis:
        insights.append({
            'type': 'kpi',
            'category': 'summary',
            'title': 'KPI Summary',
            'message': f'Generated {len(kpis)} KPIs across {len(set(kpi.get("category", "unknown") for kpi in kpis))} categories. Review aggregation KPIs for key metrics.',
            'priority': 5,
            'severity': 'low',
            'metric_value': f'{len(kpis)} total KPIs'
        })
    
    # Time series KPIs
    time_series_kpis = [kpi for kpi in kpis if kpi.get('category') == 'time_series']
    if time_series_kpis:
        insights.append({
            'type': 'kpi',
            'category': 'time_series',
            'title': 'Time Series Analysis Available',
            'message': f'{len(time_series_kpis)} time-series KPIs generated. Analyze trends and patterns over time.',
            'priority': 7,
            'severity': 'medium'
        })
    
    return insights


def generate_business_insights(df: pd.DataFrame, schema: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Generate business-focused insights.
    """
    insights = []
    numeric_cols = schema.get('numeric_columns', [])
    datetime_cols = schema.get('datetime_columns', [])
    cat_cols = schema.get('categorical_columns', [])
    
    # Revenue/Amount insights
    amount_cols = [col for col in numeric_cols if any(keyword in col.lower() 
                  for keyword in ['amount', 'revenue', 'price', 'sales', 'income'])]
    
    if amount_cols and datetime_cols:
        insights.append({
            'type': 'business',
            'category': 'revenue',
            'title': 'Revenue Analysis Recommended',
            'message': f'Revenue-related columns detected: {", ".join(amount_cols)}. Consider revenue trend analysis and forecasting.',
            'priority': 8,
            'severity': 'high',
            'recommendations': [
                'Analyze revenue trends over time',
                'Identify peak revenue periods',
                'Forecast future revenue',
                'Segment revenue by categories'
            ]
        })
    
    # Customer/User insights
    id_cols = schema.get('id_columns', [])
    user_cols = [col for col in id_cols if 'user' in col.lower() or 'customer' in col.lower()]
    
    if user_cols:
        insights.append({
            'type': 'business',
            'category': 'customers',
            'title': 'Customer Analysis Opportunity',
            'message': f'Customer/user identifiers detected. Consider customer segmentation, retention, and lifetime value analysis.',
            'priority': 7,
            'severity': 'medium',
            'recommendations': [
                'Customer segmentation analysis',
                'Retention rate calculation',
                'Customer lifetime value (CLV)',
                'Cohort analysis'
            ]
        })
    
    return insights


def format_insights_for_display(insights: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Format insights for display, grouped by category.
    """
    grouped = {
        'high_priority': [],
        'medium_priority': [],
        'low_priority': [],
        'quality': [],
        'statistical': [],
        'business': []
    }
    
    for insight in insights:
        priority = insight.get('priority', 0)
        category = insight.get('category', 'other')
        insight_type = insight.get('type', 'other')
        
        if priority >= 7:
            grouped['high_priority'].append(insight)
        elif priority >= 4:
            grouped['medium_priority'].append(insight)
        else:
            grouped['low_priority'].append(insight)
        
        if insight_type == 'quality':
            grouped['quality'].append(insight)
        elif insight_type in ['statistical', 'trend', 'correlation']:
            grouped['statistical'].append(insight)
        elif insight_type == 'business':
            grouped['business'].append(insight)
    
    return grouped

