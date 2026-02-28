# level.py

import pygame
import random
from constants import *

# --- Clases para los elementos del juego ---

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = None
        try:
            self.original_image = pygame.image.load(ITEM_IMAGE).convert_alpha()
            self.image = pygame.transform.scale(self.original_image, (ITEM_SIZE, ITEM_SIZE))
        except pygame.error as e:
            print(f"Error al cargar la imagen del ítem: {e}. Usando placeholder.")
            self.image = pygame.Surface((ITEM_SIZE, ITEM_SIZE))
            self.image.fill(YELLOW) # Placeholder
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen, camera_offset_x):
        screen.blit(self.image, (self.rect.x - camera_offset_x, self.rect.y))

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = None
        try:
            self.original_image = pygame.image.load(OBSTACLE_IMAGE).convert_alpha()
            self.image = pygame.transform.scale(self.original_image, (OBSTACLE_SIZE, OBSTACLE_SIZE))
        except pygame.error as e:
            print(f"Error al cargar la imagen del obstáculo: {e}. Usando placeholder.")
            self.image = pygame.Surface((OBSTACLE_SIZE, OBSTACLE_SIZE))
            self.image.fill(RED) # Placeholder
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen, camera_offset_x):
        screen.blit(self.image, (self.rect.x - camera_offset_x, self.rect.y))

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width=PLATFORM_WIDTH, height=PLATFORM_HEIGHT):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BROWN) # Plataformas ahora son bloques marrones sólidos
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen, camera_offset_x):
        screen.blit(self.image, (self.rect.x - camera_offset_x, self.rect.y))

class MovingPlatform(Platform):
    def __init__(self, x, y, width, height, move_range, speed):
        super().__init__(x, y, width, height)
        self.start_x = x
        self.end_x = x + move_range
        self.speed = speed
        self.direction = 1 # 1 for right, -1 for left

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.right > self.end_x or self.rect.left < self.start_x:
            self.direction *= -1 # Reverse direction
            # Ajustar la posición para evitar que se salga del rango por un tick
            if self.direction == 1: # Si va a la derecha, ajustar el left
                self.rect.left = self.start_x 
            else: # Si va a la izquierda, ajustar el right
                self.rect.right = self.end_x
            
class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = None
        try:
            self.original_image = pygame.image.load(SPIKE_IMAGE).convert_alpha()
            self.image = pygame.transform.scale(self.original_image, (SPIKE_WIDTH, SPIKE_HEIGHT))
        except pygame.error as e:
            print(f"Error al cargar la imagen de los pinchos: {e}. Usando placeholder.")
            self.image = pygame.Surface((SPIKE_WIDTH, SPIKE_HEIGHT))
            pygame.draw.polygon(self.image, GRAY, [(0, SPIKE_HEIGHT), (SPIKE_WIDTH // 2, 0), (SPIKE_WIDTH, SPIKE_HEIGHT)]) # Triángulo gris
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen, camera_offset_x):
        screen.blit(self.image, (self.rect.x - camera_offset_x, self.rect.y))

class FinishLine(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((FINISH_LINE_WIDTH, SCREEN_HEIGHT))
        self.image.fill(GREEN) 
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen, camera_offset_x):
        screen.blit(self.image, (self.rect.x - camera_offset_x, self.rect.y))

# --- Clase Level ---

class Level:
    def __init__(self, level_number):
        self.level_number = level_number
        self.terrain_type = self.get_terrain_type(level_number)
        self.items = []
        self.obstacles = []
        self.platforms = [] 
        self.spikes = []
        self.finish_line = None
        
        self.background_image = None
        try:
            self.background_image = pygame.image.load(BACKGROUND_IMAGE).convert() 
            self.background_image = pygame.transform.scale(self.background_image, (LEVEL_WIDTH, SCREEN_HEIGHT))
        except pygame.error as e:
            print(f"Error al cargar la imagen de fondo: {e}. El fondo no se mostrará.")
            self.background_image = None 

        self._generate_level_elements()

    def get_terrain_type(self, level_num):
        terrain_types = ["normal", "sand", "ice"]
        return terrain_types[(level_num - 1) % len(terrain_types)]

    def _generate_level_elements(self):
        self.items = []
        self.obstacles = []
        self.platforms = []
        self.spikes = []
        self.finish_line = None

        self.ground_rect = pygame.Rect(0, SCREEN_HEIGHT - 50, LEVEL_WIDTH, 50)
        max_content_x = LEVEL_WIDTH - FINISH_LINE_WIDTH - 250 

        # --- Lógica de generación de niveles más variada y con menos "imposibles" ---
        # Se añaden espacios mínimos y se evita la superposición directa de plataformas y pinchos del suelo.
        # Los anchos de las plataformas pequeñas se aseguran para ser al menos PLAYER_WIDTH + 10.

        # Nivel 1: Introducción a plataformas y saltos básicos.
        if self.level_number == 1:
            current_x = 200
            while current_x < max_content_x:
                # Bloque 1: Plataformas ascendentes y algunos ítems
                if current_x < max_content_x * 0.3:
                    for i in range(3):
                        self.platforms.append(Platform(current_x + i * 150, SCREEN_HEIGHT - 100 - i * 50))
                        self.items.append(Item(current_x + i * 150 + 20, SCREEN_HEIGHT - 100 - i * 50 - ITEM_SIZE))
                    current_x += 450 + random.randint(0, 50) # Añadir variación
                # Bloque 2: Pequeños saltos y algún obstáculo en el suelo (asegura espacio para saltar)
                elif current_x < max_content_x * 0.6:
                    self.platforms.append(Platform(current_x + 50, SCREEN_HEIGHT - 100))
                    obstacle_x = current_x + 180 # Mover obstáculo más allá de la plataforma inicial
                    self.obstacles.append(Obstacle(obstacle_x, SCREEN_HEIGHT - 50 - OBSTACLE_SIZE))
                    self.items.append(Item(current_x + 230, SCREEN_HEIGHT - 100 - ITEM_SIZE))
                    current_x += 350 + random.randint(0, 50)
                # Bloque 3: Introducción a pinchos (asegura espacio) y más ítems
                else:
                    spike_x = current_x + 100
                    self.spikes.append(Spike(spike_x, SCREEN_HEIGHT - 50 - SPIKE_HEIGHT))
                    # Plataforma colocada para que sea un salto sobre el pincho, no encima
                    self.platforms.append(Platform(spike_x + SPIKE_WIDTH + 50, SCREEN_HEIGHT - 150)) 
                    self.items.append(Item(spike_x + SPIKE_WIDTH + 70, SCREEN_HEIGHT - 150 - ITEM_SIZE))
                    current_x += 400 + random.randint(0, 50)

        # Nivel 2 (Arena): Más obstáculos en el suelo, saltos más difíciles entre plataformas, primeras plataformas móviles.
        elif self.level_number == 2:
            current_x = 150
            while current_x < max_content_x:
                # Bloque 1: Zona con pinchos y saltos largos (más espaciados)
                if current_x < max_content_x * 0.3:
                    spike_x1 = current_x + 50
                    self.spikes.append(Spike(spike_x1, SCREEN_HEIGHT - 50 - SPIKE_HEIGHT))
                    self.spikes.append(Spike(spike_x1 + SPIKE_WIDTH, SCREEN_HEIGHT - 50 - SPIKE_HEIGHT))
                    platform_x = spike_x1 + SPIKE_WIDTH * 2 + 80 # Mayor espacio para salto
                    self.platforms.append(Platform(platform_x, SCREEN_HEIGHT - 120, width=PLATFORM_WIDTH+50))
                    self.items.append(Item(platform_x + 20, SCREEN_HEIGHT - 120 - ITEM_SIZE))
                    current_x += 350 + random.randint(0, 50)
                # Bloque 2: Introducción a MovingPlatform (con espacio de aterrizaje)
                elif current_x < max_content_x * 0.6:
                    self.platforms.append(Platform(current_x + 50, SCREEN_HEIGHT - 100)) # Plataforma de inicio
                    mov_plat_x = current_x + 250 # Más espacio
                    self.platforms.append(MovingPlatform(mov_plat_x, SCREEN_HEIGHT - 180, PLATFORM_WIDTH, PLATFORM_HEIGHT, 150, 1.5))
                    self.items.append(Item(mov_plat_x + 50, SCREEN_HEIGHT - 180 - ITEM_SIZE))
                    current_x += 450 + random.randint(0, 50)
                # Bloque 3: Obstáculos seguidos y plataformas a diferentes alturas (con espacio intermedio)
                else:
                    self.obstacles.append(Obstacle(current_x + 50, SCREEN_HEIGHT - 50 - OBSTACLE_SIZE))
                    self.platforms.append(Platform(current_x + 180, SCREEN_HEIGHT - 150))
                    self.platforms.append(Platform(current_x + 350, SCREEN_HEIGHT - 200))
                    self.items.append(Item(current_x + 370, SCREEN_HEIGHT - 200 - ITEM_SIZE))
                    current_x += 500 + random.randint(0, 50)

        # Nivel 3 (Hielo): Saltos largos, plataformas pequeñas, más plataformas móviles.
        elif self.level_number == 3:
            current_x = 100
            while current_x < max_content_x:
                # Bloque 1: Serie de plataformas pequeñas con ítems (asegurando ancho mínimo)
                if current_x < max_content_x * 0.3:
                    for i in range(3):
                        plat_width = max(PLAYER_WIDTH + 10, PLATFORM_WIDTH-20) # Ancho mínimo
                        self.platforms.append(Platform(current_x + i * 180, SCREEN_HEIGHT - 150 - i * 30, width=plat_width))
                        self.items.append(Item(current_x + i * 180 + 10, SCREEN_HEIGHT - 150 - i * 30 - ITEM_SIZE))
                    current_x += 540 + random.randint(0, 50)
                # Bloque 2: Plataforma móvil con pinchos encima (pinchos en el mismo nivel que la plataforma, no debajo)
                elif current_x < max_content_x * 0.6:
                    mov_plat_x = current_x + 100
                    mov_plat_y = SCREEN_HEIGHT - 180
                    self.platforms.append(MovingPlatform(mov_plat_x, mov_plat_y, PLATFORM_WIDTH+50, PLATFORM_HEIGHT, 200, 2))
                    self.spikes.append(Spike(mov_plat_x + 20, mov_plat_y - SPIKE_HEIGHT)) # Pinchos en la plataforma
                    self.items.append(Item(mov_plat_x + 70, mov_plat_y - ITEM_SIZE - 10))
                    current_x += 400 + random.randint(0, 50)
                # Bloque 3: Obstáculo grande y salto a plataforma alta (con espacio para evitar)
                else:
                    self.obstacles.append(Obstacle(current_x + 80, SCREEN_HEIGHT - 50 - OBSTACLE_SIZE*2)) 
                    self.platforms.append(Platform(current_x + 350, SCREEN_HEIGHT - 250)) # Más distancia
                    self.items.append(Item(current_x + 370, SCREEN_HEIGHT - 250 - ITEM_SIZE))
                    current_x += 500 + random.randint(0, 50)
        
        # Nivel 4 (Normal): Mezcla de desafíos, incluyendo saltos de precisión y más uso de móviles.
        elif self.level_number == 4:
            current_x = 100
            while current_x < max_content_x:
                # Bloque 1: Serie de plataformas con huecos y algunos ítems
                if current_x < max_content_x * 0.3:
                    for i in range(4):
                        plat_width = max(PLAYER_WIDTH + 10, PLATFORM_WIDTH - 30)
                        self.platforms.append(Platform(current_x + i * 140, SCREEN_HEIGHT - 100 - (i % 2) * 50, width=plat_width))
                        if i % 2 == 0:
                            self.items.append(Item(current_x + i * 140 + 10, SCREEN_HEIGHT - 100 - (i % 2) * 50 - ITEM_SIZE))
                    current_x += 550 + random.randint(0, 50)
                # Bloque 2: Plataforma móvil sobre un foso de pinchos (con espacio para evitar los pinchos al saltar a la plataforma)
                elif current_x < max_content_x * 0.6:
                    self.spikes.append(Spike(current_x + 50, SCREEN_HEIGHT - 50 - SPIKE_HEIGHT))
                    self.spikes.append(Spike(current_x + 90, SCREEN_HEIGHT - 50 - SPIKE_HEIGHT))
                    self.platforms.append(MovingPlatform(current_x + 180, SCREEN_HEIGHT - 180, PLATFORM_WIDTH, PLATFORM_HEIGHT, 100, 1.8)) # Mover más a la derecha
                    self.items.append(Item(current_x + 230, SCREEN_HEIGHT - 180 - ITEM_SIZE))
                    current_x += 400 + random.randint(0, 50)
                # Bloque 3: Obstáculo alto y salto a plataformas elevadas
                else:
                    self.obstacles.append(Obstacle(current_x + 50, SCREEN_HEIGHT - 50 - OBSTACLE_SIZE*2))
                    self.platforms.append(Platform(current_x + 250, SCREEN_HEIGHT - 200)) # Más distancia
                    self.platforms.append(Platform(current_x + 400, SCREEN_HEIGHT - 250))
                    self.items.append(Item(current_x + 420, SCREEN_HEIGHT - 250 - ITEM_SIZE))
                    current_x += 500 + random.randint(0, 50)

        # Nivel 5 (Arena): Desafíos verticales y saltos más exigentes.
        elif self.level_number == 5:
            current_x = 100
            while current_x < max_content_x:
                # Bloque 1: Escalada de plataformas con ítems (asegurando ancho mínimo)
                if current_x < max_content_x * 0.3:
                    for i in range(3):
                        plat_width = max(PLAYER_WIDTH + 10, PLATFORM_WIDTH - 40)
                        self.platforms.append(Platform(current_x + i * 120, SCREEN_HEIGHT - 100 - i * 70, width=plat_width))
                        self.items.append(Item(current_x + i * 120 + 5, SCREEN_HEIGHT - 100 - i * 70 - ITEM_SIZE))
                    current_x += 450 + random.randint(0, 50)
                # Bloque 2: Serie de plataformas móviles (espaciadas para saltos)
                elif current_x < max_content_x * 0.6:
                    self.platforms.append(MovingPlatform(current_x + 50, SCREEN_HEIGHT - 150, PLATFORM_WIDTH, PLATFORM_HEIGHT, 120, 1))
                    self.platforms.append(MovingPlatform(current_x + 300, SCREEN_HEIGHT - 250, PLATFORM_WIDTH, PLATFORM_HEIGHT, 100, 1.2)) # Más separación
                    self.items.append(Item(current_x + 100, SCREEN_HEIGHT - 150 - ITEM_SIZE))
                    self.items.append(Item(current_x + 350, SCREEN_HEIGHT - 250 - ITEM_SIZE))
                    current_x += 500 + random.randint(0, 50)
                # Bloque 3: Obstáculos en el suelo y salto a plataformas elevadas con pinchos (pinchos en la plataforma)
                else:
                    self.obstacles.append(Obstacle(current_x + 50, SCREEN_HEIGHT - 50 - OBSTACLE_SIZE))
                    self.obstacles.append(Obstacle(current_x + 120, SCREEN_HEIGHT - 50 - OBSTACLE_SIZE))
                    plat_x = current_x + 250
                    self.platforms.append(Platform(plat_x, SCREEN_HEIGHT - 200))
                    self.spikes.append(Spike(plat_x + 20, SCREEN_HEIGHT - 200 - SPIKE_HEIGHT)) # Pinchos en la plataforma
                    self.items.append(Item(plat_x + 50, SCREEN_HEIGHT - 200 - ITEM_SIZE))
                    current_x += 450 + random.randint(0, 50)

        # Nivel 6 (Hielo): Dificultad creciente con más pinchos y saltos complejos
        elif self.level_number == 6:
            current_x = 100
            while current_x < max_content_x:
                # Bloque 1: Plataformas descendentes con pinchos abajo (pinchos espaciados)
                if current_x < max_content_x * 0.3:
                    for i in range(3):
                        self.platforms.append(Platform(current_x + i * 150, SCREEN_HEIGHT - 100 + i * 50, width=PLATFORM_WIDTH))
                        # Pinchos en el suelo, con espacio para la plataforma
                        if i == 0: self.spikes.append(Spike(current_x + 20, SCREEN_HEIGHT - 50 - SPIKE_HEIGHT))
                        elif i == 1: self.spikes.append(Spike(current_x + 170, SCREEN_HEIGHT - 50 - SPIKE_HEIGHT))
                        else: self.spikes.append(Spike(current_x + 320, SCREEN_HEIGHT - 50 - SPIKE_HEIGHT))
                        self.items.append(Item(current_x + i * 150 + 40, SCREEN_HEIGHT - 100 + i * 50 - ITEM_SIZE))
                    current_x += 450 + random.randint(0, 50)
                # Bloque 2: Dos plataformas móviles seguidas (con buen espacio entre ellas)
                elif current_x < max_content_x * 0.6:
                    self.platforms.append(MovingPlatform(current_x + 50, SCREEN_HEIGHT - 150, PLATFORM_WIDTH, PLATFORM_HEIGHT, 100, 1.5))
                    self.platforms.append(MovingPlatform(current_x + 300, SCREEN_HEIGHT - 200, PLATFORM_WIDTH, PLATFORM_HEIGHT, 120, 1.8)) # Más separación
                    self.items.append(Item(current_x + 100, SCREEN_HEIGHT - 150 - ITEM_SIZE))
                    self.items.append(Item(current_x + 350, SCREEN_HEIGHT - 200 - ITEM_SIZE))
                    current_x += 450 + random.randint(0, 50)
                # Bloque 3: Zona con varios obstáculos y un salto largo (asegurando el salto)
                else:
                    self.obstacles.append(Obstacle(current_x + 50, SCREEN_HEIGHT - 50 - OBSTACLE_SIZE))
                    self.obstacles.append(Obstacle(current_x + 120, SCREEN_HEIGHT - 50 - OBSTACLE_SIZE))
                    self.platforms.append(Platform(current_x + 350, SCREEN_HEIGHT - 180, width=PLATFORM_WIDTH + 50)) # Mayor distancia de salto
                    self.items.append(Item(current_x + 400, SCREEN_HEIGHT - 180 - ITEM_SIZE))
                    current_x += 550 + random.randint(0, 50)

        # Nivel 7 (Normal): Enfoque en saltos de precisión y plataformas dispersas
        elif self.level_number == 7:
            current_x = 100
            while current_x < max_content_x:
                # Bloque 1: Plataformas espaciadas en diferentes alturas (ancho mínimo)
                if current_x < max_content_x * 0.3:
                    for i in range(3):
                        plat_width = max(PLAYER_WIDTH + 10, PLATFORM_WIDTH - 20)
                        self.platforms.append(Platform(current_x + i * 200, SCREEN_HEIGHT - 100 - i * 60, width=plat_width))
                        self.items.append(Item(current_x + i * 200 + 10, SCREEN_HEIGHT - 100 - i * 60 - ITEM_SIZE))
                    current_x += 600 + random.randint(0, 50)
                # Bloque 2: Plataforma móvil grande con obstáculos (obstáculos en la plataforma)
                elif current_x < max_content_x * 0.6:
                    mov_plat_x = current_x + 50
                    mov_plat_y = SCREEN_HEIGHT - 200
                    self.platforms.append(MovingPlatform(mov_plat_x, mov_plat_y, PLATFORM_WIDTH + 100, PLATFORM_HEIGHT, 200, 1))
                    self.obstacles.append(Obstacle(mov_plat_x + 50, mov_plat_y - OBSTACLE_SIZE)) # Obstáculo en la plataforma
                    self.items.append(Item(mov_plat_x + 150, mov_plat_y - ITEM_SIZE - 10))
                    current_x += 400 + random.randint(0, 50)
                # Bloque 3: Zona con múltiples pinchos en el suelo y una plataforma lejana (asegurando el salto)
                else:
                    for i in range(3):
                        self.spikes.append(Spike(current_x + 50 + i * 60, SCREEN_HEIGHT - 50 - SPIKE_HEIGHT))
                    self.platforms.append(Platform(current_x + 350, SCREEN_HEIGHT - 150)) # Mayor distancia de salto
                    self.items.append(Item(current_x + 370, SCREEN_HEIGHT - 150 - ITEM_SIZE))
                    current_x += 500 + random.randint(0, 50)

        # Nivel 8 (Arena): Dificultad alta, muchos obstáculos y saltos precisos sobre pinchos
        elif self.level_number == 8:
            current_x = 100
            while current_x < max_content_x:
                # Bloque 1: Serie de plataformas pequeñas con pinchos debajo (pinchos espaciados)
                if current_x < max_content_x * 0.3:
                    for i in range(3):
                        plat_width = max(PLAYER_WIDTH + 10, PLATFORM_WIDTH - 30)
                        self.platforms.append(Platform(current_x + i * 150, SCREEN_HEIGHT - 100 - i * 50, width=plat_width))
                        # Pinchos en el suelo, con espacio
                        if i == 0: self.spikes.append(Spike(current_x + 10, SCREEN_HEIGHT - 50 - SPIKE_HEIGHT))
                        elif i == 1: self.spikes.append(Spike(current_x + 160, SCREEN_HEIGHT - 50 - SPIKE_HEIGHT))
                        else: self.spikes.append(Spike(current_x + 310, SCREEN_HEIGHT - 50 - SPIKE_HEIGHT))
                        self.items.append(Item(current_x + i * 150 + 5, SCREEN_HEIGHT - 100 - i * 50 - ITEM_SIZE))
                    current_x += 500 + random.randint(0, 50)
                # Bloque 2: Plataforma móvil con salto a otra plataforma (con buen espacio)
                elif current_x < max_content_x * 0.6:
                    mov_plat_x = current_x + 50
                    mov_plat_y = SCREEN_HEIGHT - 180
                    self.platforms.append(MovingPlatform(mov_plat_x, mov_plat_y, PLATFORM_WIDTH, PLATFORM_HEIGHT, 150, 2))
                    self.platforms.append(Platform(mov_plat_x + 300, SCREEN_HEIGHT - 250)) # Más separación
                    self.items.append(Item(mov_plat_x + 320, SCREEN_HEIGHT - 250 - ITEM_SIZE))
                    current_x += 450 + random.randint(0, 50)
                # Bloque 3: Zona muy densa de obstáculos y plataformas (asegurando rutas posibles)
                else:
                    self.obstacles.append(Obstacle(current_x + 50, SCREEN_HEIGHT - 50 - OBSTACLE_SIZE))
                    self.platforms.append(Platform(current_x + 180, SCREEN_HEIGHT - 100)) # Plataforma elevada
                    self.spikes.append(Spike(current_x + 200, SCREEN_HEIGHT - 100 - SPIKE_HEIGHT)) # Pinchos en la plataforma
                    self.items.append(Item(current_x + 230, SCREEN_HEIGHT - 100 - ITEM_SIZE))
                    self.obstacles.append(Obstacle(current_x + 300, SCREEN_HEIGHT - 50 - OBSTACLE_SIZE))
                    current_x += 400 + random.randint(0, 50)

        # Nivel 9 (Hielo): Desafíos de deslizamiento, caídas y saltos complejos
        elif self.level_number == 9:
            current_x = 100
            while current_x < max_content_x:
                # Bloque 1: Plataformas muy pequeñas y separadas con pinchos (asegurando ancho mínimo y espacio)
                if current_x < max_content_x * 0.3:
                    for i in range(4):
                        plat_width = max(PLAYER_WIDTH + 10, PLATFORM_WIDTH - 50)
                        self.platforms.append(Platform(current_x + i * 150, SCREEN_HEIGHT - 100 - i * 70, width=plat_width))
                        self.spikes.append(Spike(current_x + i * 150 + 5, SCREEN_HEIGHT - 100 - i * 70 - SPIKE_HEIGHT)) # Pinchos en la plataforma
                        self.items.append(Item(current_x + i * 150 + 20, SCREEN_HEIGHT - 100 - i * 70 - ITEM_SIZE - 10))
                    current_x += 550 + random.randint(0, 50)
                # Bloque 2: Tres plataformas móviles en línea (con buen espaciado)
                elif current_x < max_content_x * 0.6:
                    self.platforms.append(MovingPlatform(current_x + 50, SCREEN_HEIGHT - 150, PLATFORM_WIDTH, PLATFORM_HEIGHT, 80, 2.5))
                    self.platforms.append(MovingPlatform(current_x + 250, SCREEN_HEIGHT - 200, PLATFORM_WIDTH, PLATFORM_HEIGHT, 100, 2))
                    self.platforms.append(MovingPlatform(current_x + 450, SCREEN_HEIGHT - 250, PLATFORM_WIDTH, PLATFORM_HEIGHT, 120, 1.5))
                    self.items.append(Item(current_x + 100, SCREEN_HEIGHT - 150 - ITEM_SIZE))
                    self.items.append(Item(current_x + 300, SCREEN_HEIGHT - 200 - ITEM_SIZE))
                    self.items.append(Item(current_x + 500, SCREEN_HEIGHT - 250 - ITEM_SIZE))
                    current_x += 550 + random.randint(0, 50)
                # Bloque 3: Zona con pinchos por todos lados y saltos de fe (asegurando el camino)
                else:
                    self.spikes.append(Spike(current_x + 50, SCREEN_HEIGHT - 50 - SPIKE_HEIGHT))
                    self.spikes.append(Spike(current_x + 100, SCREEN_HEIGHT - 50 - SPIKE_HEIGHT))
                    self.platforms.append(Platform(current_x + 200, SCREEN_HEIGHT - 150, width=PLATFORM_WIDTH-30))
                    self.spikes.append(Spike(current_x + 220, SCREEN_HEIGHT - 150 - SPIKE_HEIGHT)) # Pinchos en la plataforma
                    self.items.append(Item(current_x + 250, SCREEN_HEIGHT - 150 - ITEM_SIZE))
                    current_x += 450 + random.randint(0, 50)

        # Nivel 10 (Normal): El desafío final, una mezcla de todos los elementos
        elif self.level_number == 10:
            current_x = 100
            while current_x < max_content_x:
                # Bloque 1: Combinación de plataformas normales y móviles, con obstáculos
                if current_x < max_content_x * 0.3:
                    self.platforms.append(Platform(current_x + 50, SCREEN_HEIGHT - 100))
                    self.obstacles.append(Obstacle(current_x + 180, SCREEN_HEIGHT - 50 - OBSTACLE_SIZE)) # Más separado
                    self.platforms.append(MovingPlatform(current_x + 300, SCREEN_HEIGHT - 180, PLATFORM_WIDTH, PLATFORM_HEIGHT, 100, 1.5))
                    self.items.append(Item(current_x + 350, SCREEN_HEIGHT - 180 - ITEM_SIZE))
                    current_x += 450 + random.randint(0, 50)
                # Bloque 2: Zona de pinchos densa y plataformas elevadas (asegurando espacio de aterrizaje)
                elif current_x < max_content_x * 0.6:
                    for i in range(4):
                        self.spikes.append(Spike(current_x + 50 + i * 50, SCREEN_HEIGHT - 50 - SPIKE_HEIGHT))
                    plat_x = current_x + 350
                    self.platforms.append(Platform(plat_x, SCREEN_HEIGHT - 200, width=PLATFORM_WIDTH + 50))
                    self.items.append(Item(plat_x + 50, SCREEN_HEIGHT - 200 - ITEM_SIZE))
                    self.spikes.append(Spike(plat_x + 100, SCREEN_HEIGHT - 200 - SPIKE_HEIGHT)) # Pinchos en la plataforma, pero con espacio
                    current_x += 550 + random.randint(0, 50)
                # Bloque 3: Desafío de saltos entre plataformas móviles y obstáculos (asegurando rutas)
                else:
                    plat1_x = current_x + 50
                    self.platforms.append(MovingPlatform(plat1_x, SCREEN_HEIGHT - 150, PLATFORM_WIDTH - 20, PLATFORM_HEIGHT, 100, 2))
                    self.obstacles.append(Obstacle(plat1_x + 180, SCREEN_HEIGHT - 50 - OBSTACLE_SIZE))
                    plat2_x = current_x + 300
                    self.platforms.append(MovingPlatform(plat2_x, SCREEN_HEIGHT - 250, PLATFORM_WIDTH - 20, PLATFORM_HEIGHT, 120, 1.8))
                    self.items.append(Item(plat2_x + 50, SCREEN_HEIGHT - 250 - ITEM_SIZE))
                    current_x += 500 + random.randint(0, 50)


        self.finish_line = FinishLine(LEVEL_WIDTH - FINISH_LINE_WIDTH - 50, 0) 

    def update(self):
        # Actualizar plataformas móviles
        for platform in self.platforms:
            if isinstance(platform, MovingPlatform):
                platform.update()

    def draw(self, screen, camera_offset_x):
        if self.background_image:
            screen.blit(self.background_image, (-camera_offset_x, 0))
        else:
            if self.terrain_type == "normal":
                screen.fill(LIGHT_BLUE) 
            elif self.terrain_type == "sand":
                screen.fill((210, 180, 140)) 
            elif self.terrain_type == "ice":
                screen.fill((200, 230, 255)) 
            else:
                screen.fill(LIGHT_BLUE) 
            
        if self.terrain_type == "normal":
            ground_color = GRAY
        elif self.terrain_type == "sand":
            ground_color = YELLOW
        elif self.terrain_type == "ice":
            ground_color = LIGHT_BLUE
        else:
            ground_color = GRAY 
        pygame.draw.rect(screen, ground_color,
                         (self.ground_rect.x - camera_offset_x, self.ground_rect.y,
                          self.ground_rect.width, self.ground_rect.height))

        for item in self.items:
            item.draw(screen, camera_offset_x)
        for obstacle in self.obstacles:
            obstacle.draw(screen, camera_offset_x)
        for platform in self.platforms:
            platform.draw(screen, camera_offset_x)
        for spike in self.spikes:
            spike.draw(screen, camera_offset_x)
        if self.finish_line:
            self.finish_line.draw(screen, camera_offset_x)