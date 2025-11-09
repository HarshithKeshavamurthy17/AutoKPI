"""
Chart Explanations Generator
Provides detailed explanations of what charts show and what the numbers mean
"""

from typing import Dict, Any
import pandas as pd
import numpy as np


def generate_chart_explanation(kpi: Dict[str, Any], df: pd.DataFrame) -> str:
    """
    Generate a detailed explanation of what the chart shows, what the numbers mean,
    and how to interpret them.
    
    Args:
        kpi: KPI dictionary
        df: DataFrame
        
    Returns:
        Detailed explanation string
    """
    category = kpi.get('category', '')
    column = kpi.get('column', '')
    group_by = kpi.get('group_by', '')
    sql_function = kpi.get('sql_function', 'AVG')
    kpi_name = kpi.get('name', 'This metric')
    
    explanation_parts = []
    
    # Aggregation KPIs
    if category == 'aggregation':
        if column and column in df.columns:
            if group_by and group_by in df.columns:
                # Breakdown chart (e.g., Average Price by Model)
                # Map SQL functions to pandas functions
                agg_func_map = {
                    'AVG': 'mean',
                    'SUM': 'sum',
                    'COUNT': 'count',
                    'MIN': 'min',
                    'MAX': 'max',
                    'MEDIAN': 'median',
                    'STD': 'std'
                }
                pandas_func = agg_func_map.get(sql_function.upper(), 'mean')
                breakdown = df.groupby(group_by)[column].agg(pandas_func)
                total_categories = len(breakdown)
                top_value = breakdown.max()
                bottom_value = breakdown.min()
                avg_value = breakdown.mean()
                top_category = breakdown.idxmax()
                bottom_category = breakdown.idxmin()
                range_value = top_value - bottom_value
                
                # Function name mapping for better readability
                func_name_map = {
                    'AVG': 'Average',
                    'SUM': 'Total',
                    'COUNT': 'Count',
                    'MIN': 'Minimum',
                    'MAX': 'Maximum',
                    'MEDIAN': 'Median',
                    'STD': 'Standard Deviation'
                }
                func_display = func_name_map.get(sql_function.upper(), sql_function)
                
                explanation_parts.append(f"## 📊 What This Chart Shows")
                explanation_parts.append(f"\nThis chart displays the **{func_display} {column.replace('_', ' ').title()}** for each **{group_by.replace('_', ' ').title()}** in your dataset.")
                explanation_parts.append(f"\n**Understanding the Bars:**")
                explanation_parts.append(f"- Each bar represents one {group_by.replace('_', ' ').title()}")
                explanation_parts.append(f"- The height of each bar shows the {func_display.lower()} {column.replace('_', ' ').title()} for that {group_by.replace('_', ' ').title()}")
                explanation_parts.append(f"- Bars are sorted from highest to lowest, making it easy to see top and bottom performers")
                explanation_parts.append(f"- Taller bars = higher values, shorter bars = lower values")
                
                explanation_parts.append(f"\n## 📈 What the Numbers Mean")
                
                explanation_parts.append(f"\n**Top Performer: {top_category}**")
                explanation_parts.append(f"- Value: **{top_value:,.2f}**")
                explanation_parts.append(f"- This is the {group_by.replace('_', ' ').title()} with the highest {func_display.lower()} {column.replace('_', ' ').title()}")
                if avg_value != 0:
                    explanation_parts.append(f"- It's **{((top_value - avg_value) / avg_value * 100):.1f}% above** the overall average of {avg_value:,.2f}")
                else:
                    explanation_parts.append(f"- The overall average is {avg_value:,.2f}")
                
                explanation_parts.append(f"\n**Bottom Performer: {bottom_category}**")
                explanation_parts.append(f"- Value: **{bottom_value:,.2f}**")
                explanation_parts.append(f"- This is the {group_by.replace('_', ' ').title()} with the lowest {func_display.lower()} {column.replace('_', ' ').title()}")
                if avg_value != 0:
                    explanation_parts.append(f"- It's **{((bottom_value - avg_value) / avg_value * 100):.1f}% below** the overall average")
                else:
                    explanation_parts.append(f"- Compare this to the average of {avg_value:,.2f}")
                
                explanation_parts.append(f"\n**Performance Gap:**")
                explanation_parts.append(f"- The difference between top and bottom is **{range_value:,.2f}**")
                if bottom_value != 0:
                    explanation_parts.append(f"- This represents a **{((range_value / bottom_value) * 100):.1f}% variation** across categories")
                else:
                    explanation_parts.append(f"- This shows significant variation across categories")
                explanation_parts.append(f"- Closing this gap could significantly impact your overall performance")
                explanation_parts.append(f"- If all categories performed at the top level, your total {column.replace('_', ' ').title()} would be {((top_value / avg_value - 1) * 100):.1f}% higher")
                
                explanation_parts.append(f"\n## 💡 How to Read This Chart")
                explanation_parts.append(f"\n1. **Identify Leaders**: Look at the tallest bars on the left—these are your top-performing {group_by.replace('_', ' ').title()}s")
                explanation_parts.append(f"2. **Find Opportunities**: Look at the shortest bars on the right—these have the most room for improvement")
                explanation_parts.append(f"3. **Compare to Average**: The overall average is {avg_value:,.2f}—use this as a benchmark")
                explanation_parts.append(f"4. **Understand Distribution**: If bars are similar in height, performance is consistent. If they vary widely, there's significant opportunity to improve underperformers")
                
            else:
                # Distribution chart
                values = df[column].dropna()
                mean_val = values.mean()
                median_val = values.median()
                std_val = values.std()
                min_val = values.min()
                max_val = values.max()
                q25 = values.quantile(0.25)
                q75 = values.quantile(0.75)
                
                explanation_parts.append(f"## 📊 What This Chart Shows")
                explanation_parts.append(f"\nThis histogram shows the **distribution** of {column.replace('_', ' ').title()} values across all {len(values):,} records in your dataset.")
                explanation_parts.append(f"\n**Understanding the Histogram:**")
                explanation_parts.append(f"- Each bar represents a range (or 'bin') of {column.replace('_', ' ').title()} values")
                explanation_parts.append(f"- The height of each bar shows how many records fall into that range")
                explanation_parts.append(f"- Taller bars = more records with values in that range")
                explanation_parts.append(f"- The shape of the histogram reveals patterns: normal distribution, skewed data, or multiple peaks")
                
                explanation_parts.append(f"\n## 📈 What the Numbers Mean")
                explanation_parts.append(f"\n**Central Tendency:**")
                explanation_parts.append(f"- **Mean (Average)**: {mean_val:,.2f} - This is the mathematical average of all values")
                explanation_parts.append(f"- **Median**: {median_val:,.2f} - This is the middle value when all values are sorted")
                explanation_parts.append(f"- If mean > median, your data is right-skewed (more high values). If mean < median, it's left-skewed (more low values)")
                
                explanation_parts.append(f"\n**Spread and Variability:**")
                explanation_parts.append(f"- **Range**: {min_val:,.2f} to {max_val:,.2f} (span of {max_val - min_val:,.2f})")
                explanation_parts.append(f"- **Standard Deviation**: {std_val:,.2f} - This measures how spread out the values are")
                explanation_parts.append(f"- A larger standard deviation means more variability in your data")
                explanation_parts.append(f"- **Interquartile Range (IQR)**: {q25:,.2f} to {q75:,.2f} - This contains the middle 50% of your data")
                
                explanation_parts.append(f"\n## 💡 How to Interpret This Chart")
                explanation_parts.append(f"\n1. **Distribution Shape**: ")
                if abs(mean_val - median_val) < std_val * 0.1:
                    explanation_parts.append(f"   - Your data appears roughly normally distributed (bell-shaped)")
                    explanation_parts.append(f"   - Most values cluster around the mean, with fewer extreme values")
                elif mean_val > median_val:
                    explanation_parts.append(f"   - Your data is **right-skewed** (tail extends to the right)")
                    explanation_parts.append(f"   - Most records have lower values, but some have very high values")
                    explanation_parts.append(f"   - The median ({median_val:,.2f}) is more representative than the mean ({mean_val:,.2f})")
                else:
                    explanation_parts.append(f"   - Your data is **left-skewed** (tail extends to the left)")
                    explanation_parts.append(f"   - Most records have higher values, but some have very low values")
                
                explanation_parts.append(f"\n2. **Variability Assessment**: ")
                if std_val / mean_val < 0.2:
                    explanation_parts.append(f"   - Low variability ({((std_val / mean_val) * 100):.1f}% coefficient of variation)")
                    explanation_parts.append(f"   - Values are relatively consistent across records")
                elif std_val / mean_val > 1.0:
                    explanation_parts.append(f"   - High variability ({((std_val / mean_val) * 100):.1f}% coefficient of variation)")
                    explanation_parts.append(f"   - Values vary dramatically—consider segmenting your analysis")
                else:
                    explanation_parts.append(f"   - Moderate variability ({((std_val / mean_val) * 100):.1f}% coefficient of variation)")
                    explanation_parts.append(f"   - Some variation is normal, but significant differences exist")
                
                explanation_parts.append(f"\n3. **Practical Meaning**: ")
                explanation_parts.append(f"   - **Most Common Range**: Look for the tallest bar(s)—this shows where most of your data falls")
                explanation_parts.append(f"   - **Outliers**: Values far from the main cluster may represent special cases or data quality issues")
                explanation_parts.append(f"   - **Business Context**: Consider what causes the distribution shape—is it expected or does it reveal opportunities?")
    
    # Comparative Analysis KPIs
    elif category == 'comparative_analysis':
        if group_by and group_by in df.columns and column and column in df.columns:
            breakdown = df.groupby(group_by)[column].mean()
            avg_value = df[column].mean()
            top_performer = breakdown.idxmax()
            bottom_performer = breakdown.idxmin()
            top_value = breakdown.max()
            bottom_value = breakdown.min()
            gap = top_value - bottom_value
            
            explanation_parts.append(f"## 📊 What This Chart Shows")
            explanation_parts.append(f"\nThis comparative bar chart shows how each **{group_by.replace('_', ' ').title()}** performs compared to the **overall average** ({avg_value:,.2f}) for {column.replace('_', ' ').title()}.")
            explanation_parts.append(f"\n**Understanding the Chart:**")
            explanation_parts.append(f"- Bars **above the average line** (in green/highlighted) = **outperformers**")
            explanation_parts.append(f"- Bars **below the average line** (in red/lower) = **underperformers**")
            explanation_parts.append(f"- The horizontal line shows the overall average—use this as your benchmark")
            explanation_parts.append(f"- The height of each bar shows how far above or below average each category performs")
            
            explanation_parts.append(f"\n## 📈 What the Numbers Mean")
            explanation_parts.append(f"\n**Performance Comparison:**")
            explanation_parts.append(f"- **{top_performer}**: {top_value:,.2f} ({(top_value - avg_value):+,.2f} from average, **{((top_value - avg_value) / avg_value * 100):+.1f}%** above)")
            explanation_parts.append(f"- **{bottom_performer}**: {bottom_value:,.2f} ({(bottom_value - avg_value):+,.2f} from average, **{((bottom_value - avg_value) / avg_value * 100):+.1f}%** below)")
            explanation_parts.append(f"- **Performance Gap**: {gap:,.2f} difference between top and bottom ({(gap / bottom_value * 100):.1f}% variation)")
            
            above_avg = (breakdown > avg_value).sum()
            below_avg = (breakdown < avg_value).sum()
            explanation_parts.append(f"\n**Distribution:**")
            explanation_parts.append(f"- {above_avg} {group_by.replace('_', ' ').title()}(s) **above average** ({(above_avg / len(breakdown) * 100):.1f}%)")
            explanation_parts.append(f"- {below_avg} {group_by.replace('_', ' ').title()}(s) **below average** ({(below_avg / len(breakdown) * 100):.1f}%)")
            
            explanation_parts.append(f"\n## 💡 How to Read This Chart")
            explanation_parts.append(f"\n1. **Identify Winners**: Categories with bars significantly above the average line are your best performers")
            explanation_parts.append(f"2. **Find Opportunities**: Categories below the average have the most potential for improvement")
            explanation_parts.append(f"3. **Measure Impact**: If you bring all underperformers to the average, your overall {column.replace('_', ' ').title()} would improve by approximately {((avg_value - breakdown[breakdown < avg_value].mean()) / avg_value * 100):.1f}%")
            explanation_parts.append(f"4. **Replicate Success**: Study what makes top performers successful and apply those strategies to underperformers")
    
    # Pattern Detection KPIs
    elif category == 'pattern_detection':
        subcategory = kpi.get('subcategory', '')
        
        if subcategory == 'weekly_seasonality' and group_by:
            if group_by in df.columns and column and column in df.columns:
                df['day_of_week'] = pd.to_datetime(df[group_by]).dt.day_name() if df[group_by].dtype == 'object' or 'datetime' in str(df[group_by].dtype) else df[group_by]
                daily_avg = df.groupby('day_of_week')[column].mean()
                overall_avg = df[column].mean()
                best_day = daily_avg.idxmax()
                worst_day = daily_avg.idxmin()
                best_value = daily_avg.max()
                worst_value = daily_avg.min()
                
                explanation_parts.append(f"## 📊 What This Chart Shows")
                explanation_parts.append(f"\nThis chart reveals the **weekly pattern** in your {column.replace('_', ' ').title()} data—showing how performance varies by day of the week.")
                explanation_parts.append(f"\n**Understanding the Pattern:**")
                explanation_parts.append(f"- Each bar represents one day of the week")
                explanation_parts.append(f"- The height shows the average {column.replace('_', ' ').title()} for that day")
                explanation_parts.append(f"- The horizontal line shows the overall weekly average")
                explanation_parts.append(f"- Days above the line = better than average, days below = worse than average")
                
                explanation_parts.append(f"\n## 📈 What the Numbers Mean")
                explanation_parts.append(f"\n**Peak Day: {best_day}**")
                explanation_parts.append(f"- Average: **{best_value:,.2f}**")
                explanation_parts.append(f"- This is **{((best_value - overall_avg) / overall_avg * 100):.1f}% above** the weekly average of {overall_avg:,.2f}")
                explanation_parts.append(f"- {best_day} consistently performs best across all weeks")
                
                explanation_parts.append(f"\n**Lowest Day: {worst_day}**")
                explanation_parts.append(f"- Average: **{worst_value:,.2f}**")
                explanation_parts.append(f"- This is **{((worst_value - overall_avg) / overall_avg * 100):.1f}% below** the weekly average")
                explanation_parts.append(f"- {worst_day} consistently performs lowest")
                
                explanation_parts.append(f"\n**Weekly Variation:**")
                explanation_parts.append(f"- The difference between best and worst day is **{best_value - worst_value:,.2f}**")
                explanation_parts.append(f"- This represents a **{((best_value - worst_value) / worst_value * 100):.1f}% swing** across the week")
                
                explanation_parts.append(f"\n## 💡 How to Use This Pattern")
                explanation_parts.append(f"\n1. **Optimize Scheduling**: Schedule important activities, campaigns, or promotions on {best_day} for maximum impact")
                explanation_parts.append(f"2. **Resource Allocation**: Allocate more resources (staff, inventory, marketing budget) to {best_day}")
                explanation_parts.append(f"3. **Improve Weak Days**: Investigate why {worst_day} performs lower and develop strategies to lift it")
                explanation_parts.append(f"4. **Predict Performance**: Use this pattern to forecast daily performance and plan accordingly")
    
    # Anomaly Detection KPIs
    elif category == 'anomaly_detection':
        if column and column in df.columns:
            values = df[column].dropna()
            mean_val = values.mean()
            std_val = values.std()
            z_scores = np.abs((values - mean_val) / std_val)
            anomalies = values[z_scores > 3]
            anomaly_count = len(anomalies)
            anomaly_pct = (anomaly_count / len(values)) * 100
            
            explanation_parts.append(f"## 📊 What This Chart Shows")
            explanation_parts.append(f"\nThis box plot identifies **statistical anomalies** (outliers) in your {column.replace('_', ' ').title()} data.")
            explanation_parts.append(f"\n**Understanding the Box Plot:**")
            explanation_parts.append(f"- **The Box**: Shows the interquartile range (IQR) containing the middle 50% of your data")
            explanation_parts.append(f"- **The Line in the Box**: Represents the median (middle value)")
            explanation_parts.append(f"- **The Whiskers**: Extend to show the range of 'normal' values (typically 1.5 × IQR)")
            explanation_parts.append(f"- **Points Outside Whiskers**: These are anomalies—values that are 3+ standard deviations from the mean")
            
            explanation_parts.append(f"\n## 📈 What the Numbers Mean")
            explanation_parts.append(f"\n**Anomaly Statistics:**")
            explanation_parts.append(f"- **Total Records**: {len(values):,}")
            explanation_parts.append(f"- **Anomalies Detected**: {anomaly_count:,} ({anomaly_pct:.2f}%)")
            explanation_parts.append(f"- **Normal Records**: {len(values) - anomaly_count:,} ({100 - anomaly_pct:.2f}%)")
            
            if anomaly_count > 0:
                explanation_parts.append(f"\n**Anomaly Characteristics:**")
                explanation_parts.append(f"- **Highest Anomaly**: {anomalies.max():,.2f} ({(anomalies.max() - mean_val):+,.2f} from mean)")
                explanation_parts.append(f"- **Lowest Anomaly**: {anomalies.min():,.2f} ({(anomalies.min() - mean_val):+,.2f} from mean)")
                explanation_parts.append(f"- **Mean of Normal Data**: {mean_val:,.2f}")
                explanation_parts.append(f"- **Standard Deviation**: {std_val:,.2f}")
            
            explanation_parts.append(f"\n## 💡 How to Interpret Anomalies")
            explanation_parts.append(f"\n**What Anomalies Could Mean:**")
            explanation_parts.append(f"1. **Data Quality Issues**: Typos, incorrect entries, or system errors")
            explanation_parts.append(f"2. **Exceptional Events**: One-time deals, special promotions, or unusual transactions")
            explanation_parts.append(f"3. **Fraud Indicators**: Suspiciously high or low values that don't fit normal patterns")
            explanation_parts.append(f"4. **Legitimate Outliers**: Rare but valid cases that represent unique opportunities or risks")
            
            explanation_parts.append(f"\n**Recommended Actions:**")
            if anomaly_pct > 10:
                explanation_parts.append(f"- **High anomaly rate ({anomaly_pct:.1f}%)**: Investigate each anomaly individually")
                explanation_parts.append(f"- Review data entry processes and quality controls")
                explanation_parts.append(f"- Determine if anomalies are errors (fix them) or exceptional cases (analyze separately)")
            elif anomaly_pct > 5:
                explanation_parts.append(f"- **Moderate anomaly rate ({anomaly_pct:.1f}%)**: Review a sample of anomalies")
                explanation_parts.append(f"- Consider creating separate analysis segments for normal vs. outlier data")
            else:
                explanation_parts.append(f"- **Low anomaly rate ({anomaly_pct:.1f}%)**: Your data is relatively clean")
                explanation_parts.append(f"- Anomalies are likely legitimate edge cases—analyze them separately if needed")
    
    # Distribution Analysis KPIs
    elif category == 'distribution_analysis':
        subcategory = kpi.get('subcategory', '')
        
        if subcategory == 'pareto' and column and column in df.columns:
            values = df[column].dropna().sort_values(ascending=False)
            total = values.sum()
            cumulative = values.cumsum()
            top_20_pct_count = int(len(values) * 0.2)
            top_20_value = cumulative.iloc[top_20_pct_count - 1] if top_20_pct_count > 0 else 0
            concentration = (top_20_value / total * 100) if total > 0 else 0
            
            explanation_parts.append(f"## 📊 What This Chart Shows")
            explanation_parts.append(f"\nThis Pareto chart demonstrates the **80/20 principle** (Pareto Principle) in your {column.replace('_', ' ').title()} data.")
            explanation_parts.append(f"\n**Understanding the Chart:**")
            explanation_parts.append(f"- **Bars (Left Axis)**: Show individual values sorted from highest to lowest")
            explanation_parts.append(f"- **Line (Right Axis)**: Shows cumulative percentage of total value")
            explanation_parts.append(f"- The line rising quickly = high concentration (few records drive most value)")
            explanation_parts.append(f"- If the line reaches 80% quickly, you have a strong 80/20 pattern")
            
            explanation_parts.append(f"\n## 📈 What the Numbers Mean")
            explanation_parts.append(f"\n**Concentration Analysis:**")
            explanation_parts.append(f"- **Top 20% of Records**: Contribute **{concentration:.1f}%** of total {column.replace('_', ' ').title()} value")
            explanation_parts.append(f"- **Total Value**: {total:,.2f}")
            explanation_parts.append(f"- **Top 20% Value**: {top_20_value:,.2f}")
            explanation_parts.append(f"- **Bottom 80% Value**: {total - top_20_value:,.2f} ({(100 - concentration):.1f}% of total)")
            
            if concentration > 80:
                explanation_parts.append(f"\n**Strong 80/20 Pattern Detected!**")
                explanation_parts.append(f"- This is a classic Pareto distribution")
                explanation_parts.append(f"- Just 20% of your records drive {concentration:.1f}% of your value")
                explanation_parts.append(f"- This is common in business: a small group of customers/products/transactions generates most revenue")
            elif concentration > 60:
                explanation_parts.append(f"\n**Moderate Concentration**")
                explanation_parts.append(f"- Some concentration exists, but not as extreme as 80/20")
                explanation_parts.append(f"- Value is somewhat concentrated in top performers")
            else:
                explanation_parts.append(f"\n**Even Distribution**")
                explanation_parts.append(f"- Value is more evenly distributed across records")
                explanation_parts.append(f"- Less concentration than typical Pareto patterns")
            
            explanation_parts.append(f"\n## 💡 Strategic Implications")
            explanation_parts.append(f"\n1. **Identify High-Value Segment**: Focus on the top 20%—these are your most important records")
            explanation_parts.append(f"2. **VIP Treatment**: Develop special programs, premium tiers, or dedicated resources for high-value segments")
            explanation_parts.append(f"3. **Protect Assets**: Ensure you're not losing high-value records—they drive most of your value")
            explanation_parts.append(f"4. **Replication Strategy**: Understand what makes top 20% special and find more like them")
            explanation_parts.append(f"5. **Efficiency**: Allocate resources proportionally—more investment in high-value segments")
    
    # Trend Analysis KPIs
    elif category == 'trend_analysis':
        if column and group_by and column in df.columns and group_by in df.columns:
            df_sorted = df.sort_values(group_by)
            midpoint = len(df_sorted) // 2
            first_half = df_sorted.iloc[:midpoint][column].mean()
            second_half = df_sorted.iloc[midpoint:][column].mean()
            change = ((second_half - first_half) / first_half * 100) if first_half != 0 else 0
            
            explanation_parts.append(f"## 📊 What This Chart Shows")
            explanation_parts.append(f"\nThis trend chart shows how {column.replace('_', ' ').title()} changes over time (by {group_by.replace('_', ' ').title()}).")
            explanation_parts.append(f"\n**Understanding the Trend:**")
            explanation_parts.append(f"- Each point represents a time period")
            explanation_parts.append(f"- The line connects points to show the trend direction")
            explanation_parts.append(f"- Upward slope = increasing trend, downward slope = decreasing trend")
            explanation_parts.append(f"- Flat line = stable, no significant change")
            
            explanation_parts.append(f"\n## 📈 What the Numbers Mean")
            explanation_parts.append(f"\n**Trend Comparison:**")
            explanation_parts.append(f"- **First Half Average**: {first_half:,.2f}")
            explanation_parts.append(f"- **Second Half Average**: {second_half:,.2f}")
            explanation_parts.append(f"- **Change**: {change:+.1f}% ({second_half - first_half:+,.2f} absolute change)")
            
            if change > 20:
                explanation_parts.append(f"\n**Strong Growth Trend** 📈")
                explanation_parts.append(f"- Significant increase of {change:.1f}% indicates strong positive momentum")
                explanation_parts.append(f"- This is substantial growth that suggests successful strategies or favorable conditions")
                explanation_parts.append(f"- Consider scaling what's working to accelerate growth further")
            elif change > 0:
                explanation_parts.append(f"\n**Positive Trend** ✅")
                explanation_parts.append(f"- Steady growth of {change:.1f}% shows consistent improvement")
                explanation_parts.append(f"- While not dramatic, this upward trend is a positive sign")
                explanation_parts.append(f"- Maintain current strategies and look for acceleration opportunities")
            elif change > -20:
                explanation_parts.append(f"\n**Declining Trend** ⚠️")
                explanation_parts.append(f"- Decrease of {abs(change):.1f}% requires attention")
                explanation_parts.append(f"- Investigate what changed between periods to understand the decline")
                explanation_parts.append(f"- Take corrective action to reverse the trend")
            else:
                explanation_parts.append(f"\n**Significant Decline** 📉")
                explanation_parts.append(f"- Major decrease of {abs(change):.1f}% is concerning")
                explanation_parts.append(f"- This requires immediate investigation and corrective action")
                explanation_parts.append(f"- Analyze root causes and implement fixes quickly")
            
            explanation_parts.append(f"\n## 💡 How to Use This Trend")
            explanation_parts.append(f"\n1. **Forecast Future**: Use this trend to project where {column.replace('_', ' ').title()} is heading")
            explanation_parts.append(f"2. **Set Goals**: Based on the trend, set realistic targets for the next period")
            explanation_parts.append(f"3. **Take Action**: If declining, investigate and fix. If growing, scale successful strategies")
            explanation_parts.append(f"4. **Monitor Closely**: Track this metric regularly to ensure the trend continues or reverses as desired")
    
    # Default explanation for other KPI types
    else:
        explanation_parts.append(f"## 📊 Chart Overview")
        explanation_parts.append(f"\nThis chart visualizes the **{kpi_name}** KPI from your dataset.")
        if column:
            explanation_parts.append(f"\n**Metric**: {column.replace('_', ' ').title()}")
        if group_by:
            explanation_parts.append(f"\n**Grouped By**: {group_by.replace('_', ' ').title()}")
        explanation_parts.append(f"\n**Interpretation**: Use this chart to understand patterns, trends, and relationships in your data.")
        explanation_parts.append(f"\n**Key Points**:")
        explanation_parts.append(f"- Compare values across different categories or time periods")
        explanation_parts.append(f"- Look for outliers, trends, or patterns")
        explanation_parts.append(f"- Identify top and bottom performers")
        explanation_parts.append(f"- Use insights to make data-driven decisions")
    
    return "\n".join(explanation_parts)

