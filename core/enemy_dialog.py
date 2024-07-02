import os
import pygame
from utils.constants import Constants

class EnemyDialog:
    def __init__(self):
        self.frames = {}
        self.frame_index = 0
        self.rect = pygame.Rect(0, 0, 392, 464)
        self.last_update_time = 0
        self.typing_speed = 100

    def load_frame(self, index):
        if index not in self.frames:
            frame_path = os.path.join("./assets/gifs/frames/enemy-only-dialogue", f'enemy-only-dialogue_{index}.png')
            if os.path.exists(frame_path):
                surf = pygame.image.load(frame_path).convert_alpha()
                surf = pygame.transform.scale(surf, (500, 600)) # scale
                self.frames[index] = surf
            else:
                self.frames[index] = None  # Mark as None if the frame does not exist

    def update_animation(self):
        current_time = pygame.time.get_ticks()
        self.frame_index = (current_time // Constants.FRAME_DURATION_IN_MILLIS) % 44
        self.load_frame(self.frame_index)  # Lazy load the current frame

    def draw(self, screen, x, y):
        self.rect.x = x + 392
        self.rect.y = y + 464
        if self.frames[self.frame_index] is not None:
            screen.blit(self.frames[self.frame_index], (self.rect.x, self.rect.y))


