import pygame
import math
from code.bullets import *
from code.other import AmmoBar

class ClipE:
    def __init__(self, game, max_ammo:int, reload_time:float, active_reload:bool=False):
        self.game = game
        self.max_ammo = max_ammo
        self.current_ammo = max_ammo
        self.reload_time = reload_time
        self.active = active_reload
        self.reloading = False

        self.clock = 0

    def maximise_ammo(self):
        self.current_ammo = self.max_ammo

    def shot(self):
        self.current_ammo -= 1

    def can_i_shoot(self):
        if self.current_ammo > 0:
            return True
        return False

    def tick(self):
        # there is no ammo, passive reloading
        if not self.active:
            # it is not reloading
            if not self.reloading:
                if self.current_ammo <= 0:
                    self.reloading = True
            # it is reloading
            if self.reloading:
                self.clock += self.game.dt
                if self.clock > self.reload_time:
                    self.clock = 0
                    self.reloading = False
                    self.maximise_ammo()
        # active reloading
        else:
            self.clock += self.game.dt
            if self.clock > self.reload_time and self.current_ammo < self.max_ammo:
                self.current_ammo += 1
                self.clock = 0

class GunE:
    def __init__(self, game, ship, translation, force, interval, max_ammo:int, reload_time:float, active_reload:bool,):
        self.game = game
        self.ship = ship
        self.pos = ship.pos
        self.translation = translation
        self.force = force
        self.interval = interval

        self.clock = 0
        self.clip = ClipE(game, max_ammo, reload_time, active_reload)

    def shot(self):
        pass

    def tick(self):
        self.clock += self.game.dt
        self.pos = self.ship.pos + self.translation
        self.clip.tick()

        if self.clock > self.interval:
            if self.clip.can_i_shoot():
                self.clock = 0
                self.shot()