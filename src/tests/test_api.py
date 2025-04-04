import requests
import unittest

class TestPlagiarismAPI(unittest.TestCase):
    API_URL = "http://localhost:8000/check"
    
    def test_positive_case(self):
        """Test with common code snippet that should match"""
        test_code = "import tensorflow as tf\nprint('Hello TF')"
        response = requests.post(self.API_URL, json={"code": test_code})
        self.assertEqual(response.status_code, 200)
        print("Positive test result:", response.json())

    def test_negative_case(self):
        """Test with unique code that shouldn't match"""
        test_code = "def unique_function(): return 42"
        response = requests.post(self.API_URL, json={"code": test_code})
        self.assertEqual(response.status_code, 200)
        print("Negative test result:", response.json())

    def test_api_response_structure(self):
        test_code = "def example(): pass"
        response = requests.post(self.API_URL, json={"code": test_code})
        self.assertIn("is_plagiarism", response.json())
        self.assertIn("references", response.json())

    def test_edge_cases(self):
        """Test empty code and large input"""
        # Empty code
        response = requests.post(self.API_URL, json={"code": ""})
        self.assertEqual(response.status_code, 400)
    
        # Large code (50k characters)
        large_code = "import tensorflow as tf\n" * 10000
        response = requests.post(self.API_URL, json={"code": large_code})
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()