"""
Data Quality Assessment Module
Provides comprehensive data quality checks and scoring
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from .schema_inference import infer_schema


def check_data_quality(df: pd.DataFrame, schema: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Perform comprehensive data quality assessment.
    
    Args:
        df: DataFrame
        schema: Optional pre-computed schema
        
    Returns:
        Dictionary with data quality metrics
    """
    if schema is None:
        from .schema_inference import infer_schema
        schema = infer_schema(df)
    
    quality_report = {
        'overall_score': 0.0,
        'dimensions': {},
        'issues': [],
        'recommendations': []
    }
    
    total_rows = len(df)
    total_columns = len(df.columns)
    
    # 1. Completeness Check
    completeness_score = check_completeness(df)
    quality_report['dimensions']['completeness'] = completeness_score
    
    # 2. Uniqueness Check
    uniqueness_score = check_uniqueness(df, schema)
    quality_report['dimensions']['uniqueness'] = uniqueness_score
    
    # 3. Consistency Check
    consistency_score = check_consistency(df, schema)
    quality_report['dimensions']['consistency'] = consistency_score
    
    # 4. Validity Check
    validity_score = check_validity(df, schema)
    quality_report['dimensions']['validity'] = validity_score
    
    # 5. Accuracy Check (outlier detection)
    accuracy_score = check_accuracy(df, schema)
    quality_report['dimensions']['accuracy'] = accuracy_score
    
    # Calculate overall score (weighted average)
    weights = {
        'completeness': 0.25,
        'uniqueness': 0.15,
        'consistency': 0.20,
        'validity': 0.20,
        'accuracy': 0.20
    }
    
    overall_score = sum(
        quality_report['dimensions'][dim]['score'] * weights.get(dim, 0)
        for dim in quality_report['dimensions']
    )
    
    quality_report['overall_score'] = round(overall_score, 2)
    
    # Generate issues and recommendations
    quality_report['issues'] = identify_issues(df, schema, quality_report)
    quality_report['recommendations'] = generate_recommendations(quality_report)
    
    return quality_report


def check_completeness(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Check data completeness (missing values).
    
    Returns:
        Dictionary with completeness metrics
    """
    total_cells = len(df) * len(df.columns)
    missing_cells = df.isna().sum().sum()
    completeness_ratio = 1 - (missing_cells / total_cells) if total_cells > 0 else 1.0
    
    missing_by_column = df.isna().sum().to_dict()
    missing_percentage_by_column = (df.isna().sum() / len(df) * 100).to_dict()
    
    # Identify columns with high missing values
    problematic_columns = [
        col for col, pct in missing_percentage_by_column.items()
        if pct > 10
    ]
    
    return {
        'score': round(completeness_ratio * 100, 2),
        'total_cells': total_cells,
        'missing_cells': int(missing_cells),
        'missing_percentage': round((missing_cells / total_cells * 100) if total_cells > 0 else 0, 2),
        'missing_by_column': missing_by_column,
        'missing_percentage_by_column': missing_percentage_by_column,
        'problematic_columns': problematic_columns
    }


def check_uniqueness(df: pd.DataFrame, schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check data uniqueness (duplicates).
    
    Returns:
        Dictionary with uniqueness metrics
    """
    # Check for duplicate rows
    duplicate_rows = df.duplicated().sum()
    duplicate_percentage = (duplicate_rows / len(df) * 100) if len(df) > 0 else 0
    
    # Check for duplicate IDs
    id_columns = schema.get('id_columns', [])
    duplicate_ids = {}
    for id_col in id_columns:
        if id_col in df.columns:
            duplicates = df[id_col].duplicated().sum()
            duplicate_ids[id_col] = {
                'count': int(duplicates),
                'percentage': round((duplicates / len(df) * 100) if len(df) > 0 else 0, 2)
            }
    
    uniqueness_ratio = 1 - (duplicate_rows / len(df)) if len(df) > 0 else 1.0
    
    return {
        'score': round(uniqueness_ratio * 100, 2),
        'duplicate_rows': int(duplicate_rows),
        'duplicate_percentage': round(duplicate_percentage, 2),
        'duplicate_ids': duplicate_ids,
        'unique_rows': len(df) - duplicate_rows
    }


def check_consistency(df: pd.DataFrame, schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check data consistency (data types, formats).
    
    Returns:
        Dictionary with consistency metrics
    """
    issues = []
    numeric_cols = schema.get('numeric_columns', [])
    datetime_cols = schema.get('datetime_columns', [])
    
    # Check for inconsistent data types
    for col in numeric_cols:
        if col in df.columns:
            # Check for non-numeric values in numeric columns
            non_numeric = pd.to_numeric(df[col], errors='coerce').isna().sum() - df[col].isna().sum()
            if non_numeric > 0:
                issues.append({
                    'column': col,
                    'issue': 'non_numeric_values',
                    'count': int(non_numeric)
                })
    
    # Check datetime consistency
    for col in datetime_cols:
        if col in df.columns:
            try:
                pd.to_datetime(df[col], errors='raise')
            except:
                issues.append({
                    'column': col,
                    'issue': 'invalid_datetime_format',
                    'count': 'unknown'
                })
    
    consistency_score = max(0, 100 - (len(issues) * 10))
    
    return {
        'score': round(consistency_score, 2),
        'issues': issues,
        'issues_count': len(issues)
    }


def check_validity(df: pd.DataFrame, schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check data validity (value ranges, constraints).
    
    Returns:
        Dictionary with validity metrics
    """
    issues = []
    numeric_cols = schema.get('numeric_columns', [])
    
    # Check for negative values in columns that shouldn't have them
    for col in numeric_cols:
        if col in df.columns:
            negative_count = (df[col] < 0).sum()
            if negative_count > 0 and any(keyword in col.lower() for keyword in ['count', 'quantity', 'amount', 'price', 'revenue']):
                issues.append({
                    'column': col,
                    'issue': 'negative_values',
                    'count': int(negative_count)
                })
    
    # Check for zero values in columns that shouldn't have them
    for col in numeric_cols:
        if col in df.columns:
            zero_count = (df[col] == 0).sum()
            if zero_count > len(df) * 0.5:  # More than 50% zeros
                issues.append({
                    'column': col,
                    'issue': 'excessive_zeros',
                    'count': int(zero_count),
                    'percentage': round((zero_count / len(df) * 100), 2)
                })
    
    validity_score = max(0, 100 - (len(issues) * 15))
    
    return {
        'score': round(validity_score, 2),
        'issues': issues,
        'issues_count': len(issues)
    }


def check_accuracy(df: pd.DataFrame, schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check data accuracy (outliers, anomalies).
    
    Returns:
        Dictionary with accuracy metrics
    """
    from .advanced_analytics import detect_outliers
    
    outlier_info = {}
    numeric_cols = schema.get('numeric_columns', [])
    
    total_outliers = 0
    total_values = 0
    
    for col in numeric_cols:
        outliers = detect_outliers(df, col)
        if outliers:
            outlier_info[col] = outliers
            total_outliers += outliers.get('total_outliers', 0)
            total_values += len(df[col].dropna())
    
    outlier_percentage = (total_outliers / total_values * 100) if total_values > 0 else 0
    accuracy_score = max(0, 100 - (outlier_percentage * 0.5))  # Penalize outliers
    
    return {
        'score': round(accuracy_score, 2),
        'outlier_info': outlier_info,
        'total_outliers': total_outliers,
        'outlier_percentage': round(outlier_percentage, 2)
    }


def identify_issues(df: pd.DataFrame, schema: Dict[str, Any], 
                   quality_report: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Identify data quality issues.
    
    Returns:
        List of issue dictionaries
    """
    issues = []
    
    # Completeness issues
    completeness = quality_report['dimensions'].get('completeness', {})
    for col, pct in completeness.get('missing_percentage_by_column', {}).items():
        if pct > 10:
            issues.append({
                'severity': 'high' if pct > 50 else 'medium',
                'type': 'missing_values',
                'column': col,
                'message': f'{col} has {pct:.1f}% missing values',
                'impact': 'high' if pct > 50 else 'medium'
            })
    
    # Uniqueness issues
    uniqueness = quality_report['dimensions'].get('uniqueness', {})
    if uniqueness.get('duplicate_rows', 0) > 0:
        issues.append({
            'severity': 'medium',
            'type': 'duplicate_rows',
            'message': f'{uniqueness["duplicate_rows"]} duplicate rows found',
            'impact': 'medium'
        })
    
    # Consistency issues
    consistency = quality_report['dimensions'].get('consistency', {})
    for issue in consistency.get('issues', []):
        issues.append({
            'severity': 'medium',
            'type': 'consistency',
            'column': issue.get('column'),
            'message': f'{issue.get("column")} has {issue.get("issue")}',
            'impact': 'medium'
        })
    
    # Accuracy issues
    accuracy = quality_report['dimensions'].get('accuracy', {})
    for col, outlier_data in accuracy.get('outlier_info', {}).items():
        if outlier_data.get('outlier_percentage', 0) > 5:
            issues.append({
                'severity': 'low',
                'type': 'outliers',
                'column': col,
                'message': f'{col} has {outlier_data["outlier_percentage"]:.1f}% outliers',
                'impact': 'low'
            })
    
    return issues


def generate_recommendations(quality_report: Dict[str, Any]) -> List[str]:
    """
    Generate recommendations for improving data quality.
    
    Returns:
        List of recommendation strings
    """
    recommendations = []
    
    overall_score = quality_report.get('overall_score', 0)
    
    if overall_score < 70:
        recommendations.append("⚠️ Data quality is below optimal. Consider data cleaning before analysis.")
    
    # Completeness recommendations
    completeness = quality_report['dimensions'].get('completeness', {})
    problematic_cols = completeness.get('problematic_columns', [])
    if problematic_cols:
        recommendations.append(f"📊 Consider imputation or removal of columns with high missing values: {', '.join(problematic_cols[:3])}")
    
    # Uniqueness recommendations
    uniqueness = quality_report['dimensions'].get('uniqueness', {})
    if uniqueness.get('duplicate_rows', 0) > 0:
        recommendations.append(f"🔄 Remove {uniqueness['duplicate_rows']} duplicate rows to improve data quality")
    
    # Consistency recommendations
    consistency = quality_report['dimensions'].get('consistency', {})
    if consistency.get('issues_count', 0) > 0:
        recommendations.append("🔧 Fix data type inconsistencies in the identified columns")
    
    # Accuracy recommendations
    accuracy = quality_report['dimensions'].get('accuracy', {})
    if accuracy.get('outlier_percentage', 0) > 10:
        recommendations.append("📈 Review outliers - they may indicate data entry errors or require separate analysis")
    
    if not recommendations:
        recommendations.append("✅ Data quality is good! Ready for analysis.")
    
    return recommendations



