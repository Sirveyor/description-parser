@echo off
echo ========================================
echo Atlantic Description Parser - Build Script
echo ========================================
echo.

echo Installing PyInstaller...
pip install pyinstaller

echo.
echo Building executable package...
python setup_installer.py

echo.
echo Creating distribution folder...
if not exist "distribution" mkdir distribution
if not exist "distribution\config" mkdir distribution\config
if not exist "distribution\docs" mkdir distribution\docs
if not exist "distribution\samples" mkdir distribution\samples

echo.
echo Copying files to distribution folder...
copy "dist\AtlanticDescriptionParser.exe" "distribution\" >nul
copy "property_corners.txt" "distribution\config\" >nul
copy "miscellaneous.txt" "distribution\config\" >nul
copy "description_dictionary.txt" "distribution\config\" >nul

echo.
echo Copying sample files...
copy "tests\test_data\sample_input.csv" "distribution\samples\" >nul
copy "tests\test_data\sample_replacement_dict.json" "distribution\samples\" >nul

echo.
echo Build complete!
echo Distribution files are in the 'distribution' folder
echo.
pause
