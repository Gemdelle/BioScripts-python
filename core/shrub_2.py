import os
import pygame
from utils.constants import Constants

class Shrub2:
    def __init__(self):
        self.frames = {}
        self.frame_index = 0
        self.rect = pygame.Rect(0, 0, Constants.SHRUB_2_SIZE, Constants.SHRUB_2_SIZE)
        self.is_colliding = False
        self.tooltip_text = "shrub"
        self.current_text_length = 0
        self.last_update_time = 0
        self.typing_speed = 100  # Time in milliseconds between each character
        self.visible = False

        self.gif_frames = []
        self.gif_frame_index = 0
        self.gif_last_update_time = 0
        self.gif_animation_speed = 100  # Time in milliseconds between each GIF frame
        self.is_harvesting = False

    def load_frame(self, index):
        if index not in self.frames:
            frame_path = os.path.join("./assets/gifs/frames/shrub-2", f'shrub-2_{index}.png')
            if os.path.exists(frame_path):
                surf = pygame.image.load(frame_path).convert_alpha()
                surf = pygame.transform.scale(surf, (Constants.SHRUB_2_SIZE, Constants.SHRUB_2_SIZE))
                surf = pygame.transform.flip(surf, True, False)
                self.frames[index] = surf
            else:
                self.frames[index] = None  # Mark as None if the frame does not exist
    def load_gif_frames(self):
        for i in range(29):  # Assuming the GIF has 24 frames
            frame_path = os.path.join("./assets/gifs/frames/harvest-shrub", f'harvest-shrub_{i}.png')
            if os.path.exists(frame_path):
                surf = pygame.image.load(frame_path).convert_alpha()
                surf = pygame.transform.scale(surf, (Constants.MUSHROOM_SIZE, Constants.MUSHROOM_SIZE))
                self.gif_frames.append(surf)
    def update_animation(self):
        current_time = pygame.time.get_ticks()
        if self.visible:
            self.frame_index = (current_time // Constants.FRAME_DURATION_IN_MILLIS) % 200  # Assuming 200 frames
            self.load_frame(self.frame_index)  # Lazy load the current frame

            if self.is_colliding:
                if current_time - self.last_update_time > self.typing_speed:
                    self.last_update_time = current_time
                    if self.current_text_length < len(self.tooltip_text):
                        self.current_text_length += 1
            else:
                self.current_text_length = 0

        if self.is_harvesting:
            if current_time - self.gif_last_update_time > self.gif_animation_speed:
                self.gif_last_update_time = current_time
                self.gif_frame_index = (self.gif_frame_index + 1) % len(self.gif_frames)
                if self.gif_frame_index == len(self.gif_frames) - 1:
                    self.is_harvesting = False  # Stop the animation when all frames are displayed

    def draw(self, screen, x, y):
        self.rect.x = x + Constants.SHRUB_2_SIZE
        self.rect.y = y + Constants.SHRUB_2_SIZE
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

        if self.is_harvesting and self.gif_frames:
            gif_frame = self.gif_frames[self.gif_frame_index]
            gif_frame_rect = gif_frame.get_rect(center=(self.rect.centerx, self.rect.top - 10))
            screen.blit(gif_frame, gif_frame_rect)

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

    def harvest(self, wrong_command, on_successful_harvest):
        if not self.is_colliding:
            wrong_command()
        self.load_gif_frames()
        self.is_harvesting = True
        self.gif_frame_index = 0
        self.gif_last_update_time = pygame.time.get_ticks()
        on_successful_harvest("shrub")
