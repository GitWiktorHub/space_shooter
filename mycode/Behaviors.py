import pygame
from pygame.math import *
import random

class Behavior:
    def __init__(self, game, enemy):
        self.orders = []
        self.enemy = enemy
        self.game = game
        self.process_time = 0.5
        self.clock = 0

    def tick(self):
        self.clock += self.game.dt
        # self.enemy.tick()
        if self.clock > self.process_time:
            self.clock = 0
            if self.enemy.hp.hp / self.enemy.hp.max_hp > 1 / 2 and not self.enemy.guns[0].clip.reloading:
                self.enemy.is_shooting = True
                self.enemy.destination_x = self.game.player.current_ship.pos.x
                self.enemy.destination_y = 100
            else:
                self.enemy.is_shooting = False
                if abs(self.game.player.current_ship.pos.x - self.enemy.pos.x) < 30:
                    if self.enemy.pos.x > 350:
                        angle = random.randint(1, 180)
                    else:
                        angle = random.randint(181, 359)
                    if angle > 180:
                        angle = -angle
                    if angle < -180:
                        angle = -angle
                    self.enemy.add_force(Vector2(0, self.enemy.force))
                    self.enemy.acc.rotate_ip(angle)
