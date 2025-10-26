# Quick Start Guide - Terminal Execution

## Installation

```bash
# Clone the repository
git clone https://github.com/DMelenberg/python-games.git
cd python-games/2048

# Install dependencies
pip install -r requirements.txt
```

## Running the Game

### Method 1: As a Python Module (Recommended)
From the repository root:
```bash
python -m 2048
```

### Method 2: Using the Run Script
From the 2048 directory:
```bash
python run.py
```

### Method 3: Direct Execution
From the 2048 directory:
```bash
python game.py
```

## Running Tests

```bash
# Run all tests
python -m unittest discover tests -v

# Run specific test
python tests/test_game.py

# Run comprehensive tests
python tests/test_comprehensive.py
```

## Package Installation (Optional)

For system-wide installation:
```bash
cd 2048
pip install -e .  # Editable install for development
# or
pip install .     # Regular install
```

After installation, run from anywhere:
```bash
2048
```

## Quick Test

Verify everything works:
```bash
# Test the game runs
timeout 2 python -m 2048  # Will start and timeout (expected)

# Test the tests pass
python -m unittest discover tests
```

## Controls

- **Arrow Keys**: Move tiles (↑ ↓ ← →)
- **ESC**: Pause/Resume game
- **Mouse**: Navigate menus and click buttons

## Features

✨ Organic, hand-painted artistic style
🎨 Warm color palette with flowing gradients
🔊 6 sound effects (toggleable in settings)
🎯 Complete menu system (Main, Settings, Pause)
📊 Score tracking (current + best)
🎮 Professional UI with rounded corners

Enjoy the game!
