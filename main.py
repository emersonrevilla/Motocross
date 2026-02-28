# main.py
import pygame
import sys
from constants import *
from player import Player
from level import Level
from ui import UI

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Moto Glóbulo Rojo")
clock = pygame.time.Clock()

# Game states
MENU = 0
GAME = 1
GAME_OVER = 2
CONTROLS = 3
LEVEL_COMPLETE_SCREEN = 4
GAME_WON = 5

current_state = MENU
selected_menu_option = "start"
current_level_number = 1
total_iron_collected = 0 # To keep track of total iron across levels

camera_offset_x = 0 # Camera offset for scrolling

player = Player(100, SCREEN_HEIGHT - 50 - PLAYER_HEIGHT)
current_level = Level(current_level_number)
ui = UI()

def reset_game():
    global player, current_level_number, current_level, total_iron_collected, camera_offset_x
    player = Player(100, SCREEN_HEIGHT - 50 - PLAYER_HEIGHT)
    current_level_number = 1
    current_level = Level(current_level_number)
    total_iron_collected = 0
    player.reset_iron() # Ensure player's iron count is also reset
    camera_offset_x = 0 # Reset camera on new game

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Level transition timer event
        if event.type == pygame.USEREVENT + 1: # After delay, move to next level
            current_level = Level(current_level_number)
            player.rect.x = 100 # Reset player position for new level
            player.rect.y = SCREEN_HEIGHT - 50 - PLAYER_HEIGHT
            player.vel_x = 0
            player.vel_y = 0
            camera_offset_x = 0 # Reset camera for new level
            current_state = GAME
            pygame.time.set_timer(pygame.USEREVENT + 1, 0) # Stop the timer

        if current_state == MENU:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if selected_menu_option == "exit":
                        selected_menu_option = "controls"
                    elif selected_menu_option == "controls":
                        selected_menu_option = "start"
                elif event.key == pygame.K_DOWN:
                    if selected_menu_option == "start":
                        selected_menu_option = "controls"
                    elif selected_menu_option == "controls":
                        selected_menu_option = "exit"
                elif event.key == pygame.K_RETURN:
                    if selected_menu_option == "start":
                        current_state = GAME
                        reset_game() # Ensure game starts fresh
                    elif selected_menu_option == "controls":
                        current_state = CONTROLS
                    elif event.key == pygame.K_c: # Allow 'C' to go to controls from menu
                        current_state = CONTROLS
                    elif selected_menu_option == "exit":
                        running = False
        elif current_state == CONTROLS:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    current_state = MENU
        elif current_state == GAME:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move_left()
                elif event.key == pygame.K_RIGHT:
                    player.move_right()
                elif event.key == pygame.K_UP:
                    player.jump()
                elif event.key == pygame.K_ESCAPE:
                    current_state = MENU # Return to menu from game
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.stop_moving_left()
                if event.key == pygame.K_RIGHT:
                    player.stop_moving_right()
        elif current_state == GAME_OVER:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    current_state = GAME
                elif event.key == pygame.K_ESCAPE:
                    current_state = MENU
                    selected_menu_option = "start"
        
        elif current_state == GAME_WON:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    current_state = GAME
                elif event.key == pygame.K_ESCAPE:
                    current_state = MENU
                    selected_menu_option = "start"

    # --- Game Logic ---
    if current_state == GAME:
        # Pass current_level.ground_rect to player.update
        player.update(current_level.terrain_type, current_level.platforms, current_level.ground_rect)

        # Update camera offset based on player's position
        # Keep player roughly in the center of the screen horizontally
        camera_offset_x = player.rect.x - SCREEN_WIDTH // 2
        # Clamp camera_offset_x to stay within level bounds (0 to LEVEL_WIDTH - SCREEN_WIDTH)
        if camera_offset_x < 0:
            camera_offset_x = 0
        if camera_offset_x > LEVEL_WIDTH - SCREEN_WIDTH:
            camera_offset_x = LEVEL_WIDTH - SCREEN_WIDTH
        
        # Check for item collection (iron)
        for item in current_level.items[:]: # Iterate over a copy to allow removal
            if player.rect.colliderect(item.rect):
                player.collect_item()
                player.heal(10) # Gain energy for collecting iron
                current_level.items.remove(item)
        
        # Check for obstacle collision (parasites)
        for obstacle in current_level.obstacles[:]:
            if player.rect.colliderect(obstacle.rect):
                player.take_damage(PARASITE_DAMAGE)
                current_level.obstacles.remove(obstacle) # Parasite disappears after contact
        
        # Check for spike collision
        for spike in current_level.spikes[:]:
            if player.rect.colliderect(spike.rect):
                player.take_damage(SPIKE_DAMAGE)
                # Spikes can remain or disappear;
                # decided to remain for persistent danger
                # If you want them to disappear:
                # current_level.spikes.remove(spike)

        # Game Over condition
        if player.energy <= 0:
            current_state = GAME_OVER
        
        # Level completion condition: Reach the finish line
        if current_level.finish_line and \
           player.rect.colliderect(current_level.finish_line.rect):
            total_iron_collected += player.collected_iron # Add current level's iron to total
            current_level_number += 1
            if current_level_number > MAX_LEVELS: # Max levels reached
                current_state = GAME_WON # Game is won!
            else:
                current_state = LEVEL_COMPLETE_SCREEN
                # Use the new constant for delay
                pygame.time.set_timer(pygame.USEREVENT + 1, LEVEL_TRANSITION_DELAY_MS)
            player.reset_iron() # Reset iron count for new level, but total is kept

    # --- Drawing ---
    screen.fill(WHITE) # Clear screen with white background

    if current_state == MENU:
        ui.draw_menu(screen, selected_menu_option)
    elif current_state == CONTROLS:
        ui.draw_controls_screen(screen)
    elif current_state == GAME:
        current_level.draw(screen, camera_offset_x) # Pass camera offset to level drawing
        player.draw(screen, camera_offset_x) # Pass camera offset to player drawing
        ui.draw_health_bar(screen, player.energy)
        ui.draw_score(screen, player.collected_iron)
    elif current_state == GAME_OVER:
        ui.draw_game_over(screen, total_iron_collected) # Show total iron collected
    elif current_state == LEVEL_COMPLETE_SCREEN:
        ui.draw_level_complete(screen, current_level_number - 1) # Display previous level as completed
    elif current_state == GAME_WON:
        ui.draw_game_won(screen, total_iron_collected) # Show total iron collected

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()