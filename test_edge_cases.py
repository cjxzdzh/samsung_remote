#!/usr/bin/env python3

import unittest
import sys
import os
from unittest.mock import patch, MagicMock, mock_open
import logging
import socket

# Add the current directory to the path so we can import the modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from helpers import tvcon, ssdp, tvinfo, macro


class TestEdgeCases(unittest.TestCase):
    """Test cases for edge cases and error conditions"""

    def test_tvinfo_getMethod_empty_model(self):
        """Test getMethod with empty model string"""
        result = tvinfo.getMethod("")
        self.assertEqual(result, 'websocket')

    def test_tvinfo_getMethod_short_model(self):
        """Test getMethod with model string shorter than 5 characters"""
        result = tvinfo.getMethod("UN55")
        self.assertEqual(result, 'websocket')

    def test_tvinfo_getMethod_none_model(self):
        """Test getMethod with None model"""
        result = tvinfo.getMethod(None)
        self.assertEqual(result, 'websocket')

    @patch('helpers.tvinfo.urllib.request.urlopen')
    def test_tvinfo_get_connection_error(self, mock_urlopen):
        """Test get function with connection error"""
        mock_urlopen.side_effect = Exception("Connection refused")
        
        with self.assertRaises(Exception):
            tvinfo.get('http://192.168.1.100:8001/ms/1.0/')

    @patch('helpers.tvinfo.urllib.request.urlopen')
    @patch('helpers.tvinfo.ET.fromstring')
    def test_tvinfo_get_missing_elements(self, mock_fromstring, mock_urlopen):
        """Test get function with missing XML elements"""
        mock_root = MagicMock()
        mock_root.find.return_value = None  # No elements found
        
        mock_fromstring.return_value = mock_root
        mock_urlopen.return_value = MagicMock()
        
        with self.assertRaises(AttributeError):
            tvinfo.get('http://192.168.1.100:8001/ms/1.0/')

    def test_tvcon_send_empty_config(self):
        """Test send function with empty config"""
        with patch('helpers.tvcon.samsungctl.Remote') as mock_remote:
            mock_remote.side_effect = Exception("Invalid config")
            
            result = tvcon.send({}, 'KEY_POWER')
            self.assertFalse(result)

    def test_tvcon_send_none_key(self):
        """Test send function with None key"""
        config = {'host': '192.168.1.100', 'method': 'websocket'}
        
        with patch('helpers.tvcon.samsungctl.Remote') as mock_remote:
            mock_remote_instance = MagicMock()
            mock_remote.return_value.__enter__.return_value = mock_remote_instance
            
            result = tvcon.send(config, None)
            self.assertTrue(result)

    def test_macro_execute_empty_file(self):
        """Test macro execution with empty file"""
        config = {'host': '192.168.1.100', 'method': 'websocket'}
        
        with patch('builtins.open', mock_open(read_data="key,wait\n")):
            with patch('helpers.macro.tvcon.send') as mock_send:
                macro.execute(config, 'empty_macro.csv')
                mock_send.assert_not_called()

    def test_macro_execute_invalid_csv(self):
        """Test macro execution with invalid CSV format"""
        config = {'host': '192.168.1.100', 'method': 'websocket'}
        
        with patch('builtins.open', mock_open(read_data="invalid,csv,format\n")):
            with patch('helpers.macro.tvcon.send') as mock_send:
                macro.execute(config, 'invalid_macro.csv')
                # Should handle gracefully without crashing
                self.assertTrue(True)

    def test_macro_execute_invalid_wait_time(self):
        """Test macro execution with invalid wait time"""
        config = {'host': '192.168.1.100', 'method': 'websocket'}
        
        with patch('builtins.open', mock_open(read_data="key,wait\nKEY_POWER,invalid\n")):
            with patch('helpers.macro.tvcon.send') as mock_send:
                with self.assertRaises(ValueError):
                    macro.execute(config, 'invalid_wait_macro.csv')

    @patch('helpers.ssdp.socket.socket')
    def test_ssdp_discover_timeout(self, mock_socket):
        """Test SSDP discover with immediate timeout"""
        mock_sock = MagicMock()
        mock_socket.return_value = mock_sock
        mock_sock.recv.side_effect = socket.timeout
        
        result = ssdp.discover("urn:samsung.com:device:RemoteControlReceiver:1", timeout=0.1)
        self.assertEqual(result, [])

    @patch('helpers.ssdp.discover')
    def test_ssdp_scan_network_keyboard_interrupt(self, mock_discover):
        """Test scan_network with keyboard interrupt"""
        mock_discover.side_effect = KeyboardInterrupt()
        
        result = ssdp.scan_network(wait=0.1)
        self.assertEqual(result, [])


class TestErrorHandling(unittest.TestCase):
    """Test cases for error handling scenarios"""

    def test_tvcon_send_generic_exception(self):
        """Test send function with generic exception"""
        config = {'host': '192.168.1.100', 'method': 'websocket'}
        
        with patch('helpers.tvcon.samsungctl.Remote') as mock_remote:
            mock_remote.side_effect = Exception("Unknown error")
            
            result = tvcon.send(config, 'KEY_POWER')
            self.assertFalse(result)

    @patch('helpers.tvinfo.urllib.request.urlopen')
    def test_tvinfo_get_timeout_error(self, mock_urlopen):
        """Test get function with timeout error"""
        mock_urlopen.side_effect = TimeoutError("Request timed out")
        
        with self.assertRaises(TimeoutError):
            tvinfo.get('http://192.168.1.100:8001/ms/1.0/')

    def test_macro_execute_permission_error(self):
        """Test macro execution with permission error"""
        config = {'host': '192.168.1.100', 'method': 'websocket'}
        
        with patch('builtins.open', side_effect=PermissionError("Permission denied")):
            with patch('helpers.macro.logging.error') as mock_logging:
                macro.execute(config, 'protected_file.csv')
                mock_logging.assert_called_once()


class TestBoundaryConditions(unittest.TestCase):
    """Test cases for boundary conditions"""

    def test_tvcon_send_zero_wait_time(self):
        """Test send function with zero wait time"""
        config = {'host': '192.168.1.100', 'method': 'websocket'}
        
        with patch('helpers.tvcon.samsungctl.Remote') as mock_remote:
            mock_remote_instance = MagicMock()
            mock_remote.return_value.__enter__.return_value = mock_remote_instance
            
            result = tvcon.send(config, 'KEY_POWER', wait_time=0)
            self.assertTrue(result)

    def test_tvcon_send_negative_wait_time(self):
        """Test send function with negative wait time"""
        config = {'host': '192.168.1.100', 'method': 'websocket'}
        
        with patch('helpers.tvcon.samsungctl.Remote') as mock_remote:
            mock_remote_instance = MagicMock()
            mock_remote.return_value.__enter__.return_value = mock_remote_instance
            
            result = tvcon.send(config, 'KEY_POWER', wait_time=-100)
            self.assertTrue(result)

    def test_macro_execute_zero_wait_time(self):
        """Test macro execution with zero wait time"""
        config = {'host': '192.168.1.100', 'method': 'websocket'}
        
        with patch('builtins.open', mock_open(read_data="key,wait\nKEY_POWER,0\n")):
            with patch('helpers.macro.tvcon.send') as mock_send:
                macro.execute(config, 'zero_wait_macro.csv')
                mock_send.assert_called_once_with(config, 'KEY_POWER', 0.0)


if __name__ == '__main__':
    # Set up logging for tests
    logging.basicConfig(level=logging.ERROR)
    
    # Run the tests
    unittest.main(verbosity=2)
