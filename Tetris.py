import pygame
import random
import json
import os
import math
from enum import Enum
import numpy as np

# Initialize pygame
pygame.init()

# Try to initialize sound - if it fails, continue without sound
try:
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    SOUND_AVAILABLE = True
except:
    SOUND_AVAILABLE = False
    print("Sound initialization failed - continuing without sound.")

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 800
SIDE_PANEL_WIDTH = 250
BLOCK_SIZE = 40

# Grid dimensions
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# Enhanced color palette with gradients
TETRIS_COLORS = [
    BLACK,              # 0: Empty
    (0, 255, 255),      # 1: I piece - Cyan
    (0, 100, 255),      # 2: J piece - Blue
    (255, 165, 0),      # 3: L piece - Orange
    (255, 255, 0),      # 4: O piece - Yellow
    (0, 255, 100),      # 5: S piece - Green
    (160, 32, 240),     # 6: T piece - Purple
    (255, 50, 50)       # 7: Z piece - Red
]

# Particle system colors
PARTICLE_COLORS = [
    (255, 255, 255), (255, 200, 0), (255, 100, 100),
    (100, 255, 100), (100, 100, 255), (255, 0, 255)
]

# Tetrimino shapes with official Tetris piece names
SHAPES = {
    'I': {'shape': [[1, 1, 1, 1]], 'color': 1},
    'O': {'shape': [[1, 1], [1, 1]], 'color': 4},
    'T': {'shape': [[0, 1, 0], [1, 1, 1]], 'color': 6},
    'S': {'shape': [[0, 1, 1], [1, 1, 0]], 'color': 5},
    'Z': {'shape': [[1, 1, 0], [0, 1, 1]], 'color': 7},
    'J': {'shape': [[1, 0, 0], [1, 1, 1]], 'color': 2},
    'L': {'shape': [[0, 0, 1], [1, 1, 1]], 'color': 3}
}

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-5, -1)
        self.color = color
        self.life = 60
        self.max_life = 60
        self.size = random.uniform(2, 4)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1  # gravity
        self.life -= 1
        return self.life > 0

    def draw(self, surface):
        alpha = int(255 * (self.life / self.max_life))
        size = int(self.size * (self.life / self.max_life))
        if size > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), size)

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.music_enabled = True
        self.sfx_enabled = SOUND_AVAILABLE
        if SOUND_AVAILABLE:
            self.create_sounds()

    def create_sounds(self):
        """Create simple sound effects using pygame.sndarray"""
        if not SOUND_AVAILABLE:
            return
        try:
            # Create simple beep sounds
            sample_rate = 22050
            duration = 0.1

            # Move sound
            freq = 440
            frames = int(duration * sample_rate)
            arr = []
            for i in range(frames):
                wave = int(4096 * math.sin(2 * math.pi * freq * i / sample_rate))
                arr.append([wave, wave])
            sound = pygame.sndarray.make_sound(np.array(arr, dtype=np.int16))
            self.sounds['move'] = sound

            # Rotate sound
            freq = 660
            frames = int(duration * sample_rate)
            arr = []
            for i in range(frames):
                wave = int(2048 * math.sin(2 * math.pi * freq * i / sample_rate))
                arr.append([wave, wave])
            sound = pygame.sndarray.make_sound(np.array(arr, dtype=np.int16))
            self.sounds['rotate'] = sound

            # Line clear sound
            duration = 0.3
            frames = int(duration * sample_rate)
            arr = []
            for i in range(frames):
                freq = 800 + (i / frames) * 400
                wave = int(3000 * math.sin(2 * math.pi * freq * i / sample_rate) * (1 - i/frames))
                arr.append([wave, wave])
            sound = pygame.sndarray.make_sound(np.array(arr, dtype=np.int16))
            self.sounds['line_clear'] = sound

            # Tetris sound (4 lines)
            duration = 0.5
            frames = int(duration * sample_rate)
            arr = []
            for i in range(frames):
                freq = 440 + (i / frames) * 880
                wave = int(4000 * math.sin(2 * math.pi * freq * i / sample_rate))
                arr.append([wave, wave])
            sound = pygame.sndarray.make_sound(np.array(arr, dtype=np.int16))
            self.sounds['tetris'] = sound

            # Drop sound
            duration = 0.05
            freq = 200
            frames = int(duration * sample_rate)
            arr = []
            for i in range(frames):
                wave = int(2000 * math.sin(2 * math.pi * freq * i / sample_rate))
                arr.append([wave, wave])
            sound = pygame.sndarray.make_sound(np.array(arr, dtype=np.int16))
            self.sounds['drop'] = sound

        except ImportError:
            print("NumPy not installed - sounds disabled. Run: pip install numpy")
            self.sfx_enabled = False
        except Exception as e:
            print(f"Could not create sounds: {e}")
            self.sfx_enabled = False

    def play_sound(self, sound_name):
        if self.sfx_enabled and sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except:
                pass

class Tetrimino:
    def __init__(self, piece_type=None):
        if piece_type is None:
            piece_type = random.choice(list(SHAPES.keys()))
        self.piece_type = piece_type
        self.shape = [row[:] for row in SHAPES[piece_type]['shape']]
        self.color = SHAPES[piece_type]['color']
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0
        self.rotation_state = 0

    def rotate(self):
        # Create rotated version
        rotated = [list(row) for row in zip(*self.shape[::-1])]
        return rotated

    def get_ghost_y(self, grid):
        """Calculate where the piece would land if dropped"""
        ghost_y = self.y
        while self._valid_position(self.x, ghost_y + 1, self.shape, grid):
            ghost_y += 1
        return ghost_y

    def _valid_position(self, x, y, shape, grid):
        for dy, row in enumerate(shape):
            for dx, value in enumerate(row):
                if value:
                    new_x, new_y = x + dx, y + dy
                    if (new_x < 0 or new_x >= GRID_WIDTH or 
                        new_y >= GRID_HEIGHT or
                        (new_y >= 0 and grid[new_y][new_x])):
                        return False
        return True

class TetrisGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_PANEL_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("TetriX")
        self.clock = pygame.time.Clock()

        # Fonts
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)

        # Sound manager
        self.sound_manager = SoundManager()

        # Particle system
        self.particles = []

        # Game state
        self.state = GameState.MENU
        self.reset_game()

        # Timing
        self.drop_time = 0
        self.drop_speed = 500

        # Animation and effects
        self.line_clear_animation = 0
        self.line_clear_rows = []
        self.screen_shake = 0
        self.flash_effect = 0

        # Performance tracking
        self.total_pieces = 0
        self.start_time = pygame.time.get_ticks()

        # High scores
        self.high_scores = self.load_high_scores()

    def reset_game(self):
        """Reset all game variables"""
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.locked_positions = {}
        self.current_piece = None
        self.next_pieces = []
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.combo = 0
        self.hold_piece = None
        self.can_hold = True
        self.piece_bag = []
        self.stats = {piece: 0 for piece in SHAPES.keys()}
        self.total_pieces = 0
        self.start_time = pygame.time.get_ticks()
        self.generate_next_pieces()

    def refill_bag(self):
        """Refill the piece bag with one of each piece type"""
        self.piece_bag = list(SHAPES.keys())
        random.shuffle(self.piece_bag)

    def get_next_piece(self):
        """Get the next piece from the bag"""
        if not self.piece_bag:
            self.refill_bag()
        return self.piece_bag.pop()

    def generate_next_pieces(self):
        """Generate current and next pieces"""
        if not self.current_piece:
            self.current_piece = Tetrimino(self.get_next_piece())
        while len(self.next_pieces) < 3:
            piece_type = self.get_next_piece()
            self.next_pieces.append(Tetrimino(piece_type))

    def calculate_drop_speed(self):
        """Calculate drop speed based on level"""
        return max(50, 500 - (self.level - 1) * 50)

    def move_piece(self, dx, dy, rotate=False):
        """Move or rotate the current piece if valid"""
        if not self.current_piece or self.state != GameState.PLAYING:
            return False

        old_shape = self.current_piece.shape
        if rotate:
            self.current_piece.shape = self.current_piece.rotate()

        self.current_piece.x += dx
        self.current_piece.y += dy

        if not self.current_piece._valid_position(
            self.current_piece.x, self.current_piece.y,
            self.current_piece.shape, self.grid):
            # Revert changes
            self.current_piece.x -= dx
            self.current_piece.y -= dy
            if rotate:
                self.current_piece.shape = old_shape
            return False

        # Play sound effects
        if rotate:
            self.sound_manager.play_sound('rotate')
        elif dx != 0 or dy != 0:
            self.sound_manager.play_sound('move')

        return True

    def hard_drop(self):
        """Drop piece to the bottom"""
        if not self.current_piece:
            return

        drop_distance = 0
        while self.move_piece(0, 1):
            drop_distance += 1

        self.score += drop_distance * 2
        self.lock_piece()

    def hold_current_piece(self):
        """Hold the current piece"""
        if not self.can_hold or not self.current_piece:
            return

        if self.hold_piece is None:
            self.hold_piece = Tetrimino(self.current_piece.piece_type)
            self.spawn_next_piece()
        else:
            # Swap current and hold pieces
            temp_type = self.current_piece.piece_type
            self.current_piece = Tetrimino(self.hold_piece.piece_type)
            self.hold_piece = Tetrimino(temp_type)

        self.can_hold = False

    def spawn_next_piece(self):
        """Spawn the next piece"""
        self.current_piece = self.next_pieces.pop(0)
        self.generate_next_pieces()
        self.can_hold = True
        self.total_pieces += 1

        # Check for game over
        if not self.current_piece._valid_position(
            self.current_piece.x, self.current_piece.y,
            self.current_piece.shape, self.grid):
            self.state = GameState.GAME_OVER

    def lock_piece(self):
        """Lock the current piece in place"""
        if not self.current_piece:
            return

        # Add lock particles
        for y, row in enumerate(self.current_piece.shape):
            for x, value in enumerate(row):
                if value:
                    screen_x = (self.current_piece.x + x) * BLOCK_SIZE + BLOCK_SIZE // 2
                    screen_y = (self.current_piece.y + y) * BLOCK_SIZE + BLOCK_SIZE // 2
                    self.add_particles(screen_x, screen_y, 3)

        self.sound_manager.play_sound('drop')

        # Add piece to grid
        for y, row in enumerate(self.current_piece.shape):
            for x, value in enumerate(row):
                if value:
                    grid_x = self.current_piece.x + x
                    grid_y = self.current_piece.y + y
                    if 0 <= grid_y < GRID_HEIGHT:
                        self.grid[grid_y][grid_x] = self.current_piece.color
                        self.locked_positions[(grid_x, grid_y)] = self.current_piece.color

        # Update statistics
        self.stats[self.current_piece.piece_type] += 1

        # Clear lines and calculate score
        lines_cleared = self.clear_lines()
        self.calculate_score(lines_cleared)

        # Spawn next piece
        self.spawn_next_piece()

    def clear_lines(self):
        """Clear completed lines and return number cleared"""
        lines_to_clear = []
        for y in range(GRID_HEIGHT):
            if all(self.grid[y][x] != 0 for x in range(GRID_WIDTH)):
                lines_to_clear.append(y)

        if lines_to_clear:
            self.create_line_clear_effect(lines_to_clear)

            # Play appropriate sound
            if len(lines_to_clear) == 4:
                self.sound_manager.play_sound('tetris')
                self.screen_shake = 8
            else:
                self.sound_manager.play_sound('line_clear')
                self.screen_shake = 4

            # Remove cleared lines
            for y in sorted(lines_to_clear, reverse=True):
                del self.grid[y]
                self.grid.insert(0, [0] * GRID_WIDTH)

            # Update locked positions
            new_locked = {}
            for (x, py), color in self.locked_positions.items():
                lines_below = sum(1 for line_y in lines_to_clear if line_y > py)
                new_y = py + lines_below
                if new_y < GRID_HEIGHT:
                    new_locked[(x, new_y)] = color
            self.locked_positions = new_locked

        return len(lines_to_clear)

    def calculate_score(self, lines_cleared):
        """Calculate score based on lines cleared"""
        if lines_cleared == 0:
            self.combo = 0
            return

        # Base score for lines
        line_scores = {1: 100, 2: 300, 3: 500, 4: 800}  # Tetris scoring
        base_score = line_scores.get(lines_cleared, 0) * self.level

        # Combo bonus
        combo_bonus = 50 * self.combo * self.level if self.combo > 0 else 0

        self.score += base_score + combo_bonus
        self.lines_cleared += lines_cleared
        self.combo += 1

        # Level progression
        new_level = (self.lines_cleared // 10) + 1
        if new_level > self.level:
            self.level = new_level
            self.drop_speed = self.calculate_drop_speed()

    def add_particles(self, x, y, count=10):
        """Add particles for visual effects"""
        for _ in range(count):
            color = random.choice(PARTICLE_COLORS)
            self.particles.append(Particle(x, y, color))

    def update_particles(self):
        """Update all particles"""
        self.particles = [p for p in self.particles if p.update()]

    def draw_particles(self):
        """Draw all particles"""
        for particle in self.particles:
            particle.draw(self.screen)

    def create_line_clear_effect(self, rows):
        """Create visual effect for line clearing"""
        self.line_clear_animation = 30
        self.line_clear_rows = rows
        self.flash_effect = 10

        # Add particles for each cleared line
        for row in rows:
            for x in range(GRID_WIDTH):
                screen_x = x * BLOCK_SIZE + BLOCK_SIZE // 2
                screen_y = row * BLOCK_SIZE + BLOCK_SIZE // 2
                self.add_particles(screen_x, screen_y, 5)

    def draw_enhanced_block(self, x, y, color, alpha=255, glow=False):
        """Draw a block with enhanced visual effects"""
        rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)

        # Glow effect for special pieces
        if glow:
            glow_surface = pygame.Surface((BLOCK_SIZE + 4, BLOCK_SIZE + 4), pygame.SRCALPHA)
            glow_color = (*TETRIS_COLORS[color][:3], 50)
            pygame.draw.rect(glow_surface, glow_color, (0, 0, BLOCK_SIZE + 4, BLOCK_SIZE + 4))
            self.screen.blit(glow_surface, (x - 2, y - 2))

        # Main block color with alpha
        block_surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)

        # Add gradient effect
        for i in range(BLOCK_SIZE):
            gradient_alpha = int(alpha * (0.7 + 0.3 * (1 - i / BLOCK_SIZE)))
            gradient_color = (*TETRIS_COLORS[color][:3], gradient_alpha)
            pygame.draw.rect(block_surface, gradient_color, (0, i, BLOCK_SIZE - i // 2, 1))

        # Draw the main block
        self.screen.blit(block_surface, rect)

        # Enhanced border
        border_color = tuple(min(255, c + 50) for c in TETRIS_COLORS[color][:3])
        pygame.draw.rect(self.screen, border_color, rect, 2)

        # Inner highlight
        highlight_rect = pygame.Rect(x + 2, y + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4)
        highlight_color = tuple(min(255, c + 80) for c in TETRIS_COLORS[color][:3])
        pygame.draw.rect(self.screen, highlight_color, highlight_rect, 1)

    def draw_grid(self):
        """Enhanced grid drawing with effects"""
        # Screen shake effect
        shake_x = shake_y = 0
        if self.screen_shake > 0:
            shake_x = random.randint(-self.screen_shake, self.screen_shake)
            shake_y = random.randint(-self.screen_shake, self.screen_shake)
            self.screen_shake -= 1

        # Background with subtle pattern
        self.screen.fill(BLACK)

        # Draw background grid pattern
        for x in range(0, SCREEN_WIDTH + 1, BLOCK_SIZE):
            pygame.draw.line(self.screen, (20, 20, 20),
                           (x + shake_x, 0 + shake_y),
                           (x + shake_x, SCREEN_HEIGHT + shake_y))
        for y in range(0, SCREEN_HEIGHT + 1, BLOCK_SIZE):
            pygame.draw.line(self.screen, (20, 20, 20),
                           (0 + shake_x, y + shake_y),
                           (SCREEN_WIDTH + shake_x, y + shake_y))

        # Flash effect
        if self.flash_effect > 0:
            flash_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            flash_alpha = int(50 * (self.flash_effect / 10))
            flash_surface.fill((255, 255, 255, flash_alpha))
            self.screen.blit(flash_surface, (shake_x, shake_y))
            self.flash_effect -= 1

        # Draw locked pieces with line clear animation
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x] != 0:
                    screen_x = x * BLOCK_SIZE + shake_x
                    screen_y = y * BLOCK_SIZE + shake_y

                    # Line clear animation
                    alpha = 255
                    if y in self.line_clear_rows and self.line_clear_animation > 0:
                        alpha = int(255 * (self.line_clear_animation / 30))
                        if self.line_clear_animation % 6 < 3:
                            alpha = 100

                    self.draw_enhanced_block(screen_x, screen_y, self.grid[y][x], alpha)

        # Update line clear animation
        if self.line_clear_animation > 0:
            self.line_clear_animation -= 1
            if self.line_clear_animation == 0:
                self.line_clear_rows = []

        # Draw ghost piece
        if self.current_piece and self.state == GameState.PLAYING:
            ghost_y = self.current_piece.get_ghost_y(self.grid)
            for y, row in enumerate(self.current_piece.shape):
                for x, value in enumerate(row):
                    if value:
                        screen_x = (self.current_piece.x + x) * BLOCK_SIZE + shake_x
                        screen_y = (ghost_y + y) * BLOCK_SIZE + shake_y
                        if 0 <= screen_y < SCREEN_HEIGHT:
                            self.draw_enhanced_block(screen_x, screen_y,
                                                   self.current_piece.color, 60)

        # Draw current piece with glow effect
        if self.current_piece and self.state == GameState.PLAYING:
            for y, row in enumerate(self.current_piece.shape):
                for x, value in enumerate(row):
                    if value:
                        screen_x = (self.current_piece.x + x) * BLOCK_SIZE + shake_x
                        screen_y = (self.current_piece.y + y) * BLOCK_SIZE + shake_y
                        if screen_y >= 0:
                            glow = (pygame.time.get_ticks() % 1000) < 500
                            self.draw_enhanced_block(screen_x, screen_y,
                                                   self.current_piece.color, 255, glow)

        # Draw particles
        self.draw_particles()

    def calculate_performance_metrics(self):
        """Calculate performance metrics"""
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
        pps = self.total_pieces / elapsed_time if elapsed_time > 0 else 0
        lps = self.lines_cleared / elapsed_time if elapsed_time > 0 else 0
        return pps, lps, elapsed_time

    def draw_mini_piece(self, piece, x, y, size=20, alpha=255):
        """Draw enhanced miniature piece"""
        if not piece:
            return

        for py, row in enumerate(piece.shape):
            for px, value in enumerate(row):
                if value:
                    rect = pygame.Rect(x + px * size, y + py * size, size, size)
                    # Create surface with alpha
                    mini_surface = pygame.Surface((size, size), pygame.SRCALPHA)
                    color = (*TETRIS_COLORS[piece.color][:3], alpha)
                    mini_surface.fill(color)

                    # Add border
                    border_color = tuple(min(255, c + 50) for c in TETRIS_COLORS[piece.color][:3])
                    pygame.draw.rect(mini_surface, border_color, (0, 0, size, size), 1)
                    self.screen.blit(mini_surface, rect)

    def draw_side_panel(self):
        """Enhanced side panel with more information"""
        panel_x = SCREEN_WIDTH

        # Animated background
        time_offset = pygame.time.get_ticks() * 0.001
        for i in range(0, SCREEN_HEIGHT, 20):
            color_intensity = int(30 + 10 * math.sin(time_offset + i * 0.1))
            color = (color_intensity, color_intensity, color_intensity + 10)
            pygame.draw.rect(self.screen, color, 
                           (panel_x, i, SIDE_PANEL_WIDTH, 20))

        y_offset = 20

        # Score with animation
        score_color = WHITE
        if self.combo > 0:
            score_color = (255, 255 - self.combo * 20, 255 - self.combo * 20)
        score_text = self.font_medium.render(f"Score: {self.score:,}", True, score_color)
        self.screen.blit(score_text, (panel_x + 10, y_offset))
        y_offset += 40

        # Level and lines
        level_text = self.font_medium.render(f"Level: {self.level}", True, WHITE)
        self.screen.blit(level_text, (panel_x + 10, y_offset))
        y_offset += 25

        lines_text = self.font_small.render(f"Lines: {self.lines_cleared}", True, WHITE)
        self.screen.blit(lines_text, (panel_x + 10, y_offset))
        y_offset += 25

        # Combo counter
        if self.combo > 0:
            combo_text = self.font_small.render(f"Combo: {self.combo}x", True, YELLOW)
            self.screen.blit(combo_text, (panel_x + 10, y_offset))
        y_offset += 30

        # Performance metrics
        pps, lps, elapsed_time = self.calculate_performance_metrics()
        perf_title = self.font_small.render("Performance:", True, CYAN)
        self.screen.blit(perf_title, (panel_x + 10, y_offset))
        y_offset += 20

        pps_text = self.font_small.render(f"PPS: {pps:.2f}", True, WHITE)
        self.screen.blit(pps_text, (panel_x + 10, y_offset))
        y_offset += 15

        lps_text = self.font_small.render(f"LPS: {lps:.2f}", True, WHITE)
        self.screen.blit(lps_text, (panel_x + 10, y_offset))
        y_offset += 15

        time_text = self.font_small.render(f"Time: {elapsed_time:.0f}s", True, WHITE)
        self.screen.blit(time_text, (panel_x + 10, y_offset))
        y_offset += 30

        # Hold piece
        hold_text = self.font_medium.render("Hold:", True, WHITE)
        self.screen.blit(hold_text, (panel_x + 10, y_offset))
        y_offset += 30

        if self.hold_piece:
            self.draw_mini_piece(self.hold_piece, panel_x + 10, y_offset)
        y_offset += 80

        # Next pieces
        next_text = self.font_medium.render("Next:", True, WHITE)
        self.screen.blit(next_text, (panel_x + 10, y_offset))
        y_offset += 30

        for i, piece in enumerate(self.next_pieces[:3]):
            alpha = 255 - i * 50
            self.draw_mini_piece(piece, panel_x + 10, y_offset + i * 60, alpha=alpha)

        y_offset += 200

        # Statistics
        stats_text = self.font_medium.render("Statistics:", True, WHITE)
        self.screen.blit(stats_text, (panel_x + 10, y_offset))
        y_offset += 30

        for piece_type, count in self.stats.items():
            stat_text = self.font_small.render(f"{piece_type}: {count}", True, WHITE)
            self.screen.blit(stat_text, (panel_x + 10, y_offset))
            y_offset += 20

    def draw_menu(self):
        """Draw the main menu"""
        self.screen.fill(BLACK)

        title = self.font_large.render("TETRIX", True, WHITE)
        title_rect = title.get_rect(center=(self.screen.get_width()//2, 200))
        self.screen.blit(title, title_rect)

        instructions = [
            "# CONTROLS:",
            "Left/Right : Move",
            "Down : Soft Drop", 
            "Space : Hard Drop",
            "Up : Rotate",
            "C : Hold",
            "P : Pause",
            "",
            "# Press SPACE to Start: "
        ]

        y = 300
        for line in instructions:
            text = self.font_medium.render(line, True, WHITE)
            text_rect = text.get_rect(center=(self.screen.get_width()//2, y))
            self.screen.blit(text, text_rect)
            y += 30

    def draw_pause(self):
        """Draw pause screen overlay"""
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        pause_text = self.font_large.render("PAUSED", True, WHITE)
        pause_rect = pause_text.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2))
        self.screen.blit(pause_text, pause_rect)

        resume_text = self.font_medium.render("Press 'P' to Resume", True, WHITE)
        resume_rect = resume_text.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 + 50))
        self.screen.blit(resume_text, resume_rect)

    def draw_game_over(self):
        """Draw game over screen"""
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        game_over_text = self.font_large.render("GAME OVER.", True, RED)
        go_rect = game_over_text.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 - 100))
        self.screen.blit(game_over_text, go_rect)

        final_score = self.font_medium.render(f"Final Score: {self.score:,}", True, WHITE)
        score_rect = final_score.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 - 50))
        self.screen.blit(final_score, score_rect)

        final_level = self.font_medium.render(f"Level Reached: {self.level}", True, WHITE)
        level_rect = final_level.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 - 20))
        self.screen.blit(final_level, level_rect)

        restart_text = self.font_medium.render("Press 'R'' to Restart (or) 'Q' to Quit", True, WHITE)
        restart_rect = restart_text.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 + 50))
        self.screen.blit(restart_text, restart_rect)

    def handle_events(self):
        """Handle all game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if self.state == GameState.MENU:
                    if event.key == pygame.K_SPACE:
                        self.state = GameState.PLAYING
                        self.reset_game()
                elif self.state == GameState.PLAYING:
                    if event.key == pygame.K_LEFT:
                        self.move_piece(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.move_piece(1, 0)
                    elif event.key == pygame.K_DOWN:
                        if self.move_piece(0, 1):
                            self.score += 1
                    elif event.key == pygame.K_UP:
                        self.move_piece(0, 0, rotate=True)
                    elif event.key == pygame.K_SPACE:
                        self.hard_drop()
                    elif event.key == pygame.K_c:
                        self.hold_current_piece()
                    elif event.key == pygame.K_p:
                        self.state = GameState.PAUSED
                elif self.state == GameState.PAUSED:
                    if event.key == pygame.K_p:
                        self.state = GameState.PLAYING
                elif self.state == GameState.GAME_OVER:
                    if event.key == pygame.K_r:
                        self.state = GameState.PLAYING
                        self.reset_game()
                    elif event.key == pygame.K_q:
                        return False

        return True

    def update(self):
        """Update game logic"""
        if self.state != GameState.PLAYING:
            return

        # Update particles
        self.update_particles()

        # Handle automatic piece dropping
        current_time = pygame.time.get_ticks()
        if current_time - self.drop_time > self.drop_speed:
            if not self.move_piece(0, 1):
                self.lock_piece()
            self.drop_time = current_time

    def load_high_scores(self):
        """Load high scores from file"""
        try:
            if os.path.exists("tetris_scores.json"):
                with open("tetris_scores.json", "r") as f:
                    return json.load(f)
        except:
            pass
        return []

    def save_high_score(self):
        """Save high score if applicable"""
        self.high_scores.append(self.score)
        self.high_scores.sort(reverse=True)
        self.high_scores = self.high_scores[:10]  # Keep top 10

        try:
            with open("tetris_scores.json", "w") as f:
                json.dump(self.high_scores, f)
        except:
            pass

    def run(self):
        """Main game loop"""
        running = True
        while running:
            running = self.handle_events()
            self.update()

            # Draw everything
            if self.state == GameState.MENU:
                self.draw_menu()
            else:
                self.draw_grid()
                self.draw_side_panel()

                if self.state == GameState.PAUSED:
                    self.draw_pause()
                elif self.state == GameState.GAME_OVER:
                    self.save_high_score()
                    self.draw_game_over()

            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS

        pygame.quit()

if __name__ == "__main__":
    game = TetrisGame()

    game.run()
