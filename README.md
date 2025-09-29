# TetriX (Tetris Game) 🎮:

A modern, feature-rich Tetris implementation built with Python and Pygame. This version includes official Tetris standards, advanced visual effects, sound system, and comprehensive gameplay mechanics.

## 🎯 Features:

### Core Gameplay:
- **Official Tetris Standards**: Proper piece colors, 7-bag randomization system, and standard scoring.
- **Modern Controls**: Ghost piece preview, hard drop, hold piece functionality, and smooth rotation.
- **Progressive Difficulty**: Dynamic level progression with increasing speed every 10 lines cleared.
- **Combo System**: Bonus points for consecutive line clears.
- **Performance Tracking**: Real-time PPS (Pieces Per Second) and LPS (Lines Per Second) metrics.

### Visual & Audio Effects:
- **Enhanced Graphics**: Gradient blocks with 3D appearance, particle effects, and screen shake.
- **Visual Feedback**: Line clear animations, flash effects, and animated glow around current piece.
- **Sound System**: Procedural audio generation with movement sounds, line clear effects, and special Tetris sound.
- **Professional UI**: Comprehensive side panel with statistics, hold piece preview, and next piece queue.

### Quality of Life:
- **Multiple Game States**: Main menu, pause functionality, and proper game over handling.
- **Statistics Tracking**: Detailed piece usage statistics and performance metrics.
- **High Score System**: Persistent top 10 score tracking saved to JSON file.
- **Next Piece Preview**: Shows upcoming '3' pieces instead of just '1'.

## 🚀 Installation & Setup:

## Install Dependencies:
```bash
python install.py
```

### Requirements:
```bash
# Install required dependencies
pip install pygame numpy
```

### Quick Start:
```bash
# Clone or download the repository
# Run the game
python TetriX.py
```

### System Requirements:
- Python 3.6+
- Pygame library
- NumPy (for sound generation - optional)

## 🎮 Controls:

| Key | Action |
|-----|--------|
| **Movement** | |
| ← → | Move piece left/right |
| ↓ | Soft drop (faster fall) |
| ↑ | Rotate piece clockwise |
| **Special Actions** | |
| `Space` | Hard drop (instant drop) |
| `C` | Hold current piece |
| **Game Controls** | |
| `P` | Pause/unpause game |
| `R` | Restart (on game over screen) |
| `Q` | Quit (on game over screen) |

## 📊 Game Mechanics:

### Scoring System:
- **Single Line**: 100 × level
- **Double Lines**: 300 × level  
- **Triple Lines**: 500 × level
- **Tetris (4 Lines)**: 800 × level
- **Combo Bonus**: 50 × combo × level
- **Hard Drop Bonus**: 2 points per cell dropped

### Level Progression:
- Levels increase every 10 lines cleared.
- Drop speed increases with each level.
- Maximum challenge at higher levels with near-instant piece falling.

### 7-Bag Randomization:
Uses the modern Tetris piece generation system ensuring fair distribution:
- Each "bag" contains one of each piece type (I, O, T, S, Z, J, L).
- Pieces are shuffled randomly within each bag.
- Prevents long droughts of specific pieces.

## 🏗️ Code Architecture:

### Main Classes:
- **`TetrisGame`**: Main game controller handling states, events, and rendering.
- **`Tetrimino`**: Individual piece management with rotation and collision detection.
- **`SoundManager`**: Procedural audio generation and sound effect management.
- **`Particle`**: Visual effects system for enhanced gameplay feedback.

### Game States:
- **Menu**: Professional start screen with control instructions.
- **Playing**: Active gameplay with full feature set.
- **Paused**: Game suspension with overlay.
- **Game Over**: Final statistics and restart options.

### Performance Features:
- **60 FPS**: Smooth gameplay with consistent frame rate.
- **Efficient Rendering**: Optimized drawing routines for complex visual effects.
- **Memory Management**: Proper cleanup of particles and effects.
- **Responsive Input**: Immediate control response without lag.

## 🎨 Visual Effects:

### Particle System:
- **Line Clear Effects**: Explosion particles when lines are cleared.
- **Piece Lock Effects**: Small particle burst when pieces lock in place.
- **Dynamic Colors**: Randomized particle colors for visual variety.

### Screen Effects:
- **Screen Shake**: Dramatic effect for Tetris (4-line) clears.
- **Flash Effects**: Screen flashing for major events.
- **Glow Animation**: Animated glow around the current falling piece.
- **Line Clear Animation**: Smooth animated clearing of completed lines.

### Block Enhancement:
- **Gradient Blocks**: 3D appearance with lighting effects.
- **Enhanced Borders**: Multiple border layers for depth.
- **Ghost Piece**: Semi-transparent preview showing drop position.
- **Color Coding**: Official Tetris color scheme for each piece type.

## 📈 Statistics & Tracking:

### Performance Metrics:
- **PPS (Pieces Per Second)**: Measure of play speed.
- **LPS (Lines Per Second)**: Efficiency metric.
- **Game Time**: Total elapsed time.
- **Piece Distribution**: Count of each piece type used.

### Persistent Data:
- **High Scores**: Top 10 scores saved to `tetris_scores.json`.
- **Automatic Saving**: Scores saved automatically on game over.
- **Error Handling**: Graceful handling of file system issues.

## 🔧 Configuration:

### Sound Settings:
The game automatically detects sound capabilities:
- Falls back gracefully if NumPy is not installed.
- Continues without sound if audio system fails.
- Procedural generation creates sounds dynamically.

### Performance Tuning:
- 60 FPS target with automatic frame rate management.
- Particle count automatically managed for performance.
- Visual effects can be reduced on slower systems.

## 🐛 Troubleshooting:

### Common Issues:
1. **No Sound**: Install NumPy (`pip install numpy`) or ignore - game works without sound.
2. **Slow Performance**: Reduce particle effects by modifying particle count in code.
3. **Installation Issues**: Ensure Python 3.6+ and Pygame are properly installed.

### System Requirements:
- **Minimum**: Python 3.6, Pygame.
- **Recommended**: Python 3.8+, NumPy.

## 🎯 Gameplay Tips:

### Advanced Techniques:
- **T-Spins**: Use the hold piece strategically for complex clears.
- **Combo Building**: Chain multiple line clears for maximum scoring.
- **Speed Management**: Use soft drop to maintain control at higher levels.
- **Ghost Piece**: Plan moves using the ghost piece preview.

### Strategic Play:
- Monitor piece statistics to anticipate piece droughts.
- Use the next piece preview to plan 2-3 moves ahead.
- Hold piece is crucial for avoiding difficult situations.
- Focus on Tetris clears (4 lines) for maximum points.

## 📝 Version History:

### Features Added:
- Official Tetris color scheme and piece generation.
- Hold piece system with 'C' key functionality.
- Ghost piece showing drop preview.
- Advanced visual effects with particles and animations.
- Sound system with procedural audio generation.
- Performance metrics and comprehensive statistics.
- High score persistence system.
- Enhanced UI with multiple game states.

### Technical Improvements:
- Object-oriented design with proper separation of concerns.
- Robust error handling for file operations and sound system.
- Optimized rendering pipeline for complex visual effects.
- Memory-efficient particle system with automatic cleanup.

## 🤝 Contributing:

This is a complete, standalone Tetris implementation. The code is well-structured and documented for educational purposes and further enhancement.

## 📄 License:

This project is open source and available for educational and personal use. Tetris is a trademark of Tetris Holding, LLC.

---

**Enjoy the classic game with modern enhancements!** 🎮✨
