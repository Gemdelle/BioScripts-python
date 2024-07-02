import os
import pygame
from utils.constants import Constants

class FrogAngry:
    def __init__(self):
        self.frames = {}
        self.frame_index = 1
        self.rect = pygame.Rect(0, 0, Constants.FROG_ANGRY_SIZE, Constants.FROG_ANGRY_SIZE)
        self.is_colliding = False
        self.tooltip_text = "frog"
        self.current_text_length = 0
        self.last_update_time = 0
        self.typing_speed = 100  # Time in milliseconds between each character
        self.visible = False

    def load_frame(self, index):
        if index not in self.frames:
            frame_path = os.path.join("./assets/gifs/frames/frog_angry", f'frog_angry_{index}.png')
            if os.path.exists(frame_path):
                surf = pygame.image.load(frame_path).convert_alpha()
                surf = pygame.transform.scale(surf, (Constants.FROG_ANGRY_SIZE, Constants.FROG_ANGRY_SIZE))
                self.frames[index] = surf
            else:
                self.frames[index] = None  # Mark as None if the frame does not exist

    def update_animation(self):
        if self.visible:
            current_time = pygame.time.get_ticks()
            self.frame_index = (current_time // Constants.FRAME_DURATION_IN_MILLIS) % 168  # Assuming 200 frames
            self.load_frame(self.frame_index)  # Lazy load the current frame

            if self.is_colliding:
                if current_time - self.last_update_time > self.typing_speed:
                    self.last_update_time = current_time
                    if self.current_text_length < len(self.tooltip_text):
                        self.current_text_length += 1
            else:
                self.current_text_length = 0

    def draw(self, screen, x, y):
        self.rect.x = x + Constants.FROG_ANGRY_SIZE
        self.rect.y = y + Constants.FROG_ANGRY_SIZE
        was_visible = self.visible
        self.visible = self.is_visible(screen)

        if self.visible:
            if not was_visible:
                self.load_frame(self.frame_index)
            if self.frames[self.frame_index] is not None:
                screen.blit(self.frames[self.frame_index], (self.rect.x, self.rect.y))
            if self.is_colliding:
                # Render tooltip
                font_path = os.path.join("assets", "fonts", "BavarianCrown.ttf")
                font = pygame.font.Font(font_path, 24)
                text_to_display = self.tooltip_text[:self.current_text_length]
                text_surf = font.render(text_to_display, True, Constants.WHITE)
                text_rect = text_surf.get_rect(center=(self.rect.centerx, self.rect.top - 10))
                screen.blit(text_surf, text_rect)

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
