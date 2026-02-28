# player.py
import pygame
from constants import * # Asegúrate de importar tus nuevas constantes

class Player:
    def __init__(self, x, y):
        # El rect ahora representará el área del glóbulo rojo, no una moto separada
        self.rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.color = RED # El color de fallback si la imagen no carga

        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.energy = INITIAL_ENERGY
        self.collected_iron = 0
        self.current_terrain_speed_multiplier = 1.0
        self.moving_left = False
        self.moving_right = False

        # --- Cargar la imagen del personaje (glóbulo rojo) ---
        try:
            # Cargamos el sprite principal para el personaje
            self.image = pygame.image.load(PLAYER_SPRITE_IDLE).convert_alpha()
            # Escalamos la imagen para que se ajuste al tamaño de nuestro rect de jugador
            self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
            # Podrías cargar otros sprites para animaciones aquí:
            # self.walk_frames = [
            #     pygame.transform.scale(pygame.image.load(PLAYER_SPRITE_WALK_A).convert_alpha(), (PLAYER_WIDTH, PLAYER_HEIGHT)),
            #     pygame.transform.scale(pygame.image.load(PLAYER_SPRITE_WALK_B).convert_alpha(), (PLAYER_WIDTH, PLAYER_HEIGHT))
            # ]
            # self.current_frame = self.image # Para animaciones: self.walk_frames[0]
            # self.animation_timer = 0 # Para controlar el cambio de frames
        except pygame.error as e:
            print(f"Error al cargar la imagen del jugador: {e}. Usando color de fallback.")
            self.image = None # Si la imagen no carga, usaremos el color.

    def draw(self, screen, camera_offset_x):
        # Dibujar el sprite del personaje
        if self.image:
            # Dibuja la imagen en la posición del rect del jugador, aplicando el offset de la cámara
            screen.blit(self.image, (self.rect.x - camera_offset_x, self.rect.y))
        else:
            # Si la imagen no cargó, dibuja un rectángulo simple con el color de fallback
            pygame.draw.rect(screen, self.color, (self.rect.x - camera_offset_x, self.rect.y, self.rect.width, self.rect.height))

    def update(self, terrain_type, platforms, ground_rect):
        # Apply terrain effects
        if terrain_type == "sand":
            self.current_terrain_speed_multiplier = SAND_FRICTION_MULTIPLIER
        elif terrain_type == "ice":
            self.current_terrain_speed_multiplier = ICE_ACCELERATION_MULTIPLIER
        else: # Normal
            self.current_terrain_speed_multiplier = 1.0

        # Store previous position for collision detection
        prev_x = self.rect.x
        prev_y = self.rect.y

        # Apply gravity
        self.vel_y += GRAVITY

        # Horizontal movement with acceleration
        if self.moving_left:
            self.vel_x = max(self.vel_x - PLAYER_ACCELERATION, -PLAYER_MAX_SPEED * self.current_terrain_speed_multiplier)
        elif self.moving_right:
            self.vel_x = min(self.vel_x + PLAYER_ACCELERATION, PLAYER_MAX_SPEED * self.current_terrain_speed_multiplier)
        else:
            # Apply friction only when no directional key is pressed
            if self.on_ground:
                if terrain_type == "ice":
                    self.vel_x *= 0.98 # Less friction on ice, so it slides more
                else:
                    self.vel_x *= FRICTION
            if abs(self.vel_x) < 0.1: # Stop small movements
                self.vel_x = 0

        # Update position
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        self.on_ground = False # Reset for collision detection each frame

        # Collision with left world boundary (corrected to 0)
        if self.rect.left < 0:
            self.rect.left = 0
            self.vel_x = 0 # Stop horizontal movement if hitting wall

        # Check collision with ground
        if self.rect.colliderect(ground_rect):
            # If falling and land on top of ground
            if self.vel_y > 0 and prev_y + PLAYER_HEIGHT <= ground_rect.top:
                self.rect.bottom = ground_rect.top
                self.vel_y = 0
                self.on_ground = True
            # If already on ground, confirm on ground
            elif self.rect.bottom == ground_rect.top:
                self.on_ground = True

        # Collision with platforms
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # If falling and land on top of platform
                if self.vel_y > 0 and prev_y + PLAYER_HEIGHT <= platform.rect.top:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                # If jumping into bottom of platform
                elif self.vel_y < 0 and prev_y >= platform.rect.bottom:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0
                # If colliding from left side
                elif self.vel_x > 0 and prev_x + PLAYER_WIDTH <= platform.rect.left:
                    self.rect.right = platform.rect.left
                    self.vel_x = 0
                # If colliding from right side
                elif self.vel_x < 0 and prev_x >= platform.rect.right:
                    self.rect.left = platform.rect.right
                    self.vel_x = 0

        # After all vertical movements and collisions, re-check on ground for platforms
        if self.vel_y == 0: # Only if not actively jumping/falling
            platform_collision_detected = False
            for platform in platforms:
                if self.rect.bottom == platform.rect.top and \
                   self.rect.right > platform.rect.left and \
                   self.rect.left < platform.rect.right:
                    platform_collision_detected = True
                    break
            # If not on a platform, check if on the main ground
            if not platform_collision_detected and \
               self.rect.bottom == ground_rect.top:
                self.on_ground = True
            elif platform_collision_detected:
                self.on_ground = True


    def move_left(self):
        self.moving_left = True
        self.moving_right = False # Ensure only one direction is active

    def move_right(self):
        self.moving_right = True
        self.moving_left = False # Ensure only one direction is active

    def stop_moving_left(self): # New: Method to stop left movement
        self.moving_left = False

    def stop_moving_right(self): # New: Method to stop right movement
        self.moving_right = False

    def jump(self):
        if self.on_ground:
            self.vel_y = JUMP_STRENGTH
            self.on_ground = False # Player is now in the air

    def take_damage(self, amount):
        self.energy -= amount
        if self.energy < 0:
            self.energy = 0

    def heal(self, amount):
        self.energy += amount
        if self.energy > MAX_ENERGY:
            self.energy = MAX_ENERGY

    def collect_item(self):
        self.collected_iron += 1

    def reset_iron(self):
        self.collected_iron = 0