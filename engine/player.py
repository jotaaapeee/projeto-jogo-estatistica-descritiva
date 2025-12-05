import pygame
import os
from config import PLAYER_COLOR, PLAYER_SPEED, TILE_SIZE
from engine.animation import Animation

class Player:
    def __init__(self, pos):
        self.rect = pygame.Rect(pos[0], pos[1], TILE_SIZE, TILE_SIZE)
        self.color = PLAYER_COLOR
        self.speed = PLAYER_SPEED
        self.is_moving = False
        self.facing_right = True  # Direção do sprite
        
        # Carrega animações
        self.load_animations()
        
        # Estado atual da animação
        self.current_animation = None  # Só usa animação quando correndo
        self.is_dead = False
    
    def load_animations(self):
        """Carrega imagens estáticas e animações do player"""
        base_path = os.path.join("assets", "player1", "Knight")
        
        sprite_width = 64  # Ajuste conforme necessário
        sprite_height = 64  # Ajuste conforme necessário
        
        self.animations = {}
        self.idle_image = None  # Imagem estática quando parado
        
        # Idle - carrega apenas o primeiro frame como imagem estática
        idle_path = os.path.join(base_path, "Idle", "Idle-Sheet.png")
        if os.path.exists(idle_path):
            try:
                idle_sheet = pygame.image.load(idle_path).convert_alpha()
                # Pega o primeiro frame (0, 0)
                self.idle_image = pygame.Surface((32, 32), pygame.SRCALPHA)
                self.idle_image.blit(idle_sheet, (0, 0), (0, 0, 32, 32))
            except Exception as e:
                print(f"Erro ao carregar imagem idle: {e}")
                self.idle_image = None
        
        # Run - animação quando se movendo
        run_path = os.path.join(base_path, "Run", "Run-Sheet.png")
        if os.path.exists(run_path):
            run_img = pygame.image.load(run_path)
            run_cols = run_img.get_width() // sprite_width
            run_rows = run_img.get_height() // sprite_height
            run_frames = run_cols * run_rows
            self.animations['run'] = Animation(run_path, sprite_width, sprite_height, run_frames, fps=10)
        else:
            self.animations['run'] = None
        
        # Death - animação de morte
        death_path = os.path.join(base_path, "Death", "Death-Sheet.png")
        if os.path.exists(death_path):
            death_img = pygame.image.load(death_path)
            death_cols = death_img.get_width() // sprite_width
            death_rows = death_img.get_height() // sprite_height
            death_frames = death_cols * death_rows
            self.animations['death'] = Animation(death_path, sprite_width, sprite_height, death_frames, fps=8)
            self.animations['death'].set_playing(False)  # Death não loopa
        else:
            self.animations['death'] = None

    def handle_input(self, keys, dt):
        if self.is_dead:
            return
            
        dx = dy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= 1
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += 1
            self.facing_right = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += 1
        
        self.is_moving = (dx != 0 or dy != 0)
        
        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071
        
        self.rect.x += int(dx * self.speed * dt)
        self.rect.y += int(dy * self.speed * dt)
        
        # Atualiza animação baseado no movimento
        if self.is_moving and 'run' in self.animations and self.animations['run']:
            if self.current_animation != self.animations['run']:
                self.current_animation = self.animations['run']
        else:
            # Quando parado, não usa animação
            self.current_animation = None
    
    def die(self):
        """Marca o player como morto e inicia animação de morte"""
        self.is_dead = True
        if 'death' in self.animations and self.animations['death']:
            self.current_animation = self.animations['death']
            self.current_animation.reset()
            self.current_animation.set_playing(True)
    
    def update(self, dt):
        """Atualiza a animação atual"""
        if self.current_animation:
            self.current_animation.update(dt)

    def draw(self, surface):
        # Se está morto, usa animação de morte
        if self.is_dead and 'death' in self.animations and self.animations['death']:
            frame = self.animations['death'].get_current_frame()
            if frame:
                if not self.facing_right:
                    frame = pygame.transform.flip(frame, True, False)
                frame_rect = frame.get_rect()
                draw_x = self.rect.x + (self.rect.width - frame_rect.width) // 2
                draw_y = self.rect.y + (self.rect.height - frame_rect.height) // 2
                surface.blit(frame, (draw_x, draw_y))
                return
        
        # Se está se movendo, usa animação de corrida
        if self.current_animation and self.current_animation.get_current_frame():
            frame = self.current_animation.get_current_frame()
            
            # Espelha o frame se estiver olhando para esquerda
            if not self.facing_right:
                frame = pygame.transform.flip(frame, True, False)
            
            # Centraliza o sprite no rect
            frame_rect = frame.get_rect()
            draw_x = self.rect.x + (self.rect.width - frame_rect.width) // 2
            draw_y = self.rect.y + (self.rect.height - frame_rect.height) // 2
            
            surface.blit(frame, (draw_x, draw_y))
        # Se está parado, usa imagem estática
        elif self.idle_image:
            img = self.idle_image
            
            # Espelha a imagem se estiver olhando para esquerda
            if not self.facing_right:
                img = pygame.transform.flip(img, True, False)
            
            # Centraliza o sprite no rect
            img_rect = img.get_rect()
            draw_x = self.rect.x + (self.rect.width - img_rect.width) // 2
            draw_y = self.rect.y + (self.rect.height - img_rect.height) // 2
            
            surface.blit(img, (draw_x, draw_y))
        else:
            # Fallback: desenha retângulo se não tiver sprite
            pygame.draw.rect(surface, self.color, self.rect)
