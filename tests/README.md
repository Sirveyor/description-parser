# Tests for Description Parser

This directory contains comprehensive tests for the description-parser project.

## Test Structure

```
tests/
├── __init__.py                 # Test package initialization
├── conftest.py                # Shared fixtures and configuration
├── test_data/                 # Test data files
│   ├── sample_replacement_dict.json
│   ├── sample_input.csv
│   ├── parser3_test_input.csv
│   ├── test_property_corners.txt
│   └── test_miscellaneous.txt
├── test_description_parser.py  # Tests for description_parser module
├── test_parser3.py            # Tests for parser3 module
├── test_csv_editor.py         # Tests for csv_editor module
├── test_main.py               # Tests for main module
└── test_integration.py        # Integration tests
```

## Test Categories

### Unit Tests
- **test_description_parser.py**: Tests for the DescriptionParser class
  - Dictionary loading and validation
  - File processing logic
  - Error handling
  - GUI interactions (mocked)

- **test_parser3.py**: Tests for parser3 functionality
  - Size detection algorithms
  - Code validation logic
  - File processing rules
  - Code list loading

- **test_csv_editor.py**: Tests for CSV editor GUI
  - CSV loading and display
  - Cell editing functionality
  - Save operations
  - GUI component interactions (mocked)

- **test_main.py**: Tests for main entry point
  - Module execution order
  - Error propagation
  - Integration between modules

### Integration Tests
- **test_integration.py**: End-to-end workflow tests
  - Complete processing pipeline
  - Data consistency across modules
  - Error handling integration
  - Performance testing

## Running Tests

### Install Dependencies
```bash
# Install test dependencies
pip install -e ".[test]"

# Or install manually
pip install pytest pytest-mock pytest-cov pytest-xvfb
```

### Run All Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=description-parser --cov-report=html

# Run with verbose output
pytest -v
```

### Run Specific Test Categories
```bash
# Run only unit tests
pytest tests/test_*.py -k "not integration"

# Run only integration tests
pytest tests/test_integration.py

# Run tests for specific module
pytest tests/test_description_parser.py

# Run tests with specific markers
pytest -m "not slow"  # Skip slow tests
pytest -m "integration"  # Run only integration tests
```

### Run Tests with Different Options
```bash
# Run tests in parallel (if pytest-xdist is installed)
pytest -n auto

# Run tests with coverage and generate HTML report
pytest --cov=description-parser --cov-report=html --cov-report=term

# Run tests and stop on first failure
pytest -x

# Run tests with detailed output
pytest -vv

# Run specific test function
pytest tests/test_description_parser.py::TestDescriptionParser::test_init_with_valid_dict
```

## Test Data

The `test_data/` directory contains sample files used by the tests:

- **sample_replacement_dict.json**: Sample dictionary for description replacements
- **sample_input.csv**: Basic CSV file for testing
- **parser3_test_input.csv**: CSV with complex description patterns
- **test_property_corners.txt**: Sample property corner codes
- **test_miscellaneous.txt**: Sample miscellaneous codes

## Fixtures

The `conftest.py` file provides shared fixtures:

- **temp_dir**: Temporary directory for test files
- **sample_csv_file**: Creates sample CSV files
- **sample_replacement_dict_file**: Creates dictionary files
- **property_corners_file**: Creates property corners files
- **miscellaneous_file**: Creates miscellaneous codes files
- **csv_assertions**: Custom assertions for CSV testing
- **mock_gui_components**: Mock GUI components for testing
- **performance_timer**: Timer for performance testing

## Test Markers

Tests are marked with custom markers:

- `@pytest.mark.slow`: Marks slow-running tests
- `@pytest.mark.integration`: Marks integration tests
- `@pytest.mark.gui`: Marks tests requiring GUI components

## Mocking Strategy

GUI components are extensively mocked to allow testing without requiring a display:

- Tkinter components (Tk, Treeview, Button, Entry)
- Message boxes (showinfo, showerror)
- File dialogs (askopenfilename)

## Coverage

The test suite aims for high code coverage:

- Unit tests cover individual functions and methods
- Integration tests cover complete workflows
- Error handling tests cover exception scenarios
- Edge cases and boundary conditions are tested

## Continuous Integration

The test configuration supports CI/CD environments:

- Tests can run headless (using pytest-xvfb for GUI tests)
- Coverage reports can be generated in multiple formats
- Tests are organized to allow selective execution

## Adding New Tests

When adding new tests:

1. Follow the existing naming convention (`test_*.py`)
2. Use appropriate fixtures from `conftest.py`
3. Add custom fixtures to `conftest.py` if they're reusable
4. Mock GUI components appropriately
5. Add appropriate test markers
6. Include both positive and negative test cases
7. Test error conditions and edge cases

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure the project is installed in development mode:
   ```bash
   pip install -e .
   ```

2. **GUI Test Failures**: Install pytest-xvfb for headless GUI testing:
   ```bash
   pip install pytest-xvfb
   ```

3. **Coverage Issues**: Ensure all source files are in the coverage configuration in `pyproject.toml`

4. **Slow Tests**: Use markers to skip slow tests during development:
   ```bash
   pytest -m "not slow"
   ```

### Debug Mode

Run tests with debugging enabled:
```bash
# Run with Python debugger
pytest --pdb

# Run with detailed tracebacks
pytest --tb=long

# Run with print statements visible
pytest -s
