import pygame

class GameBase:

    name = ""

    def __init__(self, name):
        self.name = name
        self.create_window()

    def create_window(self):
        screen_info = pygame.display.Info()
        screen_width = screen_info.current_w
        screen_height = screen_info.current_h
        screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
        pygame.display.set_caption(self.name)