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

        pad = 8
        wrap_width = 80
        lines = textwrap.wrap(self.question['texto'], width=wrap_width)
        text_heights = [self.font.render(line, True, (240,240,240)).get_height() for line in lines]
        text_total_h = sum(text_heights) + (len(lines) - 1) * 2 if lines else 0

        option_h = (self.font.get_height() + 6) * len(self.question.get('opcoes', []))
        hint_h = self.font.get_height() + 4

        desired_h = pad + text_total_h + 6 + option_h + hint_h + pad

        max_box_h = max(80, h // 2)
        if hasattr(self, 'max_map_height') and self.max_map_height:
            map_limit = max(80, int(self.max_map_height * 0.5))
            max_box_h = min(max_box_h, map_limit)
        box_h = min(desired_h, max_box_h)
        box_rect = pygame.Rect(16, h - box_h - 16, w - 32, box_h)

        pygame.draw.rect(self.screen, (50,50,50), box_rect)
        pygame.draw.rect(self.screen, (200,200,200), box_rect, 2)

        y = box_rect.y + pad
        for line in lines:
            txt = self.font.render(line, True, (240,240,240))
            self.screen.blit(txt, (box_rect.x + 8, y))
            y += txt.get_height() + 2

        for i, opt in enumerate(self.question.get('opcoes', [])):
            prefix = ">" if i == self.selected else " "
            txt = self.font.render(f"{prefix} {opt}", True, (220,220,220))
            if y + self.font.get_height() > box_rect.y + box_rect.height - hint_h - pad:
                break
            self.screen.blit(txt, (box_rect.x + 16, y))
            y += self.font.get_height() + 6

        hint_txt = self.font.render("ESC para sair", True, (150, 150, 150))
        self.screen.blit(hint_txt, (box_rect.x + box_rect.width - hint_txt.get_width() - 8,
                                     box_rect.y + box_rect.height - hint_txt.get_height() - 4))


class IntroDialogue:
    """Caixa de diálogo de introdução/boas-vindas. Fecha quando o jogador aperta 'E'."""
    def __init__(self, screen, font, data=None):
        self.screen = screen
        self.font = font
        self.visible = False

    def open(self, text):
        self.text = text
        self.visible = True

    def handle_event(self, event):
        if not self.visible:
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                self.visible = False

    def draw(self):
        if not self.visible:
            return
        w, h = self.screen.get_size()

        pad = 8
        wrap_width = 80
        lines = textwrap.wrap(self.text, width=wrap_width)
        text_heights = [self.font.render(line, True, (240,240,240)).get_height() for line in lines]
        text_total_h = sum(text_heights) + (len(lines) - 1) * 4 if lines else 0

        hint_h = self.font.get_height() + 6
        desired_h = pad + text_total_h + pad + hint_h + pad

        max_box_h = max(100, h // 2)
        if hasattr(self, 'max_map_height') and self.max_map_height:
            map_limit = max(80, int(self.max_map_height * 0.5))
            max_box_h = min(max_box_h, map_limit)
        box_h = min(desired_h, max_box_h)
        box_rect = pygame.Rect(16, h - box_h - 16, w - 32, box_h)

        pygame.draw.rect(self.screen, (40,40,60), box_rect)
        pygame.draw.rect(self.screen, (200,200,200), box_rect, 2)

        y = box_rect.y + pad
        for line in lines:
            txt = self.font.render(line, True, (240,240,240))
            if y + txt.get_height() > box_rect.y + box_rect.height - hint_h - pad:
                break
            self.screen.blit(txt, (box_rect.x + 8, y))
            y += txt.get_height() + 4

        hint = "Pressione 'E' para começar"
        hint_txt = self.font.render(hint, True, (200,200,120))
        self.screen.blit(hint_txt, (box_rect.x + box_rect.width - hint_txt.get_width() - 8,
                                     box_rect.y + box_rect.height - hint_txt.get_height() - 6))
