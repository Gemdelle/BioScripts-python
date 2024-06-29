import os
import pygame
import sys
import threading
import tkinter as tk
import time
from moviepy.editor import VideoFileClip
import numpy as np
from PIL import Image
import re

from JavaInterpreter import JavaInterpreterApp
from core.enemy import Enemy
from core.frog_happy import FrogHappy
from core.player import Player
from core.splash_video import SplashVideo
from utils.assets_preloader import AssetsPreloader
from utils.constants import Constants
from utils.map_reference import tile_map
from utils.resource_path_util import resource_path
from utils.sound_manager import SoundManager

# Preload Sounds
sound_manager = SoundManager()
sound_manager.load_sound("splash_music", resource_path("assets\\sounds\\splash_music.mp3"))
sound_manager.set_volume("splash_music", 0.3)

# Initialize Pygame
pygame.init()
# Initialize Pygame mixer for audio
pygame.mixer.init()

info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h

# Set up the window to occupy the maximum resolution without full screen
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("BioScripts")
clock = pygame.time.Clock()

clip = VideoFileClip(resource_path("assets\\videos\\splash.mp4"))
assets = AssetsPreloader()
assets.preload()

# Load background image and scale it
try:
    background_img = pygame.image.load(resource_path("assets\\images\\game_map.png")).convert()
except pygame.error as e:
    print("Error loading background image:", e)
    sys.exit()

background_img = pygame.transform.scale(background_img, (Constants.MAP_WIDTH * Constants.TILE_SIZE, Constants.TILE_SIZE * Constants.MAP_HEIGHT))

# Initialize Frog instance
frog = FrogHappy()

# Initialize Enemy instance
enemy = Enemy()

# Calculate initial player position to center on the screen
initial_player_x = (Constants.SCREEN_WIDTH - Constants.TILE_SIZE) // 2
initial_player_y = (Constants.SCREEN_HEIGHT - Constants.TILE_SIZE) // 2

# Create player object
player = Player(initial_player_x, initial_player_y)

# Create Splash
splash_video = SplashVideo(screen_width, screen_height)

# Function to run the Tkinter app
def start_tkinter_app():
    global pygame_paused
    pygame_paused = True

    root = tk.Tk()
    app = JavaInterpreterApp(root)
    root.protocol("WM_DELETE_WINDOW", lambda: on_close(root))
    # Remove window decorations
    root.overrideredirect(True)

    # Set the size and position of the Tkinter window
    root.geometry(f"{screen_width}x{screen_height}+0+0")

    # Function to exit the application
    def close_app(event=None):
        on_close(root)
        root.destroy()

    # Bind the Escape key to exit the application
    root.bind('<Escape>', close_app)
    root.mainloop()

# Function to handle Tkinter window close event
def on_close(root):
    root.destroy()
    resume_pygame()


# tkinter_thread = threading.Thread(target=start_tkinter_app)
# tkinter_thread.start()

# Flag to pause Pygame loop
pygame_paused = False

# Function to pause Pygame loop
def pause_pygame():
    global pygame_paused
    pygame_paused = True

# Function to resume Pygame loop
def resume_pygame():
    global pygame_paused
    pygame_paused = False

is_video_playing = False
is_clock_reseted = False

# Text area for displaying key presses
text_area_rect = pygame.Rect(70, screen_height - 210, 400, 200)
font = pygame.font.Font(None, 40)
text_area_visible = False
text_input = ""

# Allowed characters (alphanumeric and special characters)
allowed_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;':,.<>?/`~\"\\ "

# Regex patterns for commands
enemy_talk_command_pattern = r"player\.talk\(enemy\)"
frog_talk_command_pattern = r"player\.talk\(frog\)"

# Game loop
running = True
initial_time = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                text_area_visible = not text_area_visible
                text_input = ""  # Clear text when toggling
            elif text_area_visible:
                if event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]
                elif event.key == pygame.K_RETURN:
                    if re.match(enemy_talk_command_pattern, text_input):
                        enemy.talk(start_tkinter_app)
                    elif re.match(frog_talk_command_pattern, text_input):
                        print("FROG")
                    else:
                        print("wrong_code")
                        player.wrong_command()
                    text_input = ""  # Clear text after executing command
                    text_area_visible = not text_area_visible
                elif event.unicode in allowed_characters:
                    text_input += event.unicode

    if not is_clock_reseted:
        initial_time = pygame.time.get_ticks()
        is_clock_reseted = True

    # Pause Pygame loop if Tkinter app is running or if text area is visible
    if pygame_paused or text_area_visible:
        if text_area_visible:
            # Draw text area background
            screen.blit(assets.code_console_bg, (10, screen_height - 400))
            text_surface = font.render(text_input, True, Constants.BLACK)
            screen.blit(text_surface, (text_area_rect.x + 5, text_area_rect.y + 5))
            pygame.display.flip()
        continue

    # Handle player movement
    keys = pygame.key.get_pressed()
    move_x, move_y = player.handle_movement(keys)

    current_time = (pygame.time.get_ticks() - initial_time) / 1000.0

    if current_time >= clip.duration:
        camera_offset_x, camera_offset_y = player.get_camera_offset()

        screen.blit(background_img, (camera_offset_x, camera_offset_y))

        for row in range(Constants.MAP_HEIGHT):
            for col in range(Constants.MAP_WIDTH):
                tile_type = tile_map[row][col]
                if tile_type == 1:  # HOLE
                    tile_img = assets.HOLE_TILE_IMAGES[0]
                elif tile_type == 2:  # PLANT
                    tile_img = assets.PLANT_TILE_IMAGES[0]
                elif tile_type == 5:  # FROG
                    frog.update_animation()
                    tile_x = col * Constants.TILE_SIZE + camera_offset_x
                    tile_y = row * Constants.TILE_SIZE + camera_offset_y
                    frog.draw(screen, tile_x, tile_y)
                    continue
                elif tile_type == 7:  # ENEMY
                    enemy.update_animation()
                    tile_x = col * Constants.TILE_SIZE + camera_offset_x
                    tile_y = row * Constants.TILE_SIZE + camera_offset_y
                    enemy.draw(screen, tile_x, tile_y)
                    player.update_collision_objects(tile_type, enemy)
                    continue
                elif tile_type == 9:  # BLOCKER
                    tile_img = assets.HOLE_TILE_IMAGES[2]
                    tile_x = col * Constants.TILE_SIZE + camera_offset_x
                    tile_y = row * Constants.TILE_SIZE + camera_offset_y
                    screen.blit(tile_img, (tile_x, tile_y))
                    continue
                else:
                    continue

                tile_x = col * Constants.TILE_SIZE + camera_offset_x
                tile_y = row * Constants.TILE_SIZE + camera_offset_y
                screen.blit(tile_img, (tile_x, tile_y))

        player.draw(screen, camera_offset_x, camera_offset_y)
        player.update(keys, move_x, move_y, screen)
        enemy.check_collision(player)

        pygame.display.flip()
        clock.tick(60)
    else:
        # Splash Video
        if not is_video_playing:
            sound_manager.play_sound("splash_music")
            is_video_playing = True
        splash_video.play_video(screen, clock)

pygame.quit()
sys.exit()
