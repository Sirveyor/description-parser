# Atlantic Description Parser - User Manual

## Overview

The Atlantic Description Parser is a Windows application designed to process and standardize point descriptions in CSV files. It consists of two main processing modules that work together to clean and format your data.

## What This Tool Does

### Module 1: Description Standardization
- Replaces text in CSV descriptions using a customizable dictionary
- Standardizes terminology across your data files
- Processes the last column of CSV files

### Module 2: Point Description Processing
- Reorders sizes, property corner codes, and miscellaneous codes
- Ensures consistent formatting of point descriptions
- Adds appropriate slashes (/ or \) to descriptions

## Installation

1. **Download** the `AtlanticDescriptionParser.exe` file
2. **Copy** the executable to a folder on your computer
3. **Double-click** to run the application

*No additional installation required - the application is self-contained.*

## How to Use

### Starting the Application
1. Double-click `AtlanticDescriptionParser.exe`
2. The application will start both processing modules automatically

### Processing Your Files

#### Step 1: Description Standardization
1. A file dialog will appear asking you to select a CSV file
2. Browse to your CSV file and click "Open"
3. The tool will process the file and create a new file with "processed_" prefix
4. A success message will show the number of replacements made

#### Step 2: Point Description Processing
1. Another file dialog will appear for point file selection
2. Select your point file (.txt, .asc, or other formats)
3. The tool will process the file and create a new file with "_processed" suffix
4. A CSV editor will open showing the results

### Viewing and Editing Results
- The built-in CSV editor allows you to:
  - View processed data in a table format
  - Double-click cells to edit values
  - Press Enter to save changes
  - Click "Save Changes" to save the file

## Configuration Files

The application uses several configuration files:

### Replacement Dictionary
- **File**: `replacement_dict.json`
- **Purpose**: Defines text replacements for standardization
- **Format**: JSON file with "old_text": "new_text" pairs
- **Location**: The app will look for this file in multiple locations:
  1. Network path: `N:/carlson settings/f2f/replacement_dict.json`
  2. Same folder as the executable
  3. `config/` subfolder

### Property Corners and Miscellaneous Codes
- **Files**: `property_corners.txt` and `miscellaneous.txt`
- **Purpose**: Define valid codes for point processing
- **Format**: One code per line
- **Location**: Same folder as executable or `config/` subfolder

## File Requirements

### Input Files
- **CSV Files**: Must have at least 5 columns
- **Point Files**: Text files with point descriptions (.txt, .asc)
- **Encoding**: UTF-8 recommended

### Output Files
- Processed files are saved in the same location as input files
- Original files are never modified
- New files have descriptive prefixes/suffixes

## Troubleshooting

### Common Issues

**"Dictionary file not found"**
- Ensure `replacement_dict.json` exists in the correct location
- Check network connectivity if using network path
- The app will create a default dictionary if none is found

**"Configuration files not found"**
- Ensure `property_corners.txt` and `miscellaneous.txt` are present
- Check the same folder as the executable
- Contact your administrator for these files

**"CSV file must have at least 5 columns"**
- Verify your CSV file has the required number of columns
- Check for proper CSV formatting

**Application won't start**
- Ensure you have Windows 10 or later
- Try running as administrator
- Check antivirus software isn't blocking the application

### Getting Help
- Check the log messages in the console window
- Contact your IT administrator
- Refer to the original documentation

## Tips for Best Results

1. **Backup your files** before processing
2. **Review the results** in the CSV editor before saving
3. **Keep configuration files updated** with your organization's standards
4. **Process files in batches** for efficiency
5. **Check the success messages** to confirm processing completed

## File Locations

When the application runs, it looks for files in this order:

1. **Bundled with executable** (for deployed versions)
2. **Current directory** (same folder as .exe)
3. **Config subfolder** (./config/)
4. **Network locations** (if configured)

## Version Information

- **Application**: Atlantic Description Parser
- **Version**: 1.0
- **Platform**: Windows 10/11
- **Dependencies**: Self-contained (no additional software required)

---

*For technical support or questions about this application, contact your system administrator.*
