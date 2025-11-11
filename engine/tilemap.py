import pygame
from config import TILE_SIZE

class TileMap:
    def __init__(self, tileset_path):
        self.tileset = pygame.image.load(tileset_path).convert()
        self.cols = self.tileset.get_width() // TILE_SIZE

        # Simple 4x12 test map
        self.map_data = [
            [0,1,2,3,0,1,2,3,0,1,2,3],
            [4,5,6,7,4,5,6,7,4,5,6,7],
            [8,9,10,11,8,9,10,11,8,9,10,11],
            [12,13,14,15,12,13,14,15,12,13,14,15]
        ]

    def draw(self, screen):
        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):
                tx = (tile % self.cols) * TILE_SIZE
                ty = (tile // self.cols) * TILE_SIZE
                screen.blit(self.tileset, (x*TILE_SIZE, y*TILE_SIZE),
                            (tx, ty, TILE_SIZE, TILE_SIZE))
