import pygame
from pygame import mixer
from pygame.math import Vector2
import os
mixer.init()
class Bullet(object):
    def __init__(self, game, x, y, width, height, force, mass, color=(255, 255, 255), sound=None):
        self.pos = Vector2(x, y)
        self.vel = Vector2(0, 0)

        self.mass = mass
        acc = int(force / mass)
        self.acc = Vector2(0, -acc)

        self.width = width
        self.height = height
        # self.hitbox = pygame.Rect(self.pos.x - width / 2, self.pos.y - height / 2, width, height)

        self.mask = pygame.mask.from_surface(self.hitbox)

        self.game = game
        self.color = color

        if sound is not None:
            self.sound = mixer.Sound(sound)
            self.sound.set_volume(0.1)
    def tick(self):
        # Physics
        self.vel *= 0.999

        self.vel += self.acc
        self.pos += self.vel * self.game.dt
        self.acc *= 0
    def draw(self):
        self.hitbox = pygame.Rect(self.pos.x - self.width / 2, self.pos.y - self.height / 2, self.width, self.height)
        pygame.draw.rect(self.game.screen, self.color, self.hitbox)

class Kinetic60Bullet(Bullet):
    def __init__(self, game, x, y, force):
        self.width = 2
        self.height = 2
        self.force = force
        self.mass = 40
        self.color = (200, 210, 55)
        self.sound = "./shot_sounds/M60-single.wav"
        super().__init__(game, x, y, self.width, self.height, self.force, self.mass, self.color, self.sound)
    def tick(self):
        super().tick()
    def draw(self):
        super().draw()

class Kinetic9Bullet(Bullet):
    def __init__(self, game, x, y, force):
        self.width = 3
        self.height = 6
        self.force = force
        self.mass = 65
        self.color = (90, 90, 100)
        self.sound = "./shot_sounds/gunshot.wav"
        super().__init__(game, x, y, self.width, self.height, self.force, self.mass, self.color, self.sound)
    def tick(self):
        super().tick()
    def draw(self):
        super().draw()

class KineticBullet(Bullet):
    def __init__(self, game, x, y, force):
        self.width = 2
        self.height = 4
        self.force = force
        self.mass = 50
        self.color = (130, 130, 120)
        self.sound = "./shot_sounds/kinetic-gun.mp3"
        super().__init__(game, x, y, self.width, self.height, self.force, self.mass, self.color, self.sound)
    def tick(self):
        super().tick()
    def draw(self):
        super().draw()


class BlasterBullet(Bullet):
    def __init__(self, game, x, y, force):
        self.width = 4
        self.height = 10
        self.force = force
        self.mass = 100
        self.color = (175, 210, 190)
        self.sound = "./shot_sounds/blaster.mp3"
        super().__init__(game, x, y, self.width, self.height, self.force, self.mass, self.color, self.sound)
    def tick(self):
        super().tick()
    def draw(self):
        super().draw()

class EnergyGunBullet(Bullet):
    def __init__(self, game, x, y, force):
        self.width = 5
        self.height = 15
        self.force = force
        self.mass = 120
        self.color = (200, 180, 180)
        self.sound = "./shot_sounds/energy-gun.mp3"
        super().__init__(game, x, y, self.width, self.height, self.force, self.mass, self.color, self.sound)
    def tick(self):
        super().tick()
    def draw(self):
        super().draw()


class LaserCannonBullet(Bullet):
    def __init__(self, game, x, y, force):
        self.width = 8
        self.height = 50
        self.force = force
        self.mass = 300
        self.color = (140, 220, 220)
        self.sound = "./shot_sounds/laser-cannon.wav"
        super().__init__(game, x, y, self.width, self.height, self.force, self.mass, self.color, self.sound)
    def tick(self):
        super().tick()
    def draw(self):
        super().draw()

class LaserLightCannonBullet(Bullet):
    def __init__(self, game, x, y, force):
        self.width = 6
        self.height = 40
        self.force = force
        self.mass = 250
        self.color = (120, 230, 210)
        self.sound = "./shot_sounds/laser-cannon-light.mp3"
        super().__init__(game, x, y, self.width, self.height, self.force, self.mass, self.color, self.sound)
    def tick(self):
        super().tick()
    def draw(self):
        super().draw()


class LaserLightGunBullet(Bullet):
    def __init__(self, game, x, y, force):
        self.width = 3
        self.height = 8
        self.force = force
        self.mass = 30
        self.color = (150, 210, 150)
        self.sound = "./shot_sounds/laser-light-gun.wav"
        super().__init__(game, x, y, self.width, self.height, self.force, self.mass, self.color, self.sound)
    def tick(self):
        super().tick()
    def draw(self):
        super().draw()

class LaserMediumGunBullet(Bullet):
    def __init__(self, game, x, y, force):
        self.width = 4
        self.height = 10
        self.force = force
        self.mass = 60
        self.color = (150, 210, 150)
        self.sound = "./shot_sounds/laser-medium-gun.mp3"
        super().__init__(game, x, y, self.width, self.height, self.force, self.mass, self.color, self.sound)
    def tick(self):
        super().tick()
    def draw(self):
        super().draw()

class LaserHeavyGunBullet(Bullet):
    def __init__(self, game, x, y, force):
        self.width = 4
        self.height = 12
        self.force = force
        self.mass = 100
        self.color = (150, 210, 150)
        self.sound = "./shot_sounds/laser-heavy-gun.wav"
        super().__init__(game, x, y, self.width, self.height, self.force, self.mass, self.color, self.sound)
    def tick(self):
        super().tick()
    def draw(self):
        super().draw()

class LaserLongGunBullet(Bullet):
    def __init__(self, game, x, y, force):
        self.width = 4
        self.height = 40
        self.force = force
        self.mass = 90
        self.color = (150, 210, 150)
        self.sound = "./shot_sounds/laser-long-gun.mp3"
        super().__init__(game, x, y, self.width, self.height, self.force, self.mass, self.color, self.sound)
    def tick(self):
        super().tick()
    def draw(self):
        super().draw()