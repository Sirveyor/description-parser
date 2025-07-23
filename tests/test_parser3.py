"""Tests for parser3 module."""

import pytest
import csv
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch, mock_open

# Add the parent directory to the path so we can import the modules
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

import parser3


class TestParser3Functions:
    """Test cases for parser3 utility functions."""

    def test_item_is_size_valid_sizes(self):
        """Test size detection with valid size formats."""
        assert parser3.item_is_size("1/2") is True
        assert parser3.item_is_size("3/4") is True
        assert parser3.item_is_size("1") is True
        assert parser3.item_is_size("2") is True
        assert parser3.item_is_size('1/4"') is True
        assert parser3.item_is_size("1/2'") is True

    def test_item_is_size_invalid_sizes(self):
        """Test size detection with invalid formats."""
        assert parser3.item_is_size("PCF") is False
        assert parser3.item_is_size("MARKER") is False
        assert parser3.item_is_size("ABC") is False
        assert parser3.item_is_size("") is False

    def test_number_of_codes_zero_codes(self):
        """Test code counting with no valid codes."""
        property_codes = ["PCF", "PTF", "RBC"]
        misc_codes = ["TREE", "SIGN", "MARKER"]
        
        result = parser3.number_of_codes(["INVALID", "CODES"], property_codes, misc_codes)
        assert result == "zero"

    def test_number_of_codes_one_code(self):
        """Test code counting with one valid code."""
        property_codes = ["PCF", "PTF", "RBC"]
        misc_codes = ["TREE", "SIGN", "MARKER"]
        
        result = parser3.number_of_codes(["PCF", "INVALID"], property_codes, misc_codes)
        assert result == "one"
        
        result = parser3.number_of_codes(["TREE", "INVALID"], property_codes, misc_codes)
        assert result == "one"

    def test_number_of_codes_two_codes(self):
        """Test code counting with two valid codes."""
        property_codes = ["PCF", "PTF", "RBC"]
        misc_codes = ["TREE", "SIGN", "MARKER"]
        
        result = parser3.number_of_codes(["PCF", "TREE"], property_codes, misc_codes)
        assert result == "two"

    def test_number_of_codes_case_insensitive(self):
        """Test that code counting is case insensitive."""
        property_codes = ["PCF", "PTF", "RBC"]
        misc_codes = ["TREE", "SIGN", "MARKER"]
        
        result = parser3.number_of_codes(["pcf", "tree"], property_codes, misc_codes)
        assert result == "two"

    def test_number_of_codes_invalid_input(self):
        """Test code counting with invalid input."""
        property_codes = ["PCF", "PTF", "RBC"]
        misc_codes = ["TREE", "SIGN", "MARKER"]
        
        result = parser3.number_of_codes("not_a_list", property_codes, misc_codes)
        assert result == "zero"

    def test_load_code_lists_success(self, tmp_path):
        """Test successful loading of code lists."""
        # Create temporary files
        prop_file = tmp_path / "property.txt"
        misc_file = tmp_path / "misc.txt"
        
        prop_file.write_text("PCF\nPTF\nRBC\n")
        misc_file.write_text("TREE\nSIGN\nMARKER\n")
        
        prop_codes, misc_codes = parser3.load_code_lists(str(prop_file), str(misc_file))
        
        assert "pcf" in prop_codes  # Should be lowercase
        assert "ptf" in prop_codes
        assert "rbc" in prop_codes
        assert "TREE" in misc_codes
        assert "SIGN" in misc_codes
        assert "MARKER" in misc_codes

    @patch('tkinter.messagebox.showerror')
    def test_load_code_lists_file_not_found(self, mock_messagebox):
        """Test loading code lists with non-existent files."""
        prop_codes, misc_codes = parser3.load_code_lists("nonexistent1.txt", "nonexistent2.txt")
        
        assert prop_codes == []
        assert misc_codes == []
        mock_messagebox.assert_called()

    @patch('tkinter.messagebox.showerror')
    def test_load_code_lists_general_error(self, mock_messagebox, tmp_path):
        """Test loading code lists with general error."""
        # Create a directory instead of a file to cause an error
        prop_dir = tmp_path / "property_dir"
        prop_dir.mkdir()
        misc_file = tmp_path / "misc.txt"
        misc_file.write_text("TREE\n")
        
        prop_codes, misc_codes = parser3.load_code_lists(str(prop_dir), str(misc_file))
        
        assert prop_codes == []
        assert misc_codes == []
        mock_messagebox.assert_called()


class TestParser3FileProcessing:
    """Test cases for file processing functionality."""

    @pytest.fixture
    def sample_csv_data(self):
        """Sample CSV data for testing."""
        return [
            ["Point", "Northing", "Easting", "Elevation", "Description"],
            ["1", "1000.00", "2000.00", "100.00", "PCF 1/2"],
            ["2", "1001.00", "2001.00", "101.00", "1/4 PCF"],
            ["3", "1002.00", "2002.00", "102.00", "TREE PCF 3/4"],
            ["4", "1003.00", "2003.00", "103.00", "PCF TREE"],
        ]

    @pytest.fixture
    def temp_csv_file(self, tmp_path, sample_csv_data):
        """Create a temporary CSV file for testing."""
        csv_file = tmp_path / "test_input.csv"
        with open(csv_file, 'w', newline='', encoding='utf8') as f:
            writer = csv.writer(f)
            writer.writerows(sample_csv_data)
        return str(csv_file)

    @patch('tkinter.messagebox.showinfo')
    def test_process_file_success(self, mock_messagebox, temp_csv_file):
        """Test successful file processing."""
        property_codes = ["PCF", "PTF", "RBC"]
        misc_codes = ["TREE", "SIGN", "MARKER"]
        
        output_file = parser3.process_file(temp_csv_file, property_codes, misc_codes)
        
        # Check that output file exists
        assert os.path.exists(output_file)
        
        # Check that success message was shown
        mock_messagebox.assert_called_once()
        
        # Verify output file content
        with open(output_file, 'r', newline='', encoding='utf8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            
            # Check header row
            assert rows[0] == ["Point", "Northing", "Easting", "Elevation", "Description"]
            
            # Check processed descriptions
            descriptions = [row[4] for row in rows[1:]]
            assert "PCF \\1/2" in descriptions  # Size should have backslash
            assert "PCF \\1/4" in descriptions  # Swapped and size has backslash

    @patch('tkinter.messagebox.showerror')
    def test_process_file_not_found(self, mock_messagebox):
        """Test processing non-existent file."""
        property_codes = ["PCF"]
        misc_codes = ["TREE"]
        
        with pytest.raises(FileNotFoundError):
            parser3.process_file("nonexistent.csv", property_codes, misc_codes)
        
        mock_messagebox.assert_called_once()

    @patch('tkinter.messagebox.showerror')
    def test_process_file_general_error(self, mock_messagebox, tmp_path):
        """Test processing file with general error."""
        # Create a directory instead of a file
        csv_dir = tmp_path / "not_a_file.csv"
        csv_dir.mkdir()
        
        property_codes = ["PCF"]
        misc_codes = ["TREE"]
        
        with pytest.raises(Exception):
            parser3.process_file(str(csv_dir), property_codes, misc_codes)
        
        mock_messagebox.assert_called_once()

    def test_process_file_one_code_rules(self, tmp_path):
        """Test processing rules for descriptions with one code."""
        # Create test data with one code scenarios
        test_data = [
            ["Point", "Northing", "Easting", "Elevation", "Description"],
            ["1", "1000.00", "2000.00", "100.00", "PCF 1/2"],  # Property code + size
            ["2", "1001.00", "2001.00", "101.00", "1/4 PCF"],  # Size + property code
            ["3", "1002.00", "2002.00", "102.00", "PCF MARKER"],  # Property code + non-size
            ["4", "1003.00", "2003.00", "103.00", "TREE 1/2"],  # Misc code + size
        ]
        
        csv_file = tmp_path / "one_code_test.csv"
        with open(csv_file, 'w', newline='', encoding='utf8') as f:
            writer = csv.writer(f)
            writer.writerows(test_data)
        
        property_codes = ["PCF"]
        misc_codes = ["TREE", "MARKER"]
        
        with patch('tkinter.messagebox.showinfo'):
            output_file = parser3.process_file(str(csv_file), property_codes, misc_codes)
        
        # Verify the processing rules
        with open(output_file, 'r', newline='', encoding='utf8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            descriptions = [row[4] for row in rows[1:]]
            
            assert "PCF \\1/2" in descriptions  # Property + size -> add backslash
            assert "PCF \\1/4" in descriptions  # Size + property -> swap and add backslash
            assert "MARKER PCF" in descriptions  # Property + misc -> reorder (treated as two codes)

    def test_process_file_two_code_rules(self, tmp_path):
        """Test processing rules for descriptions with two codes."""
        test_data = [
            ["Point", "Northing", "Easting", "Elevation", "Description"],
            ["1", "1000.00", "2000.00", "100.00", "PCF TREE 1/2"],  # Property + misc + size
            ["2", "1001.00", "2001.00", "101.00", "TREE PCF 3/4"],  # Misc + property + size
            ["3", "1002.00", "2002.00", "102.00", "PCF TREE MARKER"],  # Property + misc + non-size
        ]
        
        csv_file = tmp_path / "two_code_test.csv"
        with open(csv_file, 'w', newline='', encoding='utf8') as f:
            writer = csv.writer(f)
            writer.writerows(test_data)
        
        property_codes = ["PCF"]
        misc_codes = ["TREE", "MARKER"]
        
        with patch('tkinter.messagebox.showinfo'):
            output_file = parser3.process_file(str(csv_file), property_codes, misc_codes)
        
        # Verify the processing rules
        with open(output_file, 'r', newline='', encoding='utf8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            descriptions = [row[4] for row in rows[1:]]
            
            # Should reorder so misc comes before property, and handle third item
            assert "TREE PCF \\1/2" in descriptions
            assert "TREE PCF \\3/4" in descriptions
            assert "TREE PCF /MARKER" in descriptions


class TestParser3GUI:
    """Test cases for GUI functions."""

    @patch('tkinter.filedialog.askopenfilename')
    @patch('tkinter.Tk')
    def test_select_input_file_success(self, mock_tk, mock_filedialog):
        """Test successful file selection."""
        mock_filedialog.return_value = "/path/to/file.txt"
        
        result = parser3.select_input_file()
        
        assert result == "/path/to/file.txt"
        mock_filedialog.assert_called_once()

    @patch('tkinter.filedialog.askopenfilename')
    @patch('tkinter.Tk')
    def test_select_input_file_cancelled(self, mock_tk, mock_filedialog):
        """Test cancelled file selection."""
        mock_filedialog.return_value = ""
        
        result = parser3.select_input_file()
        
        assert result == ""

    @patch('parser3.CSVEditor')
    def test_display_csv_file(self, mock_csv_editor):
        """Test CSV file display function."""
        mock_editor_instance = Mock()
        mock_csv_editor.return_value = mock_editor_instance
        
        parser3.display_csv_file("test.csv")
        
        mock_csv_editor.assert_called_once_with("test.csv")
        mock_editor_instance.run.assert_called_once()


class TestParser3Main:
    """Test cases for main function."""

    @patch('parser3.display_csv_file')
    @patch('parser3.process_file')
    @patch('parser3.load_code_lists')
    @patch('parser3.select_input_file')
    def test_main_function_success(self, mock_select_file, mock_load_codes, 
                                   mock_process_file, mock_display_csv):
        """Test successful main function execution."""
        # Setup mocks
        mock_select_file.return_value = "input.txt"
        mock_load_codes.return_value = (["PCF"], ["TREE"])
        mock_process_file.return_value = "output.csv"
        
        # Run main
        parser3.main()
        
        # Verify calls
        mock_select_file.assert_called_once()
        mock_load_codes.assert_called_once()
        mock_process_file.assert_called_once_with("input.txt", ["PCF"], ["TREE"])
        mock_display_csv.assert_called_once_with("output.csv")

    @patch('parser3.select_input_file')
    def test_main_function_no_file_selected(self, mock_select_file):
        """Test main function when no file is selected."""
        mock_select_file.return_value = ""
        
        # Should not raise an exception
        # Note: The current main() function doesn't handle empty file selection,
        # so this test documents the current behavior
        with pytest.raises(Exception):
            parser3.main()
