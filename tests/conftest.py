"""Shared test fixtures and configuration for description-parser tests."""

import pytest
import tempfile
import json
import csv
import pandas as pd
from pathlib import Path


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def sample_replacement_dict_data():
    """Sample replacement dictionary data."""
    return {
        "OLD_CODE": "NEW_CODE",
        "TEMP": "TEMPORARY",
        "BLDG": "BUILDING",
        "ST": "STREET",
        "MARKER": "MONUMENT"
    }


@pytest.fixture
def sample_replacement_dict_file(temp_dir, sample_replacement_dict_data):
    """Create a sample replacement dictionary JSON file."""
    dict_file = temp_dir / "replacement_dict.json"
    with open(dict_file, 'w') as f:
        json.dump(sample_replacement_dict_data, f)
    return str(dict_file)


@pytest.fixture
def sample_csv_data():
    """Sample CSV data for testing."""
    return [
        ["Point", "Northing", "Easting", "Elevation", "Description"],
        ["1", "1000.00", "2000.00", "100.00", "PCF 1/2 OLD_CODE"],
        ["2", "1001.00", "2001.00", "101.00", "1/4 PCF TEMP"],
        ["3", "1002.00", "2002.00", "102.00", "TREE PCF 3/4"],
        ["4", "1003.00", "2003.00", "103.00", "PCF TREE BLDG"],
        ["5", "1004.00", "2004.00", "104.00", "MARKER ST SIGN"]
    ]


@pytest.fixture
def sample_csv_file(temp_dir, sample_csv_data):
    """Create a sample CSV file for testing."""
    csv_file = temp_dir / "test_input.csv"
    with open(csv_file, 'w', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerows(sample_csv_data)
    return str(csv_file)


@pytest.fixture
def sample_pandas_csv_file(temp_dir):
    """Create a sample CSV file using pandas for testing."""
    csv_file = temp_dir / "pandas_test.csv"
    data = {
        'Point': [1, 2, 3, 4, 5],
        'Northing': [1000.0, 1001.0, 1002.0, 1003.0, 1004.0],
        'Easting': [2000.0, 2001.0, 2002.0, 2003.0, 2004.0],
        'Elevation': [100.0, 101.0, 102.0, 103.0, 104.0],
        'Description': ['PCF MARKER', 'TREE SIGN', 'BUILDING CORNER', 'OLD_CODE POST', 'TEMP STRUCTURE']
    }
    df = pd.DataFrame(data)
    df.to_csv(csv_file, index=False)
    return str(csv_file)


@pytest.fixture
def property_corners_data():
    """Sample property corners data."""
    return [
        "PCF", "PCFD", "PCS", "PCOS", "PTF", "PTFD",
        "RBC", "RBCS", "RBF", "RBFD", "RBRS", "RBS"
    ]


@pytest.fixture
def property_corners_file(temp_dir, property_corners_data):
    """Create a property corners file."""
    corners_file = temp_dir / "property_corners.txt"
    corners_file.write_text('\n'.join(property_corners_data) + '\n')
    return str(corners_file)


@pytest.fixture
def miscellaneous_data():
    """Sample miscellaneous codes data."""
    return [
        "TREE", "SIGN", "MARKER", "BUILDING", "CORNER",
        "POST", "POLE", "STRUCTURE", "MONUMENT", "FENCE"
    ]


@pytest.fixture
def miscellaneous_file(temp_dir, miscellaneous_data):
    """Create a miscellaneous codes file."""
    misc_file = temp_dir / "miscellaneous.txt"
    misc_file.write_text('\n'.join(miscellaneous_data) + '\n')
    return str(misc_file)


@pytest.fixture
def empty_csv_file(temp_dir):
    """Create an empty CSV file for testing error conditions."""
    empty_file = temp_dir / "empty.csv"
    empty_file.write_text("")
    return str(empty_file)


@pytest.fixture
def invalid_csv_file(temp_dir):
    """Create an invalid CSV file (insufficient columns) for testing."""
    invalid_file = temp_dir / "invalid.csv"
    data = [
        ["Point", "Northing", "Easting"],  # Only 3 columns, need 5
        ["1", "1000.0", "2000.0"],
        ["2", "1001.0", "2001.0"]
    ]
    with open(invalid_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)
    return str(invalid_file)


@pytest.fixture
def corrupted_json_file(temp_dir):
    """Create a corrupted JSON file for testing error handling."""
    corrupted_file = temp_dir / "corrupted.json"
    corrupted_file.write_text('{ "invalid": "json content without closing brace"')
    return str(corrupted_file)


@pytest.fixture
def non_dict_json_file(temp_dir):
    """Create a JSON file that doesn't contain a dictionary."""
    non_dict_file = temp_dir / "non_dict.json"
    with open(non_dict_file, 'w') as f:
        json.dump(["this", "is", "a", "list", "not", "a", "dict"], f)
    return str(non_dict_file)


@pytest.fixture
def large_csv_file(temp_dir):
    """Create a larger CSV file for performance testing."""
    large_file = temp_dir / "large_test.csv"
    
    # Generate 1000 rows of test data
    data = [["Point", "Northing", "Easting", "Elevation", "Description"]]
    for i in range(1, 1001):
        data.append([
            str(i),
            str(1000.0 + i),
            str(2000.0 + i),
            str(100.0 + i/10),
            f"PCF {i%4 + 1}/4 MARKER"
        ])
    
    with open(large_file, 'w', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerows(data)
    
    return str(large_file)


@pytest.fixture
def complex_descriptions_csv(temp_dir):
    """Create a CSV file with complex description patterns for testing."""
    complex_file = temp_dir / "complex_descriptions.csv"
    data = [
        ["Point", "Northing", "Easting", "Elevation", "Description"],
        ["1", "1000.0", "2000.0", "100.0", "PCF 1/2"],  # Property code + size
        ["2", "1001.0", "2001.0", "101.0", "3/4 PCF"],  # Size + property code
        ["3", "1002.0", "2002.0", "102.0", "TREE PCF 1"],  # Misc + property + size
        ["4", "1003.0", "2003.0", "103.0", "PCF TREE"],  # Property + misc (should reorder)
        ["5", "1004.0", "2004.0", "104.0", "PCF MARKER"],  # Property + non-size
        ["6", "1005.0", "2005.0", "105.0", "TREE 2"],  # Misc + size
        ["7", "1006.0", "2006.0", "106.0", "SIGN POST"],  # Two misc codes
        ["8", "1007.0", "2007.0", "107.0", "INVALID CODE"],  # No valid codes
    ]
    
    with open(complex_file, 'w', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerows(data)
    
    return str(complex_file)


# Test configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "gui: marks tests that require GUI components"
    )


# Custom assertions for better test readability
class CSVAssertions:
    """Custom assertions for CSV-related tests."""
    
    @staticmethod
    def assert_csv_has_columns(csv_file, expected_columns):
        """Assert that CSV file has expected columns."""
        df = pd.read_csv(csv_file)
        assert list(df.columns) == expected_columns, f"Expected columns {expected_columns}, got {list(df.columns)}"
    
    @staticmethod
    def assert_csv_row_count(csv_file, expected_count):
        """Assert that CSV file has expected number of rows."""
        df = pd.read_csv(csv_file)
        assert len(df) == expected_count, f"Expected {expected_count} rows, got {len(df)}"
    
    @staticmethod
    def assert_description_contains(csv_file, row_index, expected_text):
        """Assert that a specific row's description contains expected text."""
        df = pd.read_csv(csv_file)
        description = df.iloc[row_index]['Description']
        assert expected_text in description, f"Expected '{expected_text}' in '{description}'"
    
    @staticmethod
    def assert_descriptions_changed(original_file, processed_file, min_changes=1):
        """Assert that descriptions were changed between original and processed files."""
        original_df = pd.read_csv(original_file)
        processed_df = pd.read_csv(processed_file)
        
        original_descriptions = original_df['Description'].tolist()
        processed_descriptions = processed_df['Description'].tolist()
        
        changes = sum(1 for orig, proc in zip(original_descriptions, processed_descriptions) if orig != proc)
        assert changes >= min_changes, f"Expected at least {min_changes} changes, got {changes}"


@pytest.fixture
def csv_assertions():
    """Provide CSV assertion utilities."""
    return CSVAssertions()


# Mock GUI components for testing
@pytest.fixture
def mock_gui_components():
    """Provide mock GUI components for testing."""
    from unittest.mock import Mock, patch
    
    mocks = {
        'tk_root': Mock(),
        'treeview': Mock(),
        'button': Mock(),
        'entry': Mock(),
        'messagebox_info': Mock(),
        'messagebox_error': Mock(),
        'filedialog': Mock()
    }
    
    # Set up common mock behaviors
    mocks['filedialog'].askopenfilename.return_value = "test_file.csv"
    mocks['treeview'].get_children.return_value = ['0', '1', '2']
    mocks['treeview'].item.return_value = {'values': ['1', '1000.0', '2000.0', '100.0', 'TEST']}
    
    return mocks


# Performance testing utilities
@pytest.fixture
def performance_timer():
    """Provide a simple performance timer for tests."""
    import time
    
    class Timer:
        def __init__(self):
            self.start_time = None
            self.end_time = None
        
        def start(self):
            self.start_time = time.time()
        
        def stop(self):
            self.end_time = time.time()
        
        @property
        def elapsed(self):
            if self.start_time is None or self.end_time is None:
                return None
            return self.end_time - self.start_time
        
        def assert_under(self, max_seconds):
            assert self.elapsed is not None, "Timer not started/stopped"
            assert self.elapsed < max_seconds, f"Expected under {max_seconds}s, took {self.elapsed}s"
    
    return Timer()
