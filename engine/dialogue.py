import pygame
import textwrap

class Dialogue:
    def __init__(self, screen, font, data):
        self.screen = screen
        self.font = font
        self.visible = False
        self.selected = 0
        self.result = None

    def open(self, question):
        self.question = question
        self.visible = True
        self.selected = 0
        self.result = None

    def handle_event(self, event):
        if not self.visible:
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.question['opcoes'])
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.question['opcoes'])
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                selected_option = self.question['opcoes'][self.selected]
                correct_value = self.question['correta']
                self.result = (str(selected_option) == str(correct_value))
                self.visible = False
            elif event.key == pygame.K_ESCAPE:
                self.visible = False

    def draw(self):
        if not self.visible:
            return
        w, h = self.screen.get_size()
        box_h = 120
        box_rect = pygame.Rect(16, h - box_h - 16, w - 32, box_h)
        pygame.draw.rect(self.screen, (50,50,50), box_rect)
        pygame.draw.rect(self.screen, (200,200,200), box_rect, 2)

        lines = textwrap.wrap(self.question['texto'], width=80)
        y = box_rect.y + 8
        for line in lines:
            txt = self.font.render(line, True, (240,240,240))
            self.screen.blit(txt, (box_rect.x + 8, y))
            y += txt.get_height() + 2

        for i, opt in enumerate(self.question['opcoes']):
            prefix = ">" if i == self.selected else " "
            txt = self.font.render(f"{prefix} {opt}", True, (220,220,220))
            self.screen.blit(txt, (box_rect.x + 16, y + i * (self.font.get_height() + 6)))

        hint_txt = self.font.render("ESC para sair", True, (150, 150, 150))
        self.screen.blit(hint_txt, (box_rect.x + box_rect.width - hint_txt.get_width() - 8, 
                                     box_rect.y + box_rect.height - hint_txt.get_height() - 4))
