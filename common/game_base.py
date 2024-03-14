import pygame


class GameBase:
    
    BORDER_H = 28
    BORDER_W = 28
    BACKGROUND_COLOR = (0, 0, 0)
    BORDER_COLOR = (100, 0, 0)
    SCORE_COLOR = (255, 255, 255)

    _name = None
    _screen = None
    _screen_height = None
    _screen_width = None
    _score = None
    _best_score = None

    @property
    def maxRight(self) -> int:
        return self._screen_width - self.BORDER_W
    
    @property
    def maxLeft(self) -> int:
        return self.BORDER_W
    
    @property
    def maxTop(self) -> int:
         return self.BORDER_H
    
    @property
    def maxBottom(self) -> int:
        return self._screen_height - self.BORDER_H

    def __init__(self, name): 
        self._name = name
        self._create_window()
        self._create_border()
        self.set_score(0)
        self.set_best_score(0)

    def _create_window(self):
        screen_info = pygame.display.Info()
        self._screen_width = screen_info.current_w
        self._screen_height = screen_info.current_h
        self._screen = pygame.display.set_mode((self._screen_width, self._screen_height), pygame.FULLSCREEN)
        self._screen.fill(self.BACKGROUND_COLOR)
        pygame.display.set_caption(self._name)
    
    def _create_border(self):
        pygame.draw.rect(self._screen, self.BORDER_COLOR, (0,0,self._screen_width,self.BORDER_H))
        pygame.draw.rect(self._screen, self.BORDER_COLOR, (0,0,self.BORDER_W,self._screen_height))
        pygame.draw.rect(self._screen, self.BORDER_COLOR, (0,self._screen_height-self.BORDER_H,self._screen_width,self.BORDER_H))
        pygame.draw.rect(self._screen, self.BORDER_COLOR, (self._screen_width-self.BORDER_W,0,self.BORDER_W,self._screen_height))
        pygame.display.flip()
    
    def _render_score(self, positionX: int, positionY: int, label: str, value: int):
        FONT_SIZE = 27

        font = pygame.font.Font(None, FONT_SIZE)
        text = font.render(str(value), True, self.SCORE_COLOR)
        textSize = text.get_size()
        pygame.draw.rect(self._screen, self.BORDER_COLOR,((positionX - textSize[0] / 2), (positionY - textSize[1] / 2), textSize[0] * 2, textSize[1] * 1.5))
        self._screen.blit(text, (positionX, positionY))
        font = pygame.font.Font(None, FONT_SIZE)
        text = font.render(label, True, self.SCORE_COLOR)
        textSize = text.get_size()
        self._screen.blit(text, (positionX - textSize[0] - 5, positionY))
        pygame.display.flip()

    def set_score(self, score: int):
        self._score = score
        self._render_score(1200, 5, "SCORE:", self._score)

    def set_best_score(self, best_score: int):
        self._best_score = best_score
        self._render_score(300, 5, "BEST SCORE:", self._best_score)