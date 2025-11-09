"""
SQL query generator for KPIs
Generates human-readable SQL queries for each KPI
"""

from typing import Dict, Any, Optional
from .utils import sanitize_column_name


def generate_sql_query(kpi: Dict[str, Any], table_name: str = "your_table") -> str:
    """
    Generate a SQL query for a given KPI.
    
    Args:
        kpi: KPI dictionary
        table_name: Name of the table (default: "your_table")
        
    Returns:
        SQL query string
    """
    category = kpi.get('category', 'aggregation')
    sql_function = kpi.get('sql_function', 'SUM')
    column = kpi.get('column')
    group_by = kpi.get('group_by')
    group_by_function = kpi.get('group_by_function')
    
    # Sanitize column names
    column_sanitized = None
    group_by_sanitized = None
    if column:
        column_sanitized = sanitize_column_name(column)
    if group_by:
        group_by_sanitized = sanitize_column_name(group_by)
    
    # Base SELECT clause
    if category == 'aggregation':
        if sql_function == 'COUNT' and column is None:
            # Count all records
            select_clause = 'SELECT COUNT(*) AS total_records'
        elif sql_function == 'COUNT_DISTINCT':
            select_clause = f'SELECT COUNT(DISTINCT "{column_sanitized}") AS {sql_function.lower()}_{column_sanitized}'
        else:
            # SUM, AVG, MIN, MAX
            select_clause = f'SELECT {sql_function}("{column_sanitized}") AS {sql_function.lower()}_{column_sanitized}'
    
    elif category == 'time_series':
        if group_by_function == 'DATE':
            # Use DATE() function (works in MySQL, SQLite, PostgreSQL)
            # Note: Syntax may vary by database, this is a generic template
            select_clause = f'SELECT DATE("{group_by_sanitized}") AS day, {sql_function}("{column_sanitized}") AS total_{column_sanitized}'
        elif group_by_function == 'YEAR':
            # Use YEAR function for year-only columns
            select_clause = f'SELECT YEAR("{group_by_sanitized}") AS year, {sql_function}("{column_sanitized}") AS total_{column_sanitized}'
        elif group_by_function == 'YEAR_MONTH':
            # Use YEAR and MONTH functions (works in MySQL, SQL Server)
            # Alternative: DATE_FORMAT for MySQL, TO_CHAR for PostgreSQL
            select_clause = f'SELECT YEAR("{group_by_sanitized}") AS year, MONTH("{group_by_sanitized}") AS month, {sql_function}("{column_sanitized}") AS total_{column_sanitized}'
        else:
            select_clause = f'SELECT DATE("{group_by_sanitized}") AS day, {sql_function}("{column_sanitized}") AS total_{column_sanitized}'
    
    elif category == 'category_breakdown':
        if sql_function == 'COUNT':
            select_clause = f'SELECT "{group_by_sanitized}", COUNT(*) AS count'
        else:
            select_clause = f'SELECT "{group_by_sanitized}", {sql_function}("{column_sanitized}") AS total_{column_sanitized}'
    
    elif category == 'conversion':
        if not group_by_sanitized:
            # Fallback if group_by is not set
            select_clause = 'SELECT COUNT(*) AS count'
        elif kpi.get('subcategory') == 'distribution':
            select_clause = f'SELECT "{group_by_sanitized}", COUNT(*) AS count'
        elif kpi.get('subcategory') == 'rate':
            status_values = kpi.get('status_values', [])
            if status_values and group_by_sanitized:
                select_clause = f'SELECT (COUNT(CASE WHEN "{group_by_sanitized}" = \'{status_values[0]}\' THEN 1 END) * 100.0 / COUNT(*)) AS conversion_rate'
            else:
                select_clause = f'SELECT "{group_by_sanitized}", COUNT(*) AS count'
        else:
            select_clause = f'SELECT "{group_by_sanitized}", COUNT(*) AS count'
    
    elif category == 'statistical':
        if sql_function == 'MEDIAN':
            select_clause = f'SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY "{column_sanitized}") AS median_{column_sanitized}'
        elif sql_function == 'PERCENTILE':
            percentile = kpi.get('percentile', 50) / 100
            select_clause = f'SELECT PERCENTILE_CONT({percentile}) WITHIN GROUP (ORDER BY "{column_sanitized}") AS p{kpi.get("percentile", 50)}_{column_sanitized}'
        else:
            select_clause = f'SELECT {sql_function}("{column_sanitized}") AS {sql_function.lower()}_{column_sanitized}'
    
    elif category == 'ratio':
        denominator = kpi.get('denominator')
        if denominator and column:
            denominator_sanitized = sanitize_column_name(denominator)
            select_clause = f'SELECT SUM("{column_sanitized}") / SUM("{denominator_sanitized}") AS {column_sanitized}_to_{denominator_sanitized}_ratio'
        else:
            select_clause = 'SELECT COUNT(*) AS count'
    
    elif category == 'growth':
        # Growth rate requires window functions
        select_clause = f'SELECT DATE("{group_by_sanitized}") AS period, {sql_function}("{column_sanitized}") AS value, (({sql_function}("{column_sanitized}") - LAG({sql_function}("{column_sanitized}")) OVER (ORDER BY DATE("{group_by_sanitized}"))) / LAG({sql_function}("{column_sanitized}")) OVER (ORDER BY DATE("{group_by_sanitized}")) * 100) AS growth_rate'
    
    elif category == 'anomaly_detection':
        if sql_function == 'ANOMALY_RATE':
            select_clause = f'SELECT (COUNT(CASE WHEN ABS(({column_sanitized} - AVG({column_sanitized})) / STDDEV({column_sanitized})) > 3 THEN 1 END) * 100.0 / COUNT(*)) AS anomaly_rate'
        elif sql_function == 'OUTLIER_DETECTION':
            select_clause = f'SELECT COUNT(CASE WHEN {column_sanitized} < (Q1 - 1.5 * IQR) OR {column_sanitized} > (Q3 + 1.5 * IQR) THEN 1 END) AS outlier_count, COUNT(*) AS total_count'
        else:
            select_clause = f'SELECT COUNT(*) AS count'
    
    elif category == 'pattern_detection':
        if sql_function == 'WEEKLY_PATTERN':
            select_clause = f'SELECT DAYOFWEEK("{group_by_sanitized}") AS day_of_week, AVG("{column_sanitized}") AS avg_value'
        elif sql_function == 'MONTHLY_PATTERN':
            select_clause = f'SELECT MONTH("{group_by_sanitized}") AS month, AVG("{column_sanitized}") AS avg_value'
        else:
            select_clause = f'SELECT AVG("{column_sanitized}") AS avg_value'
    
    elif category == 'comparative_analysis':
        if sql_function == 'COMPARATIVE':
            select_clause = f'SELECT "{group_by_sanitized}", AVG("{column_sanitized}") AS avg_value, (AVG("{column_sanitized}") - (SELECT AVG("{column_sanitized}") FROM {table_name})) * 100.0 / (SELECT AVG("{column_sanitized}") FROM {table_name}) AS pct_diff_from_avg'
        elif sql_function == 'PERFORMANCE_GAP':
            select_clause = f'SELECT MAX(AVG("{column_sanitized}")) - MIN(AVG("{column_sanitized}")) AS performance_gap FROM {table_name} GROUP BY "{group_by_sanitized}"'
        else:
            select_clause = f'SELECT "{group_by_sanitized}", AVG("{column_sanitized}") AS avg_value'
    
    elif category == 'distribution_analysis':
        if sql_function == 'SKEWNESS':
            select_clause = f'SELECT (3 * (AVG("{column_sanitized}") - PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY "{column_sanitized}"))) / STDDEV("{column_sanitized}") AS skewness'
        elif sql_function == 'CONCENTRATION':
            select_clause = f'SELECT (SUM(CASE WHEN rn <= CEIL(COUNT(*) * 0.2) THEN "{column_sanitized}" ELSE 0 END) * 100.0 / SUM("{column_sanitized}")) AS concentration_pct FROM (SELECT "{column_sanitized}", ROW_NUMBER() OVER (ORDER BY "{column_sanitized}" DESC) AS rn FROM {table_name}) ranked'
        elif sql_function == 'VARIABILITY':
            select_clause = f'SELECT (STDDEV("{column_sanitized}") / AVG("{column_sanitized}") * 100) AS coefficient_of_variation'
        else:
            select_clause = f'SELECT AVG("{column_sanitized}") AS avg_value'
    
    elif category == 'trend_analysis':
        if sql_function == 'TREND_CHANGE':
            select_clause = f'SELECT AVG(CASE WHEN DATE("{group_by_sanitized}") <= (SELECT DATE("{group_by_sanitized}") FROM {table_name} ORDER BY DATE("{group_by_sanitized}") LIMIT 1 OFFSET (SELECT COUNT(*) / 2 FROM {table_name})) THEN "{column_sanitized}" END) AS first_half_avg, AVG(CASE WHEN DATE("{group_by_sanitized}") > (SELECT DATE("{group_by_sanitized}") FROM {table_name} ORDER BY DATE("{group_by_sanitized}") LIMIT 1 OFFSET (SELECT COUNT(*) / 2 FROM {table_name})) THEN "{column_sanitized}" END) AS second_half_avg'
        else:
            select_clause = f'SELECT DATE("{group_by_sanitized}") AS period, AVG("{column_sanitized}") AS avg_value'
    
    else:
        # Default fallback
        select_clause = 'SELECT COUNT(*) AS count'
    
    # FROM clause
    from_clause = f'FROM {table_name}'
    
    # GROUP BY clause
    group_by_clause = ''
    if category in ['anomaly_detection', 'distribution_analysis'] and sql_function not in ['CONCENTRATION']:
        # No GROUP BY for these
        group_by_clause = ''
    elif category == 'pattern_detection':
        if sql_function == 'WEEKLY_PATTERN':
            group_by_clause = f'GROUP BY DAYOFWEEK("{group_by_sanitized}")'
        elif sql_function == 'MONTHLY_PATTERN':
            group_by_clause = f'GROUP BY MONTH("{group_by_sanitized}")'
        elif group_by:
            if group_by_function == 'DATE':
                group_by_clause = f'GROUP BY DATE("{group_by_sanitized}")'
            else:
                group_by_clause = f'GROUP BY "{group_by_sanitized}"'
    elif category == 'comparative_analysis':
        if group_by:
            group_by_clause = f'GROUP BY "{group_by_sanitized}"'
    elif category == 'trend_analysis':
        # No GROUP BY for trend analysis (uses window functions or subqueries)
        group_by_clause = ''
    elif group_by and category != 'growth':
        if group_by_function == 'DATE':
            group_by_clause = f'GROUP BY DATE("{group_by_sanitized}")'
        elif group_by_function == 'YEAR_MONTH':
            group_by_clause = f'GROUP BY YEAR("{group_by_sanitized}"), MONTH("{group_by_sanitized}")'
        else:
            group_by_clause = f'GROUP BY "{group_by_sanitized}"'
    elif category == 'growth' and group_by:
        if group_by_function == 'DATE':
            group_by_clause = f'GROUP BY DATE("{group_by_sanitized}")'
        elif group_by_function == 'YEAR_MONTH':
            group_by_clause = f'GROUP BY YEAR("{group_by_sanitized}"), MONTH("{group_by_sanitized}")'
        else:
            group_by_clause = f'GROUP BY DATE("{group_by_sanitized}")'
    
    # ORDER BY clause
    order_by_clause = ''
    if category == 'pattern_detection':
        if sql_function == 'WEEKLY_PATTERN':
            order_by_clause = 'ORDER BY day_of_week'
        elif sql_function == 'MONTHLY_PATTERN':
            order_by_clause = 'ORDER BY month'
    elif category == 'comparative_analysis':
        if sql_function == 'COMPARATIVE':
            order_by_clause = 'ORDER BY pct_diff_from_avg DESC'
        elif sql_function == 'PERFORMANCE_GAP':
            order_by_clause = 'ORDER BY performance_gap DESC'
    elif category == 'time_series':
        if group_by_function == 'DATE':
            order_by_clause = 'ORDER BY day'
        elif group_by_function == 'YEAR':
            order_by_clause = 'ORDER BY year'
        elif group_by_function == 'YEAR_MONTH':
            order_by_clause = 'ORDER BY year, month'
    elif category == 'growth':
        order_by_clause = 'ORDER BY period'
    elif category == 'category_breakdown':
        if sql_function == 'COUNT':
            order_by_clause = 'ORDER BY count DESC'
        else:
            order_by_clause = f'ORDER BY total_{column_sanitized} DESC'
    elif category == 'conversion' and kpi.get('subcategory') == 'distribution':
        order_by_clause = 'ORDER BY count DESC'
    
    # Combine all clauses
    query_parts = [select_clause, from_clause]
    if group_by_clause:
        query_parts.append(group_by_clause)
    if order_by_clause:
        query_parts.append(order_by_clause)
    
    sql_query = '\n'.join(query_parts) + ';'
    
    return sql_query


def generate_sql_queries(kpis: list, table_name: str = "your_table") -> Dict[str, str]:
    """
    Generate SQL queries for all KPIs.
    
    Args:
        kpis: List of KPI dictionaries
        table_name: Name of the table
        
    Returns:
        Dictionary mapping KPI names to SQL queries
    """
    sql_queries = {}
    for kpi in kpis:
        kpi_name = kpi['name']
        sql_queries[kpi_name] = generate_sql_query(kpi, table_name)
    
    return sql_queries

