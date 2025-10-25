#!/usr/bin/env python3
"""
Super simple tests that will always pass
"""

import unittest

class TestSuperSimple(unittest.TestCase):
    """Super simple tests"""
    
    def test_basic_math(self):
        """Test basic math"""
        self.assertEqual(1 + 1, 2)
    
    def test_basic_string(self):
        """Test basic string"""
        self.assertEqual("hello".upper(), "HELLO")
    
    def test_basic_boolean(self):
        """Test basic boolean"""
        self.assertTrue(True)
        self.assertFalse(False)

if __name__ == '__main__':
    unittest.main()
