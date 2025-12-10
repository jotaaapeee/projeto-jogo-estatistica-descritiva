import pygame
import json, os
from engine.player import Player
from engine.npc import NPC
from engine.dialogue import Dialogue, IntroDialogue
from engine.tilemap import TileMap
from config import SCREEN_SIZE, BG_COLOR, FONT_PATH, FONT_SIZE

class SceneManager:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(FONT_PATH, FONT_SIZE)
        self.load_data()

        self.lives = 3
        self.current_phase = 0
        self.game_over = False

        self.load_map(0)
        self.player = Player((40, 40))

        self.load_phase()

        self.dialogue = Dialogue(screen, self.font, None)
        self.in_dialogue = False

        # Diálogo de introdução (bloqueia movimento até fechar)
        intro_text = (
            "Bem-vindo ao Protótipo - Quiz 8bit RPG!\n\n"
            "Use as setas ou WASD para se movimentar.\n"
            "Aproxime-se de um NPC e pressione 'E' para interagir.\n\n"
            "Responda corretamente para avançar de fase. Boa sorte!"
        )
        self.intro_dialogue = IntroDialogue(screen, self.font)
        self.intro_dialogue.open(intro_text)
        self.intro_active = True
        try:
            from config import TILE_SIZE
            map_rows = len(self.tilemap.map_data)
            map_pixel_h = map_rows * TILE_SIZE
            self.dialogue.max_map_height = map_pixel_h
            self.intro_dialogue.max_map_height = map_pixel_h
        except Exception:
            pass

    def load_data(self):
        data_path = os.path.join("data", "perguntas.json")
        with open(data_path, "r", encoding="utf-8") as f:
            self.questions = json.load(f)

    def load_map(self, map_index):
        """Carrega um mapa específico"""
        tileset_path = os.path.join("assets", "Dungeon_Tiles.png")
        self.tilemap = TileMap(tileset_path, map_index)
        try:
            from config import TILE_SIZE
            map_rows = len(self.tilemap.map_data)
            map_pixel_h = map_rows * TILE_SIZE
            if hasattr(self, 'dialogue'):
                self.dialogue.max_map_height = map_pixel_h
            if hasattr(self, 'intro_dialogue'):
                self.intro_dialogue.max_map_height = map_pixel_h
        except Exception:
            pass
    
    def load_phase(self):
        """Carrega a fase atual com a pergunta correspondente"""
        if self.current_phase < len(self.questions):
            map_index = self.current_phase % 6
            self.load_map(map_index)
            
            q = self.questions[self.current_phase]
            boss_index = self.current_phase % 3
            self.npc = NPC((240, 120), q, boss_index)
        else:
            self.game_over = True

    def handle_event(self, event):
        if self.game_over:
            return

        if self.intro_active and self.intro_dialogue.visible:
            self.intro_dialogue.handle_event(event)
            if not self.intro_dialogue.visible:
                self.intro_active = False
                self.in_dialogue = False
            return

        if self.in_dialogue and self.dialogue.visible:
            self.dialogue.handle_event(event)

            if not self.dialogue.visible:
                if self.dialogue.result is not None:
                    if self.dialogue.result:
                        self.current_phase += 1
                        if self.current_phase < len(self.questions):
                            self.load_phase()
                        else:
                            self.game_over = True
                    else:
                        self.lives -= 1
                        if self.lives <= 0:
                            self.player.die()
                            self.game_over = True
                    
                    self.dialogue.result = None
                
                self.in_dialogue = False
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                if self.player.rect.colliderect(self.npc.rect.inflate(8,8)):
                    self.dialogue.open(self.npc.question)
                    self.in_dialogue = True

    def update(self, dt):
        keys = pygame.key.get_pressed()
        dialogue_block = (self.in_dialogue and self.dialogue.visible) or (self.intro_active and self.intro_dialogue.visible)
        if not dialogue_block:
            self.player.handle_input(keys, dt)

        self.player.update(dt)
        if hasattr(self, 'npc'):
            self.npc.update(dt)

    def draw(self):
        self.tilemap.draw(self.screen)
        self.player.draw(self.screen)
        self.npc.draw(self.screen)
        self.dialogue.draw()

        if hasattr(self, 'intro_dialogue') and self.intro_active and self.intro_dialogue.visible:
            self.intro_dialogue.draw()

        self.draw_lives()

        if self.game_over:
            self.draw_game_over()

    def draw_lives(self):
        """Desenha as vidas no canto superior esquerdo"""
        x = 10
        y = 10
        for i in range(3):
            color = (200, 60, 60) if i < self.lives else (60, 60, 60)
            pygame.draw.circle(self.screen, color, (x + i * 20, y), 6)
            pygame.draw.circle(self.screen, (255, 255, 255), (x + i * 20, y), 6, 1)

    def draw_game_over(self):
        """Desenha tela de game over ou vitória"""
        w, h = self.screen.get_size()
        overlay = pygame.Surface((w, h))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        if self.lives <= 0:
            text = "GAME OVER"
            color = (200, 60, 60)
        else:
            text = "VITORIA! Voce respondeu todas as respostas de forma correta. Parabens!"
            color = (60, 200, 60)
        
        txt_surf = self.font.render(text, True, color)
        txt_rect = txt_surf.get_rect(center=(w//2, h//2))
        self.screen.blit(txt_surf, txt_rect)
