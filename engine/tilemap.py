import pygame
from config import TILE_SIZE

class TileMap:
    def __init__(self, tileset_path):
        self.tileset = pygame.image.load(tileset_path).convert()
        self.cols = self.tileset.get_width() // TILE_SIZE

        # Sala de dungeon maior:
        # - 75  = canto superior esquerdo
        # - 77  = canto superior/direito
        # - 76   = parede superior (no meio)
        # - 101 = parede inferior (no meio)
        # - 129 = parede esquerda
        # - 128 = parede direita
        # - 30  = chão
        #
        # width  = número de colunas (largura em tiles)
        # height = número de linhas (altura em tiles)
        # Com TILE_SIZE = 16 e SCREEN_SIZE = (480, 320),
        #  width  = 30 -> 30 * 16 = 480 px
        #  height = 18 -> 18 * 16 = 288 px (cabe confortavelmente na altura)

        width = 30
        height = 18

        self.map_data = []

        for y in range(height):
            row = []
            for x in range(width):
                # primeira linha: borda superior
                if y == 0:
                    if x == 0:
                        tile = 75  # canto sup. esquerdo
                    elif x == width - 1:
                        tile = 77  # canto sup. direito
                    else:
                        tile = 76   # topo

                # última linha: borda inferior
                elif y == height - 1:
                    if x == 0:
                        tile = 100
                    elif x == width - 1:
                        tile = 102
                    else:
                        tile = 101  # base

                # linhas do meio
                else:
                    if x == 0:
                        tile = 129  # parede esquerda
                    elif x == width - 1:
                        tile = 128  # parede direita
                    else:
                        tile = 30   # chão

                row.append(tile)
            self.map_data.append(row)

    def draw(self, screen):
        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):
                tx = (tile % self.cols) * TILE_SIZE
                ty = (tile // self.cols) * TILE_SIZE
                screen.blit(self.tileset, (x*TILE_SIZE, y*TILE_SIZE),
                            (tx, ty, TILE_SIZE, TILE_SIZE))
