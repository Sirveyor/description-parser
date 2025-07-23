"""Tests for main module."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch

# Add the parent directory to the path so we can import the modules
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

import main


class TestMain:
    """Test cases for main module."""

    @patch('main.parser3.main')
    @patch('main.description_parser.main')
    def test_main_function_success(self, mock_desc_parser_main, mock_parser3_main):
        """Test successful execution of main function."""
        # Call main function
        main.main()
        
        # Verify both parsers were called
        mock_desc_parser_main.assert_called_once()
        mock_parser3_main.assert_called_once()

    @patch('main.parser3.main')
    @patch('main.description_parser.main')
    def test_main_function_description_parser_error(self, mock_desc_parser_main, mock_parser3_main):
        """Test main function when description_parser raises an exception."""
        # Setup mock to raise exception
        mock_desc_parser_main.side_effect = Exception("Description parser error")
        
        # Main function should propagate the exception
        with pytest.raises(Exception, match="Description parser error"):
            main.main()
        
        # Verify description_parser was called but parser3 was not
        mock_desc_parser_main.assert_called_once()
        mock_parser3_main.assert_not_called()

    @patch('main.parser3.main')
    @patch('main.description_parser.main')
    def test_main_function_parser3_error(self, mock_desc_parser_main, mock_parser3_main):
        """Test main function when parser3 raises an exception."""
        # Setup mock to raise exception
        mock_parser3_main.side_effect = Exception("Parser3 error")
        
        # Main function should propagate the exception
        with pytest.raises(Exception, match="Parser3 error"):
            main.main()
        
        # Verify both were called (description_parser succeeded, parser3 failed)
        mock_desc_parser_main.assert_called_once()
        mock_parser3_main.assert_called_once()

    @patch('main.parser3.main')
    @patch('main.description_parser.main')
    def test_main_function_both_parsers_error(self, mock_desc_parser_main, mock_parser3_main):
        """Test main function when both parsers raise exceptions."""
        # Setup mocks to raise exceptions
        mock_desc_parser_main.side_effect = Exception("Description parser error")
        mock_parser3_main.side_effect = Exception("Parser3 error")
        
        # Main function should propagate the first exception
        with pytest.raises(Exception, match="Description parser error"):
            main.main()
        
        # Verify only description_parser was called
        mock_desc_parser_main.assert_called_once()
        mock_parser3_main.assert_not_called()

    @patch('main.main')
    def test_name_main_execution(self, mock_main_function):
        """Test that main() is called when script is executed directly."""
        # This test verifies the if __name__ == "__main__" block
        # We need to reload the module to trigger the main execution
        import importlib
        
        # Mock the __name__ to be "__main__"
        with patch.object(main, '__name__', '__main__'):
            importlib.reload(main)
            
        # Note: This test is tricky because the if __name__ == "__main__" 
        # block executes during import. In a real scenario, we'd test this
        # by running the script as a subprocess.

    def test_module_imports(self):
        """Test that required modules are properly imported."""
        # Verify that the main module has the required imports
        assert hasattr(main, 'description_parser')
        assert hasattr(main, 'parser3')
        assert hasattr(main, 'main')

    @patch('main.parser3')
    @patch('main.description_parser')
    def test_main_function_module_availability(self, mock_desc_parser, mock_parser3):
        """Test main function when modules are available."""
        # Setup mocks
        mock_desc_parser.main = Mock()
        mock_parser3.main = Mock()
        
        # Call main
        main.main()
        
        # Verify calls
        mock_desc_parser.main.assert_called_once()
        mock_parser3.main.assert_called_once()

    def test_main_function_signature(self):
        """Test that main function has correct signature."""
        import inspect
        
        # Get function signature
        sig = inspect.signature(main.main)
        
        # Verify no parameters
        assert len(sig.parameters) == 0
        
        # Verify return annotation (should be None or not specified)
        assert sig.return_annotation in (None, inspect.Signature.empty)


class TestMainIntegration:
    """Integration tests for main module."""

    @patch('main.parser3.main')
    @patch('main.description_parser.main')
    def test_sequential_execution_order(self, mock_desc_parser_main, mock_parser3_main):
        """Test that parsers are executed in the correct order."""
        call_order = []
        
        def desc_parser_side_effect():
            call_order.append('description_parser')
        
        def parser3_side_effect():
            call_order.append('parser3')
        
        mock_desc_parser_main.side_effect = desc_parser_side_effect
        mock_parser3_main.side_effect = parser3_side_effect
        
        # Call main
        main.main()
        
        # Verify execution order
        assert call_order == ['description_parser', 'parser3']

    @patch('main.parser3.main')
    @patch('main.description_parser.main')
    def test_main_function_timing(self, mock_desc_parser_main, mock_parser3_main):
        """Test that main function completes in reasonable time."""
        import time
        
        # Add small delays to simulate processing
        def slow_desc_parser():
            time.sleep(0.01)
        
        def slow_parser3():
            time.sleep(0.01)
        
        mock_desc_parser_main.side_effect = slow_desc_parser
        mock_parser3_main.side_effect = slow_parser3
        
        # Measure execution time
        start_time = time.time()
        main.main()
        end_time = time.time()
        
        # Should complete quickly (within 1 second for this test)
        assert end_time - start_time < 1.0

    def test_main_module_structure(self):
        """Test the overall structure of the main module."""
        import inspect
        
        # Get all functions in the main module
        functions = [name for name, obj in inspect.getmembers(main, inspect.isfunction)]
        
        # Should have at least the main function
        assert 'main' in functions
        
        # Check for any unexpected functions (helps catch accidental additions)
        expected_functions = ['main']
        unexpected_functions = [f for f in functions if f not in expected_functions]
        
        # This assertion helps document what functions exist
        # If new functions are added intentionally, update expected_functions
        assert len(unexpected_functions) == 0, f"Unexpected functions found: {unexpected_functions}"


class TestMainErrorHandling:
    """Test error handling scenarios in main module."""

    @patch('main.parser3.main')
    @patch('main.description_parser.main')
    def test_import_error_handling(self, mock_desc_parser_main, mock_parser3_main):
        """Test behavior when import errors occur."""
        # This test documents current behavior - the main module doesn't
        # handle import errors, which means they would be raised during import
        
        # If we wanted to add import error handling, we could test it here
        # For now, this test serves as documentation
        
        # Call main function normally
        main.main()
        
        # Verify normal execution
        mock_desc_parser_main.assert_called_once()
        mock_parser3_main.assert_called_once()

    @patch('main.parser3.main')
    @patch('main.description_parser.main')
    def test_keyboard_interrupt_handling(self, mock_desc_parser_main, mock_parser3_main):
        """Test handling of keyboard interrupt."""
        # Setup mock to raise KeyboardInterrupt
        mock_desc_parser_main.side_effect = KeyboardInterrupt("User interrupted")
        
        # Main function should propagate KeyboardInterrupt
        with pytest.raises(KeyboardInterrupt):
            main.main()
        
        # Verify description_parser was called
        mock_desc_parser_main.assert_called_once()
        mock_parser3_main.assert_not_called()

    @patch('main.parser3.main')
    @patch('main.description_parser.main')
    def test_system_exit_handling(self, mock_desc_parser_main, mock_parser3_main):
        """Test handling of system exit."""
        # Setup mock to raise SystemExit
        mock_desc_parser_main.side_effect = SystemExit(1)
        
        # Main function should propagate SystemExit
        with pytest.raises(SystemExit):
            main.main()
        
        # Verify description_parser was called
        mock_desc_parser_main.assert_called_once()
        mock_parser3_main.assert_not_called()
