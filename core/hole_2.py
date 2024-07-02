import os
import pygame
from utils.constants import Constants
from utils.resource_path_util import resource_path


class Hole2:
    def __init__(self):
        self.frames = []
        self.frame_index = 0
        self.rect = pygame.Rect(0, 0, Constants.HOLE_SIZE_2, Constants.HOLE_SIZE_2)
        self.is_colliding = False
        self.tooltip_text = "hole"
        self.current_text_length = 0
        self.last_update_time = 0
        self.is_planted = False
        self.typing_speed = 100

    def update_animation(self):
        current_time = pygame.time.get_ticks()
        if self.is_colliding:
            if current_time - self.last_update_time > self.typing_speed:
                self.last_update_time = current_time
                if self.current_text_length < len(self.tooltip_text):
                    self.current_text_length += 1
        else:
            self.current_text_length = 0

    def draw(self, screen, x, y):
        self.rect.x = x + Constants.HOLE_SIZE_2
        self.rect.y = y + Constants.HOLE_SIZE_2

        if self.is_planted:
            surf = pygame.image.load(resource_path("assets\\images\\dirt.png")).convert_alpha()
            surf = pygame.transform.scale(surf, (Constants.HOLE_SIZE_1, Constants.HOLE_HEIGHT))
            screen.blit(surf, (self.rect.x, self.rect.y))
            self.tooltip_text = "dirt"
        else:
            surf = pygame.image.load(resource_path("assets\\images\\hole-2.png")).convert_alpha()
            surf = pygame.transform.scale(surf, (Constants.HOLE_SIZE_2, Constants.HOLE_HEIGHT))
            screen.blit(surf, (self.rect.x, self.rect.y))

        if self.is_colliding:
            # Render tooltip
            font_path = os.path.join("assets", "fonts", "BavarianCrown.ttf")
            font = pygame.font.Font(font_path, 24)
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

    def plant(self, wrong_command):
        if not self.is_colliding:
            wrong_command()
            return
        self.is_planted = True