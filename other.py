import pygame

class HP:
    def __init__(self, game, amount, width, height, x, y, color=(250, 250, 250)):
        self.game = game
        self.full = amount
        self.amount = amount

        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.color = color
