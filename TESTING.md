# Testing Guide for Samsung TV Remote Control

This document describes the testing setup and how to run tests for the Samsung TV Remote Control project.

## Overview

The project includes a comprehensive test suite with the following components:

- **Unit Tests**: Test individual functions and modules in isolation
- **Integration Tests**: Test how components work together
- **Edge Case Tests**: Test error conditions and boundary cases
- **Mock Tests**: Use mocked dependencies to avoid requiring actual Samsung TVs

## Test Structure

### Main Test Files

- `test_samsung_remote.py` - Main test suite covering all modules
- `test_edge_cases.py` - Edge cases and error condition tests
- `run_tests.py` - Test runner script with various options

### Test Classes

1. **TestTVInfo** - Tests for TV information retrieval
   - Model detection (legacy vs websocket)
   - XML parsing and namespace handling
   - Network requests and error handling

2. **TestTVCon** - Tests for TV control functionality
   - Command sending with different methods
   - Error handling (socket errors, websocket errors)
   - Configuration validation

3. **TestSSDP** - Tests for network discovery
   - SSDP protocol implementation
   - Network scanning functionality
   - Response parsing

4. **TestMacro** - Tests for macro execution
   - CSV file parsing
   - Command sequence execution
   - Comment handling and error cases

5. **TestSamsungRemote** - Tests for main application logic
   - Command line argument parsing
   - Logging configuration
   - Main workflow execution

6. **TestIntegration** - Integration tests
   - End-to-end workflows
   - Component interaction

7. **TestEdgeCases** - Edge case and error handling tests
   - Invalid inputs
   - Network failures
   - File system errors

## Running Tests

### Prerequisites

Install test dependencies:

```bash
pip install -r test_requirements.txt
```

### Running All Tests

```bash
# Using the test runner script
python run_tests.py

# Using pytest directly
pytest test_samsung_remote.py test_edge_cases.py -v

# Using unittest
python -m unittest discover -v
```

### Running Specific Tests

```bash
# Run a specific test class
python run_tests.py TestTVInfo

# Run a specific test method
pytest test_samsung_remote.py::TestTVInfo::test_getMethod_legacy_models -v

# Run tests with coverage
pytest --cov=. --cov-report=html test_samsung_remote.py
```

### Test Options

```bash
# Run tests with coverage report
pytest --cov=. --cov-report=term-missing --cov-report=html

# Run only unit tests (exclude integration tests)
pytest -m "not integration"

# Run only fast tests (exclude slow tests)
pytest -m "not slow"

# Run tests with detailed output
pytest -v -s
```

## Test Coverage

The test suite aims to provide comprehensive coverage of:

- **Functionality**: All public functions and methods
- **Error Handling**: Network errors, file errors, invalid inputs
- **Edge Cases**: Empty inputs, boundary conditions, unexpected data
- **Integration**: Component interaction and workflows

### Coverage Reports

After running tests with coverage, you can view detailed reports:

- **Terminal**: Shows missing lines in terminal output
- **HTML**: Generated in `htmlcov/` directory - open `htmlcov/index.html` in browser
- **XML**: Generated for CI/CD integration

## Mocking Strategy

The tests use extensive mocking to avoid requiring actual Samsung TVs:

- **Network Calls**: Mocked using `unittest.mock.patch`
- **File System**: Mocked file operations for macro testing
- **External Libraries**: Mocked `samsungctl` and `websocket-client`
- **System Calls**: Mocked socket operations for SSDP testing

## Test Data

### Sample TV Configurations

```python
# Standard TV config for testing
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
```

### Sample Macro Files

```csv
key,wait
KEY_POWER,500
KEY_UP,100
KEY_ENTER,200
# This is a comment
KEY_DOWN,150
```

## Continuous Integration

The test suite is designed to work with CI/CD systems:

- **GitHub Actions**: Can use the pytest configuration
- **Travis CI**: Compatible with Python testing workflows
- **Jenkins**: Can generate coverage reports and test results

## Adding New Tests

When adding new functionality, follow these guidelines:

1. **Test Structure**: Use descriptive test method names
2. **Mocking**: Mock external dependencies appropriately
3. **Coverage**: Ensure new code is covered by tests
4. **Documentation**: Add docstrings to test methods

### Example Test Method

```python
def test_new_functionality_success(self):
    """Test new functionality with valid inputs"""
    # Arrange
    input_data = "test_input"
    expected_result = "expected_output"
    
    # Act
    with patch('module.external_dependency') as mock_dep:
        mock_dep.return_value = expected_result
        result = function_under_test(input_data)
    
    # Assert
    self.assertEqual(result, expected_result)
    mock_dep.assert_called_once_with(input_data)
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure you're running tests from the correct directory
2. **Mock Issues**: Check that mock patches target the correct import paths
3. **Coverage Issues**: Verify that all code paths are being tested

### Debug Mode

Run tests with debug output:

```bash
pytest -v -s --tb=long
```

This will show detailed error traces and allow you to see print statements.

## Performance

The test suite is designed to run quickly:

- **Unit Tests**: < 5 seconds
- **Integration Tests**: < 10 seconds
- **Full Suite**: < 15 seconds

Tests use minimal wait times and mock external dependencies to ensure fast execution.
