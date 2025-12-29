"""
Utility functions for AutoKPI
"""

import pandas as pd
import re
from typing import List, Dict, Any, Optional


def load_dataset(file_path: str) -> pd.DataFrame:
    """
    Load a dataset from CSV or Excel file.
    
    Args:
        file_path: Path to the file (CSV or Excel)
        
    Returns:
        DataFrame with the loaded data
    """
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith(('.xlsx', '.xls')):
        return pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Please upload a CSV or Excel file.")


def sanitize_column_name(column: str) -> str:
    """
    Sanitize column names for SQL usage.
    
    Args:
        column: Original column name
        
    Returns:
        Sanitized column name
    """
    # Replace spaces with underscores and remove special characters
    sanitized = re.sub(r'[^a-zA-Z0-9_]', '_', str(column))
    # Remove leading/trailing underscores
    sanitized = sanitized.strip('_')
    # Ensure it starts with a letter or underscore
    if sanitized and not sanitized[0].isalpha() and sanitized[0] != '_':
        sanitized = '_' + sanitized
    return sanitized if sanitized else 'col_' + str(hash(column))[:8]


def detect_column_pattern(column_name: str, patterns: List[str]) -> bool:
    """
    Check if a column name matches any of the given patterns.
    
    Args:
        column_name: Name of the column
        patterns: List of regex patterns to match
        
    Returns:
        True if any pattern matches
    """
    column_lower = str(column_name).lower()
    for pattern in patterns:
        if re.search(pattern, column_lower, re.IGNORECASE):
            return True
    return False


def get_numeric_summary(df: pd.DataFrame, column: str) -> Dict[str, Any]:
    """
    Get summary statistics for a numeric column.
    
    Args:
        df: DataFrame
        column: Column name
        
    Returns:
        Dictionary with summary statistics
    """
    return {
        'min': float(df[column].min()) if not df[column].isna().all() else None,
        'max': float(df[column].max()) if not df[column].isna().all() else None,
        'mean': float(df[column].mean()) if not df[column].isna().all() else None,
        'median': float(df[column].median()) if not df[column].isna().all() else None,
        'std': float(df[column].std()) if not df[column].isna().all() else None,
        'null_count': int(df[column].isna().sum()),
        'null_percentage': float(df[column].isna().sum() / len(df) * 100)
    }


def get_categorical_summary(df: pd.DataFrame, column: str) -> Dict[str, Any]:
    """
    Get summary statistics for a categorical column.
    
    Args:
        df: DataFrame
        column: Column name
        
    Returns:
        Dictionary with summary statistics
    """
    value_counts = df[column].value_counts()
    return {
        'unique_count': int(df[column].nunique()),
        'top_values': value_counts.head(10).to_dict(),
        'null_count': int(df[column].isna().sum()),
        'null_percentage': float(df[column].isna().sum() / len(df) * 100)
    }



