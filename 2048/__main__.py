"""
Main entry point for running the 2048 game from the command line.

Usage:
    python -m 2048
    
Or from the repository root:
    python -m 2048
"""

import sys
import os

# Add parent directory to path if running as module
if __package__:
    from .game import main
else:
    # Running directly, add to path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from game import main

if __name__ == "__main__":
    main()
