#!/usr/bin/env python3
"""
Convenient script to run the 2048 game.
Usage: ./run.py or python run.py
"""

import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game import main

if __name__ == "__main__":
    main()
