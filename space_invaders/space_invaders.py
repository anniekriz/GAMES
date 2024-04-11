import sys 
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from common.game_base import GameBase
import pygame
from typing import List, Tuple
import math
import threading
import weakref
import random

class SpaceInvaders(GameBase):
    _spaceship = None
    _invader = None
    _invaderSpot = None

    def __init__(self):
        super().__init__("Space Invaders")
        pygame.key.set_repeat(1, 1)
        self._spaceship = Spaceship(self._screen, self.BACKGROUND_COLOR)
        self._spaceship.draw(692, 850)
        self._invader = Invader(self._screen, self.BACKGROUND_COLOR)
        self._setInvaderSpot()
        self._invader.draw(self._invaderSpot, 70)
        self._handleEvents()
    
    def _setInvaderSpot(self):
        self._invaderSpot = random.randint(self.BORDER_W, self._screen_width - (self.BORDER_W + Invader.SIZE))
    

    def _moveSpaceshipRight(self):
        if self._spaceship.position[0] < self.maxRight - self._spaceship.size:
            self._spaceship.drawBy(1, 0)

    def _moveSpaceshipLeft(self):
        if self._spaceship.position[0] > self.maxLeft:
            self._spaceship.drawBy(-1, 0)

    def _handleEvents(self):
        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_RIGHT:
                        self._moveSpaceshipRight()
                    if event.key == pygame.K_LEFT:
                        self._moveSpaceshipLeft()
                    if event.key == pygame.K_SPACE:
                        self._spaceship.shoot()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_i:
                        if self._invaderSpot != None: 
                            self._invader.erase()
                        self._invader = None
                        self._invader = Invader(self._screen, self.BACKGROUND_COLOR)
                        self._invader.draw(self._invaderSpot, 70)
                        self._setInvaderSpot()
                       


def _drawShot(s):
    s._y -= 22
    rect = _calculateShotCoordinates(s)
    pygame.draw.rect(s._screen, s._color, rect)
    pygame.display.flip()


def _calculateShotCoordinates(s) -> Tuple[int, int, int, int]:
    w = 5
    h = 20
    x = s._x - w/2
    y = s._y
    return (x, y, w, h)

def _onTimerElapsed(s):
    s._timer.cancel()
    print(s._y)
    _drawShot(s)
    s._timer = threading.Timer(0.1, _onTimerElapsed, [s])
    s._timer.start()

class SpaceshipBase():

    _screen = None
    _x = None
    _y = None
    _sx = None
    _sy = None
    _backgroundColor = None
    _shot = None
    _size = None
    _color = None
    _shotColor = None
    

    @property
    def position(self) -> Tuple[int, int]:
        return (self._x, self._y)
    
    @property
    def size(self) -> int:
        return self._size

    def __init__(self, screen: pygame.Surface, backgroundColor: pygame.Color, size: int, color: pygame.Color, shotColor: pygame.Color):
        self._screen = screen
        self._backgroundColor = backgroundColor
        self._size = size
        self._color = color
        self._shotColor = shotColor

    
    def draw(self, x: int, y: int):
        self.erase()
        self._drawSpaceship(x, y, self._color)
        self._x = x
        self._y = y
        pygame.display.flip()

    def erase(self):
        if self._x != None and self._y != None:
            self._drawSpaceship(self._x, self._y, self._backgroundColor)

    def drawBy(self, dx: int, dy: int):
        self.draw(self._x + dx, self._y + dy)

    def shoot(self):
        self._shot = Spaceship.Shot(self._screen, self._backgroundColor, self._shotColor)
        shotPos = self._calculateShotPosition()
        self._shot.draw(shotPos[0], shotPos[1])

    ################################################################################################    

    def _drawSpaceship(self, x: int, y: int, color: pygame.Color):
        points = self._calculateCoordinates(x, y, self._size)
        pygame.draw.polygon(self._screen, color, points)

    # returns list of points (pole bodů)
    def _calculateCoordinates(self, x: int, y: int, size: int) -> List[Tuple[int, int]]:
         raise Exception("Must be overridden in the derived class")
    
    def _calculateShotPosition(self) -> Tuple[int, int]:
        x = self._x + self._size/2
        y = self._y - self._size
        return (x, y)
    
   

    class Shot():

        _timer = None
        _color = None

        def __init__(self, screen: pygame.Surface, backgroundColor: pygame.Color, color: pygame.Color):
            self._screen = screen
            self._backgroundColor = backgroundColor
            self._color = color
        
        
        
        def draw(self, x: int, y: int):
            self._x = x
            self._y = y
            
           
            self._drawShot()
            self._timer = threading.Timer(0.1, _onTimerElapsed, [self])
            self._timer.start()

            
        def _drawShot(self):
            rect = self._calculateShotCoordinates()
            pygame.draw.rect(self._screen, self._color, rect)
            pygame.display.flip()


        def _calculateShotCoordinates(self) -> Tuple[int, int, int, int]:
            w = 5
            h = 20
            x = self._x - w/2
            y = self._y
            return (x, y, w, h)

        def _onTimerElapsed(self):
            self._timer.cancel()
            self._drawShot()
            

        def _drawShotBy(self, dx: int, dy: int):
            if self._sx != None and self._sy != None:
                pygame.draw.rect(self._screen, self._backgroundColor, (self._sx, self._sy, 5, 20))
            self._sx += dx
            self._sy += dy
            pygame.draw.rect(self._screen, self._shotColor, (self._sx, self._sy, 5, 20))
            pygame.display.flip()


class Spaceship(SpaceshipBase):
    SIZE = 90
    COLOR = (51, 3, 231)
    SHOT_COLOR = (255, 248, 14)

    def __init__(self, screen: pygame.Surface, backgroundColor: pygame.Color):
        super().__init__(screen, backgroundColor, self.SIZE, self.COLOR, self.SHOT_COLOR)

    def _calculateCoordinates(self, x: int, y: int, size: int) -> List[Tuple[int, int]]:
        a = (x,y)
        b = (x+size, y)
        c = (x+size/2, y-math.sqrt(2)/2*size)
        return [a, b, c]

class Invader(SpaceshipBase):
    SIZE = 70
    COLOR = (99, 26, 143)
    SHOT_COLOR = (255, 248, 14)

    def __init__(self, screen: pygame.Surface, backgroundColor: pygame.Color):
        super().__init__(screen, backgroundColor, self.SIZE, self.COLOR, self.SHOT_COLOR)

    def _calculateCoordinates(self, x: int, y: int, size: int) -> List[Tuple[int, int]]:
        a = (x,y)
        b = (x+size, y)
        c = (x+size/2, y+math.sqrt(2)/2*size)
        return [a, b, c]
                  
    


pygame.init()
game = SpaceInvaders()

pygame.quit()