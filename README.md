# samsung_remote

A Samsung TV Remote Control Python Script

## Description

samsung_remote is a script written in Python that can remotely control your Samsung Smart TV through wifi. It uses the great [samsungctl](https://github.com/Ape/samsungctl) project to send the commands to TV and supports some nice features, such as:

- scan the network to find all available TV's;
- turn off all the TV's with one command;
- specify which TV to send commands;
- save common routines in a macro file to be executed later. (video of a macro being executed: https://youtu.be/UXxBB7BOMDM)

**Note**: This codebase has been refactored by Cursor to improve maintainability, add comprehensive unit testing, and enhance code quality while preserving all original functionality.

## Usage

```bash
usage: samsung_remote.py [-h] [-a | -i ip] [-k key] [-l] [-m <file>] [-p] [-q] [-s]
```

### Optional Arguments

- `-h, --help` - show this help message and exit
- `-a, --auto` - send command to the first TV available
- `-i ip, --ip ip` - defines the ip of the TV that will receive the command
- `-k key, --key key` - the key to be sent to TV (e.g., KEY_POWER, KEY_VOLUP)
- `-l, --legacy` - use legacy method instead of default mode (websocket)
- `-m <file>, --macro <file>` - the macro file with commands to be sent to TV
- `-p, --power-off-all` - search all TV's in the network and turn them off
- `-q, --quiet` - do not print messages to console
- `-s, --scan` - scans the network and print all the TV's found

### Examples

```bash
# Scan for TVs
python samsung_remote.py -s

# Send power command to specific TV
python samsung_remote.py -i 192.168.1.100 -k KEY_POWER

# Send volume up to first available TV
python samsung_remote.py -a -k KEY_VOLUP

# Power off all TVs
python samsung_remote.py -p

# Execute macro file
python samsung_remote.py -m macro.csv
```

## Dependencies

- Python 3.7 or higher
- [samsungctl](https://github.com/Ape/samsungctl)
- `websocket-client`

You can install the dependencies running:

```bash
pip3 install -r requirements.txt
```

### Development Setup

For development, it's recommended to use a virtual environment:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r test_requirements.txt
```

## Unit Testing

The refactored codebase includes comprehensive unit testing with the following features:

### Test Coverage
- **Test Coverage**: 70%+ test coverage across all modules

### Test Files
- `test_samsung_remote.py` - Main test suite
- `test_edge_cases.py` - Edge cases and error conditions
- `run_tests.py` - Test runner script

### Test Categories
- Unit tests for individual functions and modules
- Integration tests for component interaction
- Mock tests using mocked dependencies
- Edge case tests for error conditions

### Running Tests

```bash
# Install test dependencies
pip install -r test_requirements.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest test_samsung_remote.py
```

### Test Classes
- `TestTVInfo` - TV information retrieval tests
- `TestTVCon` - TV control functionality tests
- `TestSSDP` - Network discovery tests
- `TestMacro` - Macro execution tests
- `TestSamsungRemote` - Main application logic tests
- `TestIntegration` - End-to-end workflow tests
- `TestEdgeCases` - Error handling and edge cases

## Refactoring Improvements

The codebase has been refactored to improve:

- **Code Quality**: Better structure, type hints, and error handling
- **Maintainability**: Modular design with clear separation of concerns
- **Testing**: Comprehensive test suite with mocking strategies
- **Documentation**: Enhanced inline documentation and examples
- **Error Handling**: Consistent error handling with context managers
- **Configuration**: Dataclass-based configuration management

## References

- SSDP discovery: https://gist.github.com/dankrause/6000248 and http://forum.micasaverde.com/index.php?topic=7878.15
- Regular expression to get the XML namespace: https://stackoverflow.com/a/12946675/2383657
- Correctly parse XML with namespaces: https://codereview.stackexchange.com/a/51132
- Samsung TV Commands Documentation: [`SAMSUNG_TV_COMMANDS.md`](SAMSUNG_TV_COMMANDS.md)
