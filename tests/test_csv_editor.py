"""Tests for csv_editor module."""

import pytest
import pandas as pd
import tkinter as tk
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tempfile

# Add the parent directory to the path so we can import the modules
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from csv_editor import CSVEditor


class TestCSVEditor:
    """Test cases for CSVEditor class."""

    @pytest.fixture
    def sample_csv_file(self, tmp_path):
        """Create a sample CSV file for testing."""
        csv_file = tmp_path / "test.csv"
        test_data = {
            'Point': [1, 2, 3],
            'Northing': [1000.0, 1001.0, 1002.0],
            'Easting': [2000.0, 2001.0, 2002.0],
            'Elevation': [100.0, 101.0, 102.0],
            'Description': ['PCF MARKER', 'TREE SIGN', 'BUILDING CORNER']
        }
        df = pd.DataFrame(test_data)
        df.to_csv(csv_file, index=False)
        return str(csv_file)

    @patch('tkinter.Tk')
    def test_init_success(self, mock_tk, sample_csv_file):
        """Test successful initialization of CSVEditor."""
        mock_root = Mock()
        mock_tk.return_value = mock_root
        
        with patch('tkinter.ttk.Treeview') as mock_treeview:
            mock_tree = Mock()
            mock_treeview.return_value = mock_tree
            
            with patch('tkinter.Button') as mock_button:
                editor = CSVEditor(sample_csv_file)
                
                # Verify initialization
                assert editor.csv_file == sample_csv_file
                assert isinstance(editor.df, pd.DataFrame)
                assert len(editor.df) == 3
                assert list(editor.df.columns) == ['Point', 'Northing', 'Easting', 'Elevation', 'Description']
                
                # Verify GUI setup
                mock_root.title.assert_called_once_with("Description Editor")
                mock_treeview.assert_called_once()
                mock_button.assert_called_once()

    def test_init_file_not_found(self):
        """Test initialization with non-existent CSV file."""
        with pytest.raises(FileNotFoundError):
            CSVEditor("nonexistent.csv")

    @patch('tkinter.Tk')
    def test_init_invalid_csv(self, mock_tk, tmp_path):
        """Test initialization with invalid CSV file."""
        invalid_csv = tmp_path / "invalid.csv"
        invalid_csv.write_text("invalid,csv,content\nwith,missing,")
        
        mock_root = Mock()
        mock_tk.return_value = mock_root
        
        # Should handle pandas parsing errors gracefully
        with patch('tkinter.ttk.Treeview'):
            with patch('tkinter.Button'):
                try:
                    editor = CSVEditor(str(invalid_csv))
                    # If it doesn't raise an exception, verify the DataFrame was created
                    assert isinstance(editor.df, pd.DataFrame)
                except Exception as e:
                    # If it does raise an exception, it should be a pandas-related error
                    assert "pandas" in str(type(e)).lower() or "csv" in str(type(e)).lower()

    @patch('tkinter.Tk')
    def test_treeview_setup(self, mock_tk, sample_csv_file):
        """Test that Treeview is properly set up with CSV data."""
        mock_root = Mock()
        mock_tk.return_value = mock_root
        
        with patch('tkinter.ttk.Treeview') as mock_treeview:
            mock_tree = Mock()
            mock_treeview.return_value = mock_tree
            
            with patch('tkinter.Button'):
                editor = CSVEditor(sample_csv_file)
                
                # Verify Treeview configuration
                expected_columns = ['Point', 'Northing', 'Easting', 'Elevation', 'Description']
                mock_treeview.assert_called_once_with(mock_root, columns=expected_columns, show='headings')
                
                # Verify column setup calls
                assert mock_tree.heading.call_count == len(expected_columns)
                assert mock_tree.column.call_count == len(expected_columns)
                
                # Verify data insertion calls
                assert mock_tree.insert.call_count == 3  # 3 rows of data

    @patch('tkinter.Tk')
    def test_on_double_click_setup(self, mock_tk, sample_csv_file):
        """Test that double-click event is properly bound."""
        mock_root = Mock()
        mock_tk.return_value = mock_root
        
        with patch('tkinter.ttk.Treeview') as mock_treeview:
            mock_tree = Mock()
            mock_treeview.return_value = mock_tree
            
            with patch('tkinter.Button'):
                editor = CSVEditor(sample_csv_file)
                
                # Verify event binding
                mock_tree.bind.assert_called_once_with('<Double-1>', editor.on_double_click)

    @patch('tkinter.Tk')
    def test_on_double_click_functionality(self, mock_tk, sample_csv_file):
        """Test double-click functionality for cell editing."""
        mock_root = Mock()
        mock_tk.return_value = mock_root
        
        with patch('tkinter.ttk.Treeview') as mock_treeview:
            mock_tree = Mock()
            mock_tree.selection.return_value = ['item1']
            mock_tree.identify_column.return_value = '#2'
            mock_tree.item.return_value = {'values': ['1', '1000.0', '2000.0', '100.0', 'PCF MARKER']}
            mock_treeview.return_value = mock_tree
            
            with patch('tkinter.Button'):
                with patch('tkinter.Entry') as mock_entry:
                    mock_entry_instance = Mock()
                    mock_entry.return_value = mock_entry_instance
                    
                    editor = CSVEditor(sample_csv_file)
                    
                    # Create mock event
                    mock_event = Mock()
                    mock_event.x = 100
                    mock_event.y = 50
                    
                    # Call on_double_click
                    editor.on_double_click(mock_event)
                    
                    # Verify Entry widget creation and setup
                    mock_entry.assert_called_once_with(mock_root)
                    mock_entry_instance.insert.assert_called_once_with(0, '1000.0')
                    mock_entry_instance.place.assert_called_once_with(x=100, y=50)
                    mock_entry_instance.focus.assert_called_once()
                    mock_entry_instance.bind.assert_called_once()

    @patch('tkinter.Tk')
    def test_save_changes(self, mock_tk, sample_csv_file):
        """Test save changes functionality."""
        mock_root = Mock()
        mock_tk.return_value = mock_root
        
        with patch('tkinter.ttk.Treeview') as mock_treeview:
            mock_tree = Mock()
            mock_tree.get_children.return_value = ['0', '1', '2']
            mock_tree.item.side_effect = [
                {'values': ['1', '1000.0', '2000.0', '100.0', 'UPDATED MARKER']},
                {'values': ['2', '1001.0', '2001.0', '101.0', 'TREE SIGN']},
                {'values': ['3', '1002.0', '2002.0', '102.0', 'BUILDING CORNER']}
            ]
            mock_treeview.return_value = mock_tree
            
            with patch('tkinter.Button'):
                with patch('builtins.print') as mock_print:
                    editor = CSVEditor(sample_csv_file)
                    
                    # Call save_changes
                    editor.save_changes()
                    
                    # Verify that DataFrame was updated
                    assert editor.df.loc[0, 'Description'] == 'UPDATED MARKER'
                    
                    # Verify that file was saved
                    saved_df = pd.read_csv(sample_csv_file)
                    assert saved_df.loc[0, 'Description'] == 'UPDATED MARKER'
                    
                    # Verify print statement
                    mock_print.assert_called_once_with("Changes saved to", sample_csv_file)

    @patch('tkinter.Tk')
    def test_run_method(self, mock_tk, sample_csv_file):
        """Test the run method."""
        mock_root = Mock()
        mock_tk.return_value = mock_root
        
        with patch('tkinter.ttk.Treeview'):
            with patch('tkinter.Button'):
                editor = CSVEditor(sample_csv_file)
                
                # Call run method
                editor.run()
                
                # Verify mainloop and destroy calls
                mock_root.mainloop.assert_called_once()
                mock_root.destroy.assert_called_once()

    @patch('tkinter.Tk')
    def test_save_changes_with_empty_treeview(self, mock_tk, sample_csv_file):
        """Test save changes with empty treeview."""
        mock_root = Mock()
        mock_tk.return_value = mock_root
        
        with patch('tkinter.ttk.Treeview') as mock_treeview:
            mock_tree = Mock()
            mock_tree.get_children.return_value = []  # Empty treeview
            mock_treeview.return_value = mock_tree
            
            with patch('tkinter.Button'):
                with patch('builtins.print') as mock_print:
                    editor = CSVEditor(sample_csv_file)
                    
                    # Call save_changes
                    editor.save_changes()
                    
                    # Should still save (even if no changes)
                    mock_print.assert_called_once_with("Changes saved to", sample_csv_file)

    @patch('tkinter.Tk')
    def test_column_identification(self, mock_tk, sample_csv_file):
        """Test column identification in double-click handler."""
        mock_root = Mock()
        mock_tk.return_value = mock_root
        
        with patch('tkinter.ttk.Treeview') as mock_treeview:
            mock_tree = Mock()
            mock_tree.selection.return_value = ['item1']
            mock_tree.identify_column.return_value = '#1'  # First column
            mock_tree.item.return_value = {'values': ['1', '1000.0', '2000.0', '100.0', 'PCF MARKER']}
            mock_treeview.return_value = mock_tree
            
            with patch('tkinter.Button'):
                with patch('tkinter.Entry') as mock_entry:
                    mock_entry_instance = Mock()
                    mock_entry.return_value = mock_entry_instance
                    
                    editor = CSVEditor(sample_csv_file)
                    
                    # Create mock event
                    mock_event = Mock()
                    mock_event.x = 100
                    mock_event.y = 50
                    
                    # Call on_double_click
                    editor.on_double_click(mock_event)
                    
                    # Verify that first column value ('1') was inserted
                    mock_entry_instance.insert.assert_called_once_with(0, '1')


class TestCSVEditorIntegration:
    """Integration tests for CSVEditor."""

    def test_full_edit_workflow(self, tmp_path):
        """Test a complete edit workflow without GUI."""
        # Create test CSV
        csv_file = tmp_path / "integration_test.csv"
        test_data = {
            'Point': [1, 2],
            'Description': ['OLD VALUE', 'ANOTHER VALUE']
        }
        df = pd.DataFrame(test_data)
        df.to_csv(csv_file, index=False)
        
        # Mock the GUI components but test the data handling
        with patch('tkinter.Tk'):
            with patch('tkinter.ttk.Treeview') as mock_treeview:
                mock_tree = Mock()
                mock_tree.get_children.return_value = ['0', '1']
                mock_tree.item.side_effect = [
                    {'values': ('1', 'NEW VALUE')},
                    {'values': ('2', 'ANOTHER VALUE')}
                ]
                mock_treeview.return_value = mock_tree
                
                with patch('tkinter.Button'):
                    with patch('builtins.print'):
                        editor = CSVEditor(str(csv_file))
                        
                        # Simulate editing
                        editor.save_changes()
                        
                        # Verify the DataFrame was updated in memory
                        # The save_changes method sets df.loc[int(item)] = row_values
                        assert editor.df.iloc[0, 0] == '1'  # Point column
                        assert editor.df.iloc[0, 1] == 'NEW VALUE'  # Description column
                        assert editor.df.iloc[1, 0] == '2'  # Point column  
                        assert editor.df.iloc[1, 1] == 'ANOTHER VALUE'  # Description column

    def test_main_execution(self):
        """Test the main execution block."""
        # This tests the if __name__ == "__main__" block
        with patch('csv_editor.CSVEditor') as mock_csv_editor:
            mock_editor_instance = Mock()
            mock_csv_editor.return_value = mock_editor_instance
            
            # Import and execute the main block
            import csv_editor
            
            # The main block should create an editor with the default filename
            # Note: This test documents current behavior but the hardcoded filename
            # in the main block should probably be made configurable
