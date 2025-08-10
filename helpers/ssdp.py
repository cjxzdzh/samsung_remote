"""
SSDP (Simple Service Discovery Protocol) Module - Simple Library-based Implementation

Simple replacement for the custom SSDP implementation using the netdisco library.
This provides the same interface as the original custom implementation.
"""

import logging
from typing import List
from dataclasses import dataclass

try:
    from netdisco import ssdp as netdisco_ssdp
    NETDISCO_AVAILABLE = True
except ImportError:
    NETDISCO_AVAILABLE = False
    logging.warning("netdisco library not available. Install with: pip install netdisco")


@dataclass
class SSDPResponse:
    """Represents an SSDP response from a network device."""
    location: str
    usn: str
    st: str
    cache: str = "0"

    def __repr__(self) -> str:
        return f"<SSDPResponse({self.location}, {self.st}, {self.usn})>"


def discover(service: str, timeout: int = 5, retries: int = 1, mx: int = 3) -> List[SSDPResponse]:
    """
    Discover SSDP services on the network using netdisco.
    
    Args:
        service: Service type to search for
        timeout: Socket timeout in seconds (not used by netdisco)
        retries: Number of discovery attempts (not used by netdisco)
        mx: Maximum wait time for responses (not used by netdisco)
        
    Returns:
        List of SSDP responses from discovered devices
    """
    logger = logging.getLogger(__name__)
    
    if not NETDISCO_AVAILABLE:
        logger.error("netdisco library not available")
        return []
    
    try:
        logger.debug(f"Starting SSDP discovery for {service}")
        
        # Scan for all devices using netdisco
        devices = netdisco_ssdp.scan()
        
        # Filter for the requested service
        matching_devices = []
        for device in devices:
            if hasattr(device, 'st') and service.lower() in str(device.st).lower():
                matching_devices.append(SSDPResponse(
                    location=getattr(device, 'location', ''),
                    usn=getattr(device, 'usn', ''),
                    st=getattr(device, 'st', ''),
                    cache='0'
                ))
        
        logger.info(f"SSDP discovery found {len(matching_devices)} devices for {service}")
        return matching_devices
        
    except Exception as e:
        logger.error(f"SSDP discovery failed: {e}")
        return []


def scan_network(wait: float = 0.3) -> List[SSDPResponse]:
    """
    Scan network for Samsung TVs using SSDP discovery.
    
    Args:
        wait: Initial timeout for discovery in seconds (not used by netdisco)
        
    Returns:
        List of SSDP responses from discovered Samsung TVs
    """
    logger = logging.getLogger(__name__)
    
    try:
        logger.debug(f"Starting network scan for Samsung TVs")
        
        # Use netdisco to scan for all devices
        devices = netdisco_ssdp.scan()
        
        # Filter for Samsung TVs
        samsung_devices = []
        for device in devices:
            if hasattr(device, 'st') and 'samsung' in str(device.st).lower():
                samsung_devices.append(SSDPResponse(
                    location=getattr(device, 'location', ''),
                    usn=getattr(device, 'usn', ''),
                    st=getattr(device, 'st', ''),
                    cache='0'
                ))
        
        logger.info(f"Network scan completed, found {len(samsung_devices)} Samsung TVs")
        return samsung_devices

    except KeyboardInterrupt:
        logger.info('Search interrupted by user')
        return []
    except Exception as e:
        logger.error(f"Network scan failed: {e}")
        return []


# Fallback to custom implementation if netdisco is not available
if not NETDISCO_AVAILABLE:
    try:
        from . import ssdp_custom as custom_ssdp
        discover = custom_ssdp.discover
        scan_network = custom_ssdp.scan_network
        SSDPResponse = custom_ssdp.SSDPResponse
        logging.info("Using custom SSDP implementation as fallback")
    except ImportError:
        logging.error("No SSDP implementation available")
