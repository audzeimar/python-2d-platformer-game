# Geometry Dash Clone (Pygame)

A small Geometry Dash-inspired game written in Python with Pygame.
The project includes a start menu, simple settings screen, side-scrolling gameplay, collision detection, particles and a death animation.

## Features

- Start menu with buttons
- Auto-running player with jump mechanic
- Tile-based level loaded from a text map
- Camera tracking
- Background scrolling
- Particle trail and death animation
- Relative asset loading (no hardcoded local paths)

## Project Structure

```text
GD_fixed/
├── assets/
│   ├── fonts/
│   ├── images/
│   ├── maps/
│   └── music/
├── src/
│   ├── assets.py
│   ├── button.py
│   ├── camera.py
│   ├── death_animation.py
│   ├── game.py
│   ├── main.py
│   ├── menu.py
│   ├── particles.py
│   ├── player.py
│   ├── settings.py
│   └── utils.py
├── requirements.txt
└── README.md
```

## How to run

1. Create a virtual environment if you want.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the game:

```bash
python src/main.py
```

## Controls

- **Space** – jump
- **Close window** – quit the game

## What I Learned

- working with game loops and real-time systems
- implementing physics and collision detection
- structuring a multi-file Python project
- managing assets and project architecture
