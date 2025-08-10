#!/usr/bin/env python3
"""
Samsung TV Remote Control

A modern Python implementation for controlling Samsung Smart TVs via WiFi.
"""

import argparse
import sys
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Optional
from contextlib import contextmanager

from helpers import tvcon, macro, ssdp, tvinfo


@dataclass
class TVConfig:
    """Configuration for Samsung TV connection."""
    name: str = 'python remote'
    ip: str = '10.0.1.2'
    mac: str = '00-AB-11-11-11-11'
    description: str = 'samsungctl'
    id: str = 'PC'
    host: str = ''
    port: int = 55000
    method: str = 'websocket'
    timeout: int = 0

    def update_from_args(self, args: argparse.Namespace) -> None:
        """Update configuration from command line arguments."""
        if args.ip:
            self.host = args.ip
        if args.legacy:
            self.method = 'legacy'


@dataclass
class TVInfo:
    """Information about a discovered TV."""
    friendly_name: str
    ip: str
    model: str

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'TVInfo':
        """Create TVInfo from dictionary."""
        return cls(
            friendly_name=data['fn'],
            ip=data['ip'],
            model=data['model']
        )

    def __str__(self) -> str:
        return f"{self.friendly_name} ({self.model}) at {self.ip}"


def get_tv_info(tvs_found: List, verbose: bool) -> List[TVInfo]:
    """Retrieve TV information for discovered devices."""
    tv_list = []
    for tv in tvs_found:
        try:
            info = tvinfo.get(tv.location)
            tv_info = TVInfo.from_dict(info)
            tv_list.append(tv_info)
            
            if verbose:
                logging.info(f'Found: {tv_info}')
            else:
                logging.debug(f'Found: {tv_info}')
                
        except Exception as e:
            logging.warning(f"Failed to get info for TV at {tv.location}: {e}")
            
    return tv_list


def setup_logging(quiet: bool = False, log_file: str = 'app.log') -> None:
    """Setup logging configuration."""
    log_format = '%(asctime)s [%(levelname)6s]: %(message)s'
    
    # Configure file logging
    logging.basicConfig(
        filename=log_file,
        format=log_format,
        level=logging.DEBUG
    )
    
    # Add console handler if not quiet
    if not quiet:
        root = logging.getLogger()
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('%(message)s')
        console_handler.setFormatter(console_formatter)
        root.addHandler(console_handler)


@contextmanager
def error_handler():
    """Context manager for graceful error handling."""
    try:
        yield
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        sys.exit(1)


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Control your Samsung SmartTV through WiFi',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -s                    # Scan for TVs
  %(prog)s -i 192.168.1.100 -k KEY_POWER  # Send power command to specific TV
  %(prog)s -a -k KEY_VOLUP       # Send volume up to first available TV
  %(prog)s -p                    # Power off all TVs
  %(prog)s -m macro.csv          # Execute macro file
        """
    )
    
    # TV selection group
    tv_group = parser.add_mutually_exclusive_group()
    tv_group.add_argument(
        '-a', '--auto',
        action='store_true',
        help='send command to the first TV available'
    )
    tv_group.add_argument(
        '-i', '--ip',
        metavar='IP',
        help='IP address of the target TV'
    )
    
    # Command options
    parser.add_argument(
        '-k', '--key',
        metavar='KEY',
        help='key command to send to TV (e.g., KEY_POWER, KEY_VOLUP)'
    )
    parser.add_argument(
        '-l', '--legacy',
        action='store_true',
        help='use legacy method instead of websocket'
    )
    parser.add_argument(
        '-m', '--macro',
        metavar='FILE',
        help='macro file with commands to execute'
    )
    parser.add_argument(
        '-p', '--power-off-all',
        action='store_true',
        help="search all TVs in network and turn them off"
    )
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='suppress console output'
    )
    parser.add_argument(
        '-s', '--scan',
        action='store_true',
        help="scan network and list all TVs found"
    )
    
    return parser.parse_args()


def main() -> None:
    """Main application entry point."""
    # Parse arguments
    args = parse_arguments()
    
    # Show help if no arguments provided
    if len(sys.argv) == 1:
        args.print_help()
        sys.exit(1)
    
    # Setup logging
    setup_logging(args.quiet)
    logging.debug(f'Program started with arguments: {sys.argv}')

    with error_handler():
        # Initialize configuration
        config = TVConfig()
        config.update_from_args(args)
        
        # Handle scan operation
        if args.scan:
            logging.info('Scanning network...')
            tvs = ssdp.scan_network(wait=1)
            if not tvs:
                logging.info("No Samsung TVs found in the network")
            else:
                get_tv_info(tvs, True)
            sys.exit(0)
        
        # Get TV information if needed
        tvs = []
        if not args.ip:  # No IP specified, need to scan
            tvs = ssdp.scan_network()
            if not tvs:
                logging.error('No Samsung TV found in the network.')
                sys.exit(1)
            
            tvs = get_tv_info(tvs, False)
            if not tvs:
                logging.error('Failed to get TV information.')
                sys.exit(1)
            
            # Use first TV if auto mode
            if args.auto:
                config.host = tvs[0].ip
                config.method = tvinfo.getMethod(tvs[0].model)
                logging.info(f'Sending command to first TV found: {tvs[0].friendly_name}')
        
        # Handle power off all operation
        if args.power_off_all:
            if not tvs:  # Need to scan if not already done
                tvs = ssdp.scan_network()
                if not tvs:
                    logging.error('No Samsung TVs found to power off.')
                    sys.exit(1)
                tvs = get_tv_info(tvs, False)
            
            for tv in tvs:
                config.host = tv.ip
                config.method = tvinfo.getMethod(tv.model)
                if tvcon.send(config, 'KEY_POWEROFF'):
                    logging.info(f'Successfully turned off {tv.friendly_name}')
                else:
                    logging.error(f'Failed to turn off {tv.friendly_name}')
        
        # Handle single command
        if args.key:
            tvcon.send(config, args.key)
        
        # Handle macro execution
        if args.macro:
            macro_path = Path(args.macro)
            if not macro_path.exists():
                logging.error(f'Macro file not found: {args.macro}')
                sys.exit(1)
            macro.execute(config, str(macro_path))


if __name__ == "__main__":
    main()
