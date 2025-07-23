# Atlantic Description Parser - Installation Guide

## For IT Administrators and Deployment

This guide provides instructions for deploying the Atlantic Description Parser to end users in your organization.

## Package Contents

The deployment package includes:
- `AtlanticDescriptionParser.exe` - Main application executable
- `config/` folder with configuration files
- `docs/` folder with user documentation
- `samples/` folder with example files

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10 (version 1903 or later)
- **Architecture**: x64 (64-bit)
- **RAM**: 512 MB available memory
- **Disk Space**: 50 MB free space
- **Display**: 1024x768 minimum resolution

### Recommended Requirements
- **Operating System**: Windows 11
- **RAM**: 2 GB available memory
- **Disk Space**: 100 MB free space
- **Network**: Access to `N:/carlson settings/f2f/` (if using network dictionary)

## Deployment Options

### Option 1: Simple Copy Deployment
1. Copy the entire application folder to user machines
2. Recommended location: `C:\Program Files\AtlanticDescriptionParser\`
3. Create desktop shortcut to `AtlanticDescriptionParser.exe`
4. No registry changes required

### Option 2: Network Deployment
1. Place application on network share
2. Create shortcuts on user desktops pointing to network location
3. Ensure users have read/execute permissions
4. Consider performance implications for large files

### Option 3: Group Policy Deployment
1. Package the application folder into an MSI (using tools like WiX)
2. Deploy via Group Policy Software Installation
3. Configure automatic updates if needed

## Configuration Setup

### Required Configuration Files

#### 1. Replacement Dictionary (`replacement_dict.json`)
```json
{
  "OLD_TEXT_1": "NEW_TEXT_1",
  "OLD_TEXT_2": "NEW_TEXT_2",
  "EXAMPLE_OLD": "EXAMPLE_NEW"
}
```

**Deployment Locations** (in order of precedence):
1. `N:/carlson settings/f2f/replacement_dict.json` (network)
2. Same folder as executable
3. `config/replacement_dict.json` (local config)

#### 2. Property Corners (`property_corners.txt`)
```
ip
mon
pc
corner
```
*One code per line, case-insensitive*

#### 3. Miscellaneous Codes (`miscellaneous.txt`)
```
found
set
calc
existing
```
*One code per line*

### Configuration File Locations
The application searches for configuration files in this order:
1. Bundled with executable (PyInstaller bundle)
2. Current directory (same as .exe)
3. `config/` subdirectory
4. Network paths (if configured)

## Network Configuration

### Shared Dictionary File
If using a centralized replacement dictionary:

1. **Network Path**: `N:/carlson settings/f2f/replacement_dict.json`
2. **Permissions**: Users need read access
3. **Backup**: Maintain backup copies
4. **Updates**: Changes apply to all users immediately

### Firewall Considerations
- Application doesn't require internet access
- Only needs local file system and network share access
- No incoming connections required

## Security Considerations

### Antivirus Exclusions
Some antivirus software may flag the executable. Consider adding exclusions for:
- `AtlanticDescriptionParser.exe`
- Application installation directory
- User data processing directories

### User Permissions
- Users need read/write access to their data directories
- No administrator privileges required for normal operation
- Consider read-only access to configuration files

### Data Security
- Application processes files locally
- No data transmitted over internet
- Temporary files created in system temp directory
- Original files are never modified (creates new processed files)

## Testing Deployment

### Pre-deployment Testing
1. Test on representative user machines
2. Verify all configuration files are accessible
3. Test with sample data files
4. Confirm GUI displays correctly
5. Validate file processing results

### Test Checklist
- [ ] Application starts without errors
- [ ] Configuration files load successfully
- [ ] File dialogs work correctly
- [ ] Processing completes successfully
- [ ] Output files are created correctly
- [ ] CSV editor functions properly
- [ ] Error messages are user-friendly

## Troubleshooting Common Issues

### Application Won't Start
- **Check**: Windows version compatibility
- **Check**: File permissions on executable
- **Check**: Antivirus blocking
- **Solution**: Run as administrator temporarily

### Configuration Files Not Found
- **Check**: File paths and permissions
- **Check**: Network connectivity (for network paths)
- **Solution**: Copy files to local config directory

### Processing Errors
- **Check**: Input file format and encoding
- **Check**: Available disk space
- **Check**: File permissions in output directory

## Monitoring and Maintenance

### Log Files
- Application logs to console window
- Consider redirecting output for automated deployments
- No persistent log files created by default

### Updates
- Replace executable file for updates
- Backup configuration files before updates
- Test updates in non-production environment first

### User Support
- Provide users with `USER_MANUAL.md`
- Train key users on basic troubleshooting
- Establish support process for configuration issues

## Uninstallation

### Manual Removal
1. Delete application directory
2. Remove desktop shortcuts
3. Clean up any user-created data files
4. No registry entries to remove

### Automated Removal
- Use Group Policy for MSI-deployed versions
- Script-based removal for copy deployments

## Advanced Configuration

### Custom Paths
Modify the source code to change default paths:
- Edit `DEFAULT_DICT_PATHS` in `description_parser.py`
- Rebuild executable with PyInstaller

### Branding
- Replace application icon
- Modify window titles in source code
- Rebuild with custom branding

## Support Information

### Technical Specifications
- **Framework**: Python 3.13 with PyInstaller
- **GUI**: Tkinter (built into Python)
- **Dependencies**: Pandas for CSV processing
- **Architecture**: Single executable with bundled dependencies

### Known Limitations
- Windows only (due to PyInstaller build)
- GUI requires display (not suitable for server automation)
- Large files may require significant memory

---

*For technical questions about deployment, contact your development team or system administrator.*
