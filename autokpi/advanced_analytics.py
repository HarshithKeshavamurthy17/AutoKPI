"""
Advanced Analytics Module
Provides comprehensive statistical analysis, correlations, distributions, and insights
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from scipy import stats
from scipy.stats import chi2_contingency
import warnings
warnings.filterwarnings('ignore')


def calculate_correlations(df: pd.DataFrame, numeric_columns: List[str]) -> pd.DataFrame:
    """
    Calculate correlation matrix for numeric columns.
    
    Args:
        df: DataFrame
        numeric_columns: List of numeric column names
        
    Returns:
        Correlation matrix DataFrame
    """
    if len(numeric_columns) < 2:
        return pd.DataFrame()
    
    corr_df = df[numeric_columns].corr()
    return corr_df


def detect_outliers(df: pd.DataFrame, column: str, method: str = 'iqr') -> Dict[str, Any]:
    """
    Detect outliers in a numeric column.
    
    Args:
        df: DataFrame
        column: Column name
        method: Method to use ('iqr' or 'zscore')
        
    Returns:
        Dictionary with outlier information
    """
    if column not in df.columns or not pd.api.types.is_numeric_dtype(df[column]):
        return {}
    
    data = df[column].dropna()
    
    if method == 'iqr':
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = data[(data < lower_bound) | (data > upper_bound)]
    else:  # zscore
        z_scores = np.abs(stats.zscore(data))
        outliers = data[z_scores > 3]
    
    return {
        'column': column,
        'total_outliers': len(outliers),
        'outlier_percentage': (len(outliers) / len(data)) * 100 if len(data) > 0 else 0,
        'outlier_values': outliers.tolist()[:10],  # First 10 outliers
        'lower_bound': float(lower_bound) if method == 'iqr' else None,
        'upper_bound': float(upper_bound) if method == 'iqr' else None
    }


def calculate_distribution_stats(df: pd.DataFrame, column: str) -> Dict[str, Any]:
    """
    Calculate distribution statistics for a numeric column.
    
    Args:
        df: DataFrame
        column: Column name
        
    Returns:
        Dictionary with distribution statistics
    """
    if column not in df.columns or not pd.api.types.is_numeric_dtype(df[column]):
        return {}
    
    data = df[column].dropna()
    
    # Normality test
    if len(data) > 3:
        try:
            _, p_value = stats.normaltest(data)
            is_normal = p_value > 0.05
        except:
            is_normal = None
            p_value = None
    else:
        is_normal = None
        p_value = None
    
    # Percentiles
    percentiles = [10, 25, 50, 75, 90, 95, 99]
    percentile_values = {f'p{p}': float(data.quantile(p/100)) for p in percentiles}
    
    # Skewness and Kurtosis
    skewness = float(stats.skew(data))
    kurtosis = float(stats.kurtosis(data))
    
    return {
        'column': column,
        'mean': float(data.mean()),
        'median': float(data.median()),
        'std': float(data.std()),
        'variance': float(data.var()),
        'min': float(data.min()),
        'max': float(data.max()),
        'range': float(data.max() - data.min()),
        'skewness': skewness,
        'kurtosis': kurtosis,
        'is_normal': is_normal,
        'normality_p_value': p_value,
        'percentiles': percentile_values,
        'iqr': float(data.quantile(0.75) - data.quantile(0.25))
    }


def calculate_growth_rates(df: pd.DataFrame, value_column: str, 
                          date_column: str, periods: List[str] = ['day', 'month', 'year']) -> Dict[str, Any]:
    """
    Calculate growth rates for time series data.
    
    Args:
        df: DataFrame
        value_column: Column with values to analyze
        date_column: Date column
        periods: List of periods to analyze
        
    Returns:
        Dictionary with growth rate information
    """
    if date_column not in df.columns or value_column not in df.columns:
        return {}
    
    df_copy = df.copy()
    df_copy[date_column] = pd.to_datetime(df_copy[date_column], errors='coerce')
    df_copy = df_copy.dropna(subset=[date_column, value_column])
    
    if len(df_copy) == 0:
        return {}
    
    growth_rates = {}
    
    for period in periods:
        if period == 'day':
            df_period = df_copy.groupby(df_copy[date_column].dt.date)[value_column].sum().reset_index()
        elif period == 'month':
            df_period = df_copy.groupby(df_copy[date_column].dt.to_period('M'))[value_column].sum().reset_index()
        elif period == 'year':
            df_period = df_copy.groupby(df_copy[date_column].dt.year)[value_column].sum().reset_index()
        else:
            continue
        
        if len(df_period) > 1:
            df_period['pct_change'] = df_period[value_column].pct_change() * 100
            growth_rates[period] = {
                'avg_growth_rate': float(df_period['pct_change'].mean()),
                'median_growth_rate': float(df_period['pct_change'].median()),
                'volatility': float(df_period['pct_change'].std()),
                'trend': 'increasing' if df_period['pct_change'].mean() > 0 else 'decreasing'
            }
    
    return growth_rates


def detect_trends(df: pd.DataFrame, value_column: str, date_column: str) -> Dict[str, Any]:
    """
    Detect trends in time series data.
    
    Args:
        df: DataFrame
        value_column: Column with values
        date_column: Date column
        
    Returns:
        Dictionary with trend information
    """
    if date_column not in df.columns or value_column not in df.columns:
        return {}
    
    df_copy = df.copy()
    df_copy[date_column] = pd.to_datetime(df_copy[date_column], errors='coerce')
    df_copy = df_copy.dropna(subset=[date_column, value_column]).sort_values(date_column)
    
    if len(df_copy) < 3:
        return {}
    
    # Linear regression to detect trend
    x = np.arange(len(df_copy))
    y = df_copy[value_column].values
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    
    # Determine trend direction
    if slope > 0:
        trend_direction = 'increasing'
    elif slope < 0:
        trend_direction = 'decreasing'
    else:
        trend_direction = 'stable'
    
    return {
        'trend_direction': trend_direction,
        'slope': float(slope),
        'r_squared': float(r_value ** 2),
        'p_value': float(p_value),
        'strength': 'strong' if abs(r_value) > 0.7 else 'moderate' if abs(r_value) > 0.4 else 'weak',
        'is_significant': p_value < 0.05
    }


def calculate_ratios_and_metrics(df: pd.DataFrame, schema: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Calculate advanced ratios and derived metrics.
    
    Args:
        df: DataFrame
        schema: Inferred schema
        
    Returns:
        List of ratio/metric dictionaries
    """
    metrics = []
    numeric_cols = schema.get('numeric_columns', [])
    
    if len(numeric_cols) >= 2:
        # Calculate ratios between numeric columns
        for i, col1 in enumerate(numeric_cols):
            for col2 in numeric_cols[i+1:]:
                if df[col1].sum() != 0:
                    ratio = df[col2].sum() / df[col1].sum()
                    metrics.append({
                        'name': f'{col2} to {col1} Ratio',
                        'description': f'Ratio of {col2} to {col1}',
                        'value': float(ratio),
                        'columns': [col1, col2],
                        'type': 'ratio'
                    })
    
    # Calculate averages per ID (if ID columns exist)
    id_cols = schema.get('id_columns', [])
    if id_cols and numeric_cols:
        for id_col in id_cols[:1]:  # Use first ID column
            for num_col in numeric_cols:
                if df[id_col].nunique() > 0:
                    avg_per_id = df[num_col].sum() / df[id_col].nunique()
                    metrics.append({
                        'name': f'Average {num_col} per {id_col}',
                        'description': f'Average {num_col} per unique {id_col}',
                        'value': float(avg_per_id),
                        'columns': [id_col, num_col],
                        'type': 'average_per_id'
                    })
    
    return metrics


def analyze_categorical_relationships(df: pd.DataFrame, cat_columns: List[str], 
                                     target_column: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Analyze relationships between categorical columns.
    
    Args:
        df: DataFrame
        cat_columns: List of categorical column names
        target_column: Optional target column for analysis
        
    Returns:
        List of relationship analysis results
    """
    insights = []
    
    if len(cat_columns) < 2:
        return insights
    
    # Chi-square test for independence
    for i, col1 in enumerate(cat_columns):
        for col2 in cat_columns[i+1:]:
            try:
                contingency_table = pd.crosstab(df[col1], df[col2])
                chi2, p_value, dof, expected = chi2_contingency(contingency_table)
                
                insights.append({
                    'columns': [col1, col2],
                    'test': 'chi_square',
                    'chi2_statistic': float(chi2),
                    'p_value': float(p_value),
                    'is_significant': p_value < 0.05,
                    'relationship': 'dependent' if p_value < 0.05 else 'independent'
                })
            except:
                continue
    
    return insights


def generate_statistical_summary(df: pd.DataFrame, schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate comprehensive statistical summary.
    
    Args:
        df: DataFrame
        schema: Inferred schema
        
    Returns:
        Dictionary with statistical summary
    """
    summary = {
        'dataset_info': {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2
        },
        'column_statistics': {},
        'correlations': {},
        'outliers': {},
        'distributions': {}
    }
    
    # Numeric columns statistics
    numeric_cols = schema.get('numeric_columns', [])
    for col in numeric_cols:
        summary['column_statistics'][col] = {
            'mean': float(df[col].mean()) if not df[col].isna().all() else None,
            'median': float(df[col].median()) if not df[col].isna().all() else None,
            'std': float(df[col].std()) if not df[col].isna().all() else None,
            'min': float(df[col].min()) if not df[col].isna().all() else None,
            'max': float(df[col].max()) if not df[col].isna().all() else None,
            'null_count': int(df[col].isna().sum()),
            'null_percentage': float(df[col].isna().sum() / len(df) * 100)
        }
        
        # Distribution stats
        dist_stats = calculate_distribution_stats(df, col)
        if dist_stats:
            summary['distributions'][col] = dist_stats
        
        # Outliers
        outliers = detect_outliers(df, col)
        if outliers:
            summary['outliers'][col] = outliers
    
    # Correlations
    if len(numeric_cols) >= 2:
        corr_matrix = calculate_correlations(df, numeric_cols)
        if not corr_matrix.empty:
            summary['correlations'] = corr_matrix.to_dict()
    
    # Categorical columns
    cat_cols = schema.get('categorical_columns', [])
    for col in cat_cols:
        summary['column_statistics'][col] = {
            'unique_count': int(df[col].nunique()),
            'top_values': df[col].value_counts().head(5).to_dict(),
            'null_count': int(df[col].isna().sum()),
            'null_percentage': float(df[col].isna().sum() / len(df) * 100)
        }
    
    return summary



