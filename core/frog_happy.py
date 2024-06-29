import os

import pygame

from utils.constants import Constants


class FrogHappy:
    def __init__(self):
        self.frames = []
        self.frame_index = 0
        self.load_frames()

    def load_frames(self):
        frame_index = 1
        while True:
            frame_path = os.path.join("./assets/gifs/frames/frog_happy", f'frog_happy_{frame_index}.png')
            if not os.path.exists(frame_path):
                break
            surf = pygame.image.load(frame_path).convert_alpha()
            surf = pygame.transform.scale(surf, (Constants.FROG_SIZE, Constants.FROG_SIZE))
            self.frames.append(surf)
            frame_index += 1

    def update_animation(self):
        current_time = pygame.time.get_ticks()
        self.frame_index = (current_time // Constants.FRAME_DURATION_IN_MILLIS) % len(self.frames)

    def draw(self, screen, x, y):
        screen.blit(self.frames[int(self.frame_index)], (x, y))