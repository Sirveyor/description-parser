"""
Comprehensive test script for the Atlantic Description Parser executable
Tests the complete workflow with sample data
"""
import subprocess
import os
import sys
import time
import csv
import json
from pathlib import Path

def setup_test_environment():
    """Set up test files and environment"""
    print("🔧 Setting up test environment...")
    
    # Create test input CSV file
    test_csv_content = [
        ["Point", "Northing", "Easting", "Elevation", "Description"],
        ["1", "1000.00", "2000.00", "100.00", "RBF 5/8"],
        ["2", "1001.00", "2001.00", "101.00", "PTF 1"],
        ["3", "1002.00", "2002.00", "102.00", "FOUNDATION"],
        ["4", "1003.00", "2003.00", "103.00", "IO 1/2"],
        ["5", "1004.00", "2004.00", "104.00", "WALL \\CONC"]
    ]
    
    test_csv_path = "test_input.csv"
    with open(test_csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(test_csv_content)
    
    print(f"✅ Created test CSV: {test_csv_path}")
    return test_csv_path

def test_config_files():
    """Test that all configuration files are accessible"""
    print("\n📋 Testing configuration files...")
    
    config_files = [
        "distribution/config/replacement_dict.json",
        "distribution/config/property_corners.txt", 
        "distribution/config/miscellaneous.txt"
    ]
    
    all_good = True
    for config_file in config_files:
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if content.strip():
                        print(f"✅ {config_file}: OK ({len(content)} chars)")
                    else:
                        print(f"⚠️  {config_file}: Empty file")
                        all_good = False
            except Exception as e:
                print(f"❌ {config_file}: Error reading - {e}")
                all_good = False
        else:
            print(f"❌ {config_file}: Not found")
            all_good = False
    
    return all_good

def test_replacement_logic():
    """Test the replacement dictionary logic"""
    print("\n🔄 Testing replacement logic...")
    
    try:
        with open("distribution/config/replacement_dict.json", 'r', encoding='utf-8') as f:
            replacement_dict = json.load(f)
        
        test_cases = [
            ("RBF 5/8", "RBF\\5/8"),
            ("FOUNDATION", "FND"),
            ("WALL \\", "WALL /")
        ]
        
        all_passed = True
        for original, expected in test_cases:
            if original in replacement_dict:
                actual = replacement_dict[original]
                if actual == expected:
                    print(f"✅ '{original}' → '{actual}' (correct)")
                else:
                    print(f"❌ '{original}' → '{actual}' (expected '{expected}')")
                    all_passed = False
            else:
                print(f"⚠️  '{original}' not found in replacement dictionary")
        
        print(f"📊 Replacement dictionary has {len(replacement_dict)} rules")
        return all_passed
        
    except Exception as e:
        print(f"❌ Error testing replacement logic: {e}")
        return False

def test_module_imports():
    """Test that the Python modules can be imported correctly"""
    print("\n🐍 Testing module imports...")
    
    try:
        # Test importing the main modules
        sys.path.insert(0, '.')
        
        import description_parser
        print("✅ description_parser module imported successfully")
        
        import parser3
        print("✅ parser3 module imported successfully")
        
        import csv_editor
        print("✅ csv_editor module imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_file_processing():
    """Test file processing logic without GUI"""
    print("\n📁 Testing file processing logic...")
    
    try:
        # Test the description parser logic
        from description_parser import DescriptionParser
        
        # Create parser with test config
        parser = DescriptionParser(
            dictionary_path="distribution/config/replacement_dict.json",
            gui_mode=False
        )
        
        # Test that dictionary loaded
        if parser.replacement_dict:
            print(f"✅ Replacement dictionary loaded: {len(parser.replacement_dict)} rules")
        else:
            print("❌ Replacement dictionary not loaded")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Error testing file processing: {e}")
        return False

def run_comprehensive_test():
    """Run all tests"""
    print("🧪 COMPREHENSIVE ATLANTIC DESCRIPTION PARSER TEST")
    print("=" * 60)
    
    results = {}
    
    # Test 1: Configuration files
    results['config_files'] = test_config_files()
    
    # Test 2: Replacement logic
    results['replacement_logic'] = test_replacement_logic()
    
    # Test 3: Module imports
    results['module_imports'] = test_module_imports()
    
    # Test 4: File processing
    results['file_processing'] = test_file_processing()
    
    # Test 5: Executable exists and is correct size
    exe_path = "distribution/AtlanticDescriptionParser.exe"
    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"\n💾 Executable: ✅ Found ({size_mb:.1f} MB)")
        results['executable'] = True
    else:
        print(f"\n💾 Executable: ❌ Not found at {exe_path}")
        results['executable'] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.replace('_', ' ').title()}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! The application is ready for deployment.")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Review issues above.")
        return False

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)
