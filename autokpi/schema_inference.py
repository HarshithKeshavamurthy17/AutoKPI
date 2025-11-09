"""
Schema inference module for AutoKPI
Detects column types: ID, datetime, categorical, numeric, text
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any
from datetime import datetime
from .utils import detect_column_pattern


# Pattern definitions for column type detection
ID_PATTERNS = [
    r'\bid\b',
    r'^id$',
    r'_id$',
    r'id_',
    r'key$',
    r'pk$',
    r'primary_key',
    r'uuid',
    r'serial',
    r'index'
]

DATETIME_PATTERNS = [
    r'date',
    r'time',
    r'timestamp',
    r'created',
    r'updated',
    r'modified',
    r'when',
    r'dt$',
    r'_at$',
    r'day',
    r'month',
    r'year'
]

CATEGORICAL_PATTERNS = [
    r'category',
    r'type',
    r'status',
    r'state',
    r'country',
    r'region',
    r'city',
    r'segment',
    r'group',
    r'class',
    r'kind',
    r'label',
    r'tag',
    r'flag'
]


def infer_column_type(df: pd.DataFrame, column: str) -> str:
    """
    Infer the type of a column based on its name and data.
    
    Args:
        df: DataFrame
        column: Column name
        
    Returns:
        Column type: 'id', 'datetime', 'categorical', 'numeric', 'text'
    """
    # Check if column name suggests a type
    if detect_column_pattern(column, ID_PATTERNS):
        return 'id'
    
    if detect_column_pattern(column, DATETIME_PATTERNS):
        # Try to parse as datetime
        try:
            import warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                pd.to_datetime(df[column].dropna().head(100), errors='raise')
            return 'datetime'
        except:
            pass
    
    # Check data type
    dtype = df[column].dtype
    
    # Numeric types
    if pd.api.types.is_numeric_dtype(dtype):
        # Check if it's actually an ID (all unique integers)
        if dtype in [np.int64, np.int32, np.int16, np.int8]:
            unique_ratio = df[column].nunique() / len(df)
            if unique_ratio > 0.95:  # More than 95% unique values
                return 'id'
        return 'numeric'
    
    # Datetime types
    if pd.api.types.is_datetime64_any_dtype(dtype):
        return 'datetime'
    
    # Try to parse as datetime
    if dtype == 'object':
        sample = df[column].dropna().head(100)
        if len(sample) > 0:
            try:
                pd.to_datetime(sample, errors='raise')
                return 'datetime'
            except:
                pass
    
    # Object/string types
    if dtype == 'object' or pd.api.types.is_string_dtype(dtype):
        # Check if it's categorical (low cardinality)
        unique_ratio = df[column].nunique() / max(len(df), 1)
        avg_length = df[column].astype(str).str.len().mean()
        
        # If low cardinality and short strings, it's categorical
        if unique_ratio < 0.5 and avg_length < 50:
            if detect_column_pattern(column, CATEGORICAL_PATTERNS):
                return 'categorical'
            # Also check if values look categorical
            if df[column].nunique() < min(50, len(df) * 0.1):
                return 'categorical'
        
        # If very long strings, it's text
        if avg_length > 100:
            return 'text'
        
        # Default to categorical for object types with low cardinality
        if unique_ratio < 0.3:
            return 'categorical'
        
        return 'text'
    
    # Boolean types
    if pd.api.types.is_bool_dtype(dtype):
        return 'categorical'
    
    return 'categorical'  # Default fallback


def infer_schema(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Infer the complete schema of a DataFrame.
    
    Args:
        df: DataFrame to analyze
        
    Returns:
        Dictionary with schema information:
        {
            'id_columns': [...],
            'datetime_columns': [...],
            'categorical_columns': [...],
            'numeric_columns': [...],
            'text_columns': [...],
            'raw_columns': [...]
        }
    """
    schema = {
        'id_columns': [],
        'datetime_columns': [],
        'categorical_columns': [],
        'numeric_columns': [],
        'text_columns': [],
        'raw_columns': list(df.columns)
    }
    
    for column in df.columns:
        col_type = infer_column_type(df, column)
        
        if col_type == 'id':
            schema['id_columns'].append(column)
        elif col_type == 'datetime':
            schema['datetime_columns'].append(column)
        elif col_type == 'categorical':
            schema['categorical_columns'].append(column)
        elif col_type == 'numeric':
            schema['numeric_columns'].append(column)
        elif col_type == 'text':
            schema['text_columns'].append(column)
        else:
            # Fallback to categorical for unknown types
            schema['categorical_columns'].append(column)
    
    return schema


def get_schema_summary(df: pd.DataFrame, schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get a detailed summary of the inferred schema.
    
    Args:
        df: DataFrame
        schema: Inferred schema dictionary
        
    Returns:
        Detailed schema summary
    """
    summary = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'id_columns': [],
        'datetime_columns': [],
        'categorical_columns': [],
        'numeric_columns': [],
        'text_columns': []
    }
    
    for col in schema['id_columns']:
        summary['id_columns'].append({
            'name': col,
            'dtype': str(df[col].dtype),
            'unique_count': int(df[col].nunique()),
            'null_count': int(df[col].isna().sum())
        })
    
    for col in schema['datetime_columns']:
        try:
            df[col] = pd.to_datetime(df[col], errors='coerce')
            summary['datetime_columns'].append({
                'name': col,
                'dtype': 'datetime64',
                'min': str(df[col].min()) if not df[col].isna().all() else None,
                'max': str(df[col].max()) if not df[col].isna().all() else None,
                'null_count': int(df[col].isna().sum())
            })
        except:
            summary['datetime_columns'].append({
                'name': col,
                'dtype': str(df[col].dtype),
                'null_count': int(df[col].isna().sum())
            })
    
    for col in schema['categorical_columns']:
        value_counts = df[col].value_counts().head(5)
        summary['categorical_columns'].append({
            'name': col,
            'dtype': str(df[col].dtype),
            'unique_count': int(df[col].nunique()),
            'top_values': value_counts.to_dict(),
            'null_count': int(df[col].isna().sum())
        })
    
    for col in schema['numeric_columns']:
        summary['numeric_columns'].append({
            'name': col,
            'dtype': str(df[col].dtype),
            'min': float(df[col].min()) if not df[col].isna().all() else None,
            'max': float(df[col].max()) if not df[col].isna().all() else None,
            'mean': float(df[col].mean()) if not df[col].isna().all() else None,
            'null_count': int(df[col].isna().sum())
        })
    
    for col in schema['text_columns']:
        avg_length = df[col].astype(str).str.len().mean()
        summary['text_columns'].append({
            'name': col,
            'dtype': str(df[col].dtype),
            'avg_length': float(avg_length),
            'null_count': int(df[col].isna().sum())
        })
    
    return summary

