# UML Tools Dashboard Tests

This directory contains a streamlined test suite for the UML Tools Dashboard application with **comprehensive test files** that cover all functionality without redundancy.

## Test Files

### `test_basic_validation.py` ⭐ **Start Here**
Basic validation test that runs without external dependencies:
- **File structure**: Validates all required files exist
- **CSV format**: Checks snapshot.csv format and content
- **App structure**: Verifies app.py has required functions and imports
- **Fallback logic**: Confirms fallback mechanism is implemented

**Coverage:**
- ✅ No external dependencies required
- ✅ File structure validation
- ✅ CSV data format verification
- ✅ App.py structure validation
- ✅ Fallback mechanism presence verification

**Usage:**
```bash
python tests/test_basic_validation.py
```

### `test_normal_operation.py`
Comprehensive test suite for normal dashboard operation:
- **Basic functionality**: File structure, imports, and dependencies
- **CSV data handling**: Loading, validation, and format conversion
- **Normal API operation**: Mocked successful GitHub API calls
- **Integration testing**: End-to-end functionality verification

**Coverage:**
- ✅ File structure validation
- ✅ Module imports and dependencies
- ✅ CSV data loading and integrity
- ✅ CSV to GitHub API format conversion
- ✅ Normal GitHub API response handling
- ✅ Function availability and import capability

**Usage:**
```bash
python tests/test_normal_operation.py
```

### `test_fallback_mechanism.py`
Comprehensive test suite for the API fallback mechanism:
- **Fallback triggers**: Network errors, HTTP errors, timeouts
- **Data handling**: BOM handling, conversion accuracy, consistency
- **User notifications**: Error messages, warnings, success confirmations
- **Edge cases**: Missing files, corrupted data handling

**Coverage:**
- ✅ Network error fallback handling
- ✅ HTTP error response fallback
- ✅ Request timeout fallback
- ✅ CSV BOM (Byte Order Mark) handling
- ✅ Data conversion accuracy during fallback
- ✅ Data consistency validation
- ✅ User notification system
- ✅ Edge case handling (missing files, corrupted data)

**Usage:**
```bash
python tests/test_fallback_mechanism.py
```

## Running Tests

### Quick Start (No Dependencies Required) ⭐
For immediate validation without installing anything:
```bash
cd /path/to/oss-uml-tools
python tests/test_basic_validation.py
```

### Prerequisites for Full Tests
Make sure you have all required dependencies installed:
```bash
pip install -r requirements.txt
```

### Normal Operation Test
For basic functionality verification:
```bash
cd /path/to/oss-uml-tools
python tests/test_normal_operation.py
```

### Fallback Mechanism Test
For comprehensive fallback mechanism testing:
```bash
cd /path/to/oss-uml-tools
python tests/test_fallback_mechanism.py
```

### Run All Tests
To run all tests:
```bash
python tests/test_basic_validation.py && python tests/test_normal_operation.py && python tests/test_fallback_mechanism.py
```

## Test Architecture

### Why This Structure?
The original five test files had significant overlap and redundancy. The new structure consolidates all functionality into three focused files:

1. **Basic Validation** - Quick verification without dependencies
2. **Normal Operation** - Everything that should work when the system is functioning correctly  
3. **Fallback Mechanism** - Everything related to graceful degradation when the GitHub API fails

### Benefits of Consolidation
- ✅ **Reduced maintenance**: Three focused files instead of five overlapping ones
- ✅ **No redundancy**: Each test serves a unique purpose
- ✅ **Complete coverage**: All original functionality is preserved
- ✅ **Progressive complexity**: Start basic, then move to comprehensive tests
- ✅ **Clearer organization**: Tests are grouped by functional area
- ✅ **Faster execution**: Less duplicate test setup and teardown

## Test Coverage

### Normal Operation Tests
- Basic Python module imports
- Required file existence (app.py, analysis.py, requirements.txt, snapshot.csv)
- CSV data integrity and format validation
- Data type validation and conversion logic
- Function import capability from app.py
- Mocked successful GitHub API operations
- Dependency availability checking

### Fallback Mechanism Tests
- Network error handling and fallback triggering
- HTTP error responses (403, 404, 500, 503) and fallback
- Request timeout handling
- CSV loading with proper BOM handling
- Data conversion accuracy during fallback scenarios  
- Data structure consistency after fallback
- User notification system (errors, warnings, info messages)
- Edge cases: missing snapshot.csv, corrupted data

## Expected Behavior

### When GitHub API is Available (Normal Operation)
1. Fetch repositories from GitHub API
2. Process and filter data according to criteria
3. Display repositories in dashboard with full functionality

### When GitHub API Fails (Fallback Mechanism)
1. Detect API failure (network error, HTTP error, or timeout)
2. Display appropriate error message to user
3. Show warning about switching to snapshot data
4. Load data from `snapshot.csv` with proper BOM handling
5. Convert CSV data to GitHub API format
6. Continue normal operation with fallback data
7. Display success message about loaded snapshot data

## Test Data

The tests use the `snapshot.csv` file located in the root directory. This file contains repository data in the following format:

| Column | Description |
|--------|-------------|
| Name | Repository name |
| Stars⭐ | Star count |
| Last Updated | Last commit date (YYYY-MM-DD) |
| First Commit | Creation date (YYYY-MM-DD) |
| URL | GitHub repository URL |
| Forks | Fork count |
| Issues | Open issues count |
| Language | Primary programming language |
| License | License type |
| Description | Repository description |
| Topics | Comma-separated topics |

## Troubleshooting

### Common Issues

1. **Missing snapshot.csv**: Ensure the snapshot.csv file exists in the root directory
2. **Import errors**: Make sure the current working directory is the root of the project
3. **Dependency issues**: Run `pip install -r requirements.txt`
4. **Streamlit warnings**: These are expected during testing and can be ignored
5. **BOM issues**: Tests verify proper BOM handling in CSV files

### Test Failures

If tests fail, check:
1. All dependencies are installed (`pip install -r requirements.txt`)
2. The snapshot.csv file exists and has the correct format
3. You're running tests from the correct directory (project root)
4. Network connectivity (for API-related tests, though they use mocks)

## Contributing

When adding new tests:
1. Determine if the test belongs in **normal operation** or **fallback mechanism**
2. Add to the appropriate existing file rather than creating new files
3. Follow the existing naming convention and structure
4. Include proper docstrings and test descriptions
5. Add both positive and negative test cases where appropriate
6. Update this README if significant functionality is added

The goal is to maintain comprehensive test coverage while keeping the test suite simple and maintainable with just these two focused test files. 