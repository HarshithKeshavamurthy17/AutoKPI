"""
Export functions for KPIs
Exports KPIs to JSON, Markdown, and Dashboard Spec formats
"""

import json
from typing import Dict, List, Any
from datetime import datetime
from .sql_generator import generate_sql_queries
from .viz_suggestions import get_chart_suggestions


def export_to_json(kpis: List[Dict[str, Any]], schema: Dict[str, Any], 
                   table_name: str = "your_table") -> str:
    """
    Export KPIs to JSON format.
    
    Args:
        kpis: List of KPI dictionaries
        schema: Inferred schema
        table_name: Name of the table
        
    Returns:
        JSON string
    """
    sql_queries = generate_sql_queries(kpis, table_name)
    chart_suggestions = get_chart_suggestions(kpis)
    
    export_data = {
        'metadata': {
            'export_date': datetime.now().isoformat(),
            'table_name': table_name,
            'total_kpis': len(kpis),
            'schema': schema
        },
        'kpis': []
    }
    
    for kpi in kpis:
        kpi_export = {
            'name': kpi.get('name', ''),
            'description': kpi.get('description', ''),
            'category': kpi.get('category', ''),
            'subcategory': kpi.get('subcategory', ''),
            'difficulty': kpi.get('difficulty', 'easy'),
            'columns_used': kpi.get('columns_used', []),
            'logic': kpi.get('logic', ''),
            'sql_query': sql_queries.get(kpi.get('name', ''), ''),
            'chart_type': chart_suggestions.get(kpi.get('name', ''), 'bar'),
            'refined_by_llm': kpi.get('refined_by_llm', False)
        }
        export_data['kpis'].append(kpi_export)
    
    return json.dumps(export_data, indent=2)


def export_to_markdown(kpis: List[Dict[str, Any]], schema: Dict[str, Any],
                       table_name: str = "your_table", dataset_name: str = "Dataset") -> str:
    """
    Export KPIs to Markdown format.
    
    Args:
        kpis: List of KPI dictionaries
        schema: Inferred schema
        table_name: Name of the table
        dataset_name: Name of the dataset
        
    Returns:
        Markdown string
    """
    sql_queries = generate_sql_queries(kpis, table_name)
    chart_suggestions = get_chart_suggestions(kpis)
    
    md_lines = [
        f"# KPI Catalogue – {dataset_name}",
        "",
        f"**Export Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Table Name:** `{table_name}`",
        f"**Total KPIs:** {len(kpis)}",
        "",
        "---",
        ""
    ]
    
    # Group KPIs by category
    kpis_by_category = {}
    for kpi in kpis:
        category = kpi.get('category', 'other')
        if category not in kpis_by_category:
            kpis_by_category[category] = []
        kpis_by_category[category].append(kpi)
    
    # Export each category
    for category, category_kpis in kpis_by_category.items():
        md_lines.append(f"## {category.replace('_', ' ').title()} KPIs")
        md_lines.append("")
        
        for i, kpi in enumerate(category_kpis, 1):
            kpi_name = kpi.get('name', f'KPI {i}')
            kpi_description = kpi.get('description', '')
            sql_query = sql_queries.get(kpi_name, '')
            chart_type = chart_suggestions.get(kpi_name, 'bar')
            columns_used = kpi.get('columns_used', [])
            difficulty = kpi.get('difficulty', 'easy')
            
            md_lines.append(f"### {i}. {kpi_name}")
            md_lines.append("")
            md_lines.append(f"- **Description:** {kpi_description}")
            md_lines.append(f"- **Category:** {category.replace('_', ' ').title()}")
            md_lines.append(f"- **Difficulty:** {difficulty.title()}")
            md_lines.append(f"- **Columns Used:** {', '.join(columns_used) if columns_used else 'N/A'}")
            md_lines.append(f"- **Chart Type:** {chart_type.replace('_', ' ').title()}")
            if kpi.get('refined_by_llm'):
                md_lines.append(f"- **Refined by LLM:** Yes")
            md_lines.append("")
            md_lines.append("**SQL Query:**")
            md_lines.append("```sql")
            md_lines.append(sql_query)
            md_lines.append("```")
            md_lines.append("")
            md_lines.append("---")
            md_lines.append("")
    
    return "\n".join(md_lines)


def export_to_dashboard_spec(kpis: List[Dict[str, Any]], schema: Dict[str, Any],
                             table_name: str = "your_table") -> str:
    """
    Export KPIs to Dashboard Spec format (JSON for BI tools).
    
    Args:
        kpis: List of KPI dictionaries
        schema: Inferred schema
        table_name: Name of the table
        
    Returns:
        JSON string in dashboard spec format
    """
    sql_queries = generate_sql_queries(kpis, table_name)
    chart_suggestions = get_chart_suggestions(kpis)
    
    # Map chart types to BI tool chart types
    chart_type_mapping = {
        'metric': 'kpi_card',
        'line': 'line_chart',
        'bar': 'bar_chart',
        'pie': 'pie_chart',
        'area': 'area_chart'
    }
    
    dashboard_spec = {
        'dashboard_name': f'AutoKPI Dashboard - {table_name}',
        'version': '1.0',
        'created_at': datetime.now().isoformat(),
        'data_source': {
            'type': 'table',
            'name': table_name
        },
        'widgets': []
    }
    
    # Group KPIs by category for dashboard layout
    kpis_by_category = {}
    for kpi in kpis:
        category = kpi.get('category', 'other')
        if category not in kpis_by_category:
            kpis_by_category[category] = []
        kpis_by_category[category].append(kpi)
    
    widget_id = 1
    for category, category_kpis in kpis_by_category.items():
        # Add section header
        dashboard_spec['widgets'].append({
            'id': f'section_{category}',
            'type': 'text',
            'title': f'{category.replace("_", " ").title()} KPIs',
            'content': f'This section contains {len(category_kpis)} KPIs related to {category}.'
        })
        
        # Add KPIs as widgets
        for kpi in category_kpis:
            kpi_name = kpi.get('name', '')
            chart_type = chart_suggestions.get(kpi_name, 'bar')
            bi_chart_type = chart_type_mapping.get(chart_type, 'bar_chart')
            
            widget = {
                'id': f'widget_{widget_id}',
                'type': bi_chart_type,
                'title': kpi_name,
                'description': kpi.get('description', ''),
                'sql_query': sql_queries.get(kpi_name, ''),
                'columns': kpi.get('columns_used', []),
                'category': category,
                'difficulty': kpi.get('difficulty', 'easy')
            }
            
            dashboard_spec['widgets'].append(widget)
            widget_id += 1
    
    return json.dumps(dashboard_spec, indent=2)



