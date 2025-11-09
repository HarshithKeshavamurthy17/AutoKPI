"""
Creative Insights Generator
Generates actionable insights and ideas from KPIs
"""

from typing import Dict, List, Any
import pandas as pd


def generate_kpi_insights(kpi: Dict[str, Any], df: pd.DataFrame) -> List[str]:
    """
    Generate creative insights and ideas for a KPI with storytelling.
    
    Args:
        kpi: KPI dictionary
        df: DataFrame
        
    Returns:
        List of insight strings with narrative
    """
    insights = []
    category = kpi.get('category', '')
    column = kpi.get('column')
    kpi_name = kpi.get('name', 'This metric')
    
    # Anomaly detection insights with story
    if category == 'anomaly_detection':
        anomaly_pct = kpi.get('anomaly_percentage', 0)
        anomaly_count = kpi.get('anomaly_count', 0)
        total_count = len(df) if column and column in df.columns else 0
        
        if anomaly_pct > 10:
            insights.append(f"🔍 **The Story**: Out of {total_count:,} records, {anomaly_count:,} ({anomaly_pct:.1f}%) are statistical anomalies—values that are 3+ standard deviations from the mean. This is unusually high and tells an important story.")
            insights.append(f"📊 **What This Means**: These outliers could be: (1) **Data quality issues**—typos, incorrect entries, or system errors; (2) **Exceptional events**—one-time deals, special promotions, or unusual transactions; (3) **Fraud indicators**—suspiciously high or low values that don't fit normal patterns.")
            insights.append(f"💡 **The Action**: Investigate these {anomaly_count:,} outlier records individually. If they're legitimate, they represent unique opportunities or risks. If they're errors, fixing them will improve your data quality significantly.")
        elif anomaly_pct > 5:
            insights.append(f"⚠️ **The Story**: {anomaly_pct:.1f}% of your data ({anomaly_count:,} out of {total_count:,} records) consists of statistical anomalies. This moderate level suggests a mix of normal variation and some unusual cases.")
            insights.append(f"📊 **What This Means**: Your data has some outliers that stand out from the crowd. These could be edge cases, special circumstances, or data entry variations.")
            insights.append(f"💡 **The Action**: Review a sample of these outliers to understand their nature. Consider creating separate analysis segments: one for 'normal' data and one for 'outlier' cases to see if they behave differently.")
        else:
            insights.append(f"✅ **The Story**: Only {anomaly_pct:.1f}% of your data ({anomaly_count:,} records) are statistical anomalies. This is a healthy sign—your data is relatively clean and consistent.")
            insights.append(f"📊 **What This Means**: The vast majority of your records follow expected patterns. The few outliers that exist are likely legitimate edge cases or minor variations.")
            insights.append(f"💡 **The Action**: You can confidently use standard statistical methods on this data. The small number of outliers won't significantly impact your analysis.")
    
    # Pattern detection insights with story
    elif category == 'pattern_detection':
        subcategory = kpi.get('subcategory', '')
        
        if subcategory == 'weekly_seasonality' and 'best_day' in kpi:
            best_day = kpi.get('best_day')
            worst_day = kpi.get('worst_day', '')
            best_value = kpi.get('best_value', 0)
            worst_value = kpi.get('worst_value', 0)
            
            insights.append(f"📅 **The Story**: Your data reveals a clear weekly rhythm. {best_day} consistently outperforms other days, with an average of {best_value:.2f} compared to {worst_day}'s {worst_value:.2f}—a difference that could be driving significant business impact.")
            insights.append(f"📊 **What This Means**: This pattern suggests day-of-week effects: customer behavior, operational factors, or market dynamics that vary by weekday. Understanding why {best_day} performs better can unlock opportunities across your entire week.")
            insights.append(f"💡 **The Action**: (1) **Schedule strategically**: Move important campaigns, product launches, or promotions to {best_day} for maximum impact. (2) **Investigate the why**: What makes {best_day} special? Is it customer availability, marketing timing, or operational efficiency? (3) **Replicate success**: Apply {best_day}'s winning factors to other days to lift overall performance.")
        
        if subcategory == 'monthly_seasonality' and 'best_month' in kpi:
            best_month = kpi.get('best_month')
            worst_month = kpi.get('worst_month', '')
            best_value = kpi.get('best_value', 0)
            worst_value = kpi.get('worst_value', 0)
            
            insights.append(f"🗓️ **The Story**: Your data tells a seasonal story. {best_month} emerges as your peak month with {best_value:.2f}, while {worst_month} is your slowest at {worst_value:.2f}. This seasonal pattern is a powerful planning tool.")
            insights.append(f"📊 **What This Means**: Seasonal variations are common in business—holidays, weather, fiscal cycles, or industry patterns create predictable ups and downs. Recognizing this pattern helps you prepare rather than react.")
            insights.append(f"💡 **The Action**: (1) **Plan ahead**: Build inventory, staffing, and marketing budgets around {best_month}'s peak demand. (2) **Create momentum**: Start campaigns 1-2 months before {best_month} to maximize the peak. (3) **Optimize slow periods**: Use {worst_month} for maintenance, training, or strategic planning when demand is lower.")
    
    # Comparative analysis insights with story
    elif category == 'comparative_analysis':
        group_by = kpi.get('group_by', 'category')
        column = kpi.get('column', 'metric')
        top_performer = kpi.get('top_performer', '')
        bottom_performer = kpi.get('bottom_performer', '')
        top_value = kpi.get('top_value', 0)
        bottom_value = kpi.get('bottom_value', 0)
        avg_value = kpi.get('avg_value', 0)
        top_performance_pct = kpi.get('top_performance_pct', 0)
        gap_percentage = kpi.get('gap_percentage', 0)
        
        if top_performer and bottom_performer:
            insights.append(f"🏆 **The Story**: When comparing {group_by.replace('_', ' ')}s, a clear winner emerges: **{top_performer}** achieves {top_value:.2f} in {column.replace('_', ' ')} while **{bottom_performer}** only reaches {bottom_value:.2f}. This {gap_percentage:.1f}% gap represents both a challenge and an opportunity.")
            insights.append(f"📊 **What This Means**: The performance difference between your best and worst {group_by.replace('_', ' ')}s is substantial. {top_performer} has discovered something that works—whether it's strategy, execution, market positioning, or operational efficiency. Understanding this difference is key to improving overall performance.")
            insights.append(f"💡 **The Action**: (1) **Study the champion**: Conduct a deep-dive analysis of {top_performer}. What are they doing differently? Document their processes, strategies, and characteristics. (2) **Create a playbook**: Turn {top_performer}'s success into actionable guidelines that can be applied elsewhere. (3) **Close the gap**: Focus on bringing {bottom_performer} (and other underperformers) closer to {top_performer}'s level. Even moving them halfway would significantly improve your overall {column.replace('_', ' ')}.")
        
        if top_performance_pct > 20:
            insights.append(f"🚀 **Exceptional Opportunity**: {top_performer} is performing {top_performance_pct:.1f}% above the average. This isn't just good performance—it's exceptional. If you can replicate even 50% of this advantage across all {group_by.replace('_', ' ')}s, your overall {column.replace('_', ' ')} would increase dramatically.")
        elif top_performance_pct > 10:
            insights.append(f"✅ **Strong Performance**: {top_performer} exceeds the average by {top_performance_pct:.1f}%. This represents a clear best practice that should be studied and replicated.")
        
        if gap_percentage > 50:
            insights.append(f"📊 **The Opportunity**: The {gap_percentage:.1f}% gap between top and bottom performers is significant. Closing this gap by bringing underperformers to even the median level could improve your overall {column.replace('_', ' ')} by {gap_percentage/2:.1f}% or more.")
    
    # Distribution analysis insights with story
    elif category == 'distribution_analysis':
        subcategory = kpi.get('subcategory', '')
        column = kpi.get('column', 'metric')
        
        if subcategory == 'pareto' and 'concentration_percentage' in kpi:
            conc = kpi.get('concentration_percentage', 0)
            total_value = df[column].sum() if column and column in df.columns else 0
            
            if conc > 80:
                top_20_value = total_value * (conc / 100)
                insights.append(f"📈 **The Story**: The famous 80/20 rule is alive and well in your data! Just 20% of your records are driving {conc:.1f}% of your total {column.replace('_', ' ')} value (approximately {top_20_value:,.2f} out of {total_value:,.2f}). This is a powerful concentration pattern.")
                insights.append(f"📊 **What This Means**: Your business has a clear 'power user' or 'high-value' segment. These top 20% are your most important customers/products/transactions. Understanding what makes them special and how to find more like them is crucial for growth.")
                insights.append(f"💡 **The Action**: (1) **Identify the top 20%**: Create a list of these high-value records and analyze their characteristics. What do they have in common? (2) **Create VIP treatment**: Develop special programs, premium tiers, or dedicated resources for this segment. (3) **Find more like them**: Use the characteristics of the top 20% to identify and acquire similar high-value records. (4) **Protect your assets**: Ensure you're not losing these high-value segments—they're driving most of your value!")
            elif conc > 60:
                insights.append(f"⚖️ **The Story**: Your {column.replace('_', ' ')} shows moderate concentration ({conc:.1f}%)—value is somewhat concentrated in a subset of records, but not as extreme as the classic 80/20 pattern.")
                insights.append(f"📊 **What This Means**: You have distinct value tiers in your data. Some records are clearly more valuable than others, suggesting opportunities for segmentation and tiered strategies.")
                insights.append(f"💡 **The Action**: Consider creating segmentation strategies: (1) **High-value tier**: Premium service, dedicated resources, special offers. (2) **Mid-value tier**: Standard service with growth opportunities. (3) **Low-value tier**: Efficient, automated service with potential to move up.")
        
        if subcategory == 'variability' and 'coefficient_of_variation' in kpi:
            cv = kpi.get('coefficient_of_variation', 0)
            mean_value = df[column].mean() if column and column in df.columns else 0
            std_value = df[column].std() if column and column in df.columns else 0
            
            if cv > 100:
                insights.append(f"📉 **The Story**: Your {column.replace('_', ' ')} has high variability (CV: {cv:.1f}%). The standard deviation ({std_value:.2f}) is larger than the mean ({mean_value:.2f}), meaning values vary dramatically across your records.")
                insights.append(f"📊 **What This Means**: Your data isn't uniform—you have a diverse mix of high and low values. This variability suggests different segments, use cases, or behavior patterns that should be analyzed separately.")
                insights.append(f"💡 **The Action**: (1) **Segment your data**: Group records by similar {column.replace('_', ' ')} values to understand different patterns. (2) **Cluster analysis**: Use clustering techniques to identify natural groups. (3) **Separate strategies**: Develop different approaches for high-value vs. low-value segments. (4) **Understand the drivers**: What causes some records to have high {column.replace('_', ' ')} while others have low?")
        
        if subcategory == 'skewness' and 'skewness_value' in kpi:
            skew = kpi.get('skewness_value', 0)
            if abs(skew) > 2:
                direction = "right" if skew > 0 else "left"
                insights.append(f"📊 **The Story**: Your {column.replace('_', ' ')} distribution is highly skewed ({skew:.2f}), meaning most values cluster on one side with a long tail on the {direction}.")
                insights.append(f"📊 **What This Means**: The distribution isn't normal—most records have similar values, but a few have very different (much higher or lower) values. This affects how you should analyze and interpret the data.")
                insights.append(f"💡 **The Action**: (1) **Use median instead of mean**: The median is less affected by outliers. (2) **Consider log transformation**: For highly skewed data, log transformation can normalize the distribution for better analysis. (3) **Separate analysis**: Analyze the 'normal' segment and the 'tail' segment separately. (4) **Understand the tail**: What makes the tail values different? They might represent a distinct segment.")
    
    # Trend analysis insights with story
    elif category == 'trend_analysis':
        if 'change_percentage' in kpi:
            change = kpi.get('change_percentage', 0)
            first_half = kpi.get('first_half_avg', 0)
            second_half = kpi.get('second_half_avg', 0)
            column = kpi.get('column', 'metric')
            
            if change > 20:
                insights.append(f"📈 **The Story**: Your {column.replace('_', ' ')} tells a growth story. It increased from {first_half:.2f} in the first half to {second_half:.2f} in the second half—a {change:.1f}% increase. This is strong, consistent growth.")
                insights.append(f"📊 **What This Means**: Something is working well. Whether it's market conditions, your strategies, operational improvements, or external factors, this positive trend represents momentum you should capitalize on.")
                insights.append(f"💡 **The Action**: (1) **Identify the drivers**: What changed between the first and second half? Document the factors driving this growth. (2) **Double down**: Invest more in the strategies that are working. (3) **Scale**: If this growth is sustainable, consider scaling operations, marketing, or resources to accelerate further. (4) **Forecast**: Use this trend to project future performance and set ambitious but realistic goals.")
            elif change < -20:
                insights.append(f"📉 **The Story**: Your {column.replace('_', ' ')} shows a concerning decline. It decreased from {first_half:.2f} in the first half to {second_half:.2f} in the second half—a {abs(change):.1f}% decrease. This requires immediate attention.")
                insights.append(f"📊 **What This Means**: A decline of this magnitude suggests something significant has changed—market conditions, competitive pressure, operational issues, or strategic misalignment. Understanding the root cause is critical.")
                insights.append(f"💡 **The Action**: (1) **Investigate immediately**: Conduct a root cause analysis. What changed? When did it start? (2) **Compare periods**: Analyze what was different between the first and second half. (3) **Take corrective action**: Based on findings, implement fixes quickly. (4) **Monitor closely**: Track this metric daily/weekly to ensure the decline stops and reverses.")
            elif change > 0:
                insights.append(f"✅ **The Story**: Your {column.replace('_', ' ')} shows steady positive growth ({change:.1f}% increase from {first_half:.2f} to {second_half:.2f}). While not dramatic, this consistent upward trend is a good sign.")
                insights.append(f"📊 **What This Means**: You're on the right track. The growth may be gradual, but it's consistent and sustainable. This is often healthier than volatile spikes.")
                insights.append(f"💡 **The Action**: (1) **Maintain momentum**: Continue current strategies that are working. (2) **Look for acceleration opportunities**: Identify ways to increase the growth rate. (3) **Monitor**: Keep tracking to ensure the trend continues. (4) **Set goals**: Use this trend to set realistic growth targets for the next period.")
    
    # Time series insights
    elif category == 'time_series':
        insights.append(f"⏰ **Time-Based Analysis**: This KPI shows how the metric changes over time. Use this to identify trends, seasonality, and forecast future performance.")
        insights.append(f"💡 **Action Idea**: Create time-based alerts for significant changes. Set up monitoring for this metric.")
    
    # Category breakdown insights
    elif category == 'category_breakdown':
        insights.append(f"🏷️ **Category Analysis**: This shows how the metric varies across different categories. Use this to identify top and bottom performers.")
        insights.append(f"💡 **Action Idea**: Focus resources on high-performing categories and investigate ways to improve underperforming ones.")
    
    return insights


def generate_creative_ideas(kpis: List[Dict[str, Any]], df: pd.DataFrame, schema: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Generate creative ideas and recommendations based on KPIs.
    
    Args:
        kpis: List of KPI dictionaries
        df: DataFrame
        schema: Inferred schema
        
    Returns:
        List of creative idea dictionaries
    """
    ideas = []
    
    # Find top performing categories
    categorical_cols = schema.get('categorical_columns', [])
    numeric_cols = schema.get('numeric_columns', [])
    
    if categorical_cols and numeric_cols:
        for cat_col in categorical_cols[:2]:
            for num_col in numeric_cols:
                category_means = df.groupby(cat_col)[num_col].mean().sort_values(ascending=False)
                if len(category_means) >= 2:
                    top = category_means.index[0]
                    second = category_means.index[1]
                    gap = ((category_means.iloc[0] - category_means.iloc[1]) / category_means.iloc[1] * 100) if category_means.iloc[1] != 0 else 0
                    
                    if gap > 10:
                        ideas.append({
                            'type': 'opportunity',
                            'title': f'Learn from {top}',
                            'description': f'{top} outperforms {second} by {gap:.1f}% in {num_col}. Study what makes {top} successful and apply those lessons to other categories.',
                            'priority': 'high',
                            'action': f'Conduct analysis on {top} vs {second} to identify success factors'
                        })
    
    # Find trend opportunities
    datetime_cols = schema.get('datetime_columns', [])
    if datetime_cols and numeric_cols:
        ideas.append({
            'type': 'analysis',
            'title': 'Forecast Future Trends',
            'description': f'With {len(datetime_cols)} date column(s) and {len(numeric_cols)} metric(s), you can build forecasting models to predict future performance.',
            'priority': 'medium',
            'action': 'Consider time series forecasting or regression analysis'
        })
    
    # Segmentation ideas
    if len(categorical_cols) >= 2 and numeric_cols:
        ideas.append({
            'type': 'analysis',
            'title': 'Multi-Dimensional Segmentation',
            'description': f'Combine {len(categorical_cols)} categorical dimensions to create detailed customer or product segments for targeted analysis.',
            'priority': 'medium',
            'action': 'Create segmentation analysis combining multiple categories'
        })
    
    return ideas

