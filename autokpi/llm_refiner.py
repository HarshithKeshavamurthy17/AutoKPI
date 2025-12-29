"""
LLM integration for refining KPI names and descriptions
Uses OpenAI GPT-4 to enhance language and clarity
"""

import os
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


def is_openai_available() -> bool:
    """
    Check if OpenAI is available and API key is set.
    
    Returns:
        True if OpenAI is available and configured
    """
    if not OPENAI_AVAILABLE:
        return False
    
    api_key = os.getenv('OPENAI_API_KEY')
    return api_key is not None and api_key.strip() != ''


def refine_kpi_with_llm(kpi: Dict[str, Any], context: Optional[str] = None) -> Dict[str, Any]:
    """
    Refine a KPI's name and description using GPT-4.
    
    Args:
        kpi: KPI dictionary
        context: Optional context about the dataset
        
    Returns:
        Refined KPI dictionary
    """
    if not is_openai_available():
        return kpi
    
    try:
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Build prompt
        prompt = f"""You are a data analytics expert. Refine the following KPI definition to make it more professional, clear, and business-ready.

Original KPI Name: {kpi.get('name', '')}
Original Description: {kpi.get('description', '')}
Category: {kpi.get('category', '')}
Columns Used: {', '.join(kpi.get('columns_used', []))}

{f'Context: {context}' if context else ''}

Please provide:
1. A refined, professional KPI name (keep it concise, under 50 characters)
2. A clear, business-friendly description (1-2 sentences)

Respond in this format:
NAME: [refined name]
DESCRIPTION: [refined description]
"""
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a data analytics expert specializing in KPI definitions and business intelligence."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )
        
        # Parse response
        response_text = response.choices[0].message.content
        
        # Extract name and description
        lines = response_text.split('\n')
        refined_name = kpi.get('name', '')
        refined_description = kpi.get('description', '')
        
        for line in lines:
            if line.startswith('NAME:'):
                refined_name = line.replace('NAME:', '').strip()
            elif line.startswith('DESCRIPTION:'):
                refined_description = line.replace('DESCRIPTION:', '').strip()
        
        # Update KPI
        refined_kpi = kpi.copy()
        refined_kpi['name'] = refined_name
        refined_kpi['description'] = refined_description
        refined_kpi['refined_by_llm'] = True
        
        return refined_kpi
    
    except Exception as e:
        # If refinement fails, return original KPI
        print(f"Error refining KPI with LLM: {str(e)}")
        return kpi


def refine_kpis_with_llm(kpis: List[Dict[str, Any]], context: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Refine multiple KPIs using GPT-4.
    
    Args:
        kpis: List of KPI dictionaries
        context: Optional context about the dataset
        
    Returns:
        List of refined KPI dictionaries
    """
    if not is_openai_available():
        return kpis
    
    refined_kpis = []
    for kpi in kpis:
        refined_kpi = refine_kpi_with_llm(kpi, context)
        refined_kpis.append(refined_kpi)
    
    return refined_kpis


def batch_refine_kpis_with_llm(kpis: List[Dict[str, Any]], context: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Refine multiple KPIs in a single batch request (more efficient).
    
    Args:
        kpis: List of KPI dictionaries
        context: Optional context about the dataset
        
    Returns:
        List of refined KPI dictionaries
    """
    if not is_openai_available():
        return kpis
    
    try:
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Build batch prompt
        kpi_list_text = "\n".join([
            f"{i+1}. {kpi.get('name', '')}: {kpi.get('description', '')} (Category: {kpi.get('category', '')})"
            for i, kpi in enumerate(kpis)
        ])
        
        prompt = f"""You are a data analytics expert. Refine the following KPI definitions to make them more professional, clear, and business-ready.

KPIs to refine:
{kpi_list_text}

{f'Context: {context}' if context else ''}

For each KPI, provide:
1. A refined, professional KPI name (keep it concise, under 50 characters)
2. A clear, business-friendly description (1-2 sentences)

Respond in this format for each KPI:
{i+1}. NAME: [refined name]
    DESCRIPTION: [refined description]
"""
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a data analytics expert specializing in KPI definitions and business intelligence."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        # Parse response
        response_text = response.choices[0].message.content
        
        # Parse refined KPIs
        refined_kpis = []
        lines = response_text.split('\n')
        current_index = -1
        
        for line in lines:
            if line.strip().startswith(tuple(f"{i+1}." for i in range(len(kpis)))):
                # New KPI
                current_index = int(line.strip().split('.')[0]) - 1
                if current_index < len(kpis):
                    refined_kpis.append(kpis[current_index].copy())
                    refined_kpis[current_index]['refined_by_llm'] = True
            elif line.strip().startswith('NAME:'):
                if current_index >= 0 and current_index < len(refined_kpis):
                    refined_kpis[current_index]['name'] = line.replace('NAME:', '').strip()
            elif line.strip().startswith('DESCRIPTION:'):
                if current_index >= 0 and current_index < len(refined_kpis):
                    refined_kpis[current_index]['description'] = line.replace('DESCRIPTION:', '').strip()
        
        # Fill in any missing KPIs
        while len(refined_kpis) < len(kpis):
            refined_kpis.append(kpis[len(refined_kpis)].copy())
        
        return refined_kpis[:len(kpis)]
    
    except Exception as e:
        # If batch refinement fails, try individual refinement
        print(f"Error in batch refinement, falling back to individual refinement: {str(e)}")
        return refine_kpis_with_llm(kpis, context)



