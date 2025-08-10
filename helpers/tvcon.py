"""
TV Control Module

Handles sending commands to Samsung TVs using the samsungctl library.
"""

import socket
import websocket
import samsungctl
import logging
import time
from typing import Dict, Any


def send(config: Dict[str, Any], key: str, wait_time: float = 100.0) -> bool:
    """
    Send a command to a Samsung TV.
    
    Args:
        config: TV configuration dictionary
        key: Command key to send (e.g., 'KEY_POWER', 'KEY_VOLUP')
        wait_time: Time to wait after sending command (in milliseconds)
        
    Returns:
        True if command was sent successfully, False otherwise
    """
    logger = logging.getLogger(__name__)
    
    try:
        with samsungctl.Remote(config) as remote:
            remote.control(key)

        time.sleep(wait_time / 1000.0)
        logger.debug(f"Successfully sent command '{key}' to {config.get('host', 'unknown')}")
        return True

    except socket.error as e:
        logger.error(f"Socket error sending command '{key}': {e}")
        return False
    except websocket._exceptions.WebSocketConnectionClosedException as e:
        logger.error(f"WebSocket connection error: {e}. Try using legacy mode (-l)")
        return False
    except Exception as e:
        logger.error(f"Unexpected error sending command '{key}': {e}")
        return False
