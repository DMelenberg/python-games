"""
Setup script for 2048 Game - Deluxe Edition
"""

from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="2048-deluxe",
    version="2.0.0",
    author="2048 Game Team",
    description="A beautifully redesigned 2048 game with organic hand-painted textures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DMelenberg/python-games",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Games/Entertainment :: Puzzle Games",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "2048=2048.game:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["assets/sounds/*.wav", "assets/textures/*.png"],
    },
)
