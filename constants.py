# constants.py

import pygame

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Game world dimensions
LEVEL_WIDTH = 5000 # Make levels much wider

# Player properties
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50 # Adjust to fit your character sprite
PLAYER_MAX_SPEED = 7
PLAYER_ACCELERATION = 0.5
GRAVITY = 0.5
JUMP_STRENGTH = -10
INITIAL_ENERGY = 100
MAX_ENERGY = 100
FRICTION = 0.9 # Added friction constant for smooth stopping

# Item properties
ITEM_SIZE = 30

# Obstacle properties
OBSTACLE_SIZE = 40
PARASITE_DAMAGE = 20

# Platform properties
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20

# Spike properties
SPIKE_WIDTH = 40 # Aumentado para que la sierra se vea mejor
SPIKE_HEIGHT = 40 # Aumentado
SPIKE_DAMAGE = 15

# Finish Line properties
FINISH_LINE_WIDTH = 50

# Terrain effects
SAND_FRICTION_MULTIPLIER = 0.5
ICE_ACCELERATION_MULTIPLIER = 1.5

# Level transition
MAX_LEVELS = 10
LEVEL_TRANSITION_DELAY_MS = 3000 # 3 seconds

# Colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
BROWN = (139, 69, 19)
ORANGE = (255, 165, 0)
DARK_GREEN = (0, 100, 0)
LIGHT_BLUE = (173, 216, 230)
GRAY = (128, 128, 128)
FINISH_LINE_COLOR = GREEN # Just for the visual cue, will be replaced by image

# --- IMAGENES ---
# Rutas de imágenes del jugador
# Usaremos 'character_green_front' como el sprite base para el glóbulo rojo/vehículo
PLAYER_SPRITE_IDLE = 'assets/Sprites/Characters/Default/character_green_front.png'
# Puedes añadir más para animaciones en el futuro:
PLAYER_SPRITE_WALK_A = 'assets/Sprites/Characters/Default/character_green_walk_a.png'
PLAYER_SPRITE_WALK_B = 'assets/Sprites/Characters/Default/character_green_walk_b.png'
PLAYER_SPRITE_JUMP = 'assets/Sprites/Characters/Default/character_green_jump.png'
PLAYER_SPRITE_HIT = 'assets/Sprites/Characters/Default/character_green_hit.png'

# Rutas para otros elementos
# Puedes usar un sprite de ítem que parezca una molécula de hierro o un cristal
ITEM_IMAGE = 'assets/Sprites/Tiles/Default/fish.png' # O busca uno que se parezca al hierro

# Sprites de Enemigos (Parásitos)
# Puedes elegir cuál te gusta más para el obstáculo principal
OBSTACLE_IMAGE = 'assets/Sprites/Enemies/Default/slime_normal_rest.png'

# Sprite de Spikes (Pinchos)
SPIKE_IMAGE = 'assets/Sprites/Tiles/Default/saw.png' # Usaremos la sierra

# Rutas para el entorno
PLATFORM_IMAGE = 'assets/Sprites/Tiles/Default/brick_brown.png' # Todavía necesitas crear o encontrar esta
FINISH_LINE_IMAGE = 'assets/Sprites/Tiles/Default/fish.png' # Todavía necesitas crear o encontrar esta

BACKGROUND_IMAGE = 'assets/Sprites/Backgrounds/Default/background_clouds.png' # Por ejemplo