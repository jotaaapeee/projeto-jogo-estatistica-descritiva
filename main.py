import pygame
from engine.scene_manager import SceneManager
from config import SCREEN_SIZE, FPS

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Protótipo - Quiz RPG")
    clock = pygame.time.Clock()
    manager = SceneManager(screen)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            manager.handle_event(event)

        manager.update(dt)
        manager.draw()
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
