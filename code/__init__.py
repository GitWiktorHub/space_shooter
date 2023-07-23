import pygame
from code.bullets import *
from code.bullets2 import *
from code.cannons import *
from code.enemies import *
from code.levels import *
from code.maneuvering_cannons import *
from code.other import *
from code.player import *
from code.ships import *
from code.two_players import *
from code.UI import *


class MainObject(object):
    def __init__(self):
        pass

    def tick(self):
        pass

    def draw(self):
        pass

class StaticObject(MainObject):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.x = x
        self.y = y

class UnClickable(StaticObject):
    def __init__(self, game, x, y, surf):
        super().__init__(game, x, y)
        self.surf = surf

    def draw(self):
        self.game.screen.blit(self.surf, (self.x, self.y))

class TextObject(UnClickable):
    def __init__(self, game, x, y, ):
        self.text =
        super().__init__(game, x, y, )