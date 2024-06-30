import os
import pygame
from utils.constants import Constants
from utils.resource_path_util import resource_path


class Hole4:
    def __init__(self):
        self.frames = []
        self.frame_index = 0
        self.rect = pygame.Rect(0, 0, Constants.HOLE_SIZE_4, Constants.HOLE_SIZE_4)
        self.is_colliding = False
        self.tooltip_text = "hole"
        self.current_text_length = 0
        self.last_update_time = 0

    def draw(self, screen, x, y):
        self.rect.x = x + Constants.HOLE_SIZE_4
        self.rect.y = y + Constants.HOLE_SIZE_4
        surf = pygame.image.load(resource_path("assets\\images\\hole-4.png")).convert_alpha()
        surf = pygame.transform.scale(surf, (Constants.HOLE_SIZE_4, Constants.HOLE_SIZE_4))
        screen.blit(surf, (self.rect.x, self.rect.y))

        if self.is_colliding:
            # Render tooltip
            font = pygame.font.Font(None, 24)  # You can specify a font file instead of None
            text_to_display = self.tooltip_text[:self.current_text_length]
            text_surf = font.render(text_to_display, True, Constants.WHITE)
            text_rect = text_surf.get_rect(center=(self.rect.centerx, self.rect.top - 10))
            screen.blit(text_surf, text_rect)

    def check_collision(self, player):
        enemy_collision_rect = pygame.Rect(self.rect.x - 30, self.rect.y - 30, self.rect.w + 30, self.rect.h + 30)
        camera_offset_x, camera_offset_y = player.get_camera_offset()
        player_collision_rect = pygame.Rect(player.rect.x + camera_offset_x, player.rect.y + camera_offset_y, player.rect.w, player.rect.h)
        if enemy_collision_rect.colliderect(player_collision_rect):
            self.is_colliding = True
        else:
            self.is_colliding = False

    def talk(self, start_tkinter_app, wrong_command):
        if not self.is_colliding:
            wrong_command()
            return
        start_tkinter_app()
