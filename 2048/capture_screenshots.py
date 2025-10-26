"""
Script to capture screenshots of the game at different states.
"""
import pygame
import sys
import os
from _2048 import GameUI, GameState

def capture_screenshot(ui, state_name, state, setup_func=None):
    """Capture a screenshot of a specific game state."""
    ui.state = state
    if setup_func:
        setup_func(ui)
    
    ui.draw()
    pygame.display.flip()
    pygame.time.wait(100)
    
    # Save screenshot
    filename = f'/tmp/2048_screenshot_{state_name}.png'
    pygame.image.save(ui.screen, filename)
    print(f"Screenshot saved: {filename}")
    return filename

def setup_game_in_progress(ui):
    """Setup game with some tiles for screenshot."""
    ui.game.grid = [
        [2, 4, 8, 16],
        [32, 64, 128, 256],
        [512, 1024, 0, 0],
        [2, 4, 0, 0]
    ]
    ui.game.score = 5432
    ui.game.best_score = 8750

def setup_win(ui):
    """Setup winning game state."""
    ui.game.grid = [
        [2048, 1024, 512, 256],
        [128, 64, 32, 16],
        [8, 4, 2, 0],
        [0, 0, 0, 0]
    ]
    ui.game.score = 25432
    ui.game.best_score = 25432

def main():
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    
    pygame.init()
    screen = pygame.display.set_mode((600, 750))
    pygame.display.set_caption("2048 - Deluxe Edition")
    
    ui = GameUI(screen)
    
    # Capture different states
    capture_screenshot(ui, 'menu', GameState.MENU)
    capture_screenshot(ui, 'playing', GameState.PLAYING, setup_game_in_progress)
    capture_screenshot(ui, 'settings', GameState.SETTINGS)
    capture_screenshot(ui, 'win', GameState.WIN, setup_win)
    
    print("\nAll screenshots captured successfully!")
    pygame.quit()

if __name__ == "__main__":
    main()
