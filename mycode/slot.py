import pygame
from pygame.math import Vector2
from typing import Callable
from weapons import Weapon
from spacecraft import Spacecraft

class Slot:
    def __init__(self, translation: Vector2, trigger: Callable, weapon: Weapon):
        """
        Represents a weapon slot of a Ship,
        it can contain only one weapon
        :param translation: pygame.Vector2
        :param trigger: a function returning bool
        :param weapon: any end child class inheriting from Weapon
        """
        self.translation = translation
        self.trigger = trigger
        self.weapon = weapon
    
    def tick(self, dt: float, position: Vector2):
        pos = position + self.translation
        self.weapon.tick(dt, pos.x, pos.y)
    
    def draw(self, screen: pygame.Surface):
        self.weapon.draw(screen)
