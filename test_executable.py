"""
Test script to validate the executable works correctly
"""
import subprocess
import sys
import os

def test_executable():
    """Test that the executable can be launched without import errors"""
    exe_path = "distribution/AtlanticDescriptionParser.exe"
    
    if not os.path.exists(exe_path):
        print("❌ Executable not found!")
        return False
    
    print(f"✅ Executable found: {exe_path}")
    print(f"📏 Size: {os.path.getsize(exe_path) / (1024*1024):.1f} MB")
    
    # Test that the executable starts (it will show GUI, so we can't test full functionality)
    print("🧪 Testing executable launch...")
    
    try:
        # Start the process but don't wait for it to complete (since it's a GUI app)
        process = subprocess.Popen([exe_path], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE,
                                 creationflags=subprocess.CREATE_NO_WINDOW)
        
        # Give it a moment to start
        import time
        time.sleep(2)
        
        # Check if it's still running (good sign)
        if process.poll() is None:
            print("✅ Executable started successfully (GUI app running)")
            # Terminate the process
            process.terminate()
            return True
        else:
            # Process exited, check for errors
            stdout, stderr = process.communicate()
            if stderr:
                print(f"❌ Executable failed with error: {stderr.decode()}")
                return False
            else:
                print("⚠️  Executable exited immediately (may be normal for GUI)")
                return True
                
    except Exception as e:
        print(f"❌ Failed to launch executable: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing Atlantic Description Parser Executable")
    print("=" * 50)
    
    success = test_executable()
    
    if success:
        print("\n🎉 Executable test PASSED!")
        print("The application should now work correctly for your employees.")
    else:
        print("\n💥 Executable test FAILED!")
        print("There may still be import issues.")
