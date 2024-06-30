import pygame
from moviepy.editor import VideoFileClip
import numpy as np
from PIL import Image
from utils.resource_path_util import resource_path
from utils.sound_manager import SoundManager


class SplashVideo:
    def __init__(self, screen_width, screen_height):
        self.clip = VideoFileClip(resource_path("assets\\videos\\splash.mp4"))
        self.new_width, self.new_height = self.calculate_resize(screen_width, screen_height)
        self.sound_manager = SoundManager()
        self.is_video_playing = False
        self.is_clock_reseted = False
        self.initial_time = pygame.time.get_ticks()

    def calculate_resize(self, screen_width, screen_height):
        aspect_ratio = self.clip.size[0] / self.clip.size[1]
        if screen_width / screen_height > aspect_ratio:
            new_height = screen_height
            new_width = int(aspect_ratio * new_height)
        else:
            new_width = screen_width
            new_height = int(new_width / aspect_ratio)
        return new_width, new_height

    def resize_frame(self, frame):
        pil_image = Image.fromarray(frame)
        pil_image = pil_image.resize((self.new_width, self.new_height), Image.LANCZOS)
        return np.array(pil_image)

    def frame_to_surface(self, frame):
        frame = np.rot90(frame)
        frame = np.flipud(frame)
        surface = pygame.surfarray.make_surface(frame)
        return surface

    def play_video(self, screen, go_to_next_screen):
        current_time = (pygame.time.get_ticks() - self.initial_time) / 1000.0

        if current_time >= self.clip.duration:
            go_to_next_screen()

        if not self.is_video_playing:
            self.sound_manager.play_sound("splash_music")
            self.is_video_playing = True

        current_frame = self.clip.get_frame(current_time)
        current_frame = self.resize_frame(current_frame)
        surface = self.frame_to_surface(current_frame)

        screen.fill((0, 0, 0))
        screen.blit(surface, ((screen.get_width() - self.new_width) // 2, (screen.get_height() - self.new_height) // 2))
