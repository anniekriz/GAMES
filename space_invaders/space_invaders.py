import sys 
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from common.game_base import GameBase
import pygame

class SpaceInvaders(GameBase):

    def __init__(self):
        super().__init__("Space Invaders")

pygame.init()
game = SpaceInvaders()

running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

pygame.quit()