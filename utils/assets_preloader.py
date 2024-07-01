import os
import pygame
from utils.constants import Constants
from utils.resource_path_util import resource_path

class AssetsPreloader:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AssetsPreloader, cls).__new__(cls)
            cls._instance._initialized = False
            cls._instance._assets_preloaded = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            # UI
            self.corner_img = None
            self.character_frame_img = None
            self.level_bar_img = None
            self.item_container_img = None

            self.plant_tile_img = None
            self.hole_tile_img_4 = None
            self.hole_tile_img_3 = None
            self.hole_tile_img_2 = None
            self.hole_tile_img_1 = None
            self.dirt_img = None
            self.player_img_reference = None
            self.caterpillar_walk_frames = None
            self.HOLE_TILE_IMAGES = None
            self.PLANT_TILE_IMAGES = None
            self.code_console_bg = None
            self._assets_preloaded = None
            self.fruit_flower_img = None
            self.fruit_mushroom_img = None
            self.fruit_shrub_img = None
            self.fruit_small_tree_img = None
            self.fruit_tree_img = None
            self._initialized = True

    def preload(self):
        #UI
        self.corner_img = pygame.image.load(resource_path("assets\\images\\corner.png")).convert_alpha()
        self.corner_img = pygame.transform.scale(self.corner_img, (380, 380))

        self.character_frame_img = pygame.image.load(resource_path("assets\\images\\character-frame.png")).convert_alpha()
        self.character_frame_img = pygame.transform.scale(self.character_frame_img, (380, 380))

        self.level_bar_img = pygame.image.load(resource_path("assets\\images\\level-bar.png")).convert_alpha()
        self.level_bar_img = pygame.transform.scale(self.level_bar_img, (650, 130))

        self.item_container_img = pygame.image.load(resource_path("assets\\images\\item-container.png")).convert_alpha()
        self.item_container_img = pygame.transform.scale(self.item_container_img, (75, 75))

        #FRUITS
        self.fruit_flower_img = pygame.image.load(resource_path("assets\\images\\fruits\\fruit-flower.png")).convert_alpha()
        self.fruit_flower_img = pygame.transform.scale(self.fruit_flower_img, (75, 75))

        self.fruit_mushroom_img = pygame.image.load(resource_path("assets\\images\\fruits\\fruit-mushroom.png")).convert_alpha()
        self.fruit_mushroom_img = pygame.transform.scale(self.fruit_mushroom_img, (75, 75))

        self.fruit_shrub_img = pygame.image.load(resource_path("assets\\images\\fruits\\fruit-shrub.png")).convert_alpha()
        self.fruit_shrub_img = pygame.transform.scale(self.fruit_shrub_img, (75, 75))

        self.fruit_small_tree_img = pygame.image.load(resource_path("assets\\images\\fruits\\fruit-small-tree.png")).convert_alpha()
        self.fruit_small_tree_img = pygame.transform.scale(self.fruit_small_tree_img, (75, 75))

        self.fruit_tree_img = pygame.image.load(resource_path("assets\\images\\fruits\\fruit-tree.png")).convert_alpha()
        self.fruit_tree_img = pygame.transform.scale(self.fruit_tree_img, (75, 75))

        #PLANTS
        self.hole_tile_img_1 = pygame.image.load(resource_path("assets\\images\\hole-1.png")).convert_alpha()
        self.hole_tile_img_2 = pygame.image.load(resource_path("assets\\images\\hole-2.png")).convert_alpha()
        self.hole_tile_img_3 = pygame.image.load(resource_path("assets\\images\\hole-3.png")).convert_alpha()
        self.hole_tile_img_4 = pygame.image.load(resource_path("assets\\images\\hole-4.png")).convert_alpha()
        self.dirt_img = pygame.image.load(resource_path("assets\\images\\dirt.png")).convert_alpha()
        self.dirt_img = pygame.transform.scale(self.dirt_img, (Constants.TILE_SIZE * 4, Constants.TILE_SIZE * 4))
        self.plant_tile_img = pygame.image.load(resource_path("assets\\images\\plant.png")).convert_alpha()
        self.code_console_bg = pygame.image.load(resource_path("assets\\images\\code_console.png")).convert_alpha()
        self.code_console_bg = pygame.transform.scale(self.code_console_bg, (425, 340))
        self.HOLE_TILE_IMAGES = [
            pygame.transform.scale(self.hole_tile_img_1, (Constants.TILE_SIZE * 4, Constants.TILE_SIZE * 4)),
            pygame.transform.scale(self.hole_tile_img_2, (Constants.TILE_SIZE * 4, Constants.TILE_SIZE * 4)),
            pygame.transform.scale(self.hole_tile_img_3, (Constants.TILE_SIZE * 4, Constants.TILE_SIZE * 4)),
            pygame.transform.scale(self.hole_tile_img_4, (Constants.TILE_SIZE * 4, Constants.TILE_SIZE * 4))
        ]
        self.PLANT_TILE_IMAGES = [
            pygame.transform.scale(self.plant_tile_img, (Constants.TILE_SIZE * 4, Constants.TILE_SIZE * 8))
        ]
        self.player_img_reference = pygame.image.load(resource_path("assets\\gifs\\caterpillar_walk.gif")).convert_alpha()
        self.player_img_reference = pygame.transform.scale(self.player_img_reference, (Constants.PLAYER_SIZE, Constants.PLAYER_SIZE))

        self.generate_caterpillar_walk_frames()
        self._assets_preloaded = True

    def generate_caterpillar_walk_frames(self):
        self.caterpillar_walk_frames = []
        caterpillar_frame_index = 1
        while True:
            frame_path = os.path.join(f"./assets/gifs/frames/caterpillar_walk", f'caterpillar_walk_{caterpillar_frame_index}.png')
            if not os.path.exists(frame_path):
                break
            surf = pygame.image.load(frame_path).convert_alpha()
            surf = pygame.transform.scale(surf, (Constants.PLAYER_SIZE, Constants.PLAYER_SIZE))
            self.caterpillar_walk_frames.append(surf)
            caterpillar_frame_index += 1

    def assets_preloaded(self):
        return self._assets_preloaded

