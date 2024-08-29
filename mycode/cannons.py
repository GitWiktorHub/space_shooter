import pygame
import math
from mycode.bullets import *
# from mycode.other import AmmoBar
import random

class Clip:
    def __init__(self, game, max_ammo: int, reload_time: float, active_reload: bool = False):
        self.game = game
        self.max_ammo = max_ammo
        self.current_ammo = max_ammo
        self.reload_time = reload_time
        self.active = active_reload
        self.reloading = False

        self.clock = 0

        # self.ammo_bar = AmmoBar(game, self.max_ammo, bar_width, bar_height, bar_x, bar_y)

    def maximise_ammo(self):
        self.current_ammo = self.max_ammo
        # self.ammo_bar.fill()

    def shot(self):
        self.current_ammo -= 1
        # self.ammo_bar.decrease_by(1)

    def can_i_shoot(self):
        if self.current_ammo > 0:
            return True
        # If ammo is equal or below 0, then undeniably returns False
        return False

    def tick(self):
        # self.ammo_bar.tick()
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
                self.current_ammo += 100
                self.clock = 0
                # self.ammo_bar.increase_by(1)
        # self.ammo_bar.draw()


class Weapon:
    def __init__(self, game, slot, key):
        self.game = game
        self.slot = slot
        self.clock = 0

        if type(key) == int:
            # if passed pygame.key value
            self.is_player = True
            self.key: int = key
        else:
            # if passed other bool type variable
            self.is_player = False
            self.key: bool = key

    def tick(self):
        self.clock += self.game.dt


class Gun(Weapon):
    def __init__(self, game, slot, key, bullet, force, interval, max_ammo: int, reload_time: float,
                 active_reload: bool):
        super().__init__(game, slot, key)
        self.interval = interval
        self.bul = bullet
        self.bullets = []
        self.clip = Clip(game, max_ammo, reload_time, active_reload)

        if self.is_player:
            self.force = force
        else:
            self.force = -force

    def shot(self):
        bullet = self.bul(self.game, self, self.slot.pos.x, self.slot.pos.y, self.force)
        if not self.is_player: bullet.image = pygame.transform.flip(bullet.image, False, True)
        self.bullets.append(bullet)
        bullet.sound.play(0, 800)
        self.clip.shot()

    def _shootCheck(self, condition):
        if condition and self.clock > self.interval:
            if self.clip.can_i_shoot():
                self.clock = 0
                self.shot()

    def tick(self):
        super().tick()
        self.clip.tick()
        pressed = pygame.key.get_pressed()

        if self.is_player:
            self._shootCheck((pressed[pygame.K_KP_0] or pressed[self.key]))
        else:
            self.key = self.slot.ship.is_shooting
            self._shootCheck(self.key)

        for bullet in self.bullets:
            bullet.tick()

    def draw(self):
        for bullet in self.bullets:
            bullet.draw()


class KineticLight(Gun):
    def __init__(self, game, slot, key=pygame.K_KP_0):
        super().__init__(
            game, slot, key,
            bullet=BulletSmallBlue,
            force=3500,
            interval=0.1,
            max_ammo=50,
            reload_time=3.0,
            active_reload=False
        )
class KineticMedium(Gun):
    def __init__(self, game, slot, key=pygame.K_KP_0):
        super().__init__(
            game, slot, key,
            bullet=BulletMediumBlue,
            force=3500,
            interval=0.15,
            max_ammo=50,
            reload_time=2.0,
            active_reload=False
        )


class ShotGun(Weapon):
    def __init__(self, game, slot, key, bullet, spread, intensity, force, interval, max_ammo: int, reload_time: float,
                 active_reload: bool):
        super().__init__(game, slot, key)
        self.bullets = []
        self.bul = bullet
        self.spread = [-spread / 2, spread / 2]
        self.bullets_at_once = intensity
        self.interval = interval
        self.clip = Clip(game, max_ammo, reload_time, active_reload)

        if self.is_player:
            self.force = force
        else:
            self.force = -force

    def shot(self):
        for _ in range(self.bullets_at_once):
            bullet = self.bul(self.game, self.slot.weapon, self.slot.pos.x, self.slot.pos.y, self.force,
                              random.uniform(self.spread[0], self.spread[1]))
            self.bullets.append(bullet)
            bullet.sound.play(0, 800)
            self.clip.shot()

    def _shootCheck(self, condition):
        if condition and self.clock > self.interval:
            if self.clip.can_i_shoot():
                self.clock = 0
                self.shot()

    def tick(self):
        super().tick()
        self.clip.tick()
        pressed = pygame.key.get_pressed()

        if self.is_player:
            self._shootCheck((pressed[pygame.K_KP_0] or pressed[self.key]))
        else:
            self.key = self.slot.ship.is_shooting
            self._shootCheck(self.key)

        for bullet in self.bullets:
            bullet.tick()

    def draw(self):
        for bullet in self.bullets:
            bullet.draw()

class ShotGun1(ShotGun):
    def __init__(self, game, slot, key=pygame.K_KP_0):
        super().__init__(
            game, slot, key,
            bullet=ShotgunBulletFire,
            force=5000,
            interval=0.2,
            spread=10,
            intensity=10,
            max_ammo=1000,
            reload_time=0.01,
            active_reload=True
        )


class Flamethrower(Weapon):
    def __init__(self, game, slot, key, particle, spread, intensity, force, interval, max_ammo: int,
                 reload_time: float, active_reload: bool):
        super().__init__(game, slot, key)
        self.particles = []
        self.particle = particle
        self.spread = [-spread / 2, spread / 2]
        self.intensity = intensity
        self.interval = interval
        self.clip = Clip(game, max_ammo, reload_time, active_reload)

        if self.is_player:
            self.force = force
        else:
            self.force = -force

    def shot(self):
        for _ in range(self.intensity):
            par = self.particle(self.game, self.slot.weapon, self.slot.pos.x, self.slot.pos.y, 2, 1, self.force,
                                random.uniform(self.spread[0], self.spread[1]))
            self.particles.append(par)
            self.clip.shot()

    def _shootCheck(self, condition):
        if condition and self.clock > self.interval:
            if self.clip.can_i_shoot():
                self.clock = 0
                self.shot()

    def tick(self):
        super().tick()
        self.clip.tick()
        pressed = pygame.key.get_pressed()

        if self.is_player:
            self._shootCheck((pressed[pygame.K_KP_0] or pressed[self.key]))
        else:
            self.key = self.slot.ship.is_shooting
            self._shootCheck(self.key)

        for particle in self.particles:
            particle.tick()

    def draw(self):
        for particle in self.particles:
            particle.draw()


class Flamethrower1(Flamethrower):
    def __init__(self, game, slot, key=pygame.K_KP_0):
        super().__init__(
            game, slot, key,
            particle=Particle,
            force=100,
            interval=0.05,
            spread=5,
            intensity=1,
            max_ammo=100,
            reload_time=2.0,
            active_reload=False
        )


class Laser(Gun):
    def __init__(self, game, ship, translation, force, interval, laser, clip_size, reload,
                 active_reload: bool = False, key: int = pygame.K_KP_0):
        super().__init__(game, ship, translation, force, interval, key, clip_size, reload, active_reload)
        self.laser = laser

    def shot(self):
        if len(self.bullets) < 1:
            laser = self.laser(self.game, self, self.pos.x, self.pos.y)
            self.bullets.append(laser)
            self.clip.shot()


class Laser1(Laser):
    def __init__(self, game, ship, translation, key=pygame.K_KP_0):
        super().__init__(
            game, ship,
            translation=translation,
            force=0,
            interval=0.01,
            laser=LaserL,
            clip_size=100,
            reload=0.5
        )
