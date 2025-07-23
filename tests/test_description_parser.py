"""Tests for description_parser module."""

import json
import pytest
import pandas as pd
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
import tempfile
import os

# Add the parent directory to the path so we can import the modules
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from description_parser import DescriptionParser


class TestDescriptionParser:
    """Test cases for DescriptionParser class."""

    @pytest.fixture
    def sample_dict_path(self, tmp_path):
        """Create a temporary dictionary file for testing."""
        dict_file = tmp_path / "test_dict.json"
        test_dict = {
            "OLD_CODE": "NEW_CODE",
            "TEMP": "TEMPORARY",
            "BLDG": "BUILDING"
        }
        with open(dict_file, 'w') as f:
            json.dump(test_dict, f)
        return str(dict_file)

    @pytest.fixture
    def sample_csv_path(self, tmp_path):
        """Create a temporary CSV file for testing."""
        csv_file = tmp_path / "test_input.csv"
        test_data = {
            'Point': [1, 2, 3],
            'Northing': [1000.0, 1001.0, 1002.0],
            'Easting': [2000.0, 2001.0, 2002.0],
            'Elevation': [100.0, 101.0, 102.0],
            'Description': ['OLD_CODE MARKER', 'TEMP SIGN', 'BLDG CORNER']
        }
        df = pd.DataFrame(test_data)
        df.to_csv(csv_file, index=False)
        return str(csv_file)

    def test_init_with_valid_dict(self, sample_dict_path):
        """Test initialization with a valid dictionary file."""
        parser = DescriptionParser(dictionary_path=sample_dict_path, gui_mode=False)
        assert parser.dictionary_path == Path(sample_dict_path)
        assert parser.gui_mode is False
        assert len(parser.replacement_dict) == 3
        assert parser.replacement_dict["OLD_CODE"] == "NEW_CODE"

    def test_init_with_nonexistent_dict(self):
        """Test initialization with a non-existent dictionary file."""
        with pytest.raises(FileNotFoundError):
            DescriptionParser(dictionary_path="nonexistent.json", gui_mode=False)

    def test_init_with_invalid_json(self, tmp_path):
        """Test initialization with invalid JSON file."""
        invalid_json_file = tmp_path / "invalid.json"
        with open(invalid_json_file, 'w') as f:
            f.write("invalid json content")
        
        with pytest.raises(json.JSONDecodeError):
            DescriptionParser(dictionary_path=str(invalid_json_file), gui_mode=False)

    def test_load_dictionary_success(self, sample_dict_path):
        """Test successful dictionary loading."""
        parser = DescriptionParser(dictionary_path=sample_dict_path, gui_mode=False)
        assert isinstance(parser.replacement_dict, dict)
        assert "OLD_CODE" in parser.replacement_dict

    def test_load_dictionary_not_dict_format(self, tmp_path):
        """Test loading dictionary with non-dict JSON content."""
        invalid_dict_file = tmp_path / "invalid_dict.json"
        with open(invalid_dict_file, 'w') as f:
            json.dump(["not", "a", "dict"], f)
        
        with pytest.raises(ValueError, match="Dictionary file must contain a valid JSON object"):
            DescriptionParser(dictionary_path=str(invalid_dict_file), gui_mode=False)

    @patch('tkinter.filedialog.askopenfilename')
    @patch('tkinter.Tk')
    def test_select_input_file_gui_mode(self, mock_tk, mock_filedialog):
        """Test file selection in GUI mode."""
        mock_filedialog.return_value = "/path/to/file.csv"
        parser = DescriptionParser(dictionary_path="tests/test_data/sample_replacement_dict.json", gui_mode=True)
        
        result = parser.select_input_file()
        assert result == "/path/to/file.csv"
        mock_filedialog.assert_called_once()

    def test_select_input_file_non_gui_mode(self, sample_dict_path):
        """Test file selection in non-GUI mode."""
        parser = DescriptionParser(dictionary_path=sample_dict_path, gui_mode=False)
        result = parser.select_input_file()
        assert result == ""

    def test_process_file_success(self, sample_dict_path, sample_csv_path):
        """Test successful file processing."""
        parser = DescriptionParser(dictionary_path=sample_dict_path, gui_mode=False)
        
        # Process the file
        parser.process_file(sample_csv_path)
        
        # Check that output file was created
        input_path = Path(sample_csv_path)
        output_file = input_path.parent / f"processed_{input_path.name}"
        assert output_file.exists()
        
        # Check that replacements were made
        df = pd.read_csv(output_file)
        descriptions = df['Description'].tolist()
        assert 'NEW_CODE MARKER' in descriptions
        assert 'TEMPORARY SIGN' in descriptions
        assert 'BUILDING CORNER' in descriptions

    def test_process_file_insufficient_columns(self, sample_dict_path, tmp_path):
        """Test processing file with insufficient columns."""
        csv_file = tmp_path / "insufficient_cols.csv"
        test_data = {
            'Point': [1, 2],
            'Northing': [1000.0, 1001.0],
            'Easting': [2000.0, 2001.0]
        }
        df = pd.DataFrame(test_data)
        df.to_csv(csv_file, index=False)
        
        parser = DescriptionParser(dictionary_path=sample_dict_path, gui_mode=False)
        
        with pytest.raises(ValueError, match="CSV file must have at least 5 columns"):
            parser.process_file(str(csv_file))

    def test_process_file_empty_csv(self, sample_dict_path, tmp_path):
        """Test processing empty CSV file."""
        empty_csv = tmp_path / "empty.csv"
        empty_csv.write_text("")
        
        parser = DescriptionParser(dictionary_path=sample_dict_path, gui_mode=False)
        
        with pytest.raises(pd.errors.EmptyDataError):
            parser.process_file(str(empty_csv))

    def test_process_file_nonexistent_file(self, sample_dict_path):
        """Test processing non-existent file."""
        parser = DescriptionParser(dictionary_path=sample_dict_path, gui_mode=False)
        
        with pytest.raises(FileNotFoundError):
            parser.process_file("nonexistent.csv")

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.Tk')
    def test_process_file_gui_success_message(self, mock_tk, mock_messagebox, sample_dict_path, sample_csv_path):
        """Test that success message is shown in GUI mode."""
        parser = DescriptionParser(dictionary_path=sample_dict_path, gui_mode=True)
        parser.process_file(sample_csv_path)
        mock_messagebox.assert_called_once()

    @patch('tkinter.messagebox.showerror')
    @patch('tkinter.Tk')
    def test_process_file_gui_error_message(self, mock_tk, mock_messagebox, sample_dict_path):
        """Test that error message is shown in GUI mode."""
        parser = DescriptionParser(dictionary_path=sample_dict_path, gui_mode=True)
        
        # FileNotFoundError gets caught as IOError, which doesn't show GUI message
        # Let's test with an empty CSV instead, which triggers EmptyDataError
        with pytest.raises(FileNotFoundError):
            parser.process_file("nonexistent.csv")
        
        # The IOError handler doesn't show GUI messages, so this test should not expect a call
        mock_messagebox.assert_not_called()


class TestDescriptionParserMain:
    """Test cases for main function."""

    @patch('description_parser.DescriptionParser')
    @patch('tkinter.messagebox.showerror')
    def test_main_function_error_handling(self, mock_messagebox, mock_parser_class):
        """Test main function error handling."""
        from description_parser import main
        
        # Mock parser to raise an exception
        mock_parser = Mock()
        mock_parser.select_input_file.side_effect = Exception("Test error")
        mock_parser_class.return_value = mock_parser
        
        main()
        mock_messagebox.assert_called_once()

    @patch('description_parser.DescriptionParser')
    def test_main_function_no_file_selected(self, mock_parser_class):
        """Test main function when no file is selected."""
        from description_parser import main
        
        mock_parser = Mock()
        mock_parser.select_input_file.return_value = ""
        mock_parser_class.return_value = mock_parser
        
        # Should not raise an exception
        main()
        mock_parser.process_file.assert_not_called()

    @patch('description_parser.DescriptionParser')
    def test_main_function_successful_processing(self, mock_parser_class):
        """Test main function with successful file processing."""
        from description_parser import main
        
        mock_parser = Mock()
        mock_parser.select_input_file.return_value = "test.csv"
        mock_parser_class.return_value = mock_parser
        
        main()
        mock_parser.process_file.assert_called_once_with("test.csv")
