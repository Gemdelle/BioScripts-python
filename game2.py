import os
import random

import pygame
import sys
import threading
import tkinter as tk
import time
from moviepy.editor import VideoFileClip
import numpy as np
from PIL import Image
import pyglet
import imageio

from JavaInterpreter import JavaInterpreterApp
from utils.map_reference import tile_map
from utils.resource_path_util import resource_path
from utils.sound_manager import SoundManager

# Constants for Pygame
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TILE_SIZE = 40
MAP_WIDTH = 200  # Number of tiles wide
MAP_HEIGHT = 200  # Number of tiles high
MOVE_SPEED = TILE_SIZE // 6  # Number of pixels to move per second
ZOOM_SCALE = 1.5  # Zoom scale factor
PLAYER_SIZE = 180  # Player Size
HOLE_SIZE = 80  # Hole Size
PLANT_SIZE = 80  # Plant Size
FROG_SIZE = 80  # Plant Size

# Constants for Tkinter
JAVA_CODE_DELAY = 5  # Delay in seconds before starting Java code interpreter

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)


# Preload Sounds
sound_manager = SoundManager()
sound_manager.load_sound("splash_music", resource_path("assets\\sounds\\splash_music.mp3"))
sound_manager.set_volume("splash_music", 0.3)

#pyglet.options['win32_gdi_font'] = True
# Preload Fonts
#pyglet.font.add_file(resource_path("assets\\font\\ModerneFraktur.ttf"))

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

collision_objects = []

aspect_ratio = clip.size[0] / clip.size[1]
if screen_width / screen_height > aspect_ratio:
    new_height = screen_height
    new_width = int(aspect_ratio * new_height)
else:
    new_width = screen_width
    new_height = int(new_width / aspect_ratio)

def resize_frame(frame):
    pil_image = Image.fromarray(frame)
    pil_image = pil_image.resize((new_width, new_height), Image.LANCZOS)
    return np.array(pil_image)

# Function to convert video frames to Pygame surface
def frame_to_surface(frame):
    # Ensure correct orientation of the frame
    frame = np.rot90(frame)
    frame = np.flipud(frame)

    # Convert to Pygame surface
    surface = pygame.surfarray.make_surface(frame)
    return surface

# Load background image and scale it
try:
    background_img = pygame.image.load(resource_path("assets\\images\\game_map.png")).convert()
except pygame.error as e:
    print("Error loading background image:", e)
    sys.exit()

background_img = pygame.transform.scale(background_img, (MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE))
# Load tile images
hole_tile_img_1 = pygame.image.load(resource_path("assets\\images\\hole-1.png")).convert_alpha()
hole_tile_img_2 = pygame.image.load(resource_path("assets\\images\\hole-2.png")).convert_alpha()
hole_tile_img_3 = pygame.image.load(resource_path("assets\\images\\hole-3.png")).convert_alpha()
hole_tile_img_4 = pygame.image.load(resource_path("assets\\images\\hole-4.png")).convert_alpha()
plant_tile_img = pygame.image.load(resource_path("assets\\images\\plant.png")).convert_alpha()

# Scale tile images to TILE_SIZE
hole_tile_images = [
    pygame.transform.scale(hole_tile_img_1, (TILE_SIZE*4, TILE_SIZE*4)),
    pygame.transform.scale(hole_tile_img_2, (TILE_SIZE*4, TILE_SIZE*4)),
    pygame.transform.scale(hole_tile_img_3, (TILE_SIZE*4, TILE_SIZE*4)),
    pygame.transform.scale(hole_tile_img_4, (TILE_SIZE*4, TILE_SIZE*4))
]
plant_tile_img = pygame.transform.scale(plant_tile_img, (TILE_SIZE*4, TILE_SIZE*8))

player_gif = pygame.image.load(resource_path("assets\\gifs\\caterpillar_walk.gif")).convert_alpha()
player_gif = pygame.transform.scale(player_gif, (PLAYER_SIZE, PLAYER_SIZE))
frame_duration = 60  # milliseconds per frame
# Load caterpillar frames into Pygame
caterpillar_walk_frames = []
caterpillar_frame_index = 1
while True:
    frame_path = os.path.join(f"./assets/gifs/frames/caterpillar_walk", f'caterpillar_walk_{caterpillar_frame_index}.png')
    if not os.path.exists(frame_path):
        break
    surf = pygame.image.load(frame_path).convert_alpha()
    surf = pygame.transform.scale(surf, (PLAYER_SIZE, PLAYER_SIZE))
    caterpillar_walk_frames.append(surf)
    caterpillar_frame_index += 1

# Variables for animation
caterpillar_frame_index = 0

# Load frog_neutral_1 frames into Pygame
frog_happy_frames = []
frog_happy_frame_index = 1
while True:
    frame_path = os.path.join(f"./assets/gifs/frames/frog_happy", f'frog_happy_{frog_happy_frame_index}.png')
    if not os.path.exists(frame_path):
        break
    surf = pygame.image.load(frame_path).convert_alpha()
    surf = pygame.transform.scale(surf, (FROG_SIZE, FROG_SIZE))
    frog_happy_frames.append(surf)
    frog_happy_frame_index += 1

# Variables for animation
frog_happy_frame_index = 0



# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = player_gif
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

# Calculate initial player position to center on the screen
initial_player_x = (SCREEN_WIDTH - TILE_SIZE) // 2
initial_player_y = (SCREEN_HEIGHT - TILE_SIZE) // 2

# Create player object
player = Player(initial_player_x, initial_player_y)

for row in range(MAP_HEIGHT):
    for col in range(MAP_WIDTH):
        tile_type = tile_map[row][col]
        if tile_type == 9:  # Orange tile
            tile_img = hole_tile_images[2]
            # Calculate tile position adjusted by camera offset
            camera_offset_x = SCREEN_WIDTH // 2 - player.rect.centerx
            camera_offset_y = SCREEN_HEIGHT // 2 - player.rect.centery
            tile_x = col * TILE_SIZE + camera_offset_x
            tile_y = row * TILE_SIZE + camera_offset_y

            # Store reference to collision object
            collision_rect = pygame.Rect(tile_x, tile_y, tile_img.get_rect().w, tile_img.get_rect().h /2)
            collision_objects.append(collision_rect)

# Function to run the Tkinter app
def start_tkinter_app(width, height):
    global pygame_paused
    pygame_paused = True

    root = tk.Tk()
    app = JavaInterpreterApp(root)
    root.protocol("WM_DELETE_WINDOW", lambda: on_close(root))
    # Remove window decorations
    root.overrideredirect(True)

    # Set the size and position of the Tkinter window
    root.geometry(f"{width}x{height}+0+0")

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

# Thread to start Tkinter app after delay
def start_tkinter_thread():
    return
    time.sleep(JAVA_CODE_DELAY)
    start_tkinter_app(screen_width, screen_height)

tkinter_thread = threading.Thread(target=start_tkinter_thread)
tkinter_thread.start()

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

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Pause Pygame loop if Tkinter app is running
    if pygame_paused:
        continue

    # Handle player movement
    keys = pygame.key.get_pressed()
    move_x = 0
    move_y = 0
    if keys[pygame.K_a]:
        move_x -= MOVE_SPEED
    if keys[pygame.K_d]:
        move_x += MOVE_SPEED
    if keys[pygame.K_w]:
        move_y -= MOVE_SPEED
    if keys[pygame.K_s]:
        move_y += MOVE_SPEED

    current_time = pygame.time.get_ticks() / 1000.0
    if current_time >= clip.duration:
        # Move the player
        # Calculate the player's new position
        new_x = player.rect.x + move_x
        new_y = player.rect.y + move_y
        player_rect = pygame.Rect(new_x, new_y, PLAYER_SIZE, PLAYER_SIZE)

        # Check collision with each object in collision_objects array
        collision_detected = False
        for obj_rect in collision_objects:
            if player_rect.colliderect(obj_rect):
                # Collision detected, player stays in the same position
                collision_detected = True
                break

        # If no collision detected, move the player
        if not collision_detected:
            player.move(move_x, move_y)

        # Ensure player stays within bounds of the map
        player.rect.x = max(0, min(player.rect.x, MAP_WIDTH * TILE_SIZE - PLAYER_SIZE - 65))
        player.rect.y = max(0, min(player.rect.y, MAP_HEIGHT * TILE_SIZE - PLAYER_SIZE - 25))

        # Calculate camera offset to center the player on the screen
        camera_offset_x = SCREEN_WIDTH // 2 - player.rect.centerx
        camera_offset_y = SCREEN_HEIGHT // 2 - player.rect.centery

        # Limit camera movement to stay within the map bounds
        camera_offset_x = min(0, camera_offset_x)  # Limit left side
        camera_offset_x = max(SCREEN_WIDTH - MAP_WIDTH * TILE_SIZE + 700, camera_offset_x)  # Limit right side
        camera_offset_y = min(0, camera_offset_y)  # Limit top side
        camera_offset_y = max(SCREEN_HEIGHT - MAP_HEIGHT * TILE_SIZE + 380, camera_offset_y)  # Limit bottom side

        # Draw the background image
        screen.blit(background_img, (camera_offset_x, camera_offset_y))
        current_time_2 = pygame.time.get_ticks()
        # Draw colored tiles on the map
        for row in range(MAP_HEIGHT):
            for col in range(MAP_WIDTH):
                tile_type = tile_map[row][col]
                if tile_type == 1:  # HOLE
                    tile_img = hole_tile_images[0]
                elif tile_type == 2:  # PLANT
                    tile_img = plant_tile_img
                elif tile_type == 5:  # FROG
                    frog_happy_frame_index = (current_time_2 // frame_duration) % len(frog_happy_frames)
                    tile_x = col * TILE_SIZE + camera_offset_x
                    tile_y = row * TILE_SIZE + camera_offset_y
                    # Draw current frame
                    screen.blit(frog_happy_frames[int(frog_happy_frame_index)], (tile_x, tile_y))  # Draw current frame
                    continue
                elif tile_type == 9:  # BLOCKER
                    tile_img = hole_tile_images[2]
                    # Calculate tile position adjusted by camera offset
                    tile_x = col * TILE_SIZE + camera_offset_x
                    tile_y = row * TILE_SIZE + camera_offset_y

                    # Draw the tile image
                    screen.blit(tile_img, (tile_x, tile_y))
                    continue
                else:
                    continue  # Skip drawing if the tile is not green or orange

                # Calculate tile position adjusted by camera offset
                tile_x = col * TILE_SIZE + camera_offset_x
                tile_y = row * TILE_SIZE + camera_offset_y

                # Draw the tile image
                screen.blit(tile_img, (tile_x, tile_y))

        caterpillar_frame_index = (current_time_2 // frame_duration) % len(caterpillar_walk_frames)
        # Draw current frame
        screen.blit(caterpillar_walk_frames[int(caterpillar_frame_index)], (player.rect.x + camera_offset_x, player.rect.y + camera_offset_y))  # Draw current frame

        # Update display
        pygame.display.flip()

        # Cap frame rate
        clock.tick(60)
    else:
        if not is_video_playing:
            # Play audio
            sound_manager.play_sound("splash_music")
            is_video_playing = True
        current_frame = clip.get_frame(current_time)

        # Resize the frame manually
        current_frame = resize_frame(current_frame)

        # Convert the frame to a Pygame surface
        surface = frame_to_surface(current_frame)

        # Fill the screen with black
        screen.fill((0, 0, 0))

        # Center the video on the screen
        screen.blit(surface, ((screen_width - new_width) // 2, (screen_height - new_height) // 2))
        # Update display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(65)

# Quit Pygame
pygame.quit()
sys.exit()
