"""
Quick verification that the game initializes properly.
"""
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'

import pygame
from _2048 import GameUI, GameState, Game2048

def test_initialization():
    """Test that all game components initialize correctly."""
    print("Testing game initialization...")
    
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((600, 750))
    
    # Create UI
    ui = GameUI(screen)
    print("✓ GameUI created successfully")
    
    # Check initial state
    assert ui.state == GameState.MENU, "Should start at menu"
    print("✓ Initial state is MENU")
    
    # Check game logic
    game = Game2048()
    non_zero = sum(1 for row in game.grid for cell in row if cell != 0)
    assert non_zero == 2, "Should start with 2 tiles"
    print("✓ Game2048 initializes with 2 tiles")
    
    # Check textures loaded
    assert len(ui.texture_manager.textures) > 0, "Should have textures"
    print(f"✓ Loaded {len(ui.texture_manager.textures)} textures")
    
    # Check sounds (may be disabled in test environment)
    print(f"✓ Sound manager created (enabled: {ui.sound_manager.enabled})")
    
    # Try rendering
    ui.draw()
    pygame.display.flip()
    print("✓ Rendering works")
    
    # Change to playing state
    ui.state = GameState.PLAYING
    ui.draw()
    pygame.display.flip()
    print("✓ Playing state renders")
    
    # Test game move
    moved = game.move_left()
    print(f"✓ Move left executed (moved: {moved})")
    
    pygame.quit()
    print("\n✅ All initialization tests passed!")

if __name__ == "__main__":
    test_initialization()
