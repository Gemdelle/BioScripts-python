import os
import pygame
from utils.constants import Constants

class Flower1:
    def __init__(self):
        self.frames = []
        self.frame_index = 0
        self.rect = pygame.Rect(0, 0, Constants.FLOWER_1_SIZE, Constants.FLOWER_1_SIZE)
        self.is_colliding = False
        self.tooltip_text = "mushroom"
        self.current_text_length = 0
        self.last_update_time = 0
        self.typing_speed = 100  # Time in milliseconds between each character
        self.visible = False

    def load_frames(self):
        if not self.frames:
            frame_index = 1
            while True:
                frame_path = os.path.join("./assets/gifs/frames/flower-1", f'flower-1_{frame_index}.png')
                if not os.path.exists(frame_path):
                    break
                surf = pygame.image.load(frame_path).convert_alpha()
                surf = pygame.transform.scale(surf, (Constants.FLOWER_1_SIZE, Constants.FLOWER_1_SIZE))
                self.frames.append(surf)
                frame_index += 1
                self.rect.width = Constants.FLOWER_1_SIZE
                self.rect.height = Constants.FLOWER_1_SIZE

    def unload_frames(self):
        self.frames.clear()

    def update_animation(self):
        if self.visible:
            current_time = pygame.time.get_ticks()
            self.frame_index = (current_time // Constants.FRAME_DURATION_IN_MILLIS) % len(self.frames)
            if self.is_colliding:
                if current_time - self.last_update_time > self.typing_speed:
                    self.last_update_time = current_time
                    if self.current_text_length < len(self.tooltip_text):
                        self.current_text_length += 1
            else:
                self.current_text_length = 0

    def draw(self, screen, x, y):
        self.rect.x = x + Constants.FLOWER_1_SIZE
        self.rect.y = y + Constants.FLOWER_1_SIZE
        was_visible = self.visible
        self.visible = self.is_visible(screen)

        if self.visible:
            if not was_visible:
                self.load_frames()
            screen.blit(self.frames[int(self.frame_index)], (self.rect.x, self.rect.y))
            if self.is_colliding:
                # Render tooltip
                font = pygame.font.Font(None, 24)  # You can specify a font file instead of None
                text_to_display = self.tooltip_text[:self.current_text_length]
                text_surf = font.render(text_to_display, True, Constants.WHITE)
                text_rect = text_surf.get_rect(center=(self.rect.centerx, self.rect.top - 10))
                screen.blit(text_surf, text_rect)
        elif was_visible:
            self.unload_frames()

    def is_visible(self, screen):
        screen_rect = screen.get_rect()
        return screen_rect.colliderect(self.rect)

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
