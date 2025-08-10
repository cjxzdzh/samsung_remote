"""
TV Information Module

Handles retrieving and parsing TV information from Samsung TVs.
"""

import re
import xml.etree.ElementTree as ET
import urllib.request
import logging
from typing import Dict, Optional


def getMethod(model: str) -> str:
    """
    Determine the connection method based on TV model.
    
    Args:
        model: TV model string (e.g., 'UN55F8000')
        
    Returns:
        Connection method: 'legacy' for older models (C, D, E, F), 'websocket' for newer
    """
    logger = logging.getLogger(__name__)
    
    # Legacy models (C, D, E, F series)
    legacy_models = {'C', 'D', 'E', 'F'}
    
    if len(model) < 5:
        logger.warning(f"Invalid model format: {model}")
        return 'websocket'
    
    model_series = model[4]
    method = 'legacy' if model_series in legacy_models else 'websocket'
    
    logger.debug(f"Model: {model_series} returns method: {method}")
    return method


def namespace(element) -> str:
    """
    Extract XML namespace from element tag.
    
    Args:
        element: XML element
        
    Returns:
        Namespace string or empty string if no namespace
    """
    m = re.match(r'\{.*\}', element.tag)
    return m.group(0) if m else ''


def get(url: str) -> Dict[str, str]:
    """
    Retrieve TV information from a Samsung TV's XML endpoint.
    
    Args:
        url: URL to the TV's XML information endpoint
        
    Returns:
        Dictionary containing TV information (friendly_name, ip, model)
        
    Raises:
        ValueError: If IP address cannot be extracted from URL
        urllib.error.URLError: If URL cannot be accessed
        xml.etree.ElementTree.ParseError: If XML cannot be parsed
    """
    logger = logging.getLogger(__name__)
    
    # Extract IP address from URL
    ip_match = re.search(r'[0-9]+(?:\.[0-9]+){3}', url)
    if not ip_match:
        raise ValueError(f"Could not extract IP address from URL: {url}")
    
    ip = ip_match.group(0)
    
    try:
        # Fetch XML data
        with urllib.request.urlopen(url, timeout=10) as response:
            xmlstr = response.read().decode('utf-8')
        
        # Parse XML
        root = ET.fromstring(xmlstr)
        ns = namespace(root)
        
        # Extract TV information
        friendly_name_elem = root.find(f'.//{ns}friendlyName')
        model_name_elem = root.find(f'.//{ns}modelName')
        
        if friendly_name_elem is None or model_name_elem is None:
            raise ValueError("Required XML elements not found")
        
        friendly_name = friendly_name_elem.text
        model = model_name_elem.text
        
        if not friendly_name or not model:
            raise ValueError("TV information is incomplete")
        
        logger.debug(f"Retrieved TV info: {friendly_name} ({model}) at {ip}")
        
        return {
            'fn': friendly_name,
            'ip': ip,
            'model': model
        }
        
    except urllib.error.URLError as e:
        logger.error(f"Failed to access URL {url}: {e}")
        raise
    except ET.ParseError as e:
        logger.error(f"Failed to parse XML from {url}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error getting TV info from {url}: {e}")
        raise
