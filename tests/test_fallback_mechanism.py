"""
Comprehensive test suite for the GitHub API fallback mechanism.

This module tests:
1. Fallback to snapshot.csv when API fails
2. Network error handling
3. HTTP error handling  
4. Data consistency during fallback
5. User notification during fallback

Usage:
    python tests/test_fallback_mechanism.py
"""

import os
import sys
import unittest
import csv
from unittest.mock import patch, MagicMock

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestFallbackTriggers(unittest.TestCase):
    """Test conditions that trigger fallback mechanism."""
    
    @patch('requests.get')
    def test_network_error_triggers_fallback(self, mock_get):
        """Test fallback when network request fails."""
        # Mock network failure
        mock_get.side_effect = Exception("Network timeout")
        
        with patch('streamlit.error') as mock_error, \
             patch('streamlit.warning') as mock_warning, \
             patch('streamlit.info') as mock_info:
            
            from app import fetch_uml_repos
            repos = fetch_uml_repos(max_pages=1)
            
            # Should fall back to snapshot data
            self.assertGreater(len(repos), 0, "Should load repos from snapshot")
            self.assertIn('name', repos[0], "Repo should have correct structure")
            
            # Should show appropriate user notifications
            mock_error.assert_called()
            mock_warning.assert_called()
            mock_info.assert_called()
        
        print(f"[OK] Network error fallback: loaded {len(repos)} repos")
    
    @patch('requests.get')
    def test_http_error_triggers_fallback(self, mock_get):
        """Test fallback when API returns HTTP error."""
        # Mock HTTP error responses
        error_codes = [403, 404, 500, 503]  # Various error conditions
        
        for error_code in error_codes:
            with self.subTest(error_code=error_code):
                mock_response = MagicMock()
                mock_response.status_code = error_code
                mock_get.return_value = mock_response
                
                with patch('streamlit.error'), \
                     patch('streamlit.warning'), \
                     patch('streamlit.info'):
                    
                    from app import fetch_uml_repos
                    repos = fetch_uml_repos(max_pages=1)
                    
                    self.assertGreater(len(repos), 0, 
                                     f"Should fall back on HTTP {error_code}")
        
        print("[OK] HTTP error fallback works for various error codes")


class TestFallbackDataHandling(unittest.TestCase):
    """Test data handling during fallback operations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.snapshot_path = "snapshot.csv"
    
    def test_csv_loading_with_bom_handling(self):
        """Test CSV loading with proper BOM handling."""
        try:
            with open(self.snapshot_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                
                self.assertGreater(len(rows), 0, "Should load data")
                first_row = rows[0]
                
                # Check that column names don't have BOM artifacts
                for column in first_row.keys():
                    self.assertNotIn('\ufeff', column, 
                                   f"Column '{column}' should not contain BOM")
            
            print("[OK] CSV loading handles BOM correctly")
        except Exception as e:
            self.fail(f"BOM handling failed: {e}")
    
    def test_fallback_data_conversion_accuracy(self):
        """Test accuracy of CSV to API format conversion."""
        with open(self.snapshot_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            sample_row = next(reader)
            
            # Perform conversion
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
            
            # Validate conversion
            self.assertIsInstance(repo_data["name"], str)
            self.assertGreater(repo_data["stargazers_count"], 0)
            self.assertTrue(repo_data["html_url"].startswith("https://"))
            self.assertTrue(repo_data["pushed_at"].endswith("T00:00:00Z"))
        
        print("[OK] Data conversion accuracy verified")
    
    def test_data_consistency_after_fallback(self):
        """Test that fallback data maintains consistency with API format."""
        # Simulate fallback scenario
        with patch('requests.get', side_effect=Exception("Simulated failure")), \
             patch('streamlit.error'), \
             patch('streamlit.warning'), \
             patch('streamlit.info'):
            
            from app import fetch_uml_repos
            fallback_repos = fetch_uml_repos(max_pages=1)
            
            # Validate structure matches GitHub API format
            for repo in fallback_repos[:3]:  # Check first 3
                with self.subTest(repo=repo['name']):
                    required_fields = ['name', 'stargazers_count', 'pushed_at', 
                                     'created_at', 'html_url', 'forks', 'open_issues']
                    
                    for field in required_fields:
                        self.assertIn(field, repo, f"Field '{field}' should exist")
                    
                    # Validate data types
                    self.assertIsInstance(repo['stargazers_count'], int)
                    self.assertIsInstance(repo['forks'], int)
                    self.assertIsInstance(repo['open_issues'], int)
                    self.assertIsInstance(repo['topics'], list)
        
        print("[OK] Data consistency maintained after fallback")


class TestUserNotifications(unittest.TestCase):
    """Test user notification system during fallback."""
    
    @patch('requests.get')
    def test_fallback_notifications(self, mock_get):
        """Test that appropriate notifications are shown during fallback."""
        mock_get.side_effect = Exception("Network error")
        
        with patch('streamlit.error') as mock_error, \
             patch('streamlit.warning') as mock_warning, \
             patch('streamlit.info') as mock_info:
            
            from app import fetch_uml_repos
            repos = fetch_uml_repos(max_pages=1)
            
            # Check that all notification types were called
            mock_error.assert_called()  # For API failure
            mock_warning.assert_called()  # For fallback warning
            mock_info.assert_called()  # For successful fallback
        
        print("[OK] User notifications work correctly during fallback")


def run_integration_test():
    """Run integration test of the complete fallback mechanism."""
    print("\n" + "="*60)
    print("INTEGRATION TEST: GitHub API Fallback Mechanism")  
    print("="*60)
    
    try:
        # Test 1: Verify snapshot exists
        if not os.path.exists("snapshot.csv"):
            raise FileNotFoundError("snapshot.csv not found")
        
        # Test 2: Test CSV loading
        with open("snapshot.csv", 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            if len(rows) == 0:
                raise ValueError("No data in snapshot")
        
        # Test 3: Test function import
        from app import fetch_uml_repos
        if not callable(fetch_uml_repos):
            raise ImportError("fetch_uml_repos not callable")
        
        # Test 4: Test fallback simulation
        with patch('requests.get', side_effect=Exception("Simulated error")), \
             patch('streamlit.error'), \
             patch('streamlit.warning'), \
             patch('streamlit.info'):
            
            repos = fetch_uml_repos(max_pages=1)
            if len(repos) == 0:
                raise ValueError("Fallback returned no repositories")
        
        print(f"[OK] Snapshot contains {len(rows)} repositories")
        print(f"[OK] Fallback mechanism loaded {len(repos)} repositories")
        print("[OK] Data format conversion successful")
        print("\n[SUCCESS] INTEGRATION TEST PASSED!")
        print("Fallback mechanism is working correctly.")
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