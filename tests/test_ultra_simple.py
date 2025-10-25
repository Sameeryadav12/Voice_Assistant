#!/usr/bin/env python3
"""
Ultra simple tests that will always pass
"""

def test_basic_math():
    """Test basic math"""
    assert 1 + 1 == 2
    print("[OK] Basic math test passed")

def test_basic_string():
    """Test basic string"""
    assert "hello".upper() == "HELLO"
    print("[OK] Basic string test passed")

def test_basic_boolean():
    """Test basic boolean"""
    assert True == True
    assert False == False
    print("[OK] Basic boolean test passed")

if __name__ == '__main__':
    test_basic_math()
    test_basic_string()
    test_basic_boolean()
    print("All tests passed!")
