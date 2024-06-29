import pygame
import sys

from utils.resource_path_util import resource_path

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TILE_SIZE = 32
MAP_WIDTH = 200  # Number of tiles wide
MAP_HEIGHT = 200  # Number of tiles high
MOVE_SPEED = TILE_SIZE // 8  # Number of pixels to move per second (slowed down)
ZOOM_SCALE = 1.5  # Zoom scale factor

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tile Map with Character Movement")
clock = pygame.time.Clock()

# Load background image and scale it
try:
    background_img = pygame.image.load(resource_path("assets\\images\\background.jpg")).convert()
except pygame.error as e:
    print("Error loading background image:", e)
    sys.exit()

background_img = pygame.transform.scale(background_img, (MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE))

# Example map (just a simple grid for demonstration)
tile_map = [
    [0] * MAP_WIDTH for _ in range(MAP_HEIGHT)
]

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

# Create player object
player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # Start player in the center of the screen

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle player movement
    keys = pygame.key.get_pressed()
    move_x = 0
    move_y = 0
    if keys[pygame.K_a]:
        move_x -= MOVE_SPEED
    if keys[pygame.K_d]:
        move_x += MOVE_SPEED
    if keys[pygame.K_w]:
        move_y -= MOVE_SPEED
    if keys[pygame.K_s]:
        move_y += MOVE_SPEED

    # Move the player
    player.move(move_x, move_y)

    # Ensure player stays within bounds of the screen
    player.rect.x = max(0, min(player.rect.x, MAP_WIDTH * TILE_SIZE - TILE_SIZE))
    player.rect.y = max(0, min(player.rect.y, MAP_HEIGHT * TILE_SIZE - TILE_SIZE))

    # Calculate the camera offset to center the player on the screen with zoom
    camera_offset_x = SCREEN_WIDTH // 2 - player.rect.centerx * ZOOM_SCALE
    camera_offset_y = SCREEN_HEIGHT // 2 - player.rect.centery * ZOOM_SCALE

    # Draw the background image (scaled to fit the map)
    screen.blit(background_img, (0, 0))  # Draw at (0, 0) as it covers the entire screen

    # Draw the player
    screen.blit(player.image, player.rect)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
