# ui.py
import pygame
from constants import * # Import constants for colors and screen dimensions

class UI:
    def __init__(self):
        # Initialize fonts
        self.font_small = pygame.font.Font(None, 30)
        self.font_medium = pygame.font.Font(None, 50)
        self.font_large = pygame.font.Font(None, 70)
        self.font_xlarge = pygame.font.Font(None, 100) # For titles

    def draw_health_bar(self, screen, current_health):
        health_bar_width = 200
        health_bar_height = 20
        health_bar_x = 10
        health_bar_y = 10

        # Background bar
        pygame.draw.rect(screen, BLACK, (health_bar_x, health_bar_y, health_bar_width, health_bar_height), 2) # Border
        
        # Fill bar based on current health
        fill_width = (current_health / MAX_ENERGY) * health_bar_width
        pygame.draw.rect(screen, RED, (health_bar_x, health_bar_y, fill_width, health_bar_height))

        # Health text
        health_text = self.font_small.render(f"Salud: {current_health}/{MAX_ENERGY}", True, BLACK)
        screen.blit(health_text, (health_bar_x + health_bar_width + 10, health_bar_y))

    def draw_score(self, screen, score):
        score_text = self.font_small.render(f"Hierro: {score}", True, BLACK)
        screen.blit(score_text, (10, 40)) # Below health bar

    def draw_menu(self, screen, selected_option):
        screen.fill(LIGHT_BLUE) # A softer background for the menu

        title_text = self.font_xlarge.render("Juego", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(title_text, title_rect)

        start_text_color = RED if selected_option == "start" else BLACK
        controls_text_color = RED if selected_option == "controls" else BLACK
        exit_text_color = RED if selected_option == "exit" else BLACK

        start_text = self.font_large.render("Iniciar Juego", True, start_text_color)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(start_text, start_rect)

        controls_text = self.font_large.render("Controles", True, controls_text_color)
        controls_rect = controls_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
        screen.blit(controls_text, controls_rect)

        exit_text = self.font_large.render("Salir", True, exit_text_color)
        exit_rect = exit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 140))
        screen.blit(exit_text, exit_rect)

    def draw_controls_screen(self, screen):
        screen.fill(LIGHT_BLUE)

        title_text = self.font_xlarge.render("Controles", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(title_text, title_rect)

        controls_lines = [
            "Flecha IZQUIERDA: Mover a la izquierda",
            "Flecha DERECHA: Mover a la derecha",
            "Flecha ARRIBA: Saltar",
            "ESC: Volver al menú principal",
            "",
            "¡Recolecta Hierro para sanarte y ganar puntos!",
            "¡Evita los Parásitos y Pinchos!"
        ]

        y_offset = SCREEN_HEIGHT // 2 - 80
        for line in controls_lines:
            text_surface = self.font_medium.render(line, True, BLACK)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            screen.blit(text_surface, text_rect)
            y_offset += 40

        back_text = self.font_small.render("Presiona ESC para volver", True, BLACK)
        screen.blit(back_text, (SCREEN_WIDTH // 2 - back_text.get_width() // 2, SCREEN_HEIGHT - 50))


    def draw_game_over(self, screen, final_score):
        screen.fill(RED) # Game Over screen is red
        game_over_text = self.font_xlarge.render("GAME OVER", True, WHITE)
        score_text = self.font_large.render(f"Hierro Total Recolectado: {final_score}", True, WHITE)
        restart_text = self.font_medium.render("Presiona 'R' para Reiniciar", True, WHITE)
        menu_text = self.font_medium.render("Presiona 'ESC' para ir al Menú", True, WHITE)

        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 130))

        screen.blit(game_over_text, game_over_rect)
        screen.blit(score_text, score_rect)
        screen.blit(restart_text, restart_rect)
        screen.blit(menu_text, menu_rect)

    def draw_level_complete(self, screen, completed_level_number):
        screen.fill(GREEN) # Green screen for level complete
        level_complete_text = self.font_xlarge.render(f"Nivel {completed_level_number} Completado!", True, WHITE)
        level_complete_rect = level_complete_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(level_complete_text, level_complete_rect)

        next_level_text = self.font_medium.render("Cargando siguiente nivel...", True, WHITE)
        next_level_rect = next_level_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(next_level_text, next_level_rect)

    def draw_game_won(self, screen, final_score):
        screen.fill(BLUE) # Blue screen for winning
        game_won_text = self.font_xlarge.render("¡Has Ganado el Juego!", True, WHITE)
        game_won_rect = game_won_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        screen.blit(game_won_text, game_won_rect)

        final_score_text = self.font_large.render(f"Hierro Total Recolectado: {final_score}", True, WHITE)
        final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(final_score_text, final_score_rect)

        restart_text = self.font_medium.render("Presiona 'R' para Jugar de Nuevo", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        screen.blit(restart_text, restart_rect)

        menu_text = self.font_medium.render("Presiona 'ESC' para ir al Menú", True, WHITE)
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 130))
        screen.blit(menu_text, menu_rect)