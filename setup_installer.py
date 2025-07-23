"""
PyInstaller setup script for Atlantic Description Parser
Creates a standalone executable for end-user distribution
"""

import PyInstaller.__main__
import os
import sys
from pathlib import Path

def create_executable():
    """Create standalone executable using PyInstaller"""
    
    # Get the current directory
    current_dir = Path(__file__).parent
    
    # Define paths
    main_script = str(current_dir / "main.py")
    icon_path = str(current_dir / "icon.ico") if (current_dir / "icon.ico").exists() else None
    
    # PyInstaller arguments
    args = [
        main_script,
        '--name=AtlanticDescriptionParser',
        '--onefile',
        '--windowed',
        '--clean',
        f'--distpath={current_dir / "dist"}',
        f'--workpath={current_dir / "build"}',
        f'--specpath={current_dir}',
        
        # Add data files
        f'--add-data={current_dir / "property_corners.txt"};.',
        f'--add-data={current_dir / "miscellaneous.txt"};.',
        f'--add-data={current_dir / "description_dictionary.txt"};.',
        
        # Hidden imports for GUI libraries
        '--hidden-import=tkinter',
        '--hidden-import=tkinter.ttk',
        '--hidden-import=tkinter.filedialog',
        '--hidden-import=tkinter.messagebox',
        '--hidden-import=pandas',
        
        # Exclude unnecessary modules to reduce size
        '--exclude-module=pytest',
        '--exclude-module=test',
        '--exclude-module=unittest',
    ]
    
    # Add icon if available
    if icon_path:
        args.append(f'--icon={icon_path}')
    
    print("Building executable with PyInstaller...")
    print(f"Main script: {main_script}")
    print(f"Output directory: {current_dir / 'dist'}")
    
    # Run PyInstaller
    PyInstaller.__main__.run(args)
    
    print("\nBuild complete!")
    print(f"Executable created: {current_dir / 'dist' / 'AtlanticDescriptionParser.exe'}")

if __name__ == "__main__":
    create_executable()
