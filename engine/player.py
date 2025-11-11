import pygame
from config import PLAYER_COLOR, PLAYER_SPEED, TILE_SIZE

class Player:
    def __init__(self, pos):
        self.rect = pygame.Rect(pos[0], pos[1], TILE_SIZE, TILE_SIZE)
        self.color = PLAYER_COLOR
        self.speed = PLAYER_SPEED

    def handle_input(self, keys, dt):
        dx = dy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += 1
        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071
        self.rect.x += int(dx * self.speed * dt)
        self.rect.y += int(dy * self.speed * dt)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
