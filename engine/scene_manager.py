import pygame
import json, os
from engine.player import Player
from engine.npc import NPC
from engine.dialogue import Dialogue
from engine.tilemap import TileMap
from config import SCREEN_SIZE, BG_COLOR, FONT_PATH, FONT_SIZE

class SceneManager:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(FONT_PATH, FONT_SIZE)
        self.load_data()

        # Sistema de vidas e fases
        self.lives = 3
        self.current_phase = 0
        self.game_over = False

        self.tilemap = TileMap(os.path.join("assets","Dungeon_Tiles.png"))
        self.player = Player((40, 40))

        # Carrega primeira pergunta
        self.load_phase()

        self.dialogue = Dialogue(screen, self.font, None)
        self.in_dialogue = False

    def load_data(self):
        data_path = os.path.join("data", "perguntas.json")
        with open(data_path, "r", encoding="utf-8") as f:
            self.questions = json.load(f)

    def load_phase(self):
        """Carrega a fase atual com a pergunta correspondente"""
        if self.current_phase < len(self.questions):
            q = self.questions[self.current_phase]
            # Posiciona NPC em posição diferente a cada fase (ou pode manter fixo)
            self.npc = NPC((240, 120), q)
        else:
            self.game_over = True

    def handle_event(self, event):
        if self.game_over:
            return

        if self.in_dialogue and self.dialogue.visible:
            self.dialogue.handle_event(event)
            
            # Verifica se diálogo foi fechado
            if not self.dialogue.visible:
                # Diálogo foi fechado (ESC ou resposta)
                if self.dialogue.result is not None:
                    # Respondeu a pergunta
                    if self.dialogue.result:
                        # Acertou - avança para próxima fase
                        self.current_phase += 1
                        if self.current_phase < len(self.questions):
                            self.load_phase()
                        else:
                            # Todas as fases completadas!
                            self.game_over = True
                    else:
                        # Errou - perde uma vida
                        self.lives -= 1
                        if self.lives <= 0:
                            self.player.die()
                            self.game_over = True
                    
                    self.dialogue.result = None
                # Se result é None, foi fechado com ESC (não faz nada)
                
                self.in_dialogue = False
        else:
            # Abre diálogo quando player chega perto do NPC
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                if self.player.rect.colliderect(self.npc.rect.inflate(8,8)):
                    self.dialogue.open(self.npc.question)
                    self.in_dialogue = True

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if not (self.in_dialogue and self.dialogue.visible):
            self.player.handle_input(keys, dt)
        
        # Atualiza animações
        self.player.update(dt)
        if hasattr(self, 'npc'):
            self.npc.update(dt)

    def draw(self):
        self.tilemap.draw(self.screen)
        self.player.draw(self.screen)
        self.npc.draw(self.screen)
        self.dialogue.draw()
        
        # Desenha vidas na tela
        self.draw_lives()
        
        # Desenha game over ou vitória
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
            text = "VITORIA! Todas as fases completadas!"
            color = (60, 200, 60)
        
        txt_surf = self.font.render(text, True, color)
        txt_rect = txt_surf.get_rect(center=(w//2, h//2))
        self.screen.blit(txt_surf, txt_rect)
