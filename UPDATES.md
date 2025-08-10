# Samsung Remote Updates

This document summarizes the changes made to update the samsung_remote project to use the updated [samsungctl library](https://github.com/kdschlosser/samsungctl).

## Overview

The project has been updated to use the latest version of samsungctl (v0.8.0b0+) which provides improved power key handling and better TV support.

## Key Changes

### 1. Updated Dependencies

**File**: `requirements.txt`
- Updated samsungctl from `==0.7.0` to `>=0.8.0b0`
- Added comment about installing from GitHub for latest features

### 2. Updated TV Control Module

**File**: `helpers/tvcon.py`
- Updated to use `samsungctl.Config` class for configuration
- Changed from direct dictionary configuration to proper Config object
- Maintained backward compatibility with existing API

### 3. Updated Main Application

**File**: `samsung_remote.py`
- Simplified `TVConfig` dataclass by removing unused fields
- Updated configuration conversion to work with new samsungctl API
- Maintained all existing functionality

### 4. Updated Tests

**File**: `test_samsung_remote.py`
- Updated `test_send_success` to mock the new `samsungctl.Config` class
- Updated assertions to use `control` method instead of `command`
- All 51 tests continue to pass

### 5. Enhanced Documentation

**File**: `README.md`
- Added section about updated samsungctl library
- Documented the three new power commands (KEY_POWER, KEY_POWERON, KEY_POWEROFF)
- Added examples section with links to example scripts
- Updated dependency information

### 6. New Examples

**Directory**: `examples/`
- Created `power_commands_example.py` demonstrating the three power commands
- Added `README.md` explaining the examples
- Provided usage instructions and expected output

## New Features

### Enhanced Power Control

The updated samsungctl library provides three distinct power commands:

1. **KEY_POWER**: Toggle power (turns TV on if off, off if on)
2. **KEY_POWERON**: Discrete power on (always turns TV on)
3. **KEY_POWEROFF**: Discrete power off (always turns TV off)

### Improved TV Support

- Better support for H and J model year (2014-2015) TVs
- Enhanced error handling and connection management
- More reliable command interface

## Installation

To use the updated features, install the latest samsungctl from GitHub:

```bash
pip install git+https://github.com/kdschlosser/samsungctl.git
```

## Backward Compatibility

All existing functionality remains unchanged:
- Command line interface is identical
- Macro files continue to work
- Network discovery and TV information retrieval unchanged
- All existing tests pass

## Testing

The project includes comprehensive testing:
- 51 unit tests covering all functionality
- Updated test suite for new API
- Example scripts for demonstration

Run tests with:
```bash
python -m pytest test_samsung_remote.py -v
```

## Migration Guide

For users upgrading from the previous version:

1. **No code changes required** - All existing scripts will continue to work
2. **Enhanced power control** - New power commands available for more precise control
3. **Better reliability** - Improved connection handling and error recovery
4. **Future-proof** - Updated to latest samsungctl API

## References

- [Updated samsungctl library](https://github.com/kdschlosser/samsungctl)
- [Original samsungctl project](https://github.com/Ape/samsungctl)
- [Samsung TV Commands Documentation](SAMSUNG_TV_COMMANDS.md)
