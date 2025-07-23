"""Integration tests for the description-parser project."""

import pytest
import pandas as pd
import json
import csv
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, Mock

# Add the parent directory to the path so we can import the modules
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestEndToEndWorkflow:
    """Test the complete workflow from input to output."""

    @pytest.fixture
    def temp_directory(self):
        """Create a temporary directory for test files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield Path(temp_dir)

    @pytest.fixture
    def sample_replacement_dict(self, temp_directory):
        """Create a sample replacement dictionary file."""
        dict_file = temp_directory / "replacement_dict.json"
        replacement_dict = {
            "OLD_MARKER": "NEW_MARKER",
            "TEMP": "TEMPORARY",
            "BLDG": "BUILDING"
        }
        with open(dict_file, 'w') as f:
            json.dump(replacement_dict, f)
        return str(dict_file)

    @pytest.fixture
    def sample_input_csv(self, temp_directory):
        """Create a sample input CSV file."""
        csv_file = temp_directory / "input.csv"
        data = [
            ["Point", "Northing", "Easting", "Elevation", "Description"],
            ["1", "1000.00", "2000.00", "100.00", "PCF 1/2 OLD_MARKER"],
            ["2", "1001.00", "2001.00", "101.00", "1/4 PCF TEMP"],
            ["3", "1002.00", "2002.00", "102.00", "TREE PCF 3/4"],
            ["4", "1003.00", "2003.00", "103.00", "PCF TREE BLDG"],
        ]
        
        with open(csv_file, 'w', newline='', encoding='utf8') as f:
            writer = csv.writer(f)
            writer.writerows(data)
        
        return str(csv_file)

    @pytest.fixture
    def property_corners_file(self, temp_directory):
        """Create a property corners file."""
        corners_file = temp_directory / "property_corners.txt"
        corners_file.write_text("PCF\nPTF\nRBC\n")
        return str(corners_file)

    @pytest.fixture
    def miscellaneous_file(self, temp_directory):
        """Create a miscellaneous codes file."""
        misc_file = temp_directory / "miscellaneous.txt"
        misc_file.write_text("TREE\nSIGN\nMARKER\nBUILDING\n")
        return str(misc_file)

    def test_description_parser_workflow(self, sample_replacement_dict, sample_input_csv):
        """Test the complete description parser workflow."""
        from description_parser import DescriptionParser
        
        # Initialize parser in non-GUI mode
        parser = DescriptionParser(dictionary_path=sample_replacement_dict, gui_mode=False)
        
        # Process the file
        parser.process_file(sample_input_csv)
        
        # Check output file was created
        input_path = Path(sample_input_csv)
        output_file = input_path.parent / f"processed_{input_path.name}"
        assert output_file.exists()
        
        # Verify replacements were made
        df = pd.read_csv(output_file)
        descriptions = df['Description'].tolist()
        
        # Check that replacements occurred
        assert any("NEW_MARKER" in desc for desc in descriptions)
        assert any("TEMPORARY" in desc for desc in descriptions)
        assert any("BUILDING" in desc for desc in descriptions)
        
        # Verify original structure is maintained
        assert len(df) == 4
        assert list(df.columns) == ["Point", "Northing", "Easting", "Elevation", "Description"]

    def test_parser3_workflow(self, sample_input_csv, property_corners_file, miscellaneous_file):
        """Test the complete parser3 workflow."""
        import parser3
        
        # Load code lists
        property_codes, misc_codes = parser3.load_code_lists(property_corners_file, miscellaneous_file)
        
        # Verify codes were loaded
        assert "pcf" in property_codes  # Should be lowercase
        assert "TREE" in misc_codes
        
        # Process file
        with patch('tkinter.messagebox.showinfo'):
            output_file = parser3.process_file(sample_input_csv, property_codes, misc_codes)
        
        # Verify output file exists
        assert os.path.exists(output_file)
        
        # Check processing results
        with open(output_file, 'r', newline='', encoding='utf8') as f:
            reader = csv.reader(f)
            rows = list(reader)
        
        # Verify header
        assert rows[0] == ["Point", "Northing", "Easting", "Elevation", "Description"]
        
        # Check that descriptions were processed according to rules
        descriptions = [row[4] for row in rows[1:]]
        
        # Should have backslashes for sizes and proper ordering
        processed_descriptions = ' '.join(descriptions)
        assert '\\' in processed_descriptions  # Should have backslashes for sizes

    def test_csv_editor_integration(self, sample_input_csv):
        """Test CSV editor integration."""
        from csv_editor import CSVEditor
        
        # Mock GUI components
        with patch('tkinter.Tk'):
            with patch('tkinter.ttk.Treeview') as mock_treeview:
                mock_tree = Mock()
                mock_tree.get_children.return_value = ['0', '1']
                mock_tree.item.side_effect = [
                    {'values': ['1', '1000.00', '2000.00', '100.00', 'EDITED DESCRIPTION']},
                    {'values': ['2', '1001.00', '2001.00', '101.00', 'ANOTHER DESCRIPTION']}
                ]
                mock_treeview.return_value = mock_tree
                
                with patch('tkinter.Button'):
                    with patch('builtins.print'):
                        # Create editor
                        editor = CSVEditor(sample_input_csv)
                        
                        # Simulate saving changes
                        editor.save_changes()
                        
                        # Verify file was updated
                        df = pd.read_csv(sample_input_csv)
                        assert df.loc[0, 'Description'] == 'EDITED DESCRIPTION'

    def test_complete_pipeline(self, sample_replacement_dict, sample_input_csv, 
                              property_corners_file, miscellaneous_file, temp_directory):
        """Test the complete processing pipeline."""
        from description_parser import DescriptionParser
        import parser3
        
        # Step 1: Run description parser
        desc_parser = DescriptionParser(dictionary_path=sample_replacement_dict, gui_mode=False)
        desc_parser.process_file(sample_input_csv)
        
        # Get the output from description parser
        input_path = Path(sample_input_csv)
        desc_output = input_path.parent / f"processed_{input_path.name}"
        
        # Step 2: Run parser3 on the description parser output
        property_codes, misc_codes = parser3.load_code_lists(property_corners_file, miscellaneous_file)
        
        with patch('tkinter.messagebox.showinfo'):
            final_output = parser3.process_file(str(desc_output), property_codes, misc_codes)
        
        # Step 3: Verify final output
        assert os.path.exists(final_output)
        
        # Check that both processing steps were applied
        with open(final_output, 'r', newline='', encoding='utf8') as f:
            reader = csv.reader(f)
            rows = list(reader)
        
        descriptions = [row[4] for row in rows[1:]]
        
        # Should have both dictionary replacements and parser3 formatting
        all_descriptions = ' '.join(descriptions)
        assert 'NEW_MARKER' in all_descriptions or 'TEMPORARY' in all_descriptions  # Dictionary replacements
        assert '\\' in all_descriptions  # Parser3 size formatting

    @patch('main.parser3.main')
    @patch('main.description_parser.main')
    def test_main_module_integration(self, mock_desc_main, mock_parser3_main):
        """Test main module integration."""
        import main
        
        # Run main function
        main.main()
        
        # Verify both modules were called
        mock_desc_main.assert_called_once()
        mock_parser3_main.assert_called_once()


class TestErrorHandlingIntegration:
    """Test error handling across modules."""

    def test_missing_dictionary_file_handling(self):
        """Test handling of missing dictionary file."""
        from description_parser import DescriptionParser
        
        with pytest.raises(FileNotFoundError):
            DescriptionParser(dictionary_path="nonexistent.json", gui_mode=False)

    def test_missing_code_files_handling(self):
        """Test handling of missing code files."""
        import parser3
        
        with patch('tkinter.messagebox.showerror'):
            prop_codes, misc_codes = parser3.load_code_lists("nonexistent1.txt", "nonexistent2.txt")
            
            # Should return empty lists
            assert prop_codes == []
            assert misc_codes == []

    def test_invalid_csv_handling(self, tmp_path):
        """Test handling of invalid CSV files."""
        from description_parser import DescriptionParser
        
        # Create invalid CSV
        invalid_csv = tmp_path / "invalid.csv"
        invalid_csv.write_text("not,enough,columns\n1,2")
        
        # Create valid dictionary
        dict_file = tmp_path / "dict.json"
        with open(dict_file, 'w') as f:
            json.dump({"OLD": "NEW"}, f)
        
        parser = DescriptionParser(dictionary_path=str(dict_file), gui_mode=False)
        
        with pytest.raises(ValueError, match="CSV file must have at least 5 columns"):
            parser.process_file(str(invalid_csv))

    def test_corrupted_json_handling(self, tmp_path):
        """Test handling of corrupted JSON files."""
        from description_parser import DescriptionParser
        
        # Create corrupted JSON
        corrupted_json = tmp_path / "corrupted.json"
        corrupted_json.write_text("{ invalid json content")
        
        with pytest.raises(json.JSONDecodeError):
            DescriptionParser(dictionary_path=str(corrupted_json), gui_mode=False)


class TestDataConsistency:
    """Test data consistency across processing steps."""

    def test_data_preservation(self, tmp_path):
        """Test that data is preserved correctly through processing."""
        # Create test data
        original_data = {
            'Point': [1, 2, 3],
            'Northing': [1000.0, 1001.0, 1002.0],
            'Easting': [2000.0, 2001.0, 2002.0],
            'Elevation': [100.0, 101.0, 102.0],
            'Description': ['PCF MARKER', 'TREE SIGN', 'BUILDING CORNER']
        }
        
        input_csv = tmp_path / "test.csv"
        df = pd.DataFrame(original_data)
        df.to_csv(input_csv, index=False)
        
        # Create dictionary
        dict_file = tmp_path / "dict.json"
        with open(dict_file, 'w') as f:
            json.dump({"MARKER": "MONUMENT"}, f)
        
        # Process with description parser
        from description_parser import DescriptionParser
        parser = DescriptionParser(dictionary_path=str(dict_file), gui_mode=False)
        parser.process_file(str(input_csv))
        
        # Check output
        output_file = tmp_path / f"processed_{input_csv.name}"
        result_df = pd.read_csv(output_file)
        
        # Verify data integrity
        assert len(result_df) == len(original_data['Point'])
        assert list(result_df['Point']) == original_data['Point']
        assert list(result_df['Northing']) == original_data['Northing']
        assert list(result_df['Easting']) == original_data['Easting']
        assert list(result_df['Elevation']) == original_data['Elevation']
        
        # Verify replacement occurred
        assert 'MONUMENT' in result_df['Description'].iloc[0]

    def test_column_order_preservation(self, tmp_path):
        """Test that column order is preserved."""
        # Create test CSV with specific column order
        csv_file = tmp_path / "ordered.csv"
        data = [
            ["Point", "Northing", "Easting", "Elevation", "Description"],
            ["1", "1000.0", "2000.0", "100.0", "TEST DESCRIPTION"]
        ]
        
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(data)
        
        # Process with both parsers
        dict_file = tmp_path / "dict.json"
        with open(dict_file, 'w') as f:
            json.dump({"TEST": "VERIFIED"}, f)
        
        from description_parser import DescriptionParser
        parser = DescriptionParser(dictionary_path=str(dict_file), gui_mode=False)
        parser.process_file(str(csv_file))
        
        # Check column order
        output_file = tmp_path / f"processed_{csv_file.name}"
        result_df = pd.read_csv(output_file)
        
        expected_columns = ["Point", "Northing", "Easting", "Elevation", "Description"]
        assert list(result_df.columns) == expected_columns
