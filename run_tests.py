#!/usr/bin/env python3
"""
Simple test runner script for the description-parser project.
This script provides easy commands to run different types of tests.
"""

import subprocess
import sys
import argparse
from pathlib import Path


def run_command(cmd, description=""):
    """Run a command and return the result."""
    if description:
        print(f"\n{'='*60}")
        print(f"Running: {description}")
        print(f"Command: {' '.join(cmd)}")
        print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.stdout:
            print("STDOUT:")
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"Error running command: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Test runner for description-parser")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--unit", action="store_true", help="Run unit tests only")
    parser.add_argument("--integration", action="store_true", help="Run integration tests only")
    parser.add_argument("--coverage", action="store_true", help="Run tests with coverage")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--fast", action="store_true", help="Skip slow tests")
    parser.add_argument("--module", help="Run tests for specific module")
    
    args = parser.parse_args()
    
    # Base pytest command
    base_cmd = [sys.executable, "-m", "pytest"]
    
    if args.verbose:
        base_cmd.append("-v")
    
    if args.coverage:
        base_cmd.extend(["--cov=.", "--cov-report=html", "--cov-report=term"])
    
    if args.fast:
        base_cmd.extend(["-m", "not slow"])
    
    success = True
    
    if args.all or (not any([args.unit, args.integration, args.module])):
        # Run all tests
        cmd = base_cmd + ["tests/"]
        success &= run_command(cmd, "All Tests")
    
    elif args.unit:
        # Run unit tests (exclude integration)
        cmd = base_cmd + ["tests/", "-k", "not integration"]
        success &= run_command(cmd, "Unit Tests")
    
    elif args.integration:
        # Run integration tests only
        cmd = base_cmd + ["tests/test_integration.py"]
        success &= run_command(cmd, "Integration Tests")
    
    elif args.module:
        # Run tests for specific module
        test_file = f"tests/test_{args.module}.py"
        if Path(test_file).exists():
            cmd = base_cmd + [test_file]
            success &= run_command(cmd, f"Tests for {args.module}")
        else:
            print(f"Test file not found: {test_file}")
            success = False
    
    # Additional useful commands
    if args.all:
        print(f"\n{'='*60}")
        print("Test Summary")
        print(f"{'='*60}")
        
        # Show test discovery
        cmd = base_cmd + ["--collect-only", "-q"]
        run_command(cmd, "Test Discovery")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
