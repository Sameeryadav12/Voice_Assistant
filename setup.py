#!/usr/bin/env python3
"""
Sigma Voice Assistant - Setup Script
A sophisticated voice-controlled assistant with modern UI and advanced NLP.
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

# Read version
def read_version():
    with open("main_professional_ui.py", "r", encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("__version__"):
                return line.split("=")[1].strip().strip('"').strip("'")
    return "2.0.0"

setup(
    name="sigma-voice-assistant",
    version=read_version(),
    author="Sigma Voice Assistant Team",
    author_email="contact@sigma-voice-assistant.com",
    description="A sophisticated voice-controlled assistant with modern UI and advanced NLP",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/sigma-voice-assistant",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/sigma-voice-assistant/issues",
        "Source": "https://github.com/yourusername/sigma-voice-assistant",
        "Documentation": "https://github.com/yourusername/sigma-voice-assistant/tree/main/docs",
        "Changelog": "https://github.com/yourusername/sigma-voice-assistant/blob/main/CHANGELOG.md",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Topic :: Communications :: Voice",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Desktop Environment :: Window Managers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: X11 Applications",
        "Environment :: Win32 (MS Windows)",
        "Environment :: MacOS X",
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
            "isort>=5.10.0",
            "pre-commit>=2.20.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "sphinx-autodoc-typehints>=1.19.0",
        ],
        "audio": [
            "pyaudio>=0.2.11",
            "webrtcvad>=2.0.10",
            "librosa>=0.10.0",
        ],
        "ml": [
            "scikit-learn>=1.3.0",
            "nltk>=3.8.1",
            "numpy>=1.24.0",
            "scipy>=1.10.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "sigma-voice=main_professional_ui:main",
            "sigma-hybrid=main_hybrid:main",
            "sigma-pushtotalk=main_pushtotalk:main",
            "sigma-original=main:main",
        ],
        "gui_scripts": [
            "sigma-voice-gui=main_professional_ui:main",
        ],
    },
    include_package_data=True,
    package_data={
        "sigma_voice_assistant": [
            "*.md",
            "docs/*.md",
            "tests/*.py",
            "examples/*.py",
        ],
    },
    data_files=[
        ("docs", [
            "docs/USER_GUIDE.md",
            "docs/API_REFERENCE.md",
            "docs/TROUBLESHOOTING.md",
            "docs/PERFORMANCE.md",
            "docs/CONTRIBUTING.md",
        ]),
        ("examples", [
            "examples/main_keyboard.py",
            "examples/run_demo.py",
        ]),
        ("tests", [
            "tests/test_microphone_volume.py",
            "tests/test_speech_recognition.py",
            "tests/test_audio_pipeline.py",
        ]),
    ],
    keywords=[
        "voice-assistant",
        "speech-recognition",
        "nlp",
        "ai",
        "assistant",
        "voice-control",
        "speech-to-text",
        "natural-language-processing",
        "ui",
        "gui",
        "desktop",
        "automation",
        "productivity",
    ],
    platforms=["Windows", "macOS", "Linux"],
    license="MIT",
    zip_safe=False,
    test_suite="tests",
    tests_require=[
        "pytest>=7.0.0",
        "pytest-cov>=4.0.0",
    ],
    cmdclass={},
    options={
        "bdist_wheel": {
            "universal": True,
        },
        "sdist": {
            "formats": ["gztar", "zip"],
        },
    },
)