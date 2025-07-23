@echo off
echo ========================================
echo Atlantic Description Parser - Build Script
echo ========================================
echo.

echo Installing PyInstaller...
pip install pyinstaller

echo.
echo Building executable with PyInstaller...
pyinstaller --name=AtlanticDescriptionParser ^
    --onefile ^
    --windowed ^
    --clean ^
    --add-data="property_corners.txt;." ^
    --add-data="miscellaneous.txt;." ^
    --add-data="replacement_dict.json;." ^
    --add-data="description_parser.py;." ^
    --add-data="parser3.py;." ^
    --add-data="csv_editor.py;." ^
    --hidden-import=tkinter ^
    --hidden-import=tkinter.ttk ^
    --hidden-import=tkinter.filedialog ^
    --hidden-import=tkinter.messagebox ^
    --hidden-import=pandas ^
    --hidden-import=description_parser ^
    --hidden-import=parser3 ^
    --hidden-import=csv_editor ^
    --exclude-module=pytest ^
    --exclude-module=test ^
    --exclude-module=unittest ^
    main.py

echo.
echo Creating distribution folder...
if not exist "distribution" mkdir distribution
if not exist "distribution\config" mkdir distribution\config
if not exist "distribution\docs" mkdir distribution\docs
if not exist "distribution\samples" mkdir distribution\samples

echo.
echo Copying files to distribution folder...
if exist "dist\AtlanticDescriptionParser.exe" (
    copy "dist\AtlanticDescriptionParser.exe" "distribution\" >nul
    echo Executable copied successfully
) else (
    echo ERROR: Executable not found in dist folder
)

copy "property_corners.txt" "distribution\config\" >nul
copy "miscellaneous.txt" "distribution\config\" >nul
copy "replacement_dict.json" "distribution\config\" >nul

echo.
echo Copying documentation...
copy "USER_MANUAL.md" "distribution\docs\" >nul
copy "INSTALLATION_GUIDE.md" "distribution\docs\" >nul
copy "PACKAGE_README.md" "distribution\docs\" >nul

echo.
echo Copying sample files...
copy "tests\test_data\sample_input.csv" "distribution\samples\" >nul
copy "tests\test_data\sample_replacement_dict.json" "distribution\samples\" >nul

echo.
echo Build complete!
echo Distribution files are in the 'distribution' folder
echo.
pause
