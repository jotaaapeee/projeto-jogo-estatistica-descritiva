import pygame
import os
from config import NPC_COLOR, TILE_SIZE

class NPC:
    def __init__(self, pos, question, boss_index=0):
        """
        Cria um NPC (boss) com sprite
        
        Args:
            pos: posição (x, y)
            question: pergunta associada ao boss
            boss_index: índice do boss (0=boss1, 1=boss2, 2=boss3)
        """
        self.rect = pygame.Rect(pos[0], pos[1], TILE_SIZE, TILE_SIZE)
        self.color = NPC_COLOR
        self.question = question
        self.boss_index = boss_index
        
        # Carrega imagem estática do boss
        self.load_boss_image()

    def load_boss_image(self):
        """Carrega a imagem estática do boss (primeiro frame da spritesheet)"""
        boss_folders = ["boss1/Wizzard", "boss2/Orc - Warrior", "boss3/Orc - Shaman"]
        
        self.boss_image = None
        
        if self.boss_index < len(boss_folders):
            boss_folder = boss_folders[self.boss_index]
            base_path = os.path.join("assets", "bosses", boss_folder, "Idle")
            idle_path = os.path.join(base_path, "Idle-Sheet.png")
            
            if os.path.exists(idle_path):
                try:
                    sprite_width = 32
                    sprite_height = 32
                    
                    idle_sheet = pygame.image.load(idle_path).convert_alpha()
                    # Pega o primeiro frame (0, 0)
                    self.boss_image = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
                    self.boss_image.blit(idle_sheet, (0, 0), (0, 0, sprite_width, sprite_height))
                except Exception as e:
                    print(f"Erro ao carregar imagem do boss: {e}")
                    self.boss_image = None

    def update(self, dt):
        """Boss não precisa atualizar animação (usa imagem estática)"""
        pass

    def draw(self, surface):
        if self.boss_image:
            img_rect = self.boss_image.get_rect()
            draw_x = self.rect.x + (self.rect.width - img_rect.width) // 2
            draw_y = self.rect.y + (self.rect.height - img_rect.height) // 2
            
            surface.blit(self.boss_image, (draw_x, draw_y))
        else:
            pygame.draw.rect(surface, self.color, self.rect)
