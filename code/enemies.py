import pygame.time
import pygame.math
import code
from code import *
from code.other import *
from code.bullets import *
import os

class BaseEnemy(ShootingDownNoMove):
    def __init__(self, game,  x, y, path, force, hp_amount, hp_width=50, hp_height=5):
        super().__init__(game, x, y, path, force, hp_amount, hp_width, hp_height)

    def add_bullet(self, bullet):
        self.bullets.append(bullet)
        bullet.sound.play(0, 800)
        # acc = -bullet.acc  # getting initial bullet velocity
        # vel = (bullet.mass * acc) / self.mass
        # # getting initial velocity from zasada zachowania pędu
        # vel.x *= vel.x
        # vel.y *= vel.y
        # energy = (self.mass * vel) / 2  # calculating kinetic energy
        # force = energy / self.barrel  # calculating kickback force
        # self.add_force(Vector2(force.x, force.y))


class Enemy1(BaseEnemy):
    def __init__(self, game, x, y):
        self.game = game
        self.image = "./enemies/Enemy1.png"
        super().__init__(self.game, self.image, x, y , 0.99, 100, 50, 400, 5, 100000)

    def add_force(self, force):
        super().add_force(force)

    def tick(self):
        super().tick()
        if self.clock >= 2.0:
            self.clock = 0
            bullet = KineticBullet(self.game, self.pos.x, self.pos.y, -self.shotforce)
            self.add_bullet(bullet)

        for bullet in self.bullets:
            if bullet.pos.y >= self.game.height:
                self.bullets.remove(bullet)
            else:
                bullet.tick()

    def draw(self):
        super().draw()
        for bullet in self.bullets:
            bullet.draw()
            if bullet.pos.y >= self.game.height:
                self.bullets.remove(bullet)

    def add_bullet(self, bullet):
        super().add_bullet(bullet)


class Enemy2(BaseEnemy):
    def __init__(self, game, x, y):
        self.game = game
        self.image = "./enemies/Enemy2.png"
        super().__init__(self.game, self.image, x, y , 0.99, 150, 100, 350, 5, 250000)

    def add_force(self, force):
        super().add_force(force)

    def tick(self):
        super().tick()
        if self.clock >= 1.5:
            self.clock = 0
            bullet = Kinetic9Bullet(self.game, self.pos.x, self.pos.y, -self.shotforce)
            self.add_bullet(bullet)

        for bullet in self.bullets:
            if bullet.pos.y >= self.game.height:
                self.bullets.remove(bullet)
            else:
                bullet.tick()

    def draw(self):
        super().draw()
        for bullet in self.bullets:
            bullet.draw()
            if bullet.pos.y >= self.game.height:
                self.bullets.remove(bullet)

    def add_bullet(self, bullet):
        super().add_bullet(bullet)


class Enemy3(BaseEnemy):
    def __init__(self, game, x, y):
        self.game = game
        self.image = "./enemies/Enemy3.png"
        super().__init__(self.game, self.image, x, y , 0.98, 540, 350, 1200, 6, 4500000)

    def add_force(self, force):
        super().add_force(force)

    def tick(self):
        super().tick()
        if self.clock >= 1.0:
            self.clock = 0
            bullet = EnergyGunBullet(self.game, self.pos.x-22, self.pos.y, -self.shotforce)
            bullet1 = EnergyGunBullet(self.game, self.pos.x+22, self.pos.y, -self.shotforce)
            self.add_bullet(bullet)
            self.add_bullet(bullet1)

        for bullet in self.bullets:
            if bullet.pos.y >= self.game.height:
                self.bullets.remove(bullet)
            else:
                bullet.tick()

    def draw(self):
        super().draw()
        for bullet in self.bullets:
            bullet.draw()
            if bullet.pos.y >= self.game.height:
                self.bullets.remove(bullet)

    def add_bullet(self, bullet):
        super().add_bullet(bullet)