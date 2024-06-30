import pygame

from utils.assets_preloader import AssetsPreloader
from utils.constants import Constants
from utils.game_objects_repository import GameObjectsRepository
from utils.map_reference import tile_map

assets = AssetsPreloader()
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = assets.player_img_reference
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.animation_frames = assets.caterpillar_walk_frames
        self.frame_index = 0
        self.frame_duration = 60  # milliseconds per frame

        # Typing animation attributes
        self.tooltip_text = "Nothing Happened..."
        self.current_text_length = 0
        self.last_update_time = 0
        self.typing_speed = 100  # Time in milliseconds between each character
        self.wrong_feedback = False
        self.typing_start_time = 0  # Time when the typing animation starts

    def update_collision_objects(self, type, character):
        collision_rect = pygame.Rect(character.rect.x, character.rect.y, character.rect.w, character.rect.h)
        GameObjectsRepository.collision_objects[type] = collision_rect

    def handle_movement(self, keys):
        move_x = 0
        move_y = 0
        if keys[pygame.K_a]:
            move_x -= Constants.MOVE_SPEED
        if keys[pygame.K_d]:
            move_x += Constants.MOVE_SPEED
        if keys[pygame.K_w]:
            move_y -= Constants.MOVE_SPEED
        if keys[pygame.K_s]:
            move_y += Constants.MOVE_SPEED
        return move_x, move_y

    def update_position(self, move_x, move_y):
        collision_objects = GameObjectsRepository.collision_objects
        camera_offset_x, camera_offset_y = self.get_camera_offset()
        new_x = max(0, min(self.rect.x + move_x, Constants.MAP_WIDTH * Constants.PLAYER_SIZE))
        new_y = max(0, min(self.rect.y + move_y, Constants.MAP_HEIGHT * Constants.PLAYER_SIZE))

        player_rect = pygame.Rect(new_x + camera_offset_x, new_y + camera_offset_y, Constants.PLAYER_SIZE, Constants.PLAYER_SIZE)

        for key, obj_rect in collision_objects.items():
            if player_rect.colliderect(obj_rect):
                return
        self.rect.x = new_x
        self.rect.y = new_y

    def get_camera_offset(self):
        camera_offset_x = Constants.SCREEN_WIDTH // 2 - self.rect.centerx + 300
        camera_offset_y = Constants.SCREEN_HEIGHT // 2 - self.rect.centery + 100

        camera_offset_x = min(0, camera_offset_x)
        camera_offset_x = max(Constants.SCREEN_WIDTH - Constants.MAP_WIDTH * Constants.TILE_SIZE + 700, camera_offset_x)
        camera_offset_y = min(0, camera_offset_y)
        camera_offset_y = max(Constants.SCREEN_HEIGHT - Constants.MAP_HEIGHT * Constants.TILE_SIZE + 380, camera_offset_y)

        return camera_offset_x, camera_offset_y

    def update_animation(self):
        current_time = pygame.time.get_ticks()
        self.frame_index = (current_time // self.frame_duration) % len(self.animation_frames)

        # Update typing animation
        if self.wrong_feedback:
            if current_time - self.last_update_time > self.typing_speed:
                self.last_update_time = current_time
                if self.current_text_length < len(self.tooltip_text):
                    self.current_text_length += 1
            if current_time - self.typing_start_time > 3000:  # 1 second in milliseconds
                self.wrong_feedback = False
                self.current_text_length = 0
        else:
            self.current_text_length = 0  # Reset text length when not showing wrong feedback

    def update(self, screen):
        keys = pygame.key.get_pressed()
        move_x, move_y = self.handle_movement(keys)
        self.update_position(move_x, move_y)
        self.update_animation()

    def draw(self, screen, camera_offset_x, camera_offset_y):
        screen.blit(self.animation_frames[int(self.frame_index)], (self.rect.x + camera_offset_x, self.rect.y + camera_offset_y))

        if self.wrong_feedback:
            # Render tooltip
            font = pygame.font.Font(None, 24)  # You can specify a font file instead of None
            text_to_display = self.tooltip_text[:self.current_text_length]
            text_surf = font.render(text_to_display, True, Constants.WHITE)
            text_rect = text_surf.get_rect(center=(self.rect.centerx + camera_offset_x, self.rect.top + camera_offset_y - 10))
            screen.blit(text_surf, text_rect)

    def wrong_command(self):
        self.wrong_feedback = True
        self.typing_start_time = pygame.time.get_ticks()  # Record the time when the typing animation starts

