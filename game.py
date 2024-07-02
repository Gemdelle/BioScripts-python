import os

import psutil
import pygame
import sys
import tkinter as tk
from moviepy.editor import VideoFileClip
import re

from pygame import MOUSEBUTTONDOWN

from core.analyze_character_enemy import AnalyzeCharacterEnemy
from core.analyze_character_flower import AnalyzeFlower
from core.analyze_character_frog import AnalyzeCharacterFrog
from core.analyze_character_housekeeper import AnalyzeCharacterHousekeeper
from core.analyze_character_shrub import AnalyzeShrub
from core.analyze_mushroom import AnalyzeMushroom
from core.analyze_small_tree import AnalyzeSmallTree
from core.analyze_tree import AnalyzeTree
from core.blue_tree import BlueTree
from core.caterpillar_dialog import CaterpillarDialog
from core.caterpillar_dialog_grey import CaterpillarDialogGrey
from core.disease_bar import AnalyzeDiseaseBar
from core.enemy_dialog import EnemyDialog
from core.enemy_dialog_grey import EnemyDialogGrey
from core.flower_1 import Flower1
from core.flower_2 import Flower2
from core.frog_angry import FrogAngry
from core.frog_neutral_1 import FrogNautral1
from core.frog_neutral_2 import FrogNautral2
from core.hole_1 import Hole1
from core.hole_2 import Hole2
from core.hole_3 import Hole3
from core.hole_4 import Hole4
from core.house_keeper_dialog import HousekeeperDialog
from core.house_keeper_dialog_grey import HousekeeperDialogGrey
from core.mushroom_plant import MushroomPlant
from core.red_tree import RedTree
from core.shrub_1 import Shrub1
from core.shrub_2 import Shrub2
from core.small_tree_1 import SmallTree1
from core.small_tree_2 import SmallTree2
from ui.tkinter.JavaInterpreter import JavaInterpreterApp
from core.enemy import Enemy
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
screen_selected = Screens.GAME_SCREEN_MEET_HOUSEKEEPER
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

# Initialize Enemy instance
enemy = Enemy()

# Initialize Housekeeper instance
housekeeper = Housekeeper()



# Calculate initial player position to center on the screen
initial_player_x = (Constants.SCREEN_WIDTH - Constants.TILE_SIZE) // 2 + 420
initial_player_y = (Constants.SCREEN_HEIGHT - Constants.TILE_SIZE) // 2 + 570

# Create player object
player = Player(initial_player_x, initial_player_y)

# Create Splash
splash_video = SplashVideo(screen_width, screen_height)

# Create Introduction1Video
introduction_1_video = None

# Create Introduction2Video
introduction_2_video = None

# Initialize objects using list comprehensions
red_tree = {str(i): RedTree() for i in range(72, 75)}
blue_tree = {str(i): BlueTree() for i in range(68, 72)}
small_tree = {str(i): (SmallTree1() if i % 2 == 0 else SmallTree2()) for i in range(64, 68)}
shrubs = {str(i): (Shrub2() if i % 2 == 0 else Shrub1()) for i in range(59, 64)}
flowers = {str(i): (Flower2() if i % 2 == 0 else Flower1()) for i in range(54, 59)}
soil = {str(i): (Hole1() if i % 4 == 1 else Hole2() if i % 4 == 2 else Hole3() if i % 4 == 3 else Hole4()) for i in range(1, 13)}
mushroom_plants = {str(i): MushroomPlant() for i in range(29, 54)}
frogs = {str(i): (FrogNautral1() if i % 3 == 0 else FrogNautral2() if i % 3 == 1 else FrogAngry()) for i in range(15, 29)}

# ANALYSYS VARIABLES
analyze_house_keeper = AnalyzeCharacterHousekeeper()
analyzing_house_keeper = False

analyze_enemy = AnalyzeCharacterEnemy()
analyzing_enemy = False

analyze_frog = AnalyzeCharacterFrog()
analyzing_frog = False

analyze_mushroom = AnalyzeMushroom()
analyzing_mushroom = False

analyze_flower = AnalyzeFlower()
analyzing_flower = False

analyze_shrub = AnalyzeShrub()
analyzing_shrub = False

analyze_small_tree = AnalyzeSmallTree()
analyzing_small_tree = False

analyze_tree = AnalyzeTree()
analyzing_tree = False

disease_bar = AnalyzeDiseaseBar()

housekeeper_dialog = HousekeeperDialog()
housekeeper_dialog_grey = HousekeeperDialogGrey()

enemy_dialog = EnemyDialog()
enemy_dialog_grey = EnemyDialogGrey()

caterpillar_dialog = CaterpillarDialog()
caterpillar_dialog_grey = CaterpillarDialogGrey()

def print_memory_usage():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    print(f"Memory Usage: {mem_info.rss / 1024 / 1024:.2f} MB")

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
father_screen_ongoing = False
def start_father_screen():
    global pygame_paused, father_screen_ongoing
    pygame_paused = True
    if father_screen_ongoing:
        return
    father_screen_ongoing = True
    root = tk.Tk()
    def close_app(event=None):
        on_close(root)

    FatherScreen(root, close_app)
    root.protocol("WM_DELETE_WINDOW", lambda: on_close(root))
    # Remove window decorations
    root.overrideredirect(True)

    # Set the size and position of the Tkinter window
    root.geometry(f"{screen_width}x{screen_height}+0+0")

    # Bind the Escape key to exit the application
    root.bind('<Escape>', close_app)
    root.mainloop()

# Function to handle Tkinter window close event
def on_close(root):
    global father_screen_ongoing
    resume_pygame()
    go_to_game_screen_meet_housekeeper()
    root.destroy()
    father_screen_ongoing = False


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
text_area_rect = pygame.Rect(180, screen_height - 320, 400, 200)
font_path = os.path.join("assets", "fonts", "BavarianCrown.ttf")
font = pygame.font.Font(font_path, 32)
text_area_visible = False
text_input = ""

# Allowed characters (alphanumeric and special characters)
allowed_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;':,.<>?/`~\"\\ "

# Regex patterns for commands
enemy_talk_command_pattern = r"player\.talk\(enemy\)"
frog_talk_command_pattern = r"player\.talk\(frog\)"
housekeeper_talk_command_pattern = r"player\.talk\(housekeeper\)"
harvest_mushroom_command_pattern = r"player\.harvest\(mushroom\)"
harvest_flower_command_pattern = r"player\.harvest\(flower\)"
harvest_shrub_command_pattern = r"player\.harvest\(shrub\)"
harvest_small_tree_command_pattern = r"player\.harvest\(small_tree\)"
harvest_tree_command_pattern = r"player\.harvest\(tree\)"

plant_hole_command_pattern = r"player\.plant\(hole\)"

analyze_housekeeper_command_pattern = r"player\.analyze\(housekeeper\)"
analyze_enemy_command_pattern = r"player\.analyze\(enemy\)"
analyze_frog_command_pattern = r"player\.analyze\(frog\)"
analyze_mushroom_command_pattern = r"player\.analyze\(mushroom\)"
analyze_flower_command_pattern = r"player\.analyze\(flower\)"
analyze_shrub_command_pattern = r"player\.analyze\(shrub\)"
analyze_small_tree_command_pattern = r"player\.analyze\(small_tree\)"
analyze_tree_command_pattern = r"player\.analyze\(red_tree\)"

print_memmory = False
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

harvested_fruits = []

def on_successful_harvest(fruit):
    harvested_fruits.append(fruit)

# Game loop
running = True

show_overlay_analyze = False
show_overlay_dialog = False
dialog_progression = 0
def draw_item_container_1():
    base = 395
    screen.blit(assets.item_container_img, (base, 190))
    if len(harvested_fruits) > 0:
        if harvested_fruits[0] == "flower":
            screen.blit(assets.fruit_flower_img, (base, 190))
        elif harvested_fruits[0] == "mushroom":
            screen.blit(assets.fruit_mushroom_img, (base, 190))
        elif harvested_fruits[0] == "shrub":
            screen.blit(assets.fruit_shrub_img, (base, 190))
        elif harvested_fruits[0] == "small-tree":
            screen.blit(assets.fruit_small_tree_img, (base, 190))
        elif harvested_fruits[0] == "tree":
            screen.blit(assets.fruit_tree_img, (base, 190))


def draw_item_container_2():
    base = 395
    suma = 95
    screen.blit(assets.item_container_img, (base + suma, 190))
    if len(harvested_fruits) > 1:
        if harvested_fruits[1] == "flower":
            screen.blit(assets.fruit_flower_img, (base + suma, 190))
        elif harvested_fruits[1] == "mushroom":
            screen.blit(assets.fruit_mushroom_img, (base + suma, 190))
        elif harvested_fruits[1] == "shrub":
            screen.blit(assets.fruit_shrub_img, (base + suma, 190))
        elif harvested_fruits[1] == "small-tree":
            screen.blit(assets.fruit_small_tree_img, (base + suma, 190))
        elif harvested_fruits[1] == "tree":
            screen.blit(assets.fruit_tree_img, (base + suma, 190))

def draw_item_container_3():
    base = 395
    suma = 95
    screen.blit(assets.item_container_img, (base + suma * 2, 190))
    if len(harvested_fruits) > 2:
        if harvested_fruits[2] == "flower":
            screen.blit(assets.fruit_flower_img, (base + suma * 2, 190))
        elif harvested_fruits[2] == "mushroom":
            screen.blit(assets.fruit_mushroom_img, (base + suma * 2, 190))
        elif harvested_fruits[2] == "shrub":
            screen.blit(assets.fruit_shrub_img, (base + suma * 2, 190))
        elif harvested_fruits[2] == "small-tree":
            screen.blit(assets.fruit_small_tree_img, (base + suma * 2, 190))
        elif harvested_fruits[2] == "tree":
            screen.blit(assets.fruit_tree_img, (base + suma * 2, 190))


def draw_item_container_4():
    base = 395
    suma = 95
    screen.blit(assets.item_container_img, (base + suma * 3, 190))
    if len(harvested_fruits) > 3:
        if harvested_fruits[3] == "flower":
            screen.blit(assets.fruit_flower_img, (base + suma * 3, 190))
        elif harvested_fruits[3] == "mushroom":
            screen.blit(assets.fruit_mushroom_img, (base + suma * 3, 190))
        elif harvested_fruits[3] == "shrub":
            screen.blit(assets.fruit_shrub_img, (base + suma * 3, 190))
        elif harvested_fruits[3] == "small-tree":
            screen.blit(assets.fruit_small_tree_img, (base + suma * 3, 190))
        elif harvested_fruits[3] == "tree":
            screen.blit(assets.fruit_tree_img, (base + suma * 3, 190))


def draw_item_container_5():
    base = 395
    suma = 95
    screen.blit(assets.item_container_img, (base + suma * 4, 190))
    if len(harvested_fruits) > 4:
        if harvested_fruits[4] == "flower":
            screen.blit(assets.fruit_flower_img, (base + suma * 4, 190))
        elif harvested_fruits[4] == "mushroom":
            screen.blit(assets.fruit_mushroom_img, (base + suma * 4, 190))
        elif harvested_fruits[4] == "shrub":
            screen.blit(assets.fruit_shrub_img, (base + suma * 4, 190))
        elif harvested_fruits[4] == "small-tree":
            screen.blit(assets.fruit_small_tree_img, (base + suma * 4, 190))
        elif harvested_fruits[4] == "tree":
            screen.blit(assets.fruit_tree_img, (base + suma * 4, 190))


def draw_item_container_6():
    base = 395
    suma = 95
    screen.blit(assets.item_container_img, (base + suma * 5, 190))
    if len(harvested_fruits) > 5:
        if harvested_fruits[5] == "flower":
            screen.blit(assets.fruit_flower_img, (base + suma * 5, 190))
        elif harvested_fruits[5] == "mushroom":
            screen.blit(assets.fruit_mushroom_img, (base + suma * 5, 190))
        elif harvested_fruits[5] == "shrub":
            screen.blit(assets.fruit_shrub_img, (base + suma * 5, 190))
        elif harvested_fruits[5] == "small-tree":
            screen.blit(assets.fruit_small_tree_img, (base + suma * 5, 190))
        elif harvested_fruits[5] == "tree":
            screen.blit(assets.fruit_tree_img, (base + suma * 5, 190))


def draw_analyze_house_keeper():
    global surf, analyze_house_keeper, screen
    OPACITY = 180
    overlay = pygame.Surface((screen_width, screen_height))
    overlay.set_alpha(OPACITY)
    overlay.fill(Constants.BLACK)
    screen.blit(overlay, (0, 0))
    surf = pygame.transform.flip(assets.corner_img, True, True)
    screen.blit(surf, (0, 0))
    #pop_up_coordinates = (screen_width // 2 - (assets.housekeeper_analyze_img.get_rect().width // 2), screen_height // 2 - (assets.mushroom_analyze_img.get_rect().height // 2))
    pop_up_coordinates = (270,50)
    screen.blit(assets.housekeeper_analyze_img, pop_up_coordinates)
    analyze_house_keeper.update_animation()
    #analyze_house_keeper.draw(screen, pop_up_coordinates[0] + (392 // 2), pop_up_coordinates[1] - (464 // 2)) # drawing
    analyze_house_keeper.draw(screen, pop_up_coordinates[0] + 270, pop_up_coordinates[1] - 300) # drawing

def draw_analyze_enemy():
    global surf, analyze_enemy, screen
    OPACITY = 180
    overlay = pygame.Surface((screen_width, screen_height))
    overlay.set_alpha(OPACITY)
    overlay.fill(Constants.BLACK)
    screen.blit(overlay, (0, 0))
    surf = pygame.transform.flip(assets.corner_img, True, True)
    screen.blit(surf, (0, 0))
    #pop_up_coordinates = (screen_width // 2 - (assets.housekeeper_analyze_img.get_rect().width // 2), screen_height // 2 - (assets.mushroom_analyze_img.get_rect().height // 2))
    pop_up_coordinates = (270,50)
    screen.blit(assets.enemy_analyze_img, pop_up_coordinates)
    analyze_enemy.update_animation()
    #analyze_house_keeper.draw(screen, pop_up_coordinates[0] + (392 // 2), pop_up_coordinates[1] - (464 // 2)) # drawing
    analyze_enemy.draw(screen, pop_up_coordinates[0] + 270, pop_up_coordinates[1] - 300) # drawing

def draw_analyze_frog():
    global surf, analyze_frog, screen
    OPACITY = 180
    overlay = pygame.Surface((screen_width, screen_height))
    overlay.set_alpha(OPACITY)
    overlay.fill(Constants.BLACK)
    screen.blit(overlay, (0, 0))
    surf = pygame.transform.flip(assets.corner_img, True, True)
    screen.blit(surf, (0, 0))
    #pop_up_coordinates = (screen_width // 2 - (assets.housekeeper_analyze_img.get_rect().width // 2), screen_height // 2 - (assets.mushroom_analyze_img.get_rect().height // 2))
    pop_up_coordinates = (270,50)
    screen.blit(assets.frog_analyze_img, pop_up_coordinates)
    analyze_frog.update_animation()
    #analyze_house_keeper.draw(screen, pop_up_coordinates[0] + (392 // 2), pop_up_coordinates[1] - (464 // 2)) # drawing
    analyze_frog.draw(screen, pop_up_coordinates[0] + 270, pop_up_coordinates[1] - 300) # drawing

def draw_analyze_mushroom():
    global surf, analyze_mushroom, screen
    OPACITY = 180
    overlay = pygame.Surface((screen_width, screen_height))
    overlay.set_alpha(OPACITY)
    overlay.fill(Constants.BLACK)
    screen.blit(overlay, (0, 0))
    surf = pygame.transform.flip(assets.corner_img, True, True)
    screen.blit(surf, (0, 0))
    #pop_up_coordinates = (screen_width // 2 - (assets.housekeeper_analyze_img.get_rect().width // 2), screen_height // 2 - (assets.mushroom_analyze_img.get_rect().height // 2))
    pop_up_coordinates = (270,50)
    screen.blit(assets.mushroom_analyze_img, pop_up_coordinates)
    analyze_mushroom.update_animation()
    #analyze_house_keeper.draw(screen, pop_up_coordinates[0] + (392 // 2), pop_up_coordinates[1] - (464 // 2)) # drawing
    analyze_mushroom.draw(screen, pop_up_coordinates[0] + 270, pop_up_coordinates[1] - 300) # drawing

def draw_analyze_flower():
    global surf, analyze_flower, screen
    OPACITY = 180
    overlay = pygame.Surface((screen_width, screen_height))
    overlay.set_alpha(OPACITY)
    overlay.fill(Constants.BLACK)
    screen.blit(overlay, (0, 0))
    surf = pygame.transform.flip(assets.corner_img, True, True)
    screen.blit(surf, (0, 0))
    #pop_up_coordinates = (screen_width // 2 - (assets.housekeeper_analyze_img.get_rect().width // 2), screen_height // 2 - (assets.mushroom_analyze_img.get_rect().height // 2))
    pop_up_coordinates = (270,50)
    screen.blit(assets.flower_analyze_img, pop_up_coordinates)
    analyze_flower.update_animation()
    #analyze_house_keeper.draw(screen, pop_up_coordinates[0] + (392 // 2), pop_up_coordinates[1] - (464 // 2)) # drawing
    analyze_flower.draw(screen, pop_up_coordinates[0] + 270, pop_up_coordinates[1] - 300) # drawing

def draw_analyze_shrub():
    global surf, analyze_shrub, screen
    OPACITY = 180
    overlay = pygame.Surface((screen_width, screen_height))
    overlay.set_alpha(OPACITY)
    overlay.fill(Constants.BLACK)
    screen.blit(overlay, (0, 0))
    surf = pygame.transform.flip(assets.corner_img, True, True)
    screen.blit(surf, (0, 0))
    #pop_up_coordinates = (screen_width // 2 - (assets.housekeeper_analyze_img.get_rect().width // 2), screen_height // 2 - (assets.mushroom_analyze_img.get_rect().height // 2))
    pop_up_coordinates = (270,50)
    screen.blit(assets.shrub_analyze_img, pop_up_coordinates)
    analyze_shrub.update_animation()
    #analyze_house_keeper.draw(screen, pop_up_coordinates[0] + (392 // 2), pop_up_coordinates[1] - (464 // 2)) # drawing
    analyze_shrub.draw(screen, pop_up_coordinates[0] + 270, pop_up_coordinates[1] - 300) # drawing

def draw_analyze_small_tree():
    global surf, analyze_small_tree, screen
    OPACITY = 180
    overlay = pygame.Surface((screen_width, screen_height))
    overlay.set_alpha(OPACITY)
    overlay.fill(Constants.BLACK)
    screen.blit(overlay, (0, 0))
    surf = pygame.transform.flip(assets.corner_img, True, True)
    screen.blit(surf, (0, 0))
    #pop_up_coordinates = (screen_width // 2 - (assets.housekeeper_analyze_img.get_rect().width // 2), screen_height // 2 - (assets.mushroom_analyze_img.get_rect().height // 2))
    pop_up_coordinates = (270,50)
    screen.blit(assets.small_tree_analyze_img, pop_up_coordinates)
    analyze_small_tree.update_animation()
    #analyze_house_keeper.draw(screen, pop_up_coordinates[0] + (392 // 2), pop_up_coordinates[1] - (464 // 2)) # drawing
    analyze_small_tree.draw(screen, pop_up_coordinates[0] + 270, pop_up_coordinates[1] - 300) # drawing

def draw_analyze_tree():
    global surf, analyze_tree, screen
    OPACITY = 180
    overlay = pygame.Surface((screen_width, screen_height))
    overlay.set_alpha(OPACITY)
    overlay.fill(Constants.BLACK)
    screen.blit(overlay, (0, 0))
    surf = pygame.transform.flip(assets.corner_img, True, True)
    screen.blit(surf, (0, 0))
    #pop_up_coordinates = (screen_width // 2 - (assets.housekeeper_analyze_img.get_rect().width // 2), screen_height // 2 - (assets.mushroom_analyze_img.get_rect().height // 2))
    pop_up_coordinates = (270,50)
    screen.blit(assets.tree_analyze_img, pop_up_coordinates)
    analyze_tree.update_animation()
    #analyze_house_keeper.draw(screen, pop_up_coordinates[0] + (392 // 2), pop_up_coordinates[1] - (464 // 2)) # drawing
    analyze_tree.draw(screen, pop_up_coordinates[0] + 270, pop_up_coordinates[1] - 300) # drawing

def draw_analyze_disease_bar():
    global disease_bar, screen
    disease_bar.update_animation()
    pop_up_coordinates = (270,50)
    disease_bar.draw(screen, pop_up_coordinates[0] - 300, pop_up_coordinates[1] + 230) # drawing

def show_dialog_1():
    dialog_img = pygame.image.load(resource_path("assets\\images\\dialogue\\dialogue-1.png")).convert_alpha()
    dialog_img = pygame.transform.scale(dialog_img, (screen_width, screen_height))
    screen.blit(dialog_img, (0,0))
    housekeeper_dialog.update_animation()
    housekeeper_dialog.draw(screen,  0, 0)  # drawing

    caterpillar_dialog_grey.update_animation()
    caterpillar_dialog_grey.draw(screen, 900, 0)  # drawing

def show_dialog_2():
    dialog_img = pygame.image.load(resource_path("assets\\images\\dialogue\\dialogue-2.png")).convert_alpha()
    dialog_img = pygame.transform.scale(dialog_img, (screen_width, screen_height))
    screen.blit(dialog_img, (0,0))
    housekeeper_dialog_grey.update_animation()
    housekeeper_dialog_grey.draw(screen,  0, 0)  # drawing

    caterpillar_dialog.update_animation()
    caterpillar_dialog.draw(screen, 900, 0)  # drawing

def show_dialog_3():
    dialog_img = pygame.image.load(resource_path("assets\\images\\dialogue\\dialogue-3.png")).convert_alpha()
    dialog_img = pygame.transform.scale(dialog_img, (screen_width, screen_height))
    screen.blit(dialog_img, (0,0))
    housekeeper_dialog.update_animation()
    housekeeper_dialog.draw(screen, 0, 0)  # drawing

    caterpillar_dialog_grey.update_animation()
    caterpillar_dialog_grey.draw(screen, 900, 0)  # drawing

def show_dialog_4():
    dialog_img = pygame.image.load(resource_path("assets\\images\\dialogue\\dialogue-4.png")).convert_alpha()
    dialog_img = pygame.transform.scale(dialog_img, (screen_width, screen_height))
    screen.blit(dialog_img, (0,0))
    housekeeper_dialog.update_animation()
    housekeeper_dialog.draw(screen, 0, 0)  # drawing

    caterpillar_dialog_grey.update_animation()
    caterpillar_dialog_grey.draw(screen, 900, 0)  # drawing

def show_dialog_5():
    dialog_img = pygame.image.load(resource_path("assets\\images\\dialogue\\dialogue-5.png")).convert_alpha()
    dialog_img = pygame.transform.scale(dialog_img, (screen_width, screen_height))
    screen.blit(dialog_img, (0,0))
    housekeeper_dialog_grey.update_animation()
    housekeeper_dialog_grey.draw(screen, 0, 0)  # drawing

    caterpillar_dialog.update_animation()
    caterpillar_dialog.draw(screen, 900, 0)  # drawing

def show_dialog_6():
    dialog_img = pygame.image.load(resource_path("assets\\images\\dialogue\\dialogue-6.png")).convert_alpha()
    dialog_img = pygame.transform.scale(dialog_img, (screen_width, screen_height))
    screen.blit(dialog_img, (0,0))
    enemy_dialog.update_animation()
    enemy_dialog.draw(screen, 0, 0)  # drawing

    caterpillar_dialog_grey.update_animation()
    caterpillar_dialog_grey.draw(screen, 900, 0)  # drawing

def show_dialog_7():
    dialog_img = pygame.image.load(resource_path("assets\\images\\dialogue\\dialogue-7.png")).convert_alpha()
    dialog_img = pygame.transform.scale(dialog_img, (screen_width, screen_height))
    screen.blit(dialog_img, (0,0))
    enemy_dialog_grey.update_animation()
    enemy_dialog_grey.draw(screen, 0, 0)  # drawing

    caterpillar_dialog.update_animation()
    caterpillar_dialog.draw(screen, 900, 0)  # drawing

def show_dialog_8():
    dialog_img = pygame.image.load(resource_path("assets\\images\\dialogue\\dialogue-8.png")).convert_alpha()
    dialog_img = pygame.transform.scale(dialog_img, (screen_width, screen_height))
    screen.blit(dialog_img, (0,0))
    enemy_dialog.update_animation()
    enemy_dialog.draw(screen, 0, 0)  # drawing

    caterpillar_dialog_grey.update_animation()
    caterpillar_dialog_grey.draw(screen, 900, 0)  # drawing

def show_dialog_9():
    dialog_img = pygame.image.load(resource_path("assets\\images\\dialogue\\dialogue-9.png")).convert_alpha()
    dialog_img = pygame.transform.scale(dialog_img, (screen_width, screen_height))
    screen.blit(dialog_img, (0,0))
    housekeeper_dialog.update_animation()
    housekeeper_dialog.draw(screen, 0, 0)  # drawing

    caterpillar_dialog_grey.update_animation()
    caterpillar_dialog_grey.draw(screen, 900, 0)  # drawing

def show_dialog_10():
    dialog_img = pygame.image.load(resource_path("assets\\images\\dialogue\\dialogue-10.png")).convert_alpha()
    dialog_img = pygame.transform.scale(dialog_img, (screen_width, screen_height))
    screen.blit(dialog_img, (0,0))
    housekeeper_dialog_grey.update_animation()
    housekeeper_dialog_grey.draw(screen, 0, 0)  # drawing

    caterpillar_dialog.update_animation()
    caterpillar_dialog.draw(screen, 900, 0)  # drawing

def show_dialog_11():
    dialog_img = pygame.image.load(resource_path("assets\\images\\dialogue\\dialogue-11.png")).convert_alpha()
    dialog_img = pygame.transform.scale(dialog_img, (screen_width, screen_height))
    screen.blit(dialog_img, (0,0))
    housekeeper_dialog.update_animation()
    housekeeper_dialog.draw(screen, 0, 0)  # drawing

    caterpillar_dialog_grey.update_animation()
    caterpillar_dialog_grey.draw(screen, 900, 0)  # drawing

def show_dialog_12():
    dialog_img = pygame.image.load(resource_path("assets\\images\\dialogue\\dialogue-12.png")).convert_alpha()
    dialog_img = pygame.transform.scale(dialog_img, (screen_width, screen_height))
    screen.blit(dialog_img, (0,0))
    enemy_dialog_grey.update_animation()
    enemy_dialog_grey.draw(screen, 0, 0)  # drawing

    caterpillar_dialog.update_animation()
    caterpillar_dialog.draw(screen, 900, 0)  # drawing

def show_dialog_13():
    dialog_img = pygame.image.load(resource_path("assets\\images\\dialogue\\dialogue-13.png")).convert_alpha()
    dialog_img = pygame.transform.scale(dialog_img, (screen_width, screen_height))
    screen.blit(dialog_img, (0,0))
    enemy_dialog.update_animation()
    enemy_dialog.draw(screen, 0, 0)  # drawing

    caterpillar_dialog_grey.update_animation()
    caterpillar_dialog_grey.draw(screen, 900, 0)  # drawing

def show_current_dialog():
    global show_overlay_dialog, dialog_progression
    dialog_progression += 1
    show_overlay_dialog = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN and show_overlay_analyze:
            mouse_x, mouse_y = event.pos
            if 0 <= mouse_x <= screen_width and 0 <= mouse_y <= screen_height:
                show_overlay_analyze = False
                analyzing_house_keeper = False
                analyzing_frog = False
                analyzing_enemy = False
                analyzing_mushroom = False
                analyzing_flower = False
                analyzing_shrub = False
                analyzing_small_tree = False
                analyzing_tree = False
        elif event.type == MOUSEBUTTONDOWN and show_overlay_dialog:
            mouse_x, mouse_y = event.pos
            if 0 <= mouse_x <= screen_width and 0 <= mouse_y <= screen_height:
                if 1 <= dialog_progression <= 2:
                    dialog_progression += 1
                elif dialog_progression == 4:
                    dialog_progression += 1
                elif 6 <= dialog_progression <= 7:
                    dialog_progression += 1
                elif 9 <= dialog_progression <= 10:
                    dialog_progression += 1
                elif  dialog_progression == 12:
                    dialog_progression += 1
                else:
                    show_overlay_dialog = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                text_area_visible = not text_area_visible
                text_input = ""
            elif text_area_visible:
                if event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]
                elif event.key == pygame.K_RETURN:
                    if re.match(enemy_talk_command_pattern, text_input):
                        enemy.talk(show_current_dialog,wrong_command)
                    elif re.match(harvest_mushroom_command_pattern, text_input):
                        for key, plant in mushroom_plants.items():
                            if plant.is_colliding:
                                plant.harvest(wrong_command, on_successful_harvest)
                    elif re.match(harvest_flower_command_pattern, text_input):
                        for key, plant in flowers.items():
                            if plant.is_colliding:
                                plant.harvest(wrong_command, on_successful_harvest)
                    elif re.match(harvest_shrub_command_pattern, text_input):
                        for key, plant in shrubs.items():
                            if plant.is_colliding:
                                plant.harvest(wrong_command, on_successful_harvest)
                    elif re.match(harvest_small_tree_command_pattern, text_input):
                        for key, plant in small_tree.items():
                            if plant.is_colliding:
                                plant.harvest(wrong_command, on_successful_harvest)
                    elif re.match(harvest_tree_command_pattern, text_input):
                        for key, plant in red_tree.items():
                            if plant.is_colliding:
                                plant.harvest(wrong_command, on_successful_harvest)
                    elif re.match(plant_hole_command_pattern, text_input):
                        for key, hole in soil.items():
                            if hole.is_colliding:
                                hole.plant(wrong_command)
                    elif re.match(frog_talk_command_pattern, text_input):
                        print("FROG")
                    elif re.match(housekeeper_talk_command_pattern, text_input):
                        housekeeper.talk(show_current_dialog,wrong_command)
                    # ANALYZE
                    elif re.match(analyze_housekeeper_command_pattern, text_input):
                        if housekeeper.is_colliding:
                            show_overlay_analyze = True
                            analyzing_house_keeper = True
                    elif re.match(analyze_enemy_command_pattern, text_input):
                        if enemy.is_colliding:
                            show_overlay_analyze = True
                            analyzing_enemy = True
                    elif re.match(analyze_frog_command_pattern, text_input):
                        for key, frog in frogs.items():
                            if frog.is_colliding:
                                show_overlay_analyze = True
                                analyzing_frog = True
                    elif re.match(analyze_mushroom_command_pattern, text_input):
                        for key, mushroom in mushroom_plants.items():
                            if mushroom.is_colliding:
                                show_overlay_analyze = True
                                analyzing_mushroom = True
                    elif re.match(analyze_flower_command_pattern, text_input):
                        for key, flower in flowers.items():
                            if flower.is_colliding:
                                show_overlay_analyze = True
                                analyzing_flower = True
                    elif re.match(analyze_shrub_command_pattern, text_input):
                        for key, shrub in shrubs.items():
                            if shrub.is_colliding:
                                show_overlay_analyze = True
                                analyzing_shrub = True
                    elif re.match(analyze_small_tree_command_pattern, text_input):
                        for key, s_tree in small_tree.items():
                            if s_tree.is_colliding:
                                show_overlay_analyze = True
                                analyzing_small_tree = True
                    elif re.match(analyze_tree_command_pattern, text_input):
                        for key, tree in red_tree.items():
                            if tree.is_colliding:
                                show_overlay_analyze = True
                                analyzing_tree = True

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
                screen.blit(assets.code_console_bg, (120, screen_height - 470))
                text_surface = font.render(text_input, True, Constants.BLACK)
                screen.blit(text_surface, (text_area_rect.x + 5, text_area_rect.y + 5))
                pygame.display.flip()
                clock.tick(60)
            continue
        camera_offset_x, camera_offset_y = player.get_camera_offset()

        screen.blit(background_img, (camera_offset_x, camera_offset_y))

        for row in range(Constants.MAP_HEIGHT):
            for col in range(Constants.MAP_WIDTH):
                tile_type = tile_map[row][col]
                # SOIL
                if 1 <= tile_type <= 12:  # HOLE
                    soil[str(tile_type)].update_animation()
                    tile_x = col * Constants.TILE_SIZE + camera_offset_x
                    tile_y = row * Constants.TILE_SIZE + camera_offset_y
                    soil[str(tile_type)].draw(screen, tile_x, tile_y)
                    soil[str(tile_type)].check_collision(player)
                    continue
                # CHARACTERS
                elif tile_type == 13:  # HOUSEKEEPER
                    housekeeper.update_animation()
                    tile_x = col * Constants.TILE_SIZE + camera_offset_x
                    tile_y = row * Constants.TILE_SIZE + camera_offset_y
                    housekeeper.draw(screen, tile_x, tile_y)
                    housekeeper.check_collision(player)
                    #player.update_collision_objects(tile_type, housekeeper)
                    continue
                elif tile_type == 14:  # ENEMY
                    enemy.update_animation()
                    tile_x = col * Constants.TILE_SIZE + camera_offset_x
                    tile_y = row * Constants.TILE_SIZE + camera_offset_y
                    enemy.draw(screen, tile_x, tile_y)
                    enemy.check_collision(player)
                    #player.update_collision_objects(tile_type, enemy)
                    continue
                # ANIMALS
                if 15 <= tile_type <= 28:  # FROG
                    frogs[str(tile_type)].update_animation()
                    tile_x = col * Constants.TILE_SIZE + camera_offset_x
                    tile_y = row * Constants.TILE_SIZE + camera_offset_y
                    frogs[str(tile_type)].draw(screen, tile_x, tile_y)
                    frogs[str(tile_type)].check_collision(player)
                    continue
                # PLANTS
                if 29 <= tile_type <= 53:  # MUSHROOMS PLANTS
                    mushroom_plants[str(tile_type)].update_animation()
                    tile_x = col * Constants.TILE_SIZE + camera_offset_x
                    tile_y = row * Constants.TILE_SIZE + camera_offset_y
                    mushroom_plants[str(tile_type)].draw(screen, tile_x, tile_y)
                    mushroom_plants[str(tile_type)].check_collision(player)
                    continue
                if 54 <= tile_type <= 58:  # FLOWER PLANTS
                    flowers[str(tile_type)].update_animation()
                    tile_x = col * Constants.TILE_SIZE + camera_offset_x
                    tile_y = row * Constants.TILE_SIZE + camera_offset_y
                    flowers[str(tile_type)].draw(screen, tile_x, tile_y)
                    flowers[str(tile_type)].check_collision(player)
                    continue
                if 59 <= tile_type <= 63:  # SHRUB PLANTS
                    shrubs[str(tile_type)].update_animation()
                    tile_x = col * Constants.TILE_SIZE + camera_offset_x
                    tile_y = row * Constants.TILE_SIZE + camera_offset_y
                    shrubs[str(tile_type)].draw(screen, tile_x, tile_y)
                    shrubs[str(tile_type)].check_collision(player)
                    continue
                if 64 <= tile_type <= 67:  # SMALL TREE PLANTS
                    small_tree[str(tile_type)].update_animation()
                    tile_x = col * Constants.TILE_SIZE + camera_offset_x
                    tile_y = row * Constants.TILE_SIZE + camera_offset_y
                    small_tree[str(tile_type)].draw(screen, tile_x, tile_y)
                    small_tree[str(tile_type)].check_collision(player)
                    continue
                if 68 <= tile_type <= 71:  # BLUE PLANTS
                    blue_tree[str(tile_type)].update_animation()
                    tile_x = col * Constants.TILE_SIZE + camera_offset_x
                    tile_y = row * Constants.TILE_SIZE + camera_offset_y
                    blue_tree[str(tile_type)].draw(screen, tile_x, tile_y)
                    blue_tree[str(tile_type)].check_collision(player)
                    continue
                if 72 <= tile_type <= 74:  # RED PLANTS
                    red_tree[str(tile_type)].update_animation()
                    tile_x = col * Constants.TILE_SIZE + camera_offset_x
                    tile_y = row * Constants.TILE_SIZE + camera_offset_y
                    red_tree[str(tile_type)].draw(screen, tile_x, tile_y)
                    red_tree[str(tile_type)].check_collision(player)
                    continue
                else:
                    continue

        player.draw(screen, camera_offset_x, camera_offset_y)
        player.update(screen)

        base = 395
        suma = 95

        screen.blit(assets.character_frame_img, (20, 20))
        screen.blit(assets.level_bar_img, (340, 50))

        draw_item_container_1()
        draw_item_container_2()
        draw_item_container_3()
        draw_item_container_4()
        draw_item_container_5()
        draw_item_container_6()

        # UI
        surf = pygame.transform.flip(assets.corner_img, False, True)
        screen.blit(surf, (screen_width-surf.get_rect().width,0))

        screen.blit(assets.corner_img, (screen_width-surf.get_rect().width,screen_height-surf.get_rect().height))

        surf2 = pygame.transform.flip(assets.corner_img, True, False)
        screen.blit(surf2, (0,screen_height-surf2.get_rect().height))

        if show_overlay_analyze:
            if analyzing_house_keeper:
                draw_analyze_house_keeper()
                draw_analyze_disease_bar()
            if analyzing_enemy:
                draw_analyze_enemy()
                draw_analyze_disease_bar()
            if analyzing_frog:
                draw_analyze_frog()
                draw_analyze_disease_bar()
            if analyzing_mushroom:
                draw_analyze_mushroom()
                draw_analyze_disease_bar()
            if analyzing_flower:
                draw_analyze_flower()
                draw_analyze_disease_bar()
            if analyzing_shrub:
                draw_analyze_shrub()
                draw_analyze_disease_bar()
            if analyzing_small_tree:
                draw_analyze_small_tree()
                draw_analyze_disease_bar()
            if analyzing_tree:
                draw_analyze_tree()
                draw_analyze_disease_bar()
        elif show_overlay_dialog:
            if dialog_progression == 1:
                show_dialog_1()
            elif dialog_progression == 2:
                show_dialog_2()
            elif dialog_progression == 3:
                show_dialog_3()
            elif dialog_progression == 4:
                show_dialog_4()
            elif dialog_progression == 5:
                show_dialog_5()
            elif dialog_progression == 6:
                show_dialog_6()
            elif dialog_progression == 7:
                show_dialog_7()
            elif dialog_progression == 8:
                show_dialog_8()
            elif dialog_progression == 9:
                show_dialog_9()
            elif dialog_progression == 10:
                show_dialog_10()
            elif dialog_progression == 11:
                show_dialog_11()
            elif dialog_progression == 12:
                show_dialog_12()
            elif dialog_progression == 13:
                show_dialog_13()

    elif screen_selected == Screens.SPLASH:
        splash_video.play_video(screen, go_to_father_screen())
    elif screen_selected == Screens.FATHER:
        start_father_screen()

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
sys.exit()
