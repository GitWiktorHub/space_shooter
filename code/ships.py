import pygame
from pygame import mixer
from pygame.math import Vector2
import os
from code import *
from code.other import *
from code.cannons import *
from code.maneuvering_cannons import *
from code import ShootingUp

mixer.init()


class PlayableShip(ShootingUp):
    def __init__(self, game, path, mass, max_speed, force, hp_amount, hp_width, hp_height, hp_x, hp_y, slip=0.98):
        size = self.game.screen.get_size()
        super().__init__(game, size[0]/2, size[1]/2, path, mass, max_speed, force, hp_amount, hp_width, hp_height, hp_x, hp_y, False, slip)

    def tick(self):
        # Input
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            self.add_force(Vector2(0, -self.force))
        if pressed[pygame.K_s]:
            self.add_force(Vector2(0, self.force))
        if pressed[pygame.K_d]:
            self.add_force(Vector2(self.force, 0))
        if pressed[pygame.K_a]:
            self.add_force(Vector2(-self.force, 0))

        super().tick()

    def draw(self):
        super().draw()

class Ship0(PlayableShip):
    def __init__(self, game):
        self.game = game
        self.path = "./images/ships/ship0.png"
        super().__init__(game, self.path, 40, 150, 200, 500000, 300, 25, 165, 710)
        self.cannon = KineticGun(self.game, self, Vector2(0, -10), self.force, 0.6)

    def tick(self):
        super().tick()
        self.cannon.tick()

class Ship1(PlayableShip):
    def __init__(self, game):
        self.game = game
        self.path = "./images/ships/ship1.png"
        super().__init__(
            game=game,
            path=self.path,
            mass=100,
            max_speed=150,
            force=400,
            hp_amount=1000000,
            hp_height=25, hp_width=300,
            hp_x=165, hp_y=710
        )
        self.cannon = ManeuveringBulletsLauncher(
            game=self.game,
            ship=self,
            translation=Vector2(0, -30),
            force=self.force,
            interval=0.7,
            key=pygame.K_SPACE
        )

    def tick(self):
        super().tick()
        self.cannon.tick()

class Ship2(PlayableShip):
    def __init__(self, game):
        self.game = game
        self.path = "./images/ships/ship2.png"
        super().__init__(
            game, self.path,
            mass=70,
            max_speed=170,
            force=1250,
            hp_amount=900000,
            hp_height=25, hp_width=300,
            hp_x=165, hp_y=710
        )
        self.cannon = Blaster(self.game, self, Vector2(27, -20), self.force, 0.35)
        self.cannon2 = Blaster(self.game, self, Vector2(-27, -20), self.force, 0.35)

    def tick(self):
        super().tick()
        self.cannon.tick()
        self.cannon2.tick()

class Ship3(PlayableShip):
    def __init__(self, game):
        self.game = game
        self.path = "./images/ships/ship3.png"
        super().__init__(
            game, self.path,
            mass=200,
            max_speed=200,
            force=5000,
            hp_amount=2000000,
            hp_height=25, hp_width=300,
            hp_x=165, hp_y=710
        )
        self.cannon = Blaster(self.game, self, Vector2(-23, -30), self.force, 0.4)
        self.cannon2 = Blaster(self.game, self, Vector2(23, -30), self.force, 0.4)

    def tick(self):
        super().tick()
        self.cannon.tick()
        self.cannon2.tick()

class Ship4(PlayableShip):
    def __init__(self, game):
        self.game = game
        self.path = "./images/ships/ship4.png"
        super().__init__(
            game, self.path,
            mass=500,
            max_speed=100,
            force=5000,
            hp_amount=3500000,
            hp_height=25, hp_width=300,
            hp_x=165, hp_y=710
        )
        self.cannon = Blaster(self.game, self, Vector2(-25, -35), self.force, 0.4)
        self.cannon2 = Blaster(self.game, self, Vector2(25, -35), self.force, 0.4)
        self.cannon3 = Blaster(self.game, self, Vector2(-47, -30), self.force, 0.4)
        self.cannon4 = Blaster(self.game, self, Vector2(47, -30), self.force, 0.4)

    def tick(self):
        super().tick()
        self.cannon.tick()
        self.cannon2.tick()
        self.cannon3.tick()
        self.cannon4.tick()

class Ship5(PlayableShip):
    def __init__(self, game):
        self.game = game
        self.path = "./images/ships/ship5.png"
        super().__init__(game, self.path, 0.98, 250, 40, 600)
        self.cannon = ShotGun1(self.game, self, Vector2(0, 0), self.force, 0.5)

    def tick(self):
        super().tick()
        self.cannon.tick()

