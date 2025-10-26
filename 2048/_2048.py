import pygame
import random
import sys
import os
from enum import Enum

# Initialize Pygame
pygame.init()
try:
    pygame.mixer.init()
except pygame.error:
    # Audio device not available (common in test environments)
    print("Warning: Audio device not available. Continuing without sound.")

# Screen Configuration
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 750
GRID_SIZE = 4
TILE_SIZE = 120
TILE_MARGIN = 15
BOARD_PADDING = 30
HEADER_HEIGHT = 150

# Colors - Warm, organic palette inspired by natural landscapes
BG_COLOR = (210, 225, 215)  # Soft sage green
BOARD_COLOR = (165, 185, 175)  # Muted teal
TEXT_DARK = (80, 70, 60)  # Warm dark brown
TEXT_LIGHT = (255, 250, 240)  # Warm white
OVERLAY_COLOR = (190, 205, 195, 220)  # Translucent sage
BUTTON_COLOR = (180, 160, 130)  # Warm sandy brown
BUTTON_HOVER_COLOR = (200, 180, 150)  # Lighter sandy brown

# Game States
class GameState(Enum):
    MENU = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4
    WIN = 5
    SETTINGS = 6

class SoundManager:
    """Manages all game sounds with enable/disable functionality."""
    def __init__(self):
        self.enabled = True
        self.sounds = {}
        self.load_sounds()
    
    def load_sounds(self):
        """Load all sound effects."""
        sounds_dir = os.path.join(os.path.dirname(__file__), 'assets', 'sounds')
        try:
            # Check if mixer is initialized
            if not pygame.mixer.get_init():
                print("Warning: Pygame mixer not initialized. Sounds disabled.")
                self.enabled = False
                return
            
            self.sounds['move'] = pygame.mixer.Sound(os.path.join(sounds_dir, 'move.wav'))
            self.sounds['merge'] = pygame.mixer.Sound(os.path.join(sounds_dir, 'merge.wav'))
            self.sounds['win'] = pygame.mixer.Sound(os.path.join(sounds_dir, 'win.wav'))
            self.sounds['lose'] = pygame.mixer.Sound(os.path.join(sounds_dir, 'lose.wav'))
            self.sounds['click'] = pygame.mixer.Sound(os.path.join(sounds_dir, 'click.wav'))
            self.sounds['new_tile'] = pygame.mixer.Sound(os.path.join(sounds_dir, 'new_tile.wav'))
            
            # Set volumes
            for sound in self.sounds.values():
                sound.set_volume(0.3)
        except Exception as e:
            print(f"Warning: Could not load sounds: {e}")
            self.enabled = False
    
    def play(self, sound_name):
        """Play a sound effect if enabled."""
        if self.enabled and sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def toggle(self):
        """Toggle sound on/off."""
        self.enabled = not self.enabled
        return self.enabled

class TextureManager:
    """Manages tile textures."""
    def __init__(self):
        self.textures = {}
        self.load_textures()
    
    def load_textures(self):
        """Load all tile textures."""
        textures_dir = os.path.join(os.path.dirname(__file__), 'assets', 'textures')
        tile_values = [0, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]
        
        for value in tile_values:
            try:
                texture_path = os.path.join(textures_dir, f'tile_{value}.png')
                texture = pygame.image.load(texture_path)
                # Scale to tile size
                self.textures[value] = pygame.transform.smoothscale(texture, (TILE_SIZE, TILE_SIZE))
            except Exception as e:
                print(f"Warning: Could not load texture for {value}: {e}")
                # Create fallback colored rectangle
                self.textures[value] = self.create_fallback_tile(value)
        
        # Load background
        try:
            bg_path = os.path.join(textures_dir, 'background.png')
            self.background = pygame.image.load(bg_path)
            self.background = pygame.transform.smoothscale(
                self.background,
                (TILE_SIZE * GRID_SIZE + TILE_MARGIN * (GRID_SIZE + 1),
                 TILE_SIZE * GRID_SIZE + TILE_MARGIN * (GRID_SIZE + 1))
            )
        except Exception as e:
            print(f"Warning: Could not load background: {e}")
            self.background = None
    
    def create_fallback_tile(self, value):
        """Create a simple colored tile as fallback."""
        colors = {
            0: (204, 192, 179), 2: (238, 228, 218), 4: (237, 224, 200),
            8: (242, 177, 121), 16: (245, 149, 99), 32: (246, 124, 95),
            64: (246, 94, 59), 128: (237, 207, 114), 256: (237, 204, 97),
            512: (237, 200, 80), 1024: (237, 197, 63), 2048: (237, 194, 46),
        }
        surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
        surface.fill(colors.get(value, (60, 58, 50)))
        return surface
    
    def get_texture(self, value):
        """Get texture for a tile value."""
        return self.textures.get(value, self.textures.get(0))

class Button:
    """Simple button class."""
    def __init__(self, x, y, width, height, text, font_size=32):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.hovered = False
    
    def draw(self, screen):
        """Draw the button."""
        color = BUTTON_HOVER_COLOR if self.hovered else BUTTON_COLOR
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, TEXT_DARK, self.rect, 2, border_radius=8)
        
        text_surface = self.font.render(self.text, True, TEXT_LIGHT)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        """Handle mouse events."""
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class Game2048:
    """Main game logic class."""
    def __init__(self):
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.score = 0
        self.best_score = 0
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty_cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if self.grid[r][c] == 0]
        if empty_cells:
            r, c = random.choice(empty_cells)
            self.grid[r][c] = 4 if random.random() > 0.9 else 2
            return True
        return False

    def move_left(self):
        moved = False
        for row in self.grid:
            compressed, score_increase = self.compress(row)
            if row != compressed:
                moved = True
            row[:] = compressed
            self.score += score_increase
        return moved

    def move_right(self):
        moved = False
        for row in self.grid:
            reversed_row = row[::-1]
            compressed, score_increase = self.compress(reversed_row)
            if row != compressed[::-1]:
                moved = True
            row[:] = compressed[::-1]
            self.score += score_increase
        return moved

    def move_up(self):
        moved = False
        for col in range(GRID_SIZE):
            column = [self.grid[row][col] for row in range(GRID_SIZE)]
            compressed, score_increase = self.compress(column)
            if [self.grid[row][col] for row in range(GRID_SIZE)] != compressed:
                moved = True
            for row in range(GRID_SIZE):
                self.grid[row][col] = compressed[row]
            self.score += score_increase
        return moved

    def move_down(self):
        moved = False
        for col in range(GRID_SIZE):
            column = [self.grid[row][col] for row in range(GRID_SIZE)][::-1]
            compressed, score_increase = self.compress(column)
            if [self.grid[row][col] for row in range(GRID_SIZE)] != compressed[::-1]:
                moved = True
            for row in range(GRID_SIZE):
                self.grid[row][col] = compressed[::-1][row]
            self.score += score_increase
        return moved

    def compress(self, row):
        new_row = [value for value in row if value != 0]
        score_increase = 0
        merged = False
        for i in range(len(new_row) - 1):
            if new_row[i] == new_row[i + 1] and new_row[i] != 0:
                new_row[i] *= 2
                score_increase += new_row[i]
                new_row[i + 1] = 0
                merged = True
        new_row = [value for value in new_row if value != 0]
        return new_row + [0] * (GRID_SIZE - len(new_row)), score_increase

    def check_game_over(self):
        if any(2048 in row for row in self.grid):
            return "WIN"
        if any(0 in row for row in self.grid):
            return None
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE - 1):
                if self.grid[r][c] == self.grid[r][c + 1] or self.grid[c][r] == self.grid[c + 1][r]:
                    return None
        return "LOSE"

    def reset(self):
        if self.score > self.best_score:
            self.best_score = self.score
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()

class GameUI:
    """Handles all UI rendering and interactions."""
    def __init__(self, screen):
        self.screen = screen
        self.sound_manager = SoundManager()
        self.texture_manager = TextureManager()
        self.game = Game2048()
        self.state = GameState.MENU
        
        # Fonts
        self.title_font = pygame.font.Font(None, 80)
        self.large_font = pygame.font.Font(None, 48)
        self.medium_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 28)
        
        # Buttons
        self.create_buttons()
    
    def create_buttons(self):
        """Create all UI buttons."""
        center_x = SCREEN_WIDTH // 2
        
        # Menu buttons
        self.menu_play_btn = Button(center_x - 100, 300, 200, 60, "Play", 40)
        self.menu_settings_btn = Button(center_x - 100, 380, 200, 60, "Settings", 40)
        self.menu_quit_btn = Button(center_x - 100, 460, 200, 60, "Quit", 40)
        
        # Pause buttons
        self.pause_resume_btn = Button(center_x - 100, 300, 200, 60, "Resume", 40)
        self.pause_restart_btn = Button(center_x - 100, 380, 200, 60, "Restart", 40)
        self.pause_menu_btn = Button(center_x - 100, 460, 200, 60, "Main Menu", 40)
        
        # Game over buttons
        self.gameover_restart_btn = Button(center_x - 100, 400, 200, 60, "Try Again", 40)
        self.gameover_menu_btn = Button(center_x - 100, 480, 200, 60, "Main Menu", 40)
        
        # Settings buttons
        self.settings_sound_btn = Button(center_x - 100, 300, 200, 60, "Sound: ON", 36)
        self.settings_back_btn = Button(center_x - 100, 400, 200, 60, "Back", 40)
    
    def draw_header(self):
        """Draw the game header with score."""
        # Title
        title_text = self.title_font.render("2048", True, TEXT_DARK)
        self.screen.blit(title_text, (30, 30))
        
        # Score boxes
        score_box_width = 120
        score_box_height = 70
        score_x = SCREEN_WIDTH - 260
        best_x = SCREEN_WIDTH - 130
        
        # Current score
        pygame.draw.rect(self.screen, BOARD_COLOR, 
                        (score_x, 40, score_box_width, score_box_height), border_radius=5)
        score_label = self.small_font.render("SCORE", True, TEXT_LIGHT)
        score_value = self.medium_font.render(str(self.game.score), True, TEXT_LIGHT)
        self.screen.blit(score_label, (score_x + 35, 45))
        self.screen.blit(score_value, (score_x + score_box_width // 2 - score_value.get_width() // 2, 70))
        
        # Best score
        pygame.draw.rect(self.screen, BOARD_COLOR, 
                        (best_x, 40, score_box_width, score_box_height), border_radius=5)
        best_label = self.small_font.render("BEST", True, TEXT_LIGHT)
        best_value = self.medium_font.render(str(self.game.best_score), True, TEXT_LIGHT)
        self.screen.blit(best_label, (best_x + 40, 45))
        self.screen.blit(best_value, (best_x + score_box_width // 2 - best_value.get_width() // 2, 70))
    
    def draw_board(self):
        """Draw the game board with tiles."""
        board_x = BOARD_PADDING
        board_y = HEADER_HEIGHT
        board_width = TILE_SIZE * GRID_SIZE + TILE_MARGIN * (GRID_SIZE + 1)
        board_height = board_width
        
        # Draw board background
        if self.texture_manager.background:
            self.screen.blit(self.texture_manager.background, (board_x, board_y))
        else:
            pygame.draw.rect(self.screen, BOARD_COLOR, 
                           (board_x, board_y, board_width, board_height), border_radius=10)
        
        # Draw tiles
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                value = self.game.grid[r][c]
                x = board_x + c * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN
                y = board_y + r * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN
                
                # Draw tile texture
                texture = self.texture_manager.get_texture(value)
                self.screen.blit(texture, (x, y))
                
                # Draw number with warmer colors
                if value != 0:
                    font_size = 60 if value < 100 else (50 if value < 1000 else 40)
                    font = pygame.font.Font(None, font_size)
                    # Use warm brown for lighter tiles, warm white for darker
                    text_color = (90, 75, 60) if value <= 4 else (255, 250, 235)
                    text = font.render(str(value), True, text_color)
                    text_rect = text.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
                    self.screen.blit(text, text_rect)
    
    def draw_menu(self):
        """Draw main menu."""
        self.screen.fill(BG_COLOR)
        
        # Title
        title = self.title_font.render("2048", True, TEXT_DARK)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)
        
        subtitle = self.small_font.render("Join tiles to reach 2048!", True, TEXT_DARK)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 220))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Buttons
        self.menu_play_btn.draw(self.screen)
        self.menu_settings_btn.draw(self.screen)
        self.menu_quit_btn.draw(self.screen)
    
    def draw_settings(self):
        """Draw settings menu."""
        self.screen.fill(BG_COLOR)
        
        # Title
        title = self.large_font.render("Settings", True, TEXT_DARK)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)
        
        # Update sound button text
        sound_status = "ON" if self.sound_manager.enabled else "OFF"
        self.settings_sound_btn.text = f"Sound: {sound_status}"
        
        # Buttons
        self.settings_sound_btn.draw(self.screen)
        self.settings_back_btn.draw(self.screen)
    
    def draw_pause_menu(self):
        """Draw pause overlay."""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BG_COLOR)
        self.screen.blit(overlay, (0, 0))
        
        # Paused text
        text = self.large_font.render("PAUSED", True, TEXT_DARK)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(text, text_rect)
        
        # Buttons
        self.pause_resume_btn.draw(self.screen)
        self.pause_restart_btn.draw(self.screen)
        self.pause_menu_btn.draw(self.screen)
    
    def draw_game_over(self, won=False):
        """Draw game over screen."""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(220)
        overlay.fill(BG_COLOR)
        self.screen.blit(overlay, (0, 0))
        
        # Game over text with warmer, organic colors
        if won:
            text = self.large_font.render("YOU WIN!", True, (120, 160, 90))  # Warm green
            subtitle = self.medium_font.render("You reached 2048!", True, TEXT_DARK)
        else:
            text = self.large_font.render("GAME OVER", True, (180, 120, 90))  # Warm orange-brown
            subtitle = self.medium_font.render("No more moves!", True, TEXT_DARK)
        
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(text, text_rect)
        
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 280))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Score
        score_text = self.medium_font.render(f"Score: {self.game.score}", True, TEXT_DARK)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 340))
        self.screen.blit(score_text, score_rect)
        
        # Buttons
        self.gameover_restart_btn.draw(self.screen)
        self.gameover_menu_btn.draw(self.screen)
    
    def draw_playing(self):
        """Draw the main game screen."""
        self.screen.fill(BG_COLOR)
        self.draw_header()
        self.draw_board()
        
        # Instructions
        instructions = self.small_font.render("Use arrow keys to play • ESC to pause", True, TEXT_DARK)
        inst_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        self.screen.blit(instructions, inst_rect)
    
    def handle_menu_events(self, event):
        """Handle menu events."""
        if self.menu_play_btn.handle_event(event):
            self.sound_manager.play('click')
            self.state = GameState.PLAYING
            self.game.reset()
        elif self.menu_settings_btn.handle_event(event):
            self.sound_manager.play('click')
            self.state = GameState.SETTINGS
        elif self.menu_quit_btn.handle_event(event):
            return False
        return True
    
    def handle_settings_events(self, event):
        """Handle settings events."""
        if self.settings_sound_btn.handle_event(event):
            self.sound_manager.toggle()
            self.sound_manager.play('click')
        elif self.settings_back_btn.handle_event(event):
            self.sound_manager.play('click')
            self.state = GameState.MENU
        return True
    
    def handle_pause_events(self, event):
        """Handle pause menu events."""
        if self.pause_resume_btn.handle_event(event):
            self.sound_manager.play('click')
            self.state = GameState.PLAYING
        elif self.pause_restart_btn.handle_event(event):
            self.sound_manager.play('click')
            self.game.reset()
            self.state = GameState.PLAYING
        elif self.pause_menu_btn.handle_event(event):
            self.sound_manager.play('click')
            self.state = GameState.MENU
        return True
    
    def handle_gameover_events(self, event):
        """Handle game over events."""
        if self.gameover_restart_btn.handle_event(event):
            self.sound_manager.play('click')
            self.game.reset()
            self.state = GameState.PLAYING
        elif self.gameover_menu_btn.handle_event(event):
            self.sound_manager.play('click')
            self.state = GameState.MENU
        return True
    
    def handle_playing_events(self, event):
        """Handle game playing events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.sound_manager.play('click')
                self.state = GameState.PAUSED
                return True
            
            moved = False
            merged = False
            
            if event.key == pygame.K_LEFT:
                moved = self.game.move_left()
            elif event.key == pygame.K_RIGHT:
                moved = self.game.move_right()
            elif event.key == pygame.K_UP:
                moved = self.game.move_up()
            elif event.key == pygame.K_DOWN:
                moved = self.game.move_down()
            
            if moved:
                self.sound_manager.play('move')
                # Check if any tiles merged by comparing old and new scores
                old_score = self.game.score
                tile_added = self.game.add_new_tile()
                
                if self.game.score > old_score:
                    self.sound_manager.play('merge')
                
                if tile_added:
                    self.sound_manager.play('new_tile')
                
                # Check game state
                game_state = self.game.check_game_over()
                if game_state == "WIN":
                    self.sound_manager.play('win')
                    self.state = GameState.WIN
                elif game_state == "LOSE":
                    self.sound_manager.play('lose')
                    self.state = GameState.GAME_OVER
        
        return True
    
    def handle_events(self):
        """Main event handler."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if self.state == GameState.MENU:
                if not self.handle_menu_events(event):
                    return False
            elif self.state == GameState.SETTINGS:
                self.handle_settings_events(event)
            elif self.state == GameState.PLAYING:
                self.handle_playing_events(event)
            elif self.state == GameState.PAUSED:
                self.handle_pause_events(event)
            elif self.state in (GameState.GAME_OVER, GameState.WIN):
                self.handle_gameover_events(event)
        
        return True
    
    def draw(self):
        """Main draw method."""
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.SETTINGS:
            self.draw_settings()
        elif self.state == GameState.PLAYING:
            self.draw_playing()
        elif self.state == GameState.PAUSED:
            self.draw_playing()
            self.draw_pause_menu()
        elif self.state == GameState.GAME_OVER:
            self.draw_playing()
            self.draw_game_over(won=False)
        elif self.state == GameState.WIN:
            self.draw_playing()
            self.draw_game_over(won=True)

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("2048 - Deluxe Edition")
    clock = pygame.time.Clock()
    
    ui = GameUI(screen)
    
    running = True
    while running:
        running = ui.handle_events()
        ui.draw()
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
