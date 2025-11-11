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

        self.tilemap = TileMap(os.path.join("assets","Dungeon_Tiles.png"))
        self.player = Player((40, 40))

        q = self.questions[0]
        self.npc = NPC((240, 120), q)

        self.dialogue = Dialogue(screen, self.font, None)
        self.dialogue.open(q)
        self.in_dialogue = True

    def load_data(self):
        data_path = os.path.join("data", "perguntas.json")
        with open(data_path, "r", encoding="utf-8") as f:
            self.questions = json.load(f)

    def handle_event(self, event):
        if self.in_dialogue and self.dialogue.visible:
            self.dialogue.handle_event(event)
            if self.dialogue.result is not None:
                print("Correto" if self.dialogue.result else "Errado")
                self.in_dialogue = False
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                if self.player.rect.colliderect(self.npc.rect.inflate(8,8)):
                    self.dialogue.open(self.npc.question)
                    self.in_dialogue = True

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if not (self.in_dialogue and self.dialogue.visible):
            self.player.handle_input(keys, dt)

    def draw(self):
        self.tilemap.draw(self.screen)
        self.player.draw(self.screen)
        self.npc.draw(self.screen)
        self.dialogue.draw()
