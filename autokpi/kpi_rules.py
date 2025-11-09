"""
Rule-based KPI generation engine
Generates KPIs based on inferred schema
"""

from typing import Dict, List, Any
import pandas as pd


def generate_aggregation_kpis(schema: Dict[str, Any], df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Generate aggregation KPIs (SUM, AVG, COUNT, MIN, MAX) for numeric columns.
    
    Args:
        schema: Inferred schema
        df: DataFrame
        
    Returns:
        List of KPI dictionaries
    """
    kpis = []
    
    for col in schema['numeric_columns']:
        # Total/Sum KPI
        kpis.append({
            'name': f'Total {col.replace("_", " ").title()}',
            'description': f'Sum of {col} across all records.',
            'logic': f'SUM({col})',
            'columns_used': [col],
            'category': 'aggregation',
            'subcategory': 'sum',
            'difficulty': 'easy',
            'sql_function': 'SUM',
            'column': col
        })
        
        # Average KPI
        kpis.append({
            'name': f'Average {col.replace("_", " ").title()}',
            'description': f'Average value of {col} across all records.',
            'logic': f'AVG({col})',
            'columns_used': [col],
            'category': 'aggregation',
            'subcategory': 'average',
            'difficulty': 'easy',
            'sql_function': 'AVG',
            'column': col
        })
        
        # Min KPI
        kpis.append({
            'name': f'Minimum {col.replace("_", " ").title()}',
            'description': f'Minimum value of {col} across all records.',
            'logic': f'MIN({col})',
            'columns_used': [col],
            'category': 'aggregation',
            'subcategory': 'min',
            'difficulty': 'easy',
            'sql_function': 'MIN',
            'column': col
        })
        
        # Max KPI
        kpis.append({
            'name': f'Maximum {col.replace("_", " ").title()}',
            'description': f'Maximum value of {col} across all records.',
            'logic': f'MAX({col})',
            'columns_used': [col],
            'category': 'aggregation',
            'subcategory': 'max',
            'difficulty': 'easy',
            'sql_function': 'MAX',
            'column': col
        })
    
    # Count KPIs for ID columns
    for col in schema['id_columns']:
        kpis.append({
            'name': f'Total Count of {col.replace("_", " ").title()}',
            'description': f'Total count of unique {col}.',
            'logic': f'COUNT(DISTINCT {col})',
            'columns_used': [col],
            'category': 'aggregation',
            'subcategory': 'count_distinct',
            'difficulty': 'easy',
            'sql_function': 'COUNT_DISTINCT',
            'column': col
        })
    
    # Overall count
    if len(df) > 0:
        kpis.append({
            'name': 'Total Records',
            'description': 'Total number of records in the dataset.',
            'logic': 'COUNT(*)',
            'columns_used': [],
            'category': 'aggregation',
            'subcategory': 'count',
            'difficulty': 'easy',
            'sql_function': 'COUNT',
            'column': None
        })
    
    return kpis


def generate_time_series_kpis(schema: Dict[str, Any], df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Generate time series KPIs (revenue per day, orders per month, etc.).
    Intelligently detects time granularity based on column name and data.
    
    Args:
        schema: Inferred schema
        df: DataFrame
        
    Returns:
        List of KPI dictionaries
    """
    kpis = []
    
    datetime_cols = schema['datetime_columns']
    numeric_cols = schema['numeric_columns']
    id_cols = schema['id_columns']
    
    if not datetime_cols:
        return kpis
    
    datetime_col = datetime_cols[0]  # Use first datetime column
    
    # Detect time granularity based on column name and data
    datetime_col_lower = datetime_col.lower()
    is_year_column = 'year' in datetime_col_lower
    
    # Check data granularity by sampling
    time_granularity = 'day'  # default
    if datetime_col in df.columns:
        try:
            # Try to parse as datetime
            sample_dates = pd.to_datetime(df[datetime_col].dropna().head(100), errors='coerce')
            sample_dates = sample_dates.dropna()
            
            if len(sample_dates) > 0:
                # Check if dates are all the same year (likely a year column)
                unique_years = sample_dates.dt.year.nunique()
                unique_days = sample_dates.dt.date.nunique()
                
                if is_year_column or (unique_years <= 2 and unique_days <= 2):
                    # This is likely a year-only column
                    time_granularity = 'year'
                elif unique_days < len(sample_dates) * 0.1:
                    # Very few unique days - likely monthly or yearly data
                    time_granularity = 'month'
                else:
                    # Many unique days - daily or finer granularity
                    time_granularity = 'day'
        except:
            # If parsing fails, use column name hint
            if is_year_column:
                time_granularity = 'year'
    
    # Time series with numeric columns
    for num_col in numeric_cols:
        if time_granularity == 'year':
            # Generate per year KPIs
            kpis.append({
                'name': f'{num_col.replace("_", " ").title()} per Year',
                'description': f'Total {num_col} aggregated by year.',
                'logic': f'SUM({num_col}) GROUP BY YEAR({datetime_col})',
                'columns_used': [num_col, datetime_col],
                'category': 'time_series',
                'subcategory': 'yearly',
                'difficulty': 'medium',
                'sql_function': 'SUM',
                'group_by': datetime_col,
                'group_by_function': 'YEAR',
                'column': num_col
            })
            
            # Also generate per month if we have enough data points
            kpis.append({
                'name': f'{num_col.replace("_", " ").title()} per Month',
                'description': f'Total {num_col} aggregated by month (if month data available).',
                'logic': f'SUM({num_col}) GROUP BY YEAR({datetime_col}), MONTH({datetime_col})',
                'columns_used': [num_col, datetime_col],
                'category': 'time_series',
                'subcategory': 'monthly',
                'difficulty': 'medium',
                'sql_function': 'SUM',
                'group_by': datetime_col,
                'group_by_function': 'YEAR_MONTH',
                'column': num_col
            })
        elif time_granularity == 'month':
            # Generate per month and per year KPIs
            kpis.append({
                'name': f'{num_col.replace("_", " ").title()} per Month',
                'description': f'Total {num_col} aggregated by month.',
                'logic': f'SUM({num_col}) GROUP BY YEAR({datetime_col}), MONTH({datetime_col})',
                'columns_used': [num_col, datetime_col],
                'category': 'time_series',
                'subcategory': 'monthly',
                'difficulty': 'medium',
                'sql_function': 'SUM',
                'group_by': datetime_col,
                'group_by_function': 'YEAR_MONTH',
                'column': num_col
            })
            
            kpis.append({
                'name': f'{num_col.replace("_", " ").title()} per Year',
                'description': f'Total {num_col} aggregated by year.',
                'logic': f'SUM({num_col}) GROUP BY YEAR({datetime_col})',
                'columns_used': [num_col, datetime_col],
                'category': 'time_series',
                'subcategory': 'yearly',
                'difficulty': 'medium',
                'sql_function': 'SUM',
                'group_by': datetime_col,
                'group_by_function': 'YEAR',
                'column': num_col
            })
        else:
            # Default: daily granularity - generate per day and per month
            kpis.append({
                'name': f'{num_col.replace("_", " ").title()} per Day',
                'description': f'Total {num_col} aggregated by day.',
                'logic': f'SUM({num_col}) GROUP BY DATE({datetime_col})',
                'columns_used': [num_col, datetime_col],
                'category': 'time_series',
                'subcategory': 'daily',
                'difficulty': 'medium',
                'sql_function': 'SUM',
                'group_by': datetime_col,
                'group_by_function': 'DATE',
                'column': num_col
            })
            
            kpis.append({
                'name': f'{num_col.replace("_", " ").title()} per Month',
                'description': f'Total {num_col} aggregated by month.',
                'logic': f'SUM({num_col}) GROUP BY YEAR({datetime_col}), MONTH({datetime_col})',
                'columns_used': [num_col, datetime_col],
                'category': 'time_series',
                'subcategory': 'monthly',
                'difficulty': 'medium',
                'sql_function': 'SUM',
                'group_by': datetime_col,
                'group_by_function': 'YEAR_MONTH',
                'column': num_col
            })
    
    # Time series with ID columns (counts)
    for id_col in id_cols[:1]:  # Use first ID column
        if time_granularity == 'year':
            kpis.append({
                'name': f'New {id_col.replace("_", " ").title()} per Year',
                'description': f'Count of new {id_col} per year.',
                'logic': f'COUNT(DISTINCT {id_col}) GROUP BY YEAR({datetime_col})',
                'columns_used': [id_col, datetime_col],
                'category': 'time_series',
                'subcategory': 'yearly',
                'difficulty': 'medium',
                'sql_function': 'COUNT_DISTINCT',
                'group_by': datetime_col,
                'group_by_function': 'YEAR',
                'column': id_col
            })
        elif time_granularity == 'month':
            kpis.append({
                'name': f'New {id_col.replace("_", " ").title()} per Month',
                'description': f'Count of new {id_col} per month.',
                'logic': f'COUNT(DISTINCT {id_col}) GROUP BY YEAR({datetime_col}), MONTH({datetime_col})',
                'columns_used': [id_col, datetime_col],
                'category': 'time_series',
                'subcategory': 'monthly',
                'difficulty': 'medium',
                'sql_function': 'COUNT_DISTINCT',
                'group_by': datetime_col,
                'group_by_function': 'YEAR_MONTH',
                'column': id_col
            })
        else:
            kpis.append({
                'name': f'New {id_col.replace("_", " ").title()} per Day',
                'description': f'Count of new {id_col} per day.',
                'logic': f'COUNT(DISTINCT {id_col}) GROUP BY DATE({datetime_col})',
                'columns_used': [id_col, datetime_col],
                'category': 'time_series',
                'subcategory': 'daily',
                'difficulty': 'medium',
                'sql_function': 'COUNT_DISTINCT',
                'group_by': datetime_col,
                'group_by_function': 'DATE',
                'column': id_col
            })
    
    return kpis


def generate_category_breakdown_kpis(schema: Dict[str, Any], df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Generate category breakdown KPIs (revenue by region, top categories, etc.).
    
    Args:
        schema: Inferred schema
        df: DataFrame
        
    Returns:
        List of KPI dictionaries
    """
    kpis = []
    
    categorical_cols = schema['categorical_columns']
    numeric_cols = schema['numeric_columns']
    
    if not categorical_cols:
        return kpis
    
    # Category breakdown with numeric columns
    for cat_col in categorical_cols:
        for num_col in numeric_cols:
            kpis.append({
                'name': f'{num_col.replace("_", " ").title()} by {cat_col.replace("_", " ").title()}',
                'description': f'Total {num_col} broken down by {cat_col}.',
                'logic': f'SUM({num_col}) GROUP BY {cat_col}',
                'columns_used': [num_col, cat_col],
                'category': 'category_breakdown',
                'subcategory': 'sum_by_category',
                'difficulty': 'medium',
                'sql_function': 'SUM',
                'group_by': cat_col,
                'column': num_col
            })
            
            kpis.append({
                'name': f'Average {num_col.replace("_", " ").title()} by {cat_col.replace("_", " ").title()}',
                'description': f'Average {num_col} broken down by {cat_col}.',
                'logic': f'AVG({num_col}) GROUP BY {cat_col}',
                'columns_used': [num_col, cat_col],
                'category': 'category_breakdown',
                'subcategory': 'avg_by_category',
                'difficulty': 'medium',
                'sql_function': 'AVG',
                'group_by': cat_col,
                'column': num_col
            })
        
        # Count by category
        kpis.append({
            'name': f'Count by {cat_col.replace("_", " ").title()}',
            'description': f'Number of records broken down by {cat_col}.',
            'logic': f'COUNT(*) GROUP BY {cat_col}',
            'columns_used': [cat_col],
            'category': 'category_breakdown',
            'subcategory': 'count_by_category',
            'difficulty': 'easy',
            'sql_function': 'COUNT',
            'group_by': cat_col,
            'column': None
        })
    
    return kpis


def generate_conversion_kpis(schema: Dict[str, Any], df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Generate conversion rate and status-based KPIs.
    
    Args:
        schema: Inferred schema
        df: DataFrame
        
    Returns:
        List of KPI dictionaries
    """
    kpis = []
    
    categorical_cols = schema['categorical_columns']
    
    # Look for status-like columns
    status_patterns = ['status', 'state', 'stage', 'phase', 'type']
    status_cols = [col for col in categorical_cols 
                   if any(pattern in col.lower() for pattern in status_patterns)]
    
    for status_col in status_cols:
        # Status distribution
        kpis.append({
            'name': f'{status_col.replace("_", " ").title()} Distribution',
            'description': f'Distribution of records by {status_col}.',
            'logic': f'COUNT(*) GROUP BY {status_col}',
            'columns_used': [status_col],
            'category': 'conversion',
            'subcategory': 'distribution',
            'difficulty': 'easy',
            'sql_function': 'COUNT',
            'group_by': status_col,
            'column': None
        })
        
        # Check for binary status (e.g., completed/cancelled, active/inactive)
        if df[status_col].nunique() == 2:
            values = df[status_col].dropna().unique().tolist()
            if len(values) == 2:
                kpis.append({
                    'name': f'{status_col.replace("_", " ").title()} Rate',
                    'description': f'Percentage of records with {status_col} = {values[0]}.',
                    'logic': f'COUNT(CASE WHEN {status_col} = "{values[0]}" THEN 1 END) / COUNT(*) * 100',
                    'columns_used': [status_col],
                    'category': 'conversion',
                    'subcategory': 'rate',
                    'difficulty': 'medium',
                    'sql_function': 'RATE',
                    'column': status_col,
                    'status_values': values
                })
    
    return kpis


def generate_advanced_kpis(schema: Dict[str, Any], df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Generate advanced KPIs (percentiles, ratios, growth rates).
    
    Args:
        schema: Inferred schema
        df: DataFrame
        
    Returns:
        List of advanced KPI dictionaries
    """
    kpis = []
    numeric_cols = schema.get('numeric_columns', [])
    datetime_cols = schema.get('datetime_columns', [])
    
    # Percentile KPIs
    for col in numeric_cols:
        # Median (50th percentile)
        kpis.append({
            'name': f'Median {col.replace("_", " ").title()}',
            'description': f'Median (50th percentile) value of {col}.',
            'logic': f'PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY {col})',
            'columns_used': [col],
            'category': 'statistical',
            'subcategory': 'percentile',
            'difficulty': 'medium',
            'sql_function': 'MEDIAN',
            'column': col,
            'percentile': 50
        })
        
        # 25th and 75th percentiles (IQR)
        for percentile in [25, 75]:
            kpis.append({
                'name': f'{percentile}th Percentile of {col.replace("_", " ").title()}',
                'description': f'{percentile}th percentile value of {col}.',
                'logic': f'PERCENTILE_CONT({percentile/100}) WITHIN GROUP (ORDER BY {col})',
                'columns_used': [col],
                'category': 'statistical',
                'subcategory': 'percentile',
                'difficulty': 'medium',
                'sql_function': 'PERCENTILE',
                'column': col,
                'percentile': percentile
            })
    
    # Ratio KPIs (between numeric columns)
    if len(numeric_cols) >= 2:
        for i, col1 in enumerate(numeric_cols):
            for col2 in numeric_cols[i+1:]:
                # Avoid division by zero
                if df[col1].sum() != 0:
                    kpis.append({
                        'name': f'{col2.replace("_", " ").title()} to {col1.replace("_", " ").title()} Ratio',
                        'description': f'Ratio of {col2} to {col1}.',
                        'logic': f'SUM({col2}) / SUM({col1})',
                        'columns_used': [col1, col2],
                        'category': 'ratio',
                        'subcategory': 'numeric_ratio',
                        'difficulty': 'medium',
                        'sql_function': 'RATIO',
                        'column': col2,
                        'denominator': col1
                    })
    
    # Growth rate KPIs (if datetime columns exist)
    if datetime_cols and numeric_cols:
        datetime_col = datetime_cols[0]
        for num_col in numeric_cols[:2]:  # Limit to first 2 numeric columns
            kpis.append({
                'name': f'{num_col.replace("_", " ").title()} Growth Rate',
                'description': f'Period-over-period growth rate of {num_col}.',
                'logic': f'(SUM({num_col}) - LAG(SUM({num_col}))) / LAG(SUM({num_col})) * 100',
                'columns_used': [num_col, datetime_col],
                'category': 'growth',
                'subcategory': 'pct_change',
                'difficulty': 'advanced',
                'sql_function': 'GROWTH_RATE',
                'column': num_col
            })
    
    return kpis


def generate_kpis(schema: Dict[str, Any], df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Generate all KPIs based on the inferred schema.
    
    Args:
        schema: Inferred schema
        df: DataFrame
        
    Returns:
        List of all generated KPI dictionaries
    """
    all_kpis = []
    
    # Generate different types of KPIs
    all_kpis.extend(generate_aggregation_kpis(schema, df))
    all_kpis.extend(generate_time_series_kpis(schema, df))
    all_kpis.extend(generate_category_breakdown_kpis(schema, df))
    all_kpis.extend(generate_conversion_kpis(schema, df))
    all_kpis.extend(generate_advanced_kpis(schema, df))
    
    # Generate creative and pattern-based KPIs
    try:
        from .creative_kpis import generate_creative_kpis
        creative_kpis = generate_creative_kpis(df, schema)
        all_kpis.extend(creative_kpis)
    except Exception as e:
        # If creative KPIs fail, continue without them
        print(f"Warning: Could not generate creative KPIs: {e}")
    
    # Remove duplicates based on name
    seen_names = set()
    unique_kpis = []
    for kpi in all_kpis:
        if kpi['name'] not in seen_names:
            seen_names.add(kpi['name'])
            unique_kpis.append(kpi)
    
    return unique_kpis

