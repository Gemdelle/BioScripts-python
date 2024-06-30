import pygame
import sys
import tkinter as tk
from moviepy.editor import VideoFileClip
import re

from ui.tkinter.JavaInterpreter import JavaInterpreterApp
from core.enemy import Enemy
from core.frog_happy import FrogHappy
from core.house_keeper import Housekeeper
from core.introduction_1_video import Introduction1Video
from core.introduction_2_video import Introduction2Video
from core.player import Player
from core.screens import Screens
from core.splash_video import SplashVideo
from ui.tkinter.father_screen import FatherScreen
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
screen_selected = Screens.SPLASH
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

# Initialize Housekeeper instance
housekeeper = Housekeeper()

# Calculate initial player position to center on the screen
initial_player_x = (Constants.SCREEN_WIDTH - Constants.TILE_SIZE) // 2
initial_player_y = (Constants.SCREEN_HEIGHT - Constants.TILE_SIZE) // 2

# Create player object
player = Player(initial_player_x, initial_player_y)

# Create Splash
splash_video = SplashVideo(screen_width, screen_height)

# Create Introduction1Video
introduction_1_video = None

# Create Introduction2Video
introduction_2_video = None

# Function to run the Tkinter app
def start_tkinter_app():
    global pygame_paused
    pygame_paused = True

    root = tk.Tk()
    JavaInterpreterApp(root)
    root.protocol("WM_DELETE_WINDOW", lambda: on_close(root))
    # Remove window decorations
    root.overrideredirect(True)

    # Set the size and position of the Tkinter window
    root.geometry(f"{screen_width}x{screen_height}+0+0")

    # Function to exit the application
    def close_app(event=None):
        on_close(root)

    # Bind the Escape key to exit the application
    root.bind('<Escape>', close_app)
    root.mainloop()

def start_father_screen():
    global pygame_paused
    pygame_paused = True

    root = tk.Tk()
    FatherScreen(root)
    root.protocol("WM_DELETE_WINDOW", lambda: on_close(root))
    # Remove window decorations
    root.overrideredirect(True)

    # Set the size and position of the Tkinter window
    root.geometry(f"{screen_width}x{screen_height}+0+0")

    # Function to exit the application
    def close_app(event=None):
        on_close(root)
        go_to_game_screen_meet_housekeeper()

    # Bind the Escape key to exit the application
    root.bind('<Escape>', close_app)
    root.mainloop()

# Function to handle Tkinter window close event
def on_close(root):
    root.destroy()
    resume_pygame()


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
housekeeper_talk_command_pattern = r"player\.talk\(housekeeper\)"

def wrong_command():
    player.wrong_command()

def go_to_game_screen_meet_housekeeper():
    global screen_selected
    print("CURRENT_SCREEN: GAME_SCREEN_MEET_HOUSEKEEPER")
    screen_selected = Screens.GAME_SCREEN_MEET_HOUSEKEEPER

def go_to_introduction_1():
    global screen_selected, introduction_1_video
    introduction_1_video = Introduction1Video(screen_width, screen_height)
    print("CURRENT_SCREEN: INTRODUCTION_1")
    screen_selected = Screens.INTRODUCTION_1

def go_to_introduction_2():
    global screen_selected, introduction_2_video
    introduction_2_video = Introduction2Video(screen_width, screen_height)
    print("CURRENT_SCREEN: INTRODUCTION_2")
    screen_selected = Screens.INTRODUCTION_2

def go_to_father_screen():
    global screen_selected
    print("CURRENT_SCREEN: FATHER")
    screen_selected = Screens.FATHER

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                text_area_visible = not text_area_visible
                text_input = ""
            elif text_area_visible:
                if event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]
                elif event.key == pygame.K_RETURN:
                    if re.match(enemy_talk_command_pattern, text_input):
                        enemy.talk(start_tkinter_app,wrong_command)
                    elif re.match(frog_talk_command_pattern, text_input):
                        print("FROG")
                    elif re.match(housekeeper_talk_command_pattern, text_input):
                        housekeeper.talk(start_tkinter_app,wrong_command)
                    else:
                        print("wrong_code")
                        player.wrong_command()
                    text_input = ""  # Clear text after executing command
                    text_area_visible = not text_area_visible
                elif event.unicode in allowed_characters:
                    text_input += event.unicode

    if screen_selected == Screens.GAME_SCREEN_MEET_HOUSEKEEPER:
        # Pause Pygame loop if Tkinter app is running or if text area is visible
        if pygame_paused or text_area_visible:
            if text_area_visible:
                # Draw text area background
                screen.blit(assets.code_console_bg, (10, screen_height - 400))
                text_surface = font.render(text_input, True, Constants.BLACK)
                screen.blit(text_surface, (text_area_rect.x + 5, text_area_rect.y + 5))
            continue

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
                elif tile_type == 6:  # HOUSEKEEPER
                    housekeeper.update_animation()
                    tile_x = col * Constants.TILE_SIZE + camera_offset_x
                    tile_y = row * Constants.TILE_SIZE + camera_offset_y
                    housekeeper.draw(screen, tile_x, tile_y)
                    player.update_collision_objects(tile_type, housekeeper)
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
        player.update(screen)
        enemy.check_collision(player)
        housekeeper.check_collision(player)
    elif screen_selected == Screens.SPLASH:
        splash_video.play_video(screen, go_to_introduction_1)
    elif screen_selected == Screens.INTRODUCTION_1:
        introduction_1_video.play_video(screen, go_to_introduction_2)
    elif screen_selected == Screens.INTRODUCTION_2:
        introduction_2_video.play_video(screen, go_to_father_screen)
    elif screen_selected == Screens.FATHER:
        start_father_screen()

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
sys.exit()
