# Atlantic Description Parser - Distribution Package

## Quick Start

1. **Run the build script**: Double-click `build_package.bat`
2. **Find your package**: Look in the `distribution/` folder
3. **Deploy to users**: Copy the `distribution/` folder contents to user machines

## Package Structure

```
description-parser/
├── AtlanticDescriptionParser.exe    # Main application
├── config/                          # Configuration files
│   ├── property_corners.txt
│   ├── miscellaneous.txt
│   └── replacement_dict.json
├── docs/                           # Documentation
│   ├── USER_MANUAL.md
│   └── INSTALLATION_GUIDE.md
└── samples/                        # Example files
    ├── sample_input.csv
    └── sample_replacement_dict.json
```

## Building the Package

### Prerequisites
- Python 3.13+ installed
- All project files in the `description-parser/` directory

### Build Process
1. Open Command Prompt in the `description-parser/` directory
2. Run: `build_package.bat`
3. The script will:
   - Install PyInstaller
   - Build the executable
   - Create the distribution folder
   - Copy all necessary files

### Build Output
- **Executable**: `distribution/AtlanticDescriptionParser.exe`
- **Configuration**: `distribution/config/` folder
- **Documentation**: `distribution/docs/` folder
- **Examples**: `distribution/samples/` folder

## Configuration Files

### replacement_dict.json
Contains your production text replacement rules:
- RBF size formatting (e.g., "5/8 RBF" → "RBF\\5/8")
- Line formatting (e.g., " LINE" → " /LINE")
- Abbreviations (e.g., "FOUNDATION" → "FND")
- And many more specific to your workflow

### property_corners.txt & miscellaneous.txt
Define valid codes for point processing - ensure these files contain your organization's standard codes.

## Deployment Options

### Option 1: Simple Copy
1. Copy the entire `distribution/` folder to user machines
2. Place in `C:\Program Files\AtlanticDescriptionParser\`
3. Create desktop shortcuts

### Option 2: Network Share
1. Place `distribution/` folder on network share
2. Users run from network location
3. Centralized updates possible

### Option 3: ZIP Distribution
1. Zip the `distribution/` folder
2. Email or distribute via file sharing
3. Users extract and run

## Testing the Package

Before distributing to users:

1. **Test on clean machine**: Verify it works without development environment
2. **Test with real data**: Use actual CSV and point files
3. **Verify configuration**: Ensure all config files are found
4. **Check permissions**: Confirm users can read/write files

## Troubleshooting Build Issues

### PyInstaller Installation Fails
```bash
pip install --upgrade pip
pip install pyinstaller
```

### Build Errors
- Check Python version (3.13+ required)
- Ensure all source files are present
- Check file permissions
- Try running as administrator

### Missing Dependencies
The build script includes all necessary dependencies. If issues occur:
```bash
pip install pandas tkinter
```

## Customization

### Updating Configuration
1. Edit the configuration files in the source directory
2. Rebuild the package
3. Redistribute to users

### Modifying the Application
1. Edit Python source files
2. Test changes
3. Rebuild with `build_package.bat`
4. Test the new executable

## Version Control

When updating the package:
1. **Backup** current configuration files
2. **Test** changes thoroughly
3. **Document** what changed
4. **Distribute** with clear version information

## Support Information

### For Developers
- Source code is in the main directory
- Tests are in the `tests/` folder
- Build configuration in `setup_installer.py`

### For IT Administrators
- See `INSTALLATION_GUIDE.md` for deployment details
- Configuration files can be centrally managed
- No registry changes required

### For End Users
- See `USER_MANUAL.md` for usage instructions
- Application is self-contained
- No technical knowledge required

## File Sizes (Approximate)
- **Executable**: ~50-100 MB (includes Python runtime)
- **Configuration**: <1 MB
- **Documentation**: <1 MB
- **Total Package**: ~50-100 MB

## Security Notes
- Application doesn't require internet access
- No data is transmitted externally
- Original files are never modified
- Temporary files are cleaned up automatically

---

**Ready to deploy!** Your Atlantic Description Parser is now packaged and ready for distribution to your employees.
