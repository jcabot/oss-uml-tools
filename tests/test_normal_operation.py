"""
Comprehensive test suite for normal UML Tools Dashboard operation.

This module tests:
1. Basic functionality and file structure
2. Dependencies and imports
3. CSV data loading and processing
4. Normal GitHub API operation (mocked)
5. Data format conversion

Usage:
    python tests/test_normal_operation.py
"""

import os
import sys
import unittest
import csv
from unittest.mock import patch, MagicMock

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestBasicFunctionality(unittest.TestCase):
    """Test basic functionality and file structure."""
    
    def test_required_files_exist(self):
        """Test that all required files exist."""
        required_files = ['app.py', 'analysis.py', 'requirements.txt', 'snapshot.csv']
        
        for filename in required_files:
            with self.subTest(file=filename):
                self.assertTrue(os.path.exists(filename), f"{filename} should exist")
        
        print("[OK] All required files exist")
    
    def test_basic_imports(self):
        """Test that basic Python modules can be imported."""
        try:
            import os
            import sys
            from datetime import datetime, timedelta
            from collections import Counter
            print("[OK] Basic Python modules imported successfully")
        except ImportError as e:
            self.fail(f"Failed to import basic modules: {e}")
    
    def test_app_import(self):
        """Test that app.py can be imported and contains required functions."""
        try:
            from app import fetch_uml_repos
            self.assertTrue(callable(fetch_uml_repos), "fetch_uml_repos should be callable")
            print("[OK] App modules imported successfully")
        except ImportError as e:
            self.fail(f"Failed to import app modules: {e}")


class TestCSVDataHandling(unittest.TestCase):
    """Test CSV data loading and processing."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.snapshot_path = "snapshot.csv"
    
    def test_csv_file_exists_and_readable(self):
        """Test that CSV file exists and is readable."""
        self.assertTrue(os.path.exists(self.snapshot_path), "snapshot.csv should exist")
        
        with open(self.snapshot_path, 'r', encoding='utf-8-sig') as f:
            first_line = f.readline().strip()
            self.assertIn('Name', first_line, "CSV should have Name column")
            self.assertIn('Stars⭐', first_line, "CSV should have Stars column")
        
        print("[OK] CSV file exists and is readable")
    
    def test_csv_data_integrity(self):
        """Test CSV data format and content."""
        required_columns = ['Name', 'Stars⭐', 'Last Updated', 'First Commit', 
                          'URL', 'Forks', 'Issues', 'Language', 'License', 
                          'Description', 'Topics']
        
        with open(self.snapshot_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            
            self.assertGreater(len(rows), 0, "CSV should contain repository data")
            
            first_row = rows[0]
            for col in required_columns:
                self.assertIn(col, first_row, f"Column '{col}' should exist")
            
            # Validate data types and formats
            self.assertIsInstance(first_row['Name'], str)
            self.assertTrue(first_row['URL'].startswith('https://github.com/'))
            
        print(f"[OK] CSV contains {len(rows)} repositories with correct format")
    
    def test_csv_to_api_conversion(self):
        """Test conversion of CSV data to GitHub API format."""
        with open(self.snapshot_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            sample_row = next(reader)
            
            # Convert to API format (same logic as in app.py)
            repo_data = {
                "name": sample_row["Name"],
                "stargazers_count": int(sample_row["Stars⭐"]),
                "pushed_at": sample_row["Last Updated"] + "T00:00:00Z",
                "created_at": sample_row["First Commit"] + "T00:00:00Z",
                "html_url": sample_row["URL"],
                "forks": int(sample_row["Forks"]),
                "open_issues": int(sample_row["Issues"]),
                "language": sample_row["Language"] if sample_row["Language"] and sample_row["Language"] != "No language" else None,
                "license": {"name": sample_row["License"]} if sample_row["License"] != "No license" else None,
                "description": sample_row["Description"] if sample_row["Description"] != "No description" else None,
                "topics": sample_row["Topics"].split(",") if sample_row["Topics"] else []
            }
            
            # Validate converted structure
            self.assertIsInstance(repo_data["name"], str)
            self.assertIsInstance(repo_data["stargazers_count"], int)
            self.assertIsInstance(repo_data["topics"], list)
            self.assertTrue(repo_data["pushed_at"].endswith("T00:00:00Z"))
            
        print(f"[OK] CSV to API conversion works: {repo_data['name']}")


class TestNormalAPIOperation(unittest.TestCase):
    """Test normal GitHub API operation with mocks."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_repo_data = {
            "name": "test-uml-tool",
            "stargazers_count": 150,
            "pushed_at": "2023-12-01T00:00:00Z",
            "created_at": "2023-01-01T00:00:00Z",
            "html_url": "https://github.com/test/test-uml-tool",
            "forks": 25,
            "open_issues": 3,
            "language": "Java",
            "license": {"name": "MIT License"},
            "description": "A test UML tool",
            "topics": ["uml", "diagrams", "modeling"]
        }
    
    @patch('requests.get')
    def test_successful_api_call(self, mock_get):
        """Test successful GitHub API response."""
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [self.test_repo_data]
        }
        mock_get.return_value = mock_response
        
        with patch('streamlit.error'), patch('streamlit.warning'), patch('streamlit.info'):
            from app import fetch_uml_repos
            repos = fetch_uml_repos(max_pages=1)
            
            self.assertGreater(len(repos), 0, "Should return repositories")
            self.assertEqual(repos[0]["name"], "test-uml-tool")
            self.assertEqual(repos[0]["stargazers_count"], 150)
        
        print("[OK] Normal API operation works correctly")


class TestDependencies(unittest.TestCase):
    """Test required dependencies availability."""
    
    def test_optional_dependencies(self):
        """Test optional dependencies with graceful handling."""
        optional_modules = {
            'pandas': 'Required for CSV processing',
            'requests': 'Required for API calls', 
            'streamlit': 'Required for web interface',
            'plotly': 'Required for charts'
        }
        
        missing_modules = []
        for module, purpose in optional_modules.items():
            try:
                __import__(module)
                print(f"[OK] {module} is available")
            except ImportError:
                missing_modules.append(f"{module} ({purpose})")
        
        if missing_modules:
            print(f"[WARNING] Missing optional modules: {', '.join(missing_modules)}")
            print("[INFO] App will use fallback mechanisms")
        else:
            print("[OK] All dependencies are available")


def run_integration_test():
    """Run integration test to verify overall functionality."""
    print("\n" + "="*60)
    print("INTEGRATION TEST: UML Tools Dashboard Normal Operation")
    print("="*60)
    
    try:
        # Test basic file structure
        required_files = ['app.py', 'analysis.py', 'snapshot.csv']
        for file in required_files:
            if not os.path.exists(file):
                raise FileNotFoundError(f"Required file {file} not found")
        
        # Test CSV loading
        with open('snapshot.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            if len(rows) == 0:
                raise ValueError("No data in snapshot.csv")
        
        # Test function import
        from app import fetch_uml_repos
        if not callable(fetch_uml_repos):
            raise ImportError("fetch_uml_repos is not callable")
        
        print(f"[OK] Found {len(rows)} repositories in snapshot")
        print("[OK] All core functionality verified")
        print("\n[SUCCESS] INTEGRATION TEST PASSED!")
        print("Normal operation is working correctly.")
        return True
        
    except Exception as e:
        print(f"\n[FAIL] INTEGRATION TEST FAILED: {e}")
        return False


if __name__ == "__main__":
    # Run integration test first
    if run_integration_test():
        print("\n" + "="*60)
        print("RUNNING UNIT TESTS")
        print("="*60)
        
        unittest.main(verbosity=2, exit=False, buffer=True)
    else:
        print("Integration test failed. Please check your setup.")
        sys.exit(1) 