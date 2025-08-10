#!/usr/bin/env python3

import unittest
import sys
import os
import tempfile
import csv
import socket
from unittest.mock import patch, MagicMock, mock_open
import logging

# Add the current directory to the path so we can import the modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from samsung_remote import get_tv_info, setup_logging, main, TVConfig, TVInfo
from helpers import tvcon, ssdp, tvinfo, macro


class TestTVInfo(unittest.TestCase):
    """Test cases for tvinfo module"""

    def test_getMethod_legacy_models(self):
        """Test getMethod returns 'legacy' for C, D, E, F models"""
        legacy_models = ['UN55C8000', 'UN55D8000', 'UN55E8000', 'UN55F8000']
        for model in legacy_models:
            with self.subTest(model=model):
                result = tvinfo.getMethod(model)
                self.assertEqual(result, 'legacy')

    def test_getMethod_websocket_models(self):
        """Test getMethod returns 'websocket' for other models"""
        websocket_models = ['UN55G8000', 'UN55H8000', 'UN55J8000', 'UN55K8000']
        for model in websocket_models:
            with self.subTest(model=model):
                result = tvinfo.getMethod(model)
                self.assertEqual(result, 'websocket')

    def test_namespace_with_namespace(self):
        """Test namespace function with element that has namespace"""
        element = MagicMock()
        element.tag = '{http://schemas.xmlsoap.org/soap/envelope/}Envelope'
        result = tvinfo.namespace(element)
        self.assertEqual(result, '{http://schemas.xmlsoap.org/soap/envelope/}')

    def test_namespace_without_namespace(self):
        """Test namespace function with element that has no namespace"""
        element = MagicMock()
        element.tag = 'Envelope'
        result = tvinfo.namespace(element)
        self.assertEqual(result, '')

    @patch('helpers.tvinfo.urllib.request.urlopen')
    @patch('helpers.tvinfo.ET.fromstring')
    def test_get_success(self, mock_fromstring, mock_urlopen):
        """Test get function with successful response"""
        # Mock the XML response
        mock_root = MagicMock()
        mock_friendly_name = MagicMock()
        mock_friendly_name.text = 'Living Room TV'
        mock_model_name = MagicMock()
        mock_model_name.text = 'UN55F8000'
        
        # Mock the tag attribute for namespace function
        mock_root.tag = '{http://schemas.xmlsoap.org/soap/envelope/}root'
        mock_root.find.side_effect = lambda x: mock_friendly_name if 'friendlyName' in x else mock_model_name
        
        mock_fromstring.return_value = mock_root
        mock_urlopen.return_value = MagicMock()
        
        url = 'http://192.168.1.100:8001/ms/1.0/'
        
        result = tvinfo.get(url)
        
        expected = {
            'fn': 'Living Room TV',
            'ip': '192.168.1.100',
            'model': 'UN55F8000'
        }
        self.assertEqual(result, expected)


class TestTVCon(unittest.TestCase):
    """Test cases for tvcon module"""

    @patch('helpers.tvcon.samsungctl.Remote')
    def test_send_success(self, mock_remote):
        """Test successful send command"""
        config = {'host': '192.168.1.100', 'method': 'websocket'}
        key = 'KEY_POWER'
        
        # Mock the context manager
        mock_remote_instance = MagicMock()
        mock_remote.return_value.__enter__.return_value = mock_remote_instance
        
        result = tvcon.send(config, key)
        
        self.assertTrue(result)
        mock_remote.assert_called_once_with(config)
        mock_remote_instance.control.assert_called_once_with(key)

    @patch('helpers.tvcon.samsungctl.Remote')
    def test_send_socket_error(self, mock_remote):
        """Test send command with socket error"""
        config = {'host': '192.168.1.100', 'method': 'websocket'}
        key = 'KEY_POWER'
        
        # Mock socket error
        mock_remote.side_effect = OSError("Connection refused")
        
        result = tvcon.send(config, key)
        
        self.assertFalse(result)

    @patch('helpers.tvcon.samsungctl.Remote')
    def test_send_websocket_error(self, mock_remote):
        """Test send command with websocket error"""
        config = {'host': '192.168.1.100', 'method': 'websocket'}
        key = 'KEY_POWER'
        
        # Mock websocket error
        from websocket._exceptions import WebSocketConnectionClosedException
        mock_remote.side_effect = WebSocketConnectionClosedException()
        
        result = tvcon.send(config, key)
        
        self.assertFalse(result)


class TestSSDP(unittest.TestCase):
    """Test cases for ssdp module"""

    def test_ssdp_response_repr(self):
        """Test SSDPResponse __repr__ method"""
        # Create a mock HTTP response with proper bytes data
        mock_response = MagicMock()
        mock_response.getheader.side_effect = lambda x: {
            'location': 'http://192.168.1.100:8001/ms/1.0/',
            'st': 'urn:samsung.com:device:RemoteControlReceiver:1',
            'usn': 'uuid:12345678-1234-1234-1234-123456789012',
            'cache-control': 'max-age=1800'
        }.get(x)
        
        # Mock the HTTPResponse to return proper data
        with patch('helpers.ssdp.http.client.HTTPResponse') as mock_http_response:
            mock_http_response.return_value.getheader.side_effect = lambda x: {
                'location': 'http://192.168.1.100:8001/ms/1.0/',
                'st': 'urn:samsung.com:device:RemoteControlReceiver:1',
                'usn': 'uuid:12345678-1234-1234-1234-123456789012',
                'cache-control': 'max-age=1800'
            }.get(x)
            
            # Create a bytes-like object for the response
            mock_response_bytes = b'HTTP/1.1 200 OK\r\nLOCATION: http://192.168.1.100:8001/ms/1.0/\r\nST: urn:samsung.com:device:RemoteControlReceiver:1\r\nUSN: uuid:12345678-1234-1234-1234-123456789012\r\nCACHE-CONTROL: max-age=1800\r\n\r\n'
            
            ssdp_response = ssdp.SSDPResponse(mock_response_bytes)
            
            expected = "<SSDPResponse(http://192.168.1.100:8001/ms/1.0/, urn:samsung.com:device:RemoteControlReceiver:1, uuid:12345678-1234-1234-1234-123456789012)>"
            self.assertEqual(repr(ssdp_response), expected)

    @patch('helpers.ssdp.socket.socket')
    def test_discover_success(self, mock_socket):
        """Test discover function with successful response"""
        # Mock socket and responses
        mock_sock = MagicMock()
        mock_socket.return_value = mock_sock
        
        # Mock successful response
        mock_response_data = b'HTTP/1.1 200 OK\r\nLOCATION: http://192.168.1.100:8001/ms/1.0/\r\nST: urn:samsung.com:device:RemoteControlReceiver:1\r\nUSN: uuid:12345678-1234-1234-1234-123456789012\r\nCACHE-CONTROL: max-age=1800\r\n\r\n'
        mock_sock.recv.return_value = mock_response_data
        
        # Mock timeout after first response
        mock_sock.recv.side_effect = [mock_response_data, socket.timeout]
        
        result = ssdp.discover("urn:samsung.com:device:RemoteControlReceiver:1", timeout=1)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].location, 'http://192.168.1.100:8001/ms/1.0/')

    @patch('helpers.ssdp.discover')
    def test_scan_network_success(self, mock_discover):
        """Test scan_network with successful discovery"""
        mock_response = MagicMock()
        mock_response.location = 'http://192.168.1.100:8001/ms/1.0/'
        mock_discover.return_value = [mock_response]
        
        result = ssdp.scan_network(wait=0.1)
        
        self.assertEqual(len(result), 1)
        mock_discover.assert_called_once()

    @patch('helpers.ssdp.discover')
    def test_scan_network_no_tvs_found(self, mock_discover):
        """Test scan_network when no TVs are found"""
        mock_discover.return_value = []
        
        result = ssdp.scan_network(wait=0.1)
        
        self.assertEqual(result, [])
        # Should be called twice due to retry logic
        self.assertEqual(mock_discover.call_count, 2)


class TestMacro(unittest.TestCase):
    """Test cases for macro module"""

    def test_execute_success(self):
        """Test successful macro execution"""
        config = {'host': '192.168.1.100', 'method': 'websocket'}

        # Mock the CSV reader to return proper data
        mock_csv_data = [
            {'key': 'KEY_POWER', 'wait': '500'},
            {'key': 'KEY_UP', 'wait': '100'},
            {'key': 'KEY_ENTER', 'wait': '200'}
        ]

        with patch('helpers.macro.Path') as mock_path:
            mock_path.return_value.exists.return_value = True
            mock_path.return_value.is_file.return_value = True
            with patch('builtins.open', mock_open()):
                with patch('helpers.macro.csv.DictReader') as mock_csv_reader:
                    mock_csv_reader.return_value = mock_csv_data
                    with patch('helpers.macro.tvcon.send') as mock_send:
                        mock_send.return_value = True
                        result = macro.execute(config, 'test_macro.csv')

                        # Should be called 3 times (one for each command)
                        self.assertEqual(mock_send.call_count, 3)
                        self.assertTrue(result)
                        
                        # Check the calls
                        calls = mock_send.call_args_list
                        self.assertEqual(calls[0][0][1], 'KEY_POWER')  # key
                        self.assertEqual(calls[0][0][2], 500.0)        # wait
                        self.assertEqual(calls[1][0][1], 'KEY_UP')     # key
                        self.assertEqual(calls[1][0][2], 100.0)       # wait
                        self.assertEqual(calls[2][0][1], 'KEY_ENTER')  # key
                        self.assertEqual(calls[2][0][2], 200.0)       # wait

    def test_execute_with_comments(self):
        """Test macro execution with comment lines"""
        config = {'host': '192.168.1.100', 'method': 'websocket'}
        
        # Mock the CSV reader to return data with comments
        mock_csv_data = [
            {'key': '# This is a comment', 'wait': ''},
            {'key': 'KEY_POWER', 'wait': '500'},
            {'key': '# Another comment', 'wait': ''},
            {'key': 'KEY_UP', 'wait': '100'}
        ]
        
        with patch('helpers.macro.Path') as mock_path:
            mock_path.return_value.exists.return_value = True
            mock_path.return_value.is_file.return_value = True
            with patch('builtins.open', mock_open()):
                with patch('helpers.macro.csv.DictReader') as mock_csv_reader:
                    mock_csv_reader.return_value = mock_csv_data
                    with patch('helpers.macro.tvcon.send') as mock_send:
                        mock_send.return_value = True
                        result = macro.execute(config, 'test_macro.csv')
                        
                        # Should be called 2 times (comments should be ignored)
                        self.assertEqual(mock_send.call_count, 2)
                        self.assertTrue(result)

    def test_execute_file_not_found(self):
        """Test macro execution with non-existent file"""
        config = {'host': '192.168.1.100', 'method': 'websocket'}

        with patch('helpers.macro.Path') as mock_path:
            mock_path.return_value.exists.return_value = False
            with patch('helpers.macro.logging.getLogger') as mock_get_logger:
                mock_logger = MagicMock()
                mock_get_logger.return_value = mock_logger
                result = macro.execute(config, 'nonexistent.csv')
                self.assertFalse(result)
                mock_logger.error.assert_called_once()


class TestSamsungRemote(unittest.TestCase):
    """Test cases for main samsung_remote module"""

    def test_get_tv_info_success(self):
        """Test get_tv_info function with successful TV info retrieval"""
        tvs_found = [MagicMock()]
        tvs_found[0].location = 'http://192.168.1.100:8001/ms/1.0/'
        
        with patch('samsung_remote.tvinfo.get') as mock_get:
            mock_get.return_value = {
                'fn': 'Living Room TV',
                'ip': '192.168.1.100',
                'model': 'UN55F8000'
            }
            
            with patch('samsung_remote.logging.info') as mock_logging:
                result = get_tv_info(tvs_found, verbose=True)
                
                self.assertEqual(len(result), 1)
                self.assertIsInstance(result[0], TVInfo)
                self.assertEqual(result[0].friendly_name, 'Living Room TV')
                mock_logging.assert_called_once()

    def test_setup_logging_quiet_mode(self):
        """Test setup_logging function in quiet mode"""
        with patch('samsung_remote.logging.basicConfig') as mock_basic_config:
            with patch('samsung_remote.logging.getLogger') as mock_get_logger:
                mock_root = MagicMock()
                mock_get_logger.return_value = mock_root
                
                setup_logging(quiet=True)
                
                mock_basic_config.assert_called_once()
                # Should not add console handler in quiet mode
                mock_root.addHandler.assert_not_called()

    def test_setup_logging_verbose_mode(self):
        """Test setup_logging function in verbose mode"""
        with patch('samsung_remote.logging.basicConfig') as mock_basic_config:
            with patch('samsung_remote.logging.getLogger') as mock_get_logger:
                with patch('samsung_remote.logging.StreamHandler') as mock_stream_handler:
                    mock_root = MagicMock()
                    mock_get_logger.return_value = mock_root
                    mock_handler = MagicMock()
                    mock_stream_handler.return_value = mock_handler
                    
                    setup_logging(quiet=False)
                    
                    mock_basic_config.assert_called_once()
                    mock_root.addHandler.assert_called_once_with(mock_handler)

    @patch('samsung_remote.sys.argv', ['samsung_remote.py'])
    @patch('samsung_remote.parse_arguments')
    @patch('samsung_remote.setup_logging')
    @patch('samsung_remote.error_handler')
    @patch('samsung_remote.sys.exit')
    def test_main_help(self, mock_exit, mock_error_handler, mock_setup_logging, mock_parse_args):
        """Test main function with no arguments (should show help)"""
        # Mock the error handler context manager
        mock_error_handler.return_value.__enter__ = MagicMock()
        mock_error_handler.return_value.__exit__ = MagicMock()
        
        # Mock the argument parser to return a namespace with print_help method
        mock_args = MagicMock()
        mock_args.print_help = MagicMock()
        # Set all flags to False to prevent other code paths from executing
        mock_args.scan = False
        mock_args.ip = None
        mock_args.auto = False
        mock_args.key = None
        mock_args.power_off_all = False
        mock_args.macro = None
        mock_args.quiet = False
        mock_parse_args.return_value = mock_args
        
        main()
        mock_args.print_help.assert_called_once()
        mock_exit.assert_called_once_with(1)

    @patch('samsung_remote.sys.argv', ['samsung_remote.py', '-s'])
    @patch('samsung_remote.parse_arguments')
    @patch('samsung_remote.setup_logging')
    @patch('samsung_remote.error_handler')
    @patch('samsung_remote.ssdp.scan_network')
    @patch('samsung_remote.get_tv_info')
    @patch('samsung_remote.sys.exit')
    def test_main_scan(self, mock_exit, mock_get_tv_info, mock_scan_network, mock_error_handler, mock_setup_logging, mock_parse_args):
        """Test main function with scan argument"""
        # Mock the error handler context manager
        mock_error_handler.return_value.__enter__ = MagicMock()
        mock_error_handler.return_value.__exit__ = MagicMock()
        
        # Mock the argument parser
        mock_args = MagicMock()
        mock_args.scan = True
        mock_args.ip = None
        mock_args.auto = False
        mock_args.key = None
        mock_args.power_off_all = False
        mock_args.macro = None
        mock_args.quiet = False
        mock_parse_args.return_value = mock_args
        
        mock_scan_network.return_value = [MagicMock()]
        
        with patch('samsung_remote.logging.info') as mock_logging:
            main()
            
            # scan_network is called once with wait=1
            mock_scan_network.assert_called_once_with(wait=1)
            # get_tv_info is called once with verbose=True
            mock_get_tv_info.assert_called_once_with([MagicMock()], True)
            mock_exit.assert_called_once_with(0)

    @patch('samsung_remote.sys.argv', ['samsung_remote.py', '-i', '192.168.1.100', '-k', 'KEY_POWER'])
    @patch('samsung_remote.tvcon.send')
    def test_main_send_key(self, mock_send):
        """Test main function with IP and key arguments"""
        main()
        mock_send.assert_called_once()

    @patch('samsung_remote.sys.argv', ['samsung_remote.py', '-p'])
    @patch('samsung_remote.ssdp.scan_network')
    @patch('samsung_remote.get_tv_info')
    @patch('samsung_remote.tvcon.send')
    def test_main_power_off_all(self, mock_send, mock_get_tv_info, mock_scan_network):
        """Test main function with power off all TVs argument"""
        mock_scan_network.return_value = [MagicMock()]
        mock_tv_info = TVInfo('Living Room TV', '192.168.1.100', 'UN55F8000')
        mock_get_tv_info.return_value = [mock_tv_info]
        mock_send.return_value = True
        
        with patch('samsung_remote.logging.info') as mock_logging:
            main()
            
            mock_send.assert_called_once()
            mock_logging.assert_called_once()


class TestIntegration(unittest.TestCase):
    """Integration test cases"""

    def test_full_workflow_with_mock_tv(self):
        """Test a complete workflow with a mocked TV"""
        # This test simulates a complete workflow
        config = {
            'name': 'python remote',
            'ip': '10.0.1.2',
            'mac': '00-AB-11-11-11-11',
            'description': 'samsungctl',
            'id': 'PC',
            'host': '192.168.1.100',
            'port': 55000,
            'method': 'websocket',
            'timeout': 0,
        }
        
        with patch('helpers.tvcon.samsungctl.Remote') as mock_remote:
            mock_remote_instance = MagicMock()
            mock_remote.return_value.__enter__.return_value = mock_remote_instance
            
            result = tvcon.send(config, 'KEY_POWER')
            
            self.assertTrue(result)
            mock_remote_instance.control.assert_called_once_with('KEY_POWER')


if __name__ == '__main__':
    # Set up logging for tests
    logging.basicConfig(level=logging.ERROR)
    
    # Run the tests
    unittest.main(verbosity=2)
