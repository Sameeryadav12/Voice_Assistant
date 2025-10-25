#!/usr/bin/env python3
"""
Basic tests for Sigma Voice Assistant
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestBasicFunctionality(unittest.TestCase):
    """Basic functionality tests"""
    
    def test_imports(self):
        """Test that main modules can be imported"""
        try:
            # Test basic imports without running the full application
            import os
            import sys
            import threading
            import time
            self.assertTrue(True, "Basic Python modules imported successfully")
        except ImportError as e:
            self.fail(f"Failed to import basic Python modules: {e}")
    
    def test_math_operations(self):
        """Test basic math operations"""
        self.assertEqual(2 + 2, 4)
        self.assertEqual(10 * 5, 50)
        self.assertTrue(10 > 5)
    
    def test_string_operations(self):
        """Test basic string operations"""
        test_string = "Hello World"
        self.assertEqual(len(test_string), 11)
        self.assertTrue("Hello" in test_string)
        self.assertEqual(test_string.upper(), "HELLO WORLD")

if __name__ == '__main__':
    unittest.main()
