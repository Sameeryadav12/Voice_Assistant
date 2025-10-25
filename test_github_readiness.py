#!/usr/bin/env python3
"""
GitHub Readiness Test Script
Tests the Jarvis Voice Assistant project for GitHub readiness
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def test_file_exists(file_path, description):
    """Test if a file exists and print result."""
    if os.path.exists(file_path):
        print(f"PASS: {description}: {file_path}")
        return True
    else:
        print(f"FAIL: {description}: {file_path} - MISSING")
        return False

def test_directory_exists(dir_path, description):
    """Test if a directory exists and print result."""
    if os.path.isdir(dir_path):
        print(f"PASS: {description}: {dir_path}")
        return True
    else:
        print(f"FAIL: {description}: {dir_path} - MISSING")
        return False

def test_python_syntax(file_path):
    """Test Python file syntax."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            compile(f.read(), file_path, 'exec')
        print(f"PASS: Python syntax: {file_path}")
        return True
    except SyntaxError as e:
        print(f"FAIL: Python syntax error in {file_path}: {e}")
        return False
    except Exception as e:
        print(f"WARN: Could not check {file_path}: {e}")
        return False

def test_imports():
    """Test if main modules can be imported."""
    try:
        # Test core imports
        sys.path.insert(0, '.')
        from core.skill_manager import SkillManager
        from skills.base_skill import BaseSkill
        from ui.theme_manager import ThemeManager
        print("PASS: Core imports successful")
        return True
    except ImportError as e:
        print(f"FAIL: Import error: {e}")
        return False

def test_requirements():
    """Test if requirements.txt is valid."""
    try:
        with open('requirements.txt', 'r') as f:
            requirements = f.read().strip().split('\n')
        
        valid_requirements = []
        for req in requirements:
            if req.strip() and not req.startswith('#'):
                valid_requirements.append(req)
        
        print(f"PASS: Requirements.txt: {len(valid_requirements)} packages")
        return True
    except Exception as e:
        print(f"FAIL: Requirements.txt error: {e}")
        return False

def test_documentation():
    """Test documentation completeness."""
    docs = [
        'README.md',
        'CONTRIBUTING.md',
        'LICENSE',
        'CHANGELOG.md',
        'docs/API_REFERENCE.md',
        'docs/USER_GUIDE.md',
        'docs/TROUBLESHOOTING.md',
        'docs/PERFORMANCE.md'
    ]
    
    missing_docs = []
    for doc in docs:
        if not os.path.exists(doc):
            missing_docs.append(doc)
    
    if missing_docs:
        print(f"FAIL: Missing documentation: {missing_docs}")
        return False
    else:
        print("PASS: All documentation present")
        return True

def test_project_structure():
    """Test project structure completeness."""
    required_dirs = [
        'audio',
        'core',
        'nlp',
        'skills',
        'ui',
        'tests',
        'docs',
        'examples',
        '.github/workflows'
    ]
    
    missing_dirs = []
    for dir_path in required_dirs:
        if not os.path.isdir(dir_path):
            missing_dirs.append(dir_path)
    
    if missing_dirs:
        print(f"FAIL: Missing directories: {missing_dirs}")
        return False
    else:
        print("PASS: Project structure complete")
        return True

def test_git_config():
    """Test Git configuration."""
    try:
        # Check if .gitignore exists
        if not os.path.exists('.gitignore'):
            print("FAIL: .gitignore missing")
            return False
        
        # Check if git is initialized
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode != 0:
            print("FAIL: Git not initialized")
            return False
        
        print("PASS: Git configuration present")
        return True
    except Exception as e:
        print(f"FAIL: Git configuration error: {e}")
        return False

def test_setup_py():
    """Test setup.py validity."""
    try:
        with open('setup.py', 'r') as f:
            content = f.read()
        
        # Basic checks
        if 'name=' in content and 'version=' in content:
            print("PASS: setup.py appears valid")
            return True
        else:
            print("FAIL: setup.py missing required fields")
            return False
    except Exception as e:
        print(f"FAIL: setup.py error: {e}")
        return False

def main():
    """Main test function."""
    print("Testing Jarvis Voice Assistant GitHub Readiness")
    print("=" * 60)
    
    tests = [
        ("Project Structure", test_project_structure),
        ("Documentation", test_documentation),
        ("Requirements", test_requirements),
        ("Git Configuration", test_git_config),
        ("Setup.py", test_setup_py),
        ("Core Imports", test_imports)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nTesting {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"FAILED: {test_name}")
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("SUCCESS: All tests passed! Project is GitHub ready!")
        return 0
    else:
        print("WARNING: Some tests failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
