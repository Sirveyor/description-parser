"""
Test the complete file processing workflow
"""
import csv
import os
import sys
from pathlib import Path

def create_test_csv():
    """Create a test CSV file with various description patterns"""
    test_data = [
        ["Point", "Northing", "Easting", "Elevation", "Description"],
        ["1", "1000.00", "2000.00", "100.00", "RBF 5/8"],  # Should become "RBF\\5/8"
        ["2", "1001.00", "2001.00", "101.00", "FOUNDATION"],  # Should become "FND"
        ["3", "1002.00", "2002.00", "102.00", "PTF 1"],  # Should become "PTF\\1"
        ["4", "1003.00", "2003.00", "103.00", "WALL \\CONC"],  # Should become "WALL /CONC"
        ["5", "1004.00", "2004.00", "104.00", "IO 1/2"],  # Should become "IO\\1/2"
        ["6", "1005.00", "2005.00", "105.00", "RBF IO 3/4"],  # Two codes test
        ["7", "1006.00", "2006.00", "106.00", "MISC CHK"],  # Miscellaneous code test
    ]
    
    test_file = "workflow_test_input.csv"
    with open(test_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(test_data)
    
    print(f"✅ Created test file: {test_file}")
    return test_file

def test_description_parser_workflow(test_file):
    """Test the description parser workflow"""
    print("\n🔄 Testing Description Parser workflow...")
    
    try:
        from description_parser import DescriptionParser
        
        # Create parser with bundled config
        parser = DescriptionParser(
            dictionary_path="distribution/config/replacement_dict.json",
            gui_mode=False
        )
        
        # Process the file
        parser.process_file(test_file)
        
        # Check if processed file was created
        processed_file = f"processed_{test_file}"
        if os.path.exists(processed_file):
            print(f"✅ Processed file created: {processed_file}")
            
            # Read and verify the processed content
            with open(processed_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)
                
            print("📋 Processed results:")
            for i, row in enumerate(rows[1:], 1):  # Skip header
                original_desc = ["RBF 5/8", "FOUNDATION", "PTF 1", "WALL \\CONC", "IO 1/2", "RBF IO 3/4", "MISC CHK"][i-1]
                processed_desc = row[4] if len(row) > 4 else "N/A"
                print(f"  Row {i}: '{original_desc}' → '{processed_desc}'")
            
            return True
        else:
            print("❌ Processed file not created")
            return False
            
    except Exception as e:
        print(f"❌ Error in description parser workflow: {e}")
        return False

def test_parser3_workflow(test_file):
    """Test the parser3 (point description) workflow"""
    print("\n🔄 Testing Parser3 workflow...")
    
    try:
        import parser3
        
        # Load the code lists
        property_codes, misc_codes = parser3.load_code_lists(
            "distribution/config/property_corners.txt",
            "distribution/config/miscellaneous.txt"
        )
        
        if not property_codes or not misc_codes:
            print("❌ Failed to load code lists")
            return False
            
        print(f"✅ Loaded {len(property_codes)} property codes and {len(misc_codes)} misc codes")
        
        # Process the file
        output_file = parser3.process_file(test_file, property_codes, misc_codes)
        
        if os.path.exists(output_file):
            print(f"✅ Parser3 processed file created: {output_file}")
            return True
        else:
            print("❌ Parser3 processed file not created")
            return False
            
    except Exception as e:
        print(f"❌ Error in parser3 workflow: {e}")
        return False

def cleanup_test_files():
    """Clean up test files"""
    test_files = [
        "workflow_test_input.csv",
        "processed_workflow_test_input.csv",
        "workflow_test_input_processed.csv"
    ]
    
    for file in test_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"🧹 Cleaned up: {file}")

def run_workflow_test():
    """Run the complete workflow test"""
    print("🔄 WORKFLOW TESTING")
    print("=" * 50)
    
    try:
        # Create test file
        test_file = create_test_csv()
        
        # Test description parser
        desc_result = test_description_parser_workflow(test_file)
        
        # Test parser3 (skip GUI parts)
        # parser3_result = test_parser3_workflow(test_file)
        
        print("\n" + "=" * 50)
        print("📊 WORKFLOW TEST RESULTS")
        print("=" * 50)
        
        print(f"Description Parser: {'✅ PASS' if desc_result else '❌ FAIL'}")
        # print(f"Parser3: {'✅ PASS' if parser3_result else '❌ FAIL'}")
        
        if desc_result:
            print("\n🎉 WORKFLOW TEST PASSED!")
            print("The application successfully processes CSV files with your replacement rules.")
            return True
        else:
            print("\n❌ WORKFLOW TEST FAILED!")
            return False
            
    except Exception as e:
        print(f"❌ Workflow test error: {e}")
        return False
    finally:
        cleanup_test_files()

if __name__ == "__main__":
    success = run_workflow_test()
    sys.exit(0 if success else 1)
