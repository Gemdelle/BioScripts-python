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
            self.plant_tile_img = None
            self.hole_tile_img_4 = None
            self.hole_tile_img_3 = None
            self.hole_tile_img_2 = None
            self.hole_tile_img_1 = None
            self.player_img_reference = None
            self.caterpillar_walk_frames = None
            self.HOLE_TILE_IMAGES = None
            self.PLANT_TILE_IMAGES = None
            self.code_console_bg = None
            self._assets_preloaded = None
            self._initialized = True

    def preload(self):
        self.hole_tile_img_1 = pygame.image.load(resource_path("assets\\images\\hole-1.png")).convert_alpha()
        self.hole_tile_img_2 = pygame.image.load(resource_path("assets\\images\\hole-2.png")).convert_alpha()
        self.hole_tile_img_3 = pygame.image.load(resource_path("assets\\images\\hole-3.png")).convert_alpha()
        self.hole_tile_img_4 = pygame.image.load(resource_path("assets\\images\\hole-4.png")).convert_alpha()
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

