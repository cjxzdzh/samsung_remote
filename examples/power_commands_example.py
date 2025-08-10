#!/usr/bin/env python3
"""
Example script demonstrating the new power commands in samsungctl.

This script shows how to use the three different power commands:
- KEY_POWER: Toggle power (turns TV on if off, off if on)
- KEY_POWERON: Discrete power on (always turns TV on)
- KEY_POWEROFF: Discrete power off (always turns TV off)
"""

import sys
import os
import time

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from helpers import tvcon


def demonstrate_power_commands(tv_ip: str):
    """
    Demonstrate the three different power commands.
    
    Args:
        tv_ip: IP address of the Samsung TV
    """
    print(f"Demonstrating power commands for TV at {tv_ip}")
    print("=" * 50)
    
    # Configuration for the TV
    config = {
        'name': 'power_demo',
        'host': tv_ip,
        'port': 55000,
        'method': 'websocket',
        'timeout': 0
    }
    
    # Test KEY_POWER (toggle)
    print("\n1. Testing KEY_POWER (toggle power)")
    print("   This will turn the TV on if it's off, or off if it's on")
    try:
        result = tvcon.send(config, 'KEY_POWER')
        if result:
            print("   ✅ KEY_POWER command sent successfully")
        else:
            print("   ❌ KEY_POWER command failed")
    except Exception as e:
        print(f"   ❌ Error sending KEY_POWER: {e}")
    
    # Wait a moment
    time.sleep(2)
    
    # Test KEY_POWERON (discrete power on)
    print("\n2. Testing KEY_POWERON (discrete power on)")
    print("   This will turn the TV on regardless of current state")
    try:
        result = tvcon.send(config, 'KEY_POWERON')
        if result:
            print("   ✅ KEY_POWERON command sent successfully")
        else:
            print("   ❌ KEY_POWERON command failed")
    except Exception as e:
        print(f"   ❌ Error sending KEY_POWERON: {e}")
    
    # Wait a moment
    time.sleep(2)
    
    # Test KEY_POWEROFF (discrete power off)
    print("\n3. Testing KEY_POWEROFF (discrete power off)")
    print("   This will turn the TV off regardless of current state")
    try:
        result = tvcon.send(config, 'KEY_POWEROFF')
        if result:
            print("   ✅ KEY_POWEROFF command sent successfully")
        else:
            print("   ❌ KEY_POWEROFF command failed")
    except Exception as e:
        print(f"   ❌ Error sending KEY_POWEROFF: {e}")
    
    print("\n" + "=" * 50)
    print("Power command demonstration completed!")
    print("\nSummary:")
    print("- KEY_POWER: Use for general power toggling")
    print("- KEY_POWERON: Use when you specifically want to turn the TV on")
    print("- KEY_POWEROFF: Use when you specifically want to turn the TV off")


def main():
    """Main function to run the power command demonstration."""
    if len(sys.argv) != 2:
        print("Usage: python power_commands_example.py <TV_IP_ADDRESS>")
        print("Example: python power_commands_example.py 192.168.1.100")
        sys.exit(1)
    
    tv_ip = sys.argv[1]
    demonstrate_power_commands(tv_ip)


if __name__ == "__main__":
    main()
