import pygame
import json
import os
import random
from config import TILE_SIZE

class TileMap:
    def __init__(self, tileset_path, map_index=0):
        """
        Cria um mapa de tiles
        
        Args:
            tileset_path: caminho para o tileset
            map_index: índice do mapa a carregar (0-5 para 6 mapas diferentes)
        """
        self.tileset = pygame.image.load(tileset_path).convert()
        self.cols = self.tileset.get_width() // TILE_SIZE

        map_path = os.path.join("data", "maps", f"map_{map_index}.json")
        if os.path.exists(map_path):
            self.load_from_file(map_path)
        else:
            self.generate_map(map_index)
    
    def load_from_file(self, map_path):
        """Carrega mapa de um arquivo JSON"""
        try:
            with open(map_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.map_data = data["map_data"]
        except Exception as e:
            print(f"Erro ao carregar mapa {map_path}: {e}")
            self.generate_map(0)
    
    def generate_map(self, map_index):
        """Gera um mapa automaticamente baseado no índice com tipos de piso variados"""
        width = 30
        height = 18

        floor_types = ["pedra", "pedra", "madeira", "madeira", "terra", "terra"]
        floor_type = floor_types[map_index]

        tiles = self._get_floor_tiles(floor_type)

        self.map_data = self._generate_room(width, height, 
                                            tiles["top_left"], tiles["top_right"], 
                                            tiles["top"], tiles["bottom_left"], 
                                            tiles["bottom_right"], tiles["bottom"],
                                            tiles["left"], tiles["right"], tiles["center"])

        self._add_floor_variety(tiles, map_index)
    
    def _get_floor_tiles(self, floor_type):
        """Retorna os tiles corretos baseado no tipo de piso"""
        if floor_type == "pedra":
            return {
                "top_left": 75,
                "top": 76,
                "top_right": 77,
                "left": 129,
                "right": 128,
                "bottom_left": 100,
                "bottom": 101,
                "bottom_right": 102,
                "center": 30,
                "variations": [30, 31, 29, 6, 4, 5, 55, 56, 54, 83] 
            }
        elif floor_type == "madeira":
            return {
                "top_left": 17,
                "top": 18,
                "top_right": 19,
                "left": 42,
                "right": 44,
                "bottom_left": 67,
                "bottom": 68,
                "bottom_right": 69,
                "center": 90,
                "variations": [90, 40, 43]
            }
        else:  # terra
            return {
                "top_left": 110,
                "top": 111,
                "top_right": 112,
                "left": 135,
                "right": 137,
                "bottom_left": 160,
                "bottom": 161,
                "bottom_right": 162,
                "center": 136,
                "variations": [136, 88, 13, 10]
            }
    
    def _add_floor_variety(self, tiles, map_index):
        """Adiciona variedade nos pisos usando tiles de sombra e variações"""
        width = 30
        height = 18
        is_stone = tiles["center"] == 30

        for y in range(1, height - 1):
            for x in range(1, width - 1):
                if random.random() < 0.20 and 2 < x < width - 2 and 2 < y < height - 2:
                    self.map_data[y][x] = random.choice(tiles["variations"])

                if is_stone:
                    if x == width - 2 and random.random() < 0.4:
                        self.map_data[y][x] = 31
                    elif x == 1 and random.random() < 0.4:
                        self.map_data[y][x] = 29
                    elif y == 1 and random.random() < 0.4:
                        self.map_data[y][x] = 55
                    elif y == height - 2 and random.random() < 0.4:
                        self.map_data[y][x] = 5

                    if x == 1 and y == 1 and random.random() < 0.6:
                        self.map_data[y][x] = 4
                    elif x == width - 2 and y == 1 and random.random() < 0.6:
                        self.map_data[y][x] = 6
                    elif x == 1 and y == height - 2 and random.random() < 0.6:
                        self.map_data[y][x] = 54
                    elif x == width - 2 and y == height - 2 and random.random() < 0.6:
                        self.map_data[y][x] = 56
    
    def _generate_room(self, width, height, top_left, top_right, top, bottom_left, 
                      bottom_right, bottom, left, right, floor):
        """Gera uma sala retangular básica"""
        map_data = []
        for y in range(height):
            row = []
            for x in range(width):
                if y == 0:
                    if x == 0:
                        tile = top_left
                    elif x == width - 1:
                        tile = top_right
                    else:
                        tile = top
                elif y == height - 1:
                    if x == 0:
                        tile = bottom_left
                    elif x == width - 1:
                        tile = bottom_right
                    else:
                        tile = bottom
                else:
                    if x == 0:
                        tile = left
                    elif x == width - 1:
                        tile = right
                    else:
                        tile = floor
                row.append(tile)
            map_data.append(row)
        return map_data

    def draw(self, screen):
        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):
                tx = (tile % self.cols) * TILE_SIZE
                ty = (tile // self.cols) * TILE_SIZE
                screen.blit(self.tileset, (x*TILE_SIZE, y*TILE_SIZE),
                            (tx, ty, TILE_SIZE, TILE_SIZE))
