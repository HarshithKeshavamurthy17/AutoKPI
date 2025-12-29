"""
Creative and Advanced KPI Generation
Generates insightful, pattern-based KPIs with creative analysis
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from scipy import stats
from scipy.stats import zscore
import warnings
warnings.filterwarnings('ignore')


def detect_anomalies_kpis(df: pd.DataFrame, schema: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Generate KPIs for anomaly detection.
    
    Args:
        df: DataFrame
        schema: Inferred schema
        
    Returns:
        List of anomaly detection KPI dictionaries
    """
    kpis = []
    numeric_cols = schema.get('numeric_columns', [])
    datetime_cols = schema.get('datetime_columns', [])
    
    for col in numeric_cols:
        # Z-score based anomalies
        z_scores = np.abs(zscore(df[col].dropna()))
        anomalies = (z_scores > 3).sum()
        anomaly_pct = (anomalies / len(df[col].dropna())) * 100 if len(df[col].dropna()) > 0 else 0
        
        if anomaly_pct > 0:
            kpis.append({
                'name': f'Anomaly Rate in {col.replace("_", " ").title()}',
                'description': f'{anomaly_pct:.1f}% of {col} values are statistical anomalies (3+ standard deviations from mean). These outliers may indicate data errors or exceptional events worth investigating.',
                'logic': f'COUNT(CASE WHEN ABS(({col} - AVG({col})) / STDDEV({col})) > 3 THEN 1 END) / COUNT(*) * 100',
                'columns_used': [col],
                'category': 'anomaly_detection',
                'subcategory': 'zscore_anomalies',
                'difficulty': 'advanced',
                'sql_function': 'ANOMALY_RATE',
                'column': col,
                'anomaly_count': int(anomalies),
                'anomaly_percentage': float(anomaly_pct),
                'insight': 'High anomaly rates may indicate data quality issues or exceptional business events.'
            })
        
        # IQR-based outliers
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers = ((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))).sum()
        outlier_pct = (outliers / len(df)) * 100
        
        if outlier_pct > 5:
            kpis.append({
                'name': f'Outlier Detection in {col.replace("_", " ").title()}',
                'description': f'{outlier_pct:.1f}% of records are outliers based on IQR method. Outliers can reveal exceptional cases or data quality issues.',
                'logic': f'IQR-based outlier detection for {col}',
                'columns_used': [col],
                'category': 'anomaly_detection',
                'subcategory': 'iqr_outliers',
                'difficulty': 'advanced',
                'sql_function': 'OUTLIER_DETECTION',
                'column': col,
                'outlier_count': int(outliers),
                'outlier_percentage': float(outlier_pct),
                'insight': 'Consider investigating outliers - they may represent opportunities or errors.'
            })
    
    return kpis


def detect_seasonality_kpis(df: pd.DataFrame, schema: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Detect seasonality patterns in time series data.
    
    Args:
        df: DataFrame
        schema: Inferred schema
        
    Returns:
        List of seasonality KPI dictionaries
    """
    kpis = []
    datetime_cols = schema.get('datetime_columns', [])
    numeric_cols = schema.get('numeric_columns', [])
    
    if not datetime_cols or not numeric_cols:
        return kpis
    
    datetime_col = datetime_cols[0]
    df_copy = df.copy()
    df_copy[datetime_col] = pd.to_datetime(df_copy[datetime_col], errors='coerce')
    df_copy = df_copy.dropna(subset=[datetime_col])
    
    if len(df_copy) < 30:  # Need enough data for seasonality
        return kpis
    
    for num_col in numeric_cols[:2]:  # Analyze top 2 numeric columns
        # Daily aggregation
        daily = df_copy.groupby(df_copy[datetime_col].dt.dayofweek)[num_col].mean()
        weekly_variance = daily.var()
        
        # Monthly aggregation
        monthly = df_copy.groupby(df_copy[datetime_col].dt.month)[num_col].mean()
        monthly_variance = monthly.var()
        
        # Detect day of week patterns
        if weekly_variance > daily.mean() * 0.1:  # Significant variation
            best_day = daily.idxmax()
            worst_day = daily.idxmin()
            day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            
            kpis.append({
                'name': f'Weekly Pattern in {num_col.replace("_", " ").title()}',
                'description': f'{num_col} shows weekly seasonality. Best performing day: {day_names[best_day]} ({daily[best_day]:.2f}), Lowest: {day_names[worst_day]} ({daily[worst_day]:.2f}). This pattern suggests day-of-week effects.',
                'logic': f'AVG({num_col}) GROUP BY DAYOFWEEK({datetime_col})',
                'columns_used': [num_col, datetime_col],
                'category': 'pattern_detection',
                'subcategory': 'weekly_seasonality',
                'difficulty': 'advanced',
                'sql_function': 'WEEKLY_PATTERN',
                'column': num_col,
                'best_day': day_names[best_day],
                'worst_day': day_names[worst_day],
                'variance': float(weekly_variance),
                'insight': f'Consider scheduling important activities on {day_names[best_day]}s when {num_col} is highest.'
            })
        
        # Detect monthly patterns
        if monthly_variance > monthly.mean() * 0.15:
            best_month = monthly.idxmax()
            worst_month = monthly.idxmin()
            month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            
            kpis.append({
                'name': f'Monthly Seasonality in {num_col.replace("_", " ").title()}',
                'description': f'{num_col} exhibits monthly seasonality. Peak month: {month_names[best_month-1]} ({monthly[best_month]:.2f}), Lowest: {month_names[worst_month-1]} ({monthly[worst_month]:.2f}).',
                'logic': f'AVG({num_col}) GROUP BY MONTH({datetime_col})',
                'columns_used': [num_col, datetime_col],
                'category': 'pattern_detection',
                'subcategory': 'monthly_seasonality',
                'difficulty': 'advanced',
                'sql_function': 'MONTHLY_PATTERN',
                'column': num_col,
                'best_month': month_names[best_month-1],
                'worst_month': month_names[worst_month-1],
                'insight': f'Plan campaigns or inventory around {month_names[best_month-1]} when {num_col} peaks.'
            })
    
    return kpis


def generate_comparative_kpis(df: pd.DataFrame, schema: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Generate comparative KPIs (vs average, vs median, vs top performer).
    
    Args:
        df: DataFrame
        schema: Inferred schema
        
    Returns:
        List of comparative KPI dictionaries
    """
    kpis = []
    numeric_cols = schema.get('numeric_columns', [])
    categorical_cols = schema.get('categorical_columns', [])
    
    # Compare categories vs overall average
    for cat_col in categorical_cols[:2]:  # Limit to 2 categories
        for num_col in numeric_cols:
            category_means = df.groupby(cat_col)[num_col].mean()
            overall_mean = df[num_col].mean()
            
            # Top performer
            top_category = category_means.idxmax()
            top_value = category_means.max()
            top_performance_pct = ((top_value - overall_mean) / overall_mean * 100) if overall_mean != 0 else 0
            
            # Bottom performer
            bottom_category = category_means.idxmin()
            bottom_value = category_means.min()
            bottom_performance_pct = ((bottom_value - overall_mean) / overall_mean * 100) if overall_mean != 0 else 0
            
            kpis.append({
                'name': f'{num_col.replace("_", " ").title()} Performance: {top_category} vs Average',
                'description': f'{top_category} outperforms the average by {top_performance_pct:.1f}% ({top_value:.2f} vs {overall_mean:.2f}). {bottom_category} underperforms by {abs(bottom_performance_pct):.1f}%.',
                'logic': f'AVG({num_col}) GROUP BY {cat_col} compared to overall AVG({num_col})',
                'columns_used': [num_col, cat_col],
                'category': 'comparative_analysis',
                'subcategory': 'vs_average',
                'difficulty': 'medium',
                'sql_function': 'COMPARATIVE',
                'column': num_col,
                'group_by': cat_col,
                'top_performer': top_category,
                'top_performance_pct': float(top_performance_pct),
                'bottom_performer': bottom_category,
                'insight': f'Learn from {top_category}\'s success. Investigate why {bottom_category} underperforms.'
            })
            
            # Performance gap
            performance_gap = top_value - bottom_value
            gap_pct = (performance_gap / bottom_value * 100) if bottom_value != 0 else 0
            
            kpis.append({
                'name': f'{num_col.replace("_", " ").title()} Performance Gap',
                'description': f'The gap between best ({top_category}: {top_value:.2f}) and worst ({bottom_category}: {bottom_value:.2f}) performers is {gap_pct:.1f}%. This represents a significant opportunity for improvement.',
                'logic': f'MAX({num_col}) - MIN({num_col}) GROUP BY {cat_col}',
                'columns_used': [num_col, cat_col],
                'category': 'comparative_analysis',
                'subcategory': 'performance_gap',
                'difficulty': 'medium',
                'sql_function': 'PERFORMANCE_GAP',
                'column': num_col,
                'group_by': cat_col,
                'gap_percentage': float(gap_pct),
                'insight': f'Closing the gap could improve overall {num_col} by {gap_pct/2:.1f}% if underperformers reach median.'
            })
    
    return kpis


def detect_distribution_patterns_kpis(df: pd.DataFrame, schema: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Detect distribution patterns and generate KPIs.
    
    Args:
        df: DataFrame
        schema: Inferred schema
        
    Returns:
        List of distribution pattern KPI dictionaries
    """
    kpis = []
    numeric_cols = schema.get('numeric_columns', [])
    
    for col in numeric_cols:
        data = df[col].dropna()
        
        if len(data) < 10:
            continue
        
        # Skewness analysis
        skewness = stats.skew(data)
        if abs(skewness) > 1:
            kpis.append({
                'name': f'{col.replace("_", " ").title()} Distribution Skewness',
                'description': f'{col} is {"positively" if skewness > 0 else "negatively"} skewed (skewness: {skewness:.2f}). This means most values are clustered on the {"left" if skewness > 0 else "right"} side, with a long tail on the {"right" if skewness > 0 else "left"}.',
                'logic': f'Statistical skewness of {col}',
                'columns_used': [col],
                'category': 'distribution_analysis',
                'subcategory': 'skewness',
                'difficulty': 'advanced',
                'sql_function': 'SKEWNESS',
                'column': col,
                'skewness_value': float(skewness),
                'insight': 'Skewed distributions may require different analytical approaches (e.g., log transformation).'
            })
        
        # Concentration analysis (80/20 rule)
        sorted_data = data.sort_values(ascending=False)
        top_20_pct_count = int(len(sorted_data) * 0.2)
        top_20_pct_value = sorted_data.head(top_20_pct_count).sum()
        total_value = sorted_data.sum()
        concentration_pct = (top_20_pct_value / total_value * 100) if total_value != 0 else 0
        
        if concentration_pct > 60:  # Pareto principle indicator
            kpis.append({
                'name': f'{col.replace("_", " ").title()} Concentration (80/20 Rule)',
                'description': f'{concentration_pct:.1f}% of {col} comes from the top 20% of records. This suggests a Pareto distribution where a small number of records contribute disproportionately.',
                'logic': f'SUM of top 20% records / SUM of all records',
                'columns_used': [col],
                'category': 'distribution_analysis',
                'subcategory': 'pareto',
                'difficulty': 'advanced',
                'sql_function': 'CONCENTRATION',
                'column': col,
                'concentration_percentage': float(concentration_pct),
                'insight': 'Focus on the top 20% - they drive most of the value. Consider targeted strategies for high-value segments.'
            })
        
        # Coefficient of variation (relative variability)
        cv = (data.std() / data.mean() * 100) if data.mean() != 0 else 0
        if cv > 50:
            kpis.append({
                'name': f'{col.replace("_", " ").title()} Variability',
                'description': f'{col} has high variability (CV: {cv:.1f}%). This means values vary widely, suggesting diverse performance or behavior patterns.',
                'logic': f'(STDDEV({col}) / AVG({col})) * 100',
                'columns_used': [col],
                'category': 'distribution_analysis',
                'subcategory': 'variability',
                'difficulty': 'medium',
                'sql_function': 'VARIABILITY',
                'column': col,
                'coefficient_of_variation': float(cv),
                'insight': 'High variability suggests segmentation opportunities. Consider grouping records to understand different patterns.'
            })
    
    return kpis


def detect_trend_breakpoints_kpis(df: pd.DataFrame, schema: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Detect trend breakpoints and significant changes.
    
    Args:
        df: DataFrame
        schema: Inferred schema
        
    Returns:
        List of trend breakpoint KPI dictionaries
    """
    kpis = []
    datetime_cols = schema.get('datetime_columns', [])
    numeric_cols = schema.get('numeric_columns', [])
    
    if not datetime_cols or not numeric_cols:
        return kpis
    
    datetime_col = datetime_cols[0]
    df_copy = df.copy()
    df_copy[datetime_col] = pd.to_datetime(df_copy[datetime_col], errors='coerce')
    df_copy = df_copy.dropna(subset=[datetime_col]).sort_values(datetime_col)
    
    if len(df_copy) < 10:
        return kpis
    
    for num_col in numeric_cols[:2]:
        # Split into halves and compare
        midpoint = len(df_copy) // 2
        first_half = df_copy.iloc[:midpoint][num_col].mean()
        second_half = df_copy.iloc[midpoint:][num_col].mean()
        
        change_pct = ((second_half - first_half) / first_half * 100) if first_half != 0 else 0
        
        if abs(change_pct) > 10:
            kpis.append({
                'name': f'{num_col.replace("_", " ").title()} Trend Change',
                'description': f'{num_col} {"increased" if change_pct > 0 else "decreased"} by {abs(change_pct):.1f}% from the first half ({first_half:.2f}) to the second half ({second_half:.2f}) of the period. This indicates a {"positive" if change_pct > 0 else "negative"} trend shift.',
                'logic': f'Compare AVG({num_col}) in first half vs second half of time period',
                'columns_used': [num_col, datetime_col],
                'category': 'trend_analysis',
                'subcategory': 'breakpoint',
                'difficulty': 'advanced',
                'sql_function': 'TREND_CHANGE',
                'column': num_col,
                'change_percentage': float(change_pct),
                'first_half_avg': float(first_half),
                'second_half_avg': float(second_half),
                'insight': f'{"Continue the positive momentum" if change_pct > 0 else "Investigate the decline and take corrective action"}.'
            })
    
    return kpis


def generate_creative_kpis(df: pd.DataFrame, schema: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Generate all creative and advanced KPIs.
    
    Args:
        df: DataFrame
        schema: Inferred schema
        
    Returns:
        List of creative KPI dictionaries
    """
    all_kpis = []
    
    # Anomaly detection KPIs
    all_kpis.extend(detect_anomalies_kpis(df, schema))
    
    # Seasonality KPIs
    all_kpis.extend(detect_seasonality_kpis(df, schema))
    
    # Comparative KPIs
    all_kpis.extend(generate_comparative_kpis(df, schema))
    
    # Distribution pattern KPIs
    all_kpis.extend(detect_distribution_patterns_kpis(df, schema))
    
    # Trend breakpoint KPIs
    all_kpis.extend(detect_trend_breakpoints_kpis(df, schema))
    
    return all_kpis



