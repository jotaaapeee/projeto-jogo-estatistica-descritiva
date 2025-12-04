import pygame


class Animation:
    def __init__(self, sprite_sheet_path, frame_width, frame_height, num_frames, fps=10, loop=True):
        """
        Inicializa uma animação a partir de uma sprite sheet.
        
        Args:
            sprite_sheet_path: Caminho para o arquivo da sprite sheet
            frame_width: Largura de cada frame
            frame_height: Altura de cada frame
            num_frames: Número total de frames na animação
            fps: Frames por segundo da animação
            loop: Se True, a animação faz loop; se False, para no último frame
        """
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.num_frames = num_frames
        self.fps = fps
        self.loop = loop
        
        # Calcula quantas colunas e linhas tem na sprite sheet
        self.cols = self.sprite_sheet.get_width() // frame_width
        self.rows = self.sprite_sheet.get_height() // frame_height
        
        # Estado da animação
        self.current_frame = 0
        self.frame_time = 0.0
        self.frame_duration = 1.0 / fps if fps > 0 else 0
        self.is_playing = True
        
        # Pré-carrega todos os frames
        self.frames = []
        self._load_frames()
    
    def _load_frames(self):
        """Carrega todos os frames da sprite sheet em uma lista"""
        self.frames = []
        for i in range(self.num_frames):
            row = i // self.cols
            col = i % self.cols
            
            x = col * self.frame_width
            y = row * self.frame_height
            
            frame = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
            frame.blit(self.sprite_sheet, (0, 0), (x, y, self.frame_width, self.frame_height))
            self.frames.append(frame)
    
    def set_playing(self, playing):
        """Define se a animação está tocando"""
        self.is_playing = playing
    
    def reset(self):
        """Reseta a animação para o primeiro frame"""
        self.current_frame = 0
        self.frame_time = 0.0
    
    def update(self, dt):
        """
        Atualiza a animação com base no tempo decorrido.
        
        Args:
            dt: Delta time (tempo decorrido desde o último frame) em segundos
        """
        if not self.is_playing or len(self.frames) == 0:
            return
        
        self.frame_time += dt
        
        # Avança para o próximo frame quando necessário
        if self.frame_time >= self.frame_duration:
            self.frame_time = 0.0
            self.current_frame += 1
            
            # Controla o loop ou para no último frame
            if self.current_frame >= self.num_frames:
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = self.num_frames - 1
                    self.is_playing = False
    
    def get_current_frame(self):
        """
        Retorna o frame atual da animação.
        
        Returns:
            pygame.Surface: O frame atual, ou None se não houver frames
        """
        if len(self.frames) == 0:
            return None
        return self.frames[self.current_frame]
    
    def is_finished(self):
        """Retorna True se a animação terminou (apenas para animações não-loop)"""
        if self.loop:
            return False
        return self.current_frame >= self.num_frames - 1 and not self.is_playing
