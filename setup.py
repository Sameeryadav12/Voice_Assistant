#!/usr/bin/env python3
"""
Jarvis Voice Assistant - Professional Edition
Setup script for package distribution
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="jarvis-voice-assistant",
    version="1.0.0",
    author="Jarvis Voice Assistant Team",
    author_email="team@jarvis-assistant.com",
    description="An intelligent, voice-controlled personal assistant with 16+ advanced skills",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/jarvis-voice-assistant",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/jarvis-voice-assistant/issues",
        "Source": "https://github.com/yourusername/jarvis-voice-assistant",
        "Documentation": "https://github.com/yourusername/jarvis-voice-assistant/tree/main/docs",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Communications :: Voice",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
            "pre-commit>=2.20.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "jarvis=main_professional_ui:main",
            "jarvis-basic=main:main",
            "jarvis-push=main_pushtotalk:main",
            "jarvis-hybrid=main_hybrid:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.ini", "*.bat"],
    },
    keywords="voice assistant, speech recognition, AI, automation, productivity, jarvis",
    zip_safe=False,
)