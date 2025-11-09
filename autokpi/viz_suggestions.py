"""
Visualization suggestions and chart generation
Recommends chart types and generates previews for each KPI
"""

from typing import Dict, Any, List, Optional
import pandas as pd
import altair as alt


def suggest_chart_type(kpi: Dict[str, Any]) -> str:
    """
    Suggest an appropriate chart type for a KPI.
    
    Args:
        kpi: KPI dictionary
        
    Returns:
        Chart type: 'metric', 'line', 'bar', 'pie', 'area', 'histogram', 'box', 'heatmap', 'sparkline'
    """
    category = kpi.get('category', 'aggregation')
    subcategory = kpi.get('subcategory', '')
    
    # Creative KPI categories
    if category == 'anomaly_detection':
        return 'box'  # Box plot for anomaly visualization
    elif category == 'pattern_detection':
        if subcategory == 'weekly_seasonality' or subcategory == 'monthly_seasonality':
            return 'bar'  # Bar chart for seasonality patterns
        else:
            return 'line'
    elif category == 'comparative_analysis':
        return 'bar'  # Bar chart for comparisons
    elif category == 'distribution_analysis':
        if subcategory == 'skewness' or subcategory == 'pareto':
            return 'histogram'  # Histogram for distributions
        else:
            return 'box'
    elif category == 'trend_analysis':
        if subcategory == 'breakpoint':
            return 'line'  # Line chart with breakpoint
        else:
            return 'line'
    # Original categories
    elif category == 'aggregation' and subcategory in ['sum', 'avg', 'min', 'max', 'count', 'count_distinct']:
        return 'metric'
    elif category == 'statistical':
        if subcategory == 'percentile':
            return 'histogram'
        else:
            return 'metric'
    elif category == 'ratio':
        return 'metric'
    elif category == 'growth':
        return 'line'
    elif category == 'time_series':
        return 'line'
    elif category == 'category_breakdown':
        if kpi.get('sql_function') == 'COUNT' and subcategory == 'distribution':
            return 'pie'
        else:
            return 'bar'
    elif category == 'conversion':
        if subcategory == 'distribution':
            return 'pie'
        elif subcategory == 'rate':
            return 'metric'
        else:
            return 'bar'
    else:
        return 'bar'  # Default fallback


def generate_chart(kpi: Dict[str, Any], df: pd.DataFrame, table_name: str = "your_table") -> Optional[Any]:
    """
    Generate an Altair chart for a KPI.
    
    Args:
        kpi: KPI dictionary
        df: DataFrame
        table_name: Name of the table (not used, but kept for consistency)
        
    Returns:
        Altair chart object or None if chart cannot be generated
    """
    chart_type = suggest_chart_type(kpi)
    category = kpi.get('category', 'aggregation')
    
    try:
        # Handle aggregation KPIs first - show meaningful comparisons
        if category == 'aggregation':
            column = kpi.get('column')
            sql_function = kpi.get('sql_function', 'AVG')
            
            if column and column in df.columns:
                # Find categorical columns for meaningful breakdown
                categorical_cols = [col for col in df.columns 
                                  if col != column 
                                  and (df[col].dtype == 'object' or df[col].dtype.name == 'category')
                                  and df[col].nunique() < 50  # Limit to reasonable number
                                  and df[col].nunique() > 1]  # Must have multiple categories
                
                # If there are categorical columns and it's an AVG function, show average by category
                if categorical_cols and sql_function == 'AVG':
                    # Use the first categorical column for breakdown
                    group_by_col = categorical_cols[0]
                    chart_df = df.groupby(group_by_col)[column].mean().reset_index()
                    chart_df.columns = [group_by_col, 'average_value']
                    chart_df = chart_df.sort_values('average_value', ascending=False).head(15)
                    
                    if len(chart_df) > 0:
                        chart = alt.Chart(chart_df).mark_bar(color='#667eea').encode(
                            x=alt.X('average_value:Q', title=f'Average {column.replace("_", " ").title()}'),
                            y=alt.Y(f'{group_by_col}:N', title=group_by_col.replace('_', ' ').title(), sort='-x'),
                            tooltip=[alt.Tooltip(f'{group_by_col}:N', title=group_by_col.replace('_', ' ').title()),
                                    alt.Tooltip('average_value:Q', format='.2f', title='Average')]
                        ).properties(
                            title=f'Average {column.replace("_", " ").title()} by {group_by_col.replace("_", " ").title()}',
                            width=600,
                            height=max(300, len(chart_df) * 30)
                        )
                        return chart
                
                # For other functions or no categorical columns, show distribution
                data = df[column].dropna()
                if len(data) > 0:
                    # Calculate the metric value
                    if sql_function == 'AVG':
                        metric_value = data.mean()
                    elif sql_function == 'SUM':
                        metric_value = data.sum()
                    elif sql_function == 'MIN':
                        metric_value = data.min()
                    elif sql_function == 'MAX':
                        metric_value = data.max()
                    else:
                        metric_value = data.mean()
                    
                    # Create a distribution chart
                    chart_df = pd.DataFrame({'value': data.values})
                    
                    # Smart binning
                    data_min = data.min()
                    data_max = data.max()
                    data_range = data_max - data_min
                    num_bins = min(30, max(10, int(len(data) / 20))) if data_range > 0 else 10
                    bin_step = data_range / num_bins if data_range > 0 else 1
                    
                    chart = alt.Chart(chart_df).mark_bar(
                        opacity=0.7,
                        color='#667eea',
                        stroke='white',
                        strokeWidth=0.5
                    ).encode(
                        x=alt.X('value:Q', 
                               bin=alt.Bin(step=bin_step, extent=[data_min, data_max]),
                               title=column.replace('_', ' ').title()),
                        y=alt.Y('count()', title='Frequency'),
                        tooltip=[alt.Tooltip('value:Q', bin=True, title='Range'), 
                                alt.Tooltip('count()', title='Count')]
                    ).properties(
                        title=f'{column.replace("_", " ").title()} Distribution ({sql_function}: {metric_value:.2f})',
                        width=600,
                        height=300
                    )
                    return chart
        
        if chart_type == 'metric':
            # Metric cards - try to show comparison if possible
            return None
        
        elif chart_type == 'line':
            # Time series line chart
            datetime_col = kpi.get('group_by')
            numeric_col = kpi.get('column')
            
            if datetime_col and numeric_col and datetime_col in df.columns and numeric_col in df.columns:
                # Convert datetime column
                df_copy = df.copy()
                df_copy[datetime_col] = pd.to_datetime(df_copy[datetime_col], errors='coerce')
                df_copy = df_copy.dropna(subset=[datetime_col, numeric_col])
                
                if len(df_copy) == 0:
                    return None
                
                # Aggregate by date
                if kpi.get('group_by_function') == 'DATE' or kpi.get('subcategory') == 'daily':
                    df_copy['date'] = df_copy[datetime_col].dt.date
                    chart_df = df_copy.groupby('date')[numeric_col].sum().reset_index()
                    chart_df.columns = ['date', 'value']
                    chart_df = chart_df.sort_values('date')
                else:
                    df_copy['month'] = df_copy[datetime_col].dt.to_period('M').astype(str)
                    chart_df = df_copy.groupby('month')[numeric_col].sum().reset_index()
                    chart_df.columns = ['month', 'value']
                    chart_df = chart_df.sort_values('month')
                
                if len(chart_df) == 0:
                    return None
                
                x_col = 'date' if 'date' in chart_df.columns else 'month'
                chart = alt.Chart(chart_df).mark_line(point=True).encode(
                    x=alt.X(x_col, title=x_col.replace('_', ' ').title()),
                    y=alt.Y('value', title=numeric_col.replace('_', ' ').title())
                ).properties(
                    title=kpi['name'],
                    width=600,
                    height=300
                )
                return chart
        
        elif chart_type == 'bar':
            # Bar chart for category breakdown
            cat_col = kpi.get('group_by')
            numeric_col = kpi.get('column')
            
            if cat_col and cat_col in df.columns:
                if numeric_col and numeric_col in df.columns:
                    # Sum or average by category
                    if kpi.get('sql_function') == 'AVG':
                        chart_df = df.groupby(cat_col)[numeric_col].mean().reset_index()
                    else:
                        chart_df = df.groupby(cat_col)[numeric_col].sum().reset_index()
                    chart_df.columns = [cat_col, 'value']
                    chart_df = chart_df.sort_values('value', ascending=False).head(10)
                else:
                    # Count by category
                    chart_df = df[cat_col].value_counts().head(10).reset_index()
                    chart_df.columns = [cat_col, 'value']
                
                if len(chart_df) == 0:
                    return None
                
                chart = alt.Chart(chart_df).mark_bar().encode(
                    x=alt.X('value', title='Value'),
                    y=alt.Y(cat_col, title=cat_col.replace('_', ' ').title(), sort='-x')
                ).properties(
                    title=kpi['name'],
                    width=600,
                    height=300
                )
                return chart
        
        elif chart_type == 'pie':
            # Pie chart for distribution
            cat_col = kpi.get('group_by')
            
            if cat_col and cat_col in df.columns:
                chart_df = df[cat_col].value_counts().head(10).reset_index()
                chart_df.columns = [cat_col, 'value']
                
                if len(chart_df) == 0:
                    return None
                
                chart = alt.Chart(chart_df).mark_arc(innerRadius=50).encode(
                    theta=alt.Theta('value', type='quantitative'),
                    color=alt.Color(cat_col, type='nominal', legend=alt.Legend(title=cat_col.replace('_', ' ').title()))
                ).properties(
                    title=kpi['name'],
                    width=400,
                    height=400
                )
                return chart
        
        # Creative KPI visualizations
        if category == 'anomaly_detection':
            column = kpi.get('column')
            if column and column in df.columns:
                # Box plot for anomaly detection
                chart_data = pd.DataFrame({
                    'value': df[column].dropna(),
                    'type': 'Normal'
                })
                
                # Identify outliers
                Q1 = chart_data['value'].quantile(0.25)
                Q3 = chart_data['value'].quantile(0.75)
                IQR = Q3 - Q1
                chart_data.loc[(chart_data['value'] < (Q1 - 1.5 * IQR)) | 
                               (chart_data['value'] > (Q3 + 1.5 * IQR)), 'type'] = 'Outlier'
                
                chart = alt.Chart(chart_data).mark_boxplot(extent='min-max').encode(
                    y=alt.Y('value', title=column.replace('_', ' ').title()),
                    color=alt.Color('type', scale=alt.Scale(domain=['Normal', 'Outlier'], 
                           range=['#3b82f6', '#ef4444']))
                ).properties(
                    title=kpi['name'],
                    width=400,
                    height=300
                )
                return chart
        
        elif category == 'pattern_detection':
            subcategory = kpi.get('subcategory', '')
            if subcategory == 'weekly_seasonality':
                datetime_col = kpi.get('columns_used', [])[1] if len(kpi.get('columns_used', [])) > 1 else None
                numeric_col = kpi.get('column')
                
                if datetime_col and numeric_col and datetime_col in df.columns and numeric_col in df.columns:
                    df_copy = df.copy()
                    df_copy[datetime_col] = pd.to_datetime(df_copy[datetime_col], errors='coerce')
                    df_copy = df_copy.dropna(subset=[datetime_col, numeric_col])
                    
                    df_copy['day_of_week'] = df_copy[datetime_col].dt.day_name()
                    chart_df = df_copy.groupby('day_of_week')[numeric_col].mean().reset_index()
                    chart_df.columns = ['day', 'value']
                    
                    # Order days
                    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                    chart_df['day'] = pd.Categorical(chart_df['day'], categories=day_order, ordered=True)
                    chart_df = chart_df.sort_values('day')
                    
                    chart = alt.Chart(chart_df).mark_bar(color='#667eea').encode(
                        x=alt.X('day', title='Day of Week', sort=day_order),
                        y=alt.Y('value', title=numeric_col.replace('_', ' ').title())
                    ).properties(
                        title=kpi['name'],
                        width=600,
                        height=300
                    )
                    return chart
        
        elif category == 'comparative_analysis':
            group_by = kpi.get('group_by')
            column = kpi.get('column')
            
            if group_by and column and group_by in df.columns and column in df.columns:
                # Calculate category means and overall average
                category_means = df.groupby(group_by)[column].mean().reset_index()
                category_means.columns = [group_by, 'value']
                overall_avg = df[column].mean()
                
                # Calculate percentage difference from average
                category_means['pct_diff'] = ((category_means['value'] - overall_avg) / overall_avg * 100) if overall_avg != 0 else 0
                category_means = category_means.sort_values('pct_diff', ascending=False).head(10)
                
                # Highlight top and bottom performers
                category_means['highlight'] = 'Normal'
                if len(category_means) > 0:
                    category_means.loc[category_means.index[0], 'highlight'] = 'Top'
                    category_means.loc[category_means.index[-1], 'highlight'] = 'Bottom'
                
                # Add average line
                avg_line = pd.DataFrame({
                    group_by: ['Average'],
                    'value': [overall_avg],
                    'pct_diff': [0],
                    'highlight': ['Average']
                })
                
                # Create bar chart
                bars = alt.Chart(category_means).mark_bar().encode(
                    x=alt.X('value', title=column.replace('_', ' ').title()),
                    y=alt.Y(group_by, title=group_by.replace('_', ' ').title(), sort='-x'),
                    color=alt.Color('highlight', scale=alt.Scale(
                        domain=['Top', 'Bottom', 'Normal'],
                        range=['#10b981', '#ef4444', '#94a3b8']
                    ), legend=None),
                    tooltip=[group_by, alt.Tooltip('value', format='.2f'), 
                            alt.Tooltip('pct_diff', format='+.1f', title='% from Avg')]
                )
                
                # Add average reference line
                avg_rule = alt.Chart(pd.DataFrame({'avg': [overall_avg]})).mark_rule(
                    color='#f59e0b',
                    strokeDash=[5, 5],
                    strokeWidth=2
                ).encode(x='avg:Q')
                
                chart = (bars + avg_rule).properties(
                    title=f"{kpi['name']} (Avg: {overall_avg:.2f})",
                    width=600,
                    height=max(300, len(category_means) * 30)
                )
                return chart
        
        elif category == 'distribution_analysis':
            subcategory = kpi.get('subcategory', '')
            column = kpi.get('column')
            
            if subcategory == 'pareto' and column and column in df.columns:
                # Create Pareto chart
                sorted_data = df[column].dropna().sort_values(ascending=False)
                cumulative_pct = (sorted_data.cumsum() / sorted_data.sum() * 100)
                
                chart_df = pd.DataFrame({
                    'rank': range(1, len(sorted_data) + 1),
                    'value': sorted_data.values,
                    'cumulative_pct': cumulative_pct.values
                })
                
                base = alt.Chart(chart_df.head(20)).encode(
                    x=alt.X('rank:O', title='Rank')
                )
                
                bars = base.mark_bar(color='#667eea').encode(
                    y=alt.Y('value', title=column.replace('_', ' ').title())
                )
                
                line = base.mark_line(color='#ef4444', point=True).encode(
                    y=alt.Y('cumulative_pct', title='Cumulative %', axis=alt.Axis(format='%'))
                )
                
                chart = alt.layer(bars, line).resolve_scale(
                    y='independent'
                ).properties(
                    title=kpi['name'],
                    width=600,
                    height=300
                )
                return chart
            
            elif (subcategory == 'skewness' or subcategory == 'variability') and column and column in df.columns:
                # Create histogram for distribution with better binning
                data = df[column].dropna()
                if len(data) > 0:
                    # Use smart binning based on data range
                    data_min = data.min()
                    data_max = data.max()
                    data_range = data_max - data_min
                    
                    # Determine appropriate number of bins
                    if data_range > 0:
                        num_bins = min(30, max(10, int(len(data) / 20)))
                        bin_step = data_range / num_bins
                    else:
                        num_bins = 10
                        bin_step = 1
                    
                    chart = alt.Chart(pd.DataFrame({'value': data.values})).mark_bar(
                        opacity=0.7,
                        color='#667eea',
                        stroke='white',
                        strokeWidth=0.5
                    ).encode(
                        x=alt.X('value:Q', 
                               bin=alt.Bin(step=bin_step, extent=[data_min, data_max]),
                               title=column.replace('_', ' ').title()),
                        y=alt.Y('count()', title='Frequency'),
                        tooltip=[alt.Tooltip('value:Q', bin=True, title='Range'), 
                                alt.Tooltip('count()', title='Count')]
                    ).properties(
                        title=f'{kpi["name"]} - Distribution Histogram',
                        width=600,
                        height=300
                    )
                    return chart
        
    except Exception as e:
        # If chart generation fails, return None
        print(f"Error generating chart for {kpi['name']}: {str(e)}")
        return None
    
    return None


def create_sparkline(data: pd.Series, title: str = "") -> Optional[Any]:
    """
    Create a sparkline chart for time series data.
    
    Args:
        data: Series with time series data
        title: Chart title
        
    Returns:
        Altair chart or None
    """
    if len(data) == 0:
        return None
    
    chart_df = pd.DataFrame({
        'index': range(len(data)),
        'value': data.values
    })
    
    chart = alt.Chart(chart_df).mark_line(
        color='#667eea',
        strokeWidth=2
    ).encode(
        x=alt.X('index:Q', axis=None),
        y=alt.Y('value:Q', axis=None)
    ).properties(
        width=200,
        height=50,
        title=title
    )
    
    return chart


def create_gauge_chart(value: float, min_val: float, max_val: float, title: str = "") -> Optional[Any]:
    """
    Create a gauge/speedometer style chart.
    
    Args:
        value: Current value
        min_val: Minimum value
        max_val: Maximum value
        title: Chart title
        
    Returns:
        Altair chart or None
    """
    # Normalize value to 0-100
    normalized = ((value - min_val) / (max_val - min_val) * 100) if (max_val - min_val) != 0 else 50
    
    # Create semi-circle gauge
    gauge_df = pd.DataFrame({
        'angle': [0, 180],
        'value': [normalized, 100 - normalized]
    })
    
    chart = alt.Chart(gauge_df).mark_arc(innerRadius=40, outerRadius=50).encode(
        theta=alt.Theta('value:Q', stack=True),
        color=alt.Color('angle:N', scale=alt.Scale(
            domain=['0', '180'],
            range=['#10b981', '#e5e7eb']
        ), legend=None)
    ).properties(
        width=150,
        height=100,
        title=title
    )
    
    return chart


def get_chart_suggestions(kpis: List[Dict[str, Any]]) -> Dict[str, str]:
    """
    Get chart type suggestions for all KPIs.
    
    Args:
        kpis: List of KPI dictionaries
        
    Returns:
        Dictionary mapping KPI names to chart types
    """
    suggestions = {}
    for kpi in kpis:
        suggestions[kpi['name']] = suggest_chart_type(kpi)
    
    return suggestions

