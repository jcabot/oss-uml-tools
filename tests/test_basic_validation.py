"""
Basic validation test for UML Tools Dashboard.
This test runs without external dependencies to verify core functionality.

Usage:
    python tests/test_basic_validation.py
"""

import os
import sys
import csv

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_required_files_exist():
    """Test that all required files exist."""
    print("Testing required files...")
    required_files = ['app.py', 'analysis.py', 'requirements.txt', 'snapshot.csv']
    
    all_exist = True
    for filename in required_files:
        if os.path.exists(filename):
            print(f"[OK] {filename} exists")
        else:
            print(f"[FAIL] {filename} missing")
            all_exist = False
    
    return all_exist

def test_csv_basic_format():
    """Test basic CSV format without pandas."""
    print("\nTesting CSV format...")
    try:
        with open('snapshot.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            
            if len(rows) == 0:
                print("[FAIL] No data in snapshot.csv")
                return False
            
            # Check required columns
            required_columns = ['Name', 'Stars⭐', 'URL']
            first_row = rows[0]
            
            for col in required_columns:
                if col not in first_row:
                    print(f"[FAIL] Missing column: {col}")
                    return False
            
            print(f"[OK] CSV contains {len(rows)} repositories")
            print(f"[OK] Sample: {first_row['Name']} with {first_row['Stars⭐']} stars")
            return True
            
    except Exception as e:
        print(f"[FAIL] CSV format test failed: {e}")
        return False

def test_app_structure():
    """Test basic app.py structure without importing it."""
    print("\nTesting app.py structure...")
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Check for key functions and imports
            required_elements = [
                'def fetch_uml_repos',
                'import streamlit',
                'import pandas',
                'snapshot.csv'
            ]
            
            for element in required_elements:
                if element in content:
                    print(f"[OK] Found: {element}")
                else:
                    print(f"[FAIL] Missing: {element}")
                    return False
            
            return True
            
    except Exception as e:
        print(f"[FAIL] App structure test failed: {e}")
        return False

def test_fallback_logic_structure():
    """Test that fallback logic is present in app.py."""
    print("\nTesting fallback logic structure...")
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Check for fallback-related code
            fallback_elements = [
                'api_failed',
                'encoding=\'utf-8-sig\'',
                'st.warning',
                'st.info',
                'snapshot_path'
            ]
            
            for element in fallback_elements:
                if element in content:
                    print(f"[OK] Found fallback element: {element}")
                else:
                    print(f"[FAIL] Missing fallback element: {element}")
                    return False
            
            return True
            
    except Exception as e:
        print(f"[FAIL] Fallback logic test failed: {e}")
        return False

def main():
    """Run all basic validation tests."""
    print("=" * 60)
    print("UML TOOLS DASHBOARD - BASIC VALIDATION")
    print("=" * 60)
    print("This test validates core functionality without external dependencies.\n")
    
    tests = [
        ("Required Files", test_required_files_exist),
        ("CSV Format", test_csv_basic_format),
        ("App Structure", test_app_structure),
        ("Fallback Logic", test_fallback_logic_structure)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'-' * 50}")
        print(f"Running: {test_name}")
        print(f"{'-' * 50}")
        results.append(test_func())
    
    print("\n" + "=" * 60)
    if all(results):
        print("SUCCESS: ALL BASIC VALIDATION TESTS PASSED!")
        print("\nCore functionality is properly structured:")
        print("✅ All required files are present")
        print("✅ CSV data is formatted correctly") 
        print("✅ App.py has the required structure")
        print("✅ Fallback mechanism is implemented")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run full tests: python tests/test_normal_operation.py")
        print("3. Test fallback: python tests/test_fallback_mechanism.py")
    else:
        print("FAILED: SOME VALIDATION TESTS FAILED!")
        print("Please check the errors above and fix the issues.")
    print("=" * 60)
    
    return all(results)

if __name__ == "__main__":
    main() 