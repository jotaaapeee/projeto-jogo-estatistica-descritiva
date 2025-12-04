import pygame
from config import NPC_COLOR, TILE_SIZE

class NPC:
    def __init__(self, pos, question):
        self.rect = pygame.Rect(pos[0], pos[1], TILE_SIZE, TILE_SIZE)
        self.color = NPC_COLOR
        self.question = question

    def update(self, dt):
        """Atualiza o NPC (pode ser usado para animações futuras)"""
        pass

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
