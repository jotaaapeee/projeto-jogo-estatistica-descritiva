import pygame
import os

from config import TILE_SIZE


def main():
    pygame.init()

    tileset_path = os.path.join("assets", "Dungeon_Tiles.png")

    pygame.display.set_mode((1, 1))
    tileset = pygame.image.load(tileset_path).convert()

    tileset_width, tileset_height = tileset.get_size()
    cols = tileset_width // TILE_SIZE
    rows = tileset_height // TILE_SIZE

    scale = 2
    tile_draw_size = TILE_SIZE * scale

    screen_width = cols * tile_draw_size
    screen_height = rows * tile_draw_size

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Visualizador de Tiles - Mostrando índices")

    font = pygame.font.SysFont(None, 18)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        index = 0
        for row in range(rows):
            for col in range(cols):
                src_rect = pygame.Rect(
                    col * TILE_SIZE,
                    row * TILE_SIZE,
                    TILE_SIZE,
                    TILE_SIZE,
                )

                dest_x = col * tile_draw_size
                dest_y = row * tile_draw_size

                tile_surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
                tile_surface.blit(tileset, (0, 0), src_rect)
                tile_surface = pygame.transform.scale(
                    tile_surface, (tile_draw_size, tile_draw_size)
                )
                screen.blit(tile_surface, (dest_x, dest_y))

                text_surf = font.render(str(index), True, (255, 255, 0))
                screen.blit(text_surf, (dest_x + 2, dest_y + 2))

                index += 1

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()


