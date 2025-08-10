# Samsung Remote Examples

This directory contains example scripts demonstrating various features of the samsung_remote project.

## Examples

### power_commands_example.py

Demonstrates the three different power commands available in the updated samsungctl library:

- **KEY_POWER**: Toggle power (turns TV on if off, off if on)
- **KEY_POWERON**: Discrete power on (always turns TV on)
- **KEY_POWEROFF**: Discrete power off (always turns TV off)

#### Usage

```bash
python power_commands_example.py <TV_IP_ADDRESS>
```

#### Example

```bash
python power_commands_example.py 192.168.1.100
```

#### Output

The script will demonstrate each power command and show the results:

```
Demonstrating power commands for TV at 192.168.1.100
==================================================

1. Testing KEY_POWER (toggle power)
   This will turn the TV on if it's off, or off if it's on
   ✅ KEY_POWER command sent successfully

2. Testing KEY_POWERON (discrete power on)
   This will turn the TV on regardless of current state
   ✅ KEY_POWERON command sent successfully

3. Testing KEY_POWEROFF (discrete power off)
   This will turn the TV off regardless of current state
   ✅ KEY_POWEROFF command sent successfully

==================================================
Power command demonstration completed!

Summary:
- KEY_POWER: Use for general power toggling
- KEY_POWERON: Use when you specifically want to turn the TV on
- KEY_POWEROFF: Use when you specifically want to turn the TV off
```

## Requirements

Make sure you have the updated samsungctl library installed:

```bash
pip install git+https://github.com/kdschlosser/samsungctl.git
```

## Notes

- These examples require a Samsung Smart TV on the same network
- The TV must have network control enabled
- Some commands may not work on all TV models
- Always test with your specific TV model before using in production
