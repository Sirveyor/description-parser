"""
Version 1.0.0

description_parser.py
This module contains the main functionality for parsing and processing surveying point descriptions
It uses a dictionary to standardize descriptions in CSV files and it call a parser3 module to
properly format the data.

The Description Dictionary is a json file that contains key-value pairs where the key is an often
used incorrect description and the value is the standardized description.

Future improvements could include:
    - Adding functiality to allow users to create a custom description dictionary
    - Adding a GUI to allow users to edit the description dictionary
    - Allowing users to select the dictionary file to use

"""
# Standard library imports
import json
import logging
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
# Third-party imports
import pandas as pd
# Local imports
from parser3 import main as parser3_main

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

""" def get_resource_path(relative_path):
    Get absolute path to resource, works for dev and for PyInstaller
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path) """

# Define the working directory
DIRNAME = Path(__file__).parent.resolve()

# Configuration - try multiple locations for the dictionary
DEFAULT_DICT_PATHS = [
    "N:/carlson settings/f2f/replacement_dict.json",  # Original network path
    # get_resource_path("replacement_dict.json"),        # Bundled with executable
    "config/replacement_dict.json",                    # Local config folder
    "replacement_dict.json"                            # Current directory
]

class DescriptionParser:
    """Class to handle the standardization of descriptions in CSV files."""

    def __init__(self, dictionary_path: str = None, gui_mode: bool = True):
        """
        Initialize the DescriptionParser with a dictionary file path.

        Args:
            dictionary_path (str): Path to the dictionary file (optional)
            gui_mode (bool): Whether to show GUI dialogs (default: True)
        """
        if dictionary_path is None:
            # Try to find dictionary file in multiple locations
            self.dictionary_path = self._find_dictionary_file()
        else:
            self.dictionary_path = Path(dictionary_path)
        self.replacement_dict = self._load_dictionary()
        self.gui_mode = gui_mode

    def _find_dictionary_file(self) -> Path:
        """Find the dictionary file from multiple possible locations."""
        for path_str in DEFAULT_DICT_PATHS:
            path = Path(path_str)
            if path.exists():
                logger.info("Found dictionary file at: %s", path)
                return path
        
        # If no file found, create a default one
        logger.warning("No dictionary file found. Creating default dictionary.")
        default_dict = {
            "OLD_TEXT": "NEW_TEXT",
            "EXAMPLE": "SAMPLE"
        }
        default_path = Path("replacement_dict.json")
        with open(default_path, 'w', encoding='utf-8') as f:
            json.dump(default_dict, f, indent=2)
        return default_path

    
    def _load_dictionary(self) -> dict:
        """
        Load and validate the replacement dictionary from file.

        Returns:
            dict: The loaded replacement dictionary

        Raises:
            FileNotFoundError: If dictionary file doesn't exist
            json.JSONDecodeError: If dictionary file is not valid JSON
        """
        try:
            if not self.dictionary_path.exists():
                error_msg = f"Dictionary file not found: {self.dictionary_path}"
                logger.error(error_msg)
                raise FileNotFoundError(error_msg)

            with open(self.dictionary_path, 'r', encoding='utf-8') as f:
                dictionary = json.load(f)

            # Validate dictionary format
            if not isinstance(dictionary, dict):
                raise ValueError("Dictionary file must contain a valid JSON object")

            logger.info("Successfully loaded dictionary with %d entries", len(dictionary))
            return dictionary

        except json.JSONDecodeError as e:
            logger.error("Error parsing dictionary file: %s", e)
            raise
        except Exception as e:
            logger.error("Unexpected error loading dictionary: %s", e)
            raise

    def select_input_file(self) -> str:
        """
        Open a file dialog for user to select input CSV file.

        Returns:
            str: Selected file path or empty string if cancelled
        """
        if not self.gui_mode:
            return ""

        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            title="Select File",
            filetypes=[
                ("All Files", "*.*"),
                ("CSV Files", "*.csv"),
                ("Text Files", "*.txt"),
            ]
        )
        if file_path:
            logger.info("Selected input file: %s", file_path)
        else:
            logger.info("File selection cancelled")
        return file_path

    def process_file(self, input_file: str) -> str:
        """
        Process the input CSV file and standardize the last column.
        Returns the path to the output file.

        Args:
            input_file (str): Path to the input CSV file

        Raises:
            pd.errors.EmptyDataError: If the CSV file is empty
            ValueError: If file has incorrect number of columns
            IOError: If there is an issue reading or writing the file
            KeyError: If replacement_dict contains keys not found in the data
        """
        try:
            # Read the CSV file
            df = pd.read_csv(input_file)

            # Validate that file has at least 5 columns
            if df.shape[1] < 5:
                error_msg = f"CSV file must have at least 5 columns. Found: {df.shape[1]}"
                logger.error(error_msg)
                raise ValueError(error_msg)

            # Store original values for verification
            original_values = df.iloc[:, -1].copy()

            # Apply replacements to the last column
            for old_text, new_text in self.replacement_dict.items():
                df.iloc[:, -1] = df.iloc[:, -1].str.replace(old_text, new_text, regex=False)

            # Calculate number of changes made
            changes_made = (original_values != df.iloc[:, -1]).sum()

            # Generate output filename
            input_path = Path(input_file)
            output_file = input_path.parent / f"preprocessed_{input_path.name}"

            # Save processed file
            df.to_csv(output_file, index=False)

            success_msg = f"Processing complete! Made {changes_made} replacements\nSaved as: {output_file}"
            logger.info(success_msg)
            
            # Show success message to user if in GUI mode
            if self.gui_mode:
                try:
                    root = tk.Tk()
                    root.withdraw()
                    messagebox.showinfo("Success", success_msg)
                except tk.TclError as e:
                    logger.warning("Could not show GUI message: %s", e)
        except pd.errors.EmptyDataError:
            error_msg = "The selected CSV file is empty"
            logger.error(error_msg)
            if self.gui_mode:
                try:
                    root = tk.Tk()
                    root.withdraw()
                    messagebox.showerror("Error", error_msg)
                except tk.TclError as gui_error:
                    logger.warning("Could not show GUI error: %s", gui_error)
            raise
        except ValueError as e:
            logger.error("Value error: %s",str(e))
            raise
        except KeyError as e:
            logger.error("Key error: %s",str(e))
            raise
        except IOError as e:
            logger.error("I/O error: %s",str(e))
            raise
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(error_msg)
            if self.gui_mode:
                try:
                    root = tk.Tk()
                    root.withdraw()
                    messagebox.showerror("Error", error_msg)
                except tk.TclError as gui_error:
                    logger.warning("Could not show GUI error: %s ", gui_error)
            raise
        return output_file
def main(argument=None):
    """Main execution function."""
    try:
        # Use the argument passed from main.py
        if argument:
            logger.info("Received argument: %s", argument)
        else:
            logger.warning("No argument received.")
            
        # Initialize parser with default dictionary file path
        parser = DescriptionParser()  # Uses DEFAULT_DICT_PATH by default

        # Let user select input file
        input_file = parser.select_input_file()

        if input_file:
            output = parser.process_file(input_file)
            parser3_main(output)  # Call parser3 main function with output file
        else:
            logger.info("No file selected. Process aborted.")

    except Exception as e:
        logger.error("Application error: %s", str(e))
        if tk._default_root is None:
            root = tk.Tk()
            root.withdraw()
        messagebox.showerror("Error", f"Application error: {str(e)}")

if __name__ == "__main__":
    main()
