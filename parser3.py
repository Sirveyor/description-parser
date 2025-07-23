# This script processes point descriptions from a CSV file,
# ensuring correct ordering of sizes, property corner codes, and miscellaneous codes.

import re
import os
import csv
import logging
# import tkinter as tk
from tkinter import messagebox
import subprocess
import sys

# set working directory atlantic-description-parser directory
DIRNAME = os.path.dirname(os.path.abspath(__file__))
# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

""" def get_resource_path(relative_path):
    # Get absolute path to resource, works for dev and for PyInstaller
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
 """
# Configuration

def load_code_lists(property_corners_path: str, miscellaneous_path: str) -> tuple[list, list]:
    """
    Load property corners and miscellaneous codes from specified files.

    Args:
        property_corners_path (str): Path to the property corners file.
        miscellaneous_path (str): Path to the miscellaneous codes file.

    Returns:
        tuple: Lists of property corners and miscellaneous codes.
    """
    try:
        # Load property corner codes
        with open(property_corners_path, 'r', encoding='utf8') as prop_crns_file:
            property_corners_list = [line.strip().lower() for line in prop_crns_file]

        # Load miscellaneous codes
        with open(miscellaneous_path, 'r', encoding='utf8') as misc_file:
            miscellaneous_list = [line.strip() for line in misc_file]

        logger.info("Loaded property corners and miscellaneous codes successfully.")
        return property_corners_list, miscellaneous_list

    except FileNotFoundError as e:
        logger.error("File not found: %s", e)
        messagebox.showerror("File Error", f"Could not find the specified file: {e}")
        return [], []
    except Exception as e:
        logger.error("Error loading code lists: %s", e)
        messagebox.showerror("Error", f"An error occurred while loading code lists: {e}")
        return [], []

def item_is_size(item: str) -> bool:
    """
    Check if the item is a size (e.g., 1/4, 1/2, 3/4, 1, 2, 3).

    Args:
        item (str): The item to check

    Returns:
        bool: True if the item is a size, False otherwise
    """
    if item.startswith('\\'):
        item = item[1:]  # Remove leading backslash if present

    size_pattern = r'(?:\d+\s+\d+/\d+|\d+/\d+|\d+)(?:"|\')?'
    return bool(re.match(size_pattern, item))




def number_of_codes(description_items: list, property_codes: list, misc_codes: list) -> str:
    """
    Check if the description contains one or two valid codes.

    Args:
        description_items (list): List of description items to check
        property_codes (list): List of valid property corner codes
        misc_codes (list): List of valid miscellaneous codes

    Returns:
        str: 'zero', 'one', or 'two' based on the number of valid codes found.
    """
    if not isinstance(description_items, list):
        logger.error("Description items is not a list: %s", description_items)
        return 'zero'

    valid_codes = 0

    # Check first two items in the description for valid codes
    for item in description_items[:2]:
        if item.upper() in (code.upper() for code in property_codes + misc_codes):
            valid_codes += 1

    if valid_codes == 0:
        return 'zero'
    elif valid_codes == 1:
        return 'one'
    else:
        return 'two'



def process_file(input_file: str, property_codes: list, misc_codes: list) -> str:
    """
    Process the input file and write results to output file.

    Args:
        input_file (str): Path to the CSV file.
        property_codes (list): List of valid property corner codes.
        misc_codes (list): List of valid miscellaneous codes.
    """
    try:
        with open(input_file, 'r', newline='', encoding='utf8') as infile:
            logger.info("Processing input file: %s", input_file)
            reader = csv.reader(infile)
            rows = list(reader)  # Read all rows at once

        # Create output filename by adding _processed before the extension
        base, ext = os.path.splitext(input_file)
        base = base.replace('preprocessed_', '')  # Remove 'preprocessed' from base
        output_file = f"{base}_processed{ext}"
        logger.info("Writing to output file: %s",output_file)

        with open(output_file, 'w', newline='', encoding='utf8') as outfile:
            writer = csv.writer(outfile)

            for row in rows:
                # Check if it's a header row by trying to convert row[1] to float
                try:
                    if len(row) >= 2:
                        float(row[1])
                        is_header = False
                    else:
                        is_header = True
                except (ValueError, TypeError):
                    is_header = True

                if is_header:
                    writer.writerow(row)
                    continue

                if len(row) >= 5:
                    description = row[4].strip()
                    desc_items = description.split()

                    if len(desc_items) >= 2:
                        # Special bypass condition: if 'TREE' is present, skip all processing
                        if any(item.upper() == 'TREE' for item in desc_items):
                            # No processing applied - keep description as is
                            pass
                        else:
                            code_count = number_of_codes(desc_items, property_codes, misc_codes)

                            if code_count == 'one':
                                # Rule for ONE code
                                if len(desc_items) >= 2 and desc_items[0] != "TREE":
                                    # If first item is property code and second is size,
                                    # add backslash
                                    if desc_items[0].upper() in (code.upper()
                                        for code in property_codes) \
                                            and item_is_size(desc_items[1]) \
                                            and not desc_items[1].startswith('\\'):
                                        desc_items[1] = '\\' + desc_items[1]
                                    # If first is size and second is property code,
                                    # swap and add backslash
                                    elif item_is_size(desc_items[0]) and desc_items[1].upper() in \
                                        (code.upper() for code in property_codes):
                                        size_item = desc_items[0]
                                        if not size_item.startswith('\\'):
                                            size_item = '\\' + size_item
                                        desc_items[0], desc_items[1] = desc_items[1], size_item
                                    # If first item is property code and second is not a size,
                                    # add forward slash
                                    elif desc_items[0].upper() in \
                                            (code.upper() for code in property_codes) \
                                            and not item_is_size(desc_items[1]) \
                                            and not desc_items[1].startswith('/') \
                                            and not desc_items[1].startswith('\\'):
                                        desc_items[1] = '/' + desc_items[1]
                                    # If first item is miscellaneous code, add forward
                                    # slash to second item
                                    elif desc_items[0].upper() in \
                                            (code.upper() for code in misc_codes):
                                        if not desc_items[1].startswith('/') \
                                                and not desc_items[1].startswith('\\'):
                                            desc_items[1] = '/' + desc_items[1]

                            elif code_count == 'two':
                                # Rule for TWO codes - ensure property corner code is
                                # after first code
                                # Check if we need to reorder codes
                                if desc_items[0].upper() in (code.upper()
                                        for code in property_codes) and desc_items[1].upper() in \
                                            (code.upper() for code in misc_codes):
                                    # Swap so property code comes after misc code
                                    desc_items[0], desc_items[1] = desc_items[1], desc_items[0]

                                # Now handle the third item
                                if len(desc_items) >= 3 and desc_items[1] != "TREE":
                                    if item_is_size(desc_items[2]):
                                        if not desc_items[2].startswith('\\'):
                                            desc_items[2] = '\\' + desc_items[2]
                                    else:
                                        if not desc_items[2].startswith('/') and not \
                                                desc_items[2].startswith('\\') and \
                                                desc_items[1] != "TREE":
                                            desc_items[2] = '/' + desc_items[2]

                    # Update the description in the row
                    row[4] = ' '.join(desc_items)

                writer.writerow(row)

        messagebox.showinfo("Processing Complete",
                            f"File processed successfully. Output saved to {output_file}.")
    except FileNotFoundError:
        logger.error("Input file not found: %s", input_file)
        messagebox.showerror("File Error", f"Could not find the specified file: {input_file}")
        raise
    except Exception as e:
        logger.error("Error processing file: %s", e)
        messagebox.showerror("Error", f"An error occurred while processing the file: {e}")
        raise
    return output_file


# GUI for file selection
# def select_input_file() -> str:
#     """
#     Open a file dialog for user to select point CSV file.

#     Returns:
#         str: Selected file path or empty string if cancelled
#     """

#     root = tk.Tk()
#     root.withdraw()
#     file_path = filedialog.askopenfilename(
#         title="Select Point File",
#         filetypes=[
#             ("Point Files", "*.txt"),
#             ("ASCII Files", "*.asc"),
#             ("All Files", "*.*")
#             ]
#     )
#     if file_path:
#         logger.info("Selected input file: %s", file_path)
#     else:
#         logger.info("File selection cancelled")
#     return file_path
# def display_csv_file(csv_file):
#     editor = CSVEditor(csv_file)
#     editor.run()
    # Ensure proper cleanup of tkinter resources
    # try:
    #     import tkinter as tk
    #     root = tk._default_root
    #     if root:
    #         root.quit()
    #         root.destroy()
    # except:
    #     pass


def main(input_file):
    """
    Main function to process an input file using configuration files for property corners and
    miscellaneous codes. This function attempts to locate configuration files from multiple
    predefined paths. If found, it loads the code lists from these files and processes the
    input file accordingly. If the configuration files are not found or cannot be loaded,
    appropriate error messages are logged and displayed.

    Args:
        input_file (str): The path to the input file that needs to be processed.

    Returns:
        None
    """



    property_corners_path = os.path.join(DIRNAME, 'config/property_corners.txt')
    miscellaneous_path = os.path.join(DIRNAME, 'config/miscellaneous.txt')

    # Find the first valid configuration files
    # for prop_path, misc_path in config_paths:
    #     if os.path.exists(prop_path) and os.path.exists(misc_path):
    #         property_corners_path = prop_path
    #         miscellaneous_path = misc_path
    #         logger.info("Using config files: %s, %s", prop_path, misc_path)
    #         break

    # if not property_corners_path or not miscellaneous_path:
    #     error_msg = "Could not find configuration files (property_corners.txt, miscellaneous.txt)"
    #     logger.error(error_msg)
    #     messagebox.showerror("Configuration Error", error_msg)
    #     return

    # INPUT_FILE = select_input_file()
    # if not INPUT_FILE:
    #     logger.info("No input file selected. Exiting.")
    #     return

    # Load the code lists from files
    property_codes, misc_codes = load_code_lists(property_corners_path, miscellaneous_path)

    if not property_codes or not misc_codes:
        logger.error("Failed to load configuration files")
        return

    # Process the file with the loaded code lists
    output_file = process_file(input_file, property_codes, misc_codes)
    # display_csv_file(output_file)
    subprocess.Popen(['notepad.exe', output_file])
    # Ensure complete application shutdown
    sys.exit()
