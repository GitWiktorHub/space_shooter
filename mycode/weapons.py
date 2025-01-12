import pygame
import math
from mycode.bullets import *
from typing import Callable
from abc import ABC, abstractmethod
import random
from clips import *

class Weapon:
    def __init__(self, trigger: Callable):
        self.trigger = trigger
        self.clock = 0
    
    def tick(self, dt: float, x: float, y: float):
        self.clock += dt
    
    def draw(self, screen: pygame.Surface):
        pass


class Gun(Weapon):
    def __init__(
        self, trigger: Callable, bullet_name: str, force: int, interval: float, clip: Clip, spread: int = 0,
        intensity: int = 1, is_player: bool = True
    ):
        super().__init__(trigger)
        self.interval: float = interval
        self.bullet_name: str = bullet_name
        self.bullets: list[Bullet] = []
        self.clip: Clip = clip
        self.spread: tuple[float, float] = (-spread / 2, spread / 2)
        self.force: int = force
        self.is_player: bool = is_player
        self.intensity: int = intensity
    
    @staticmethod
    def _create_bullet(bullet_name: str, x: float, y: float, initial_force: int, rotation: float) -> Bullet:
        builder = BulletBuilder()
        director = BulletBuilderDirector(builder, bullet_name)
        bullet: Bullet = director.build(x, y, initial_force, rotation)
        return bullet
    
    def shot(self, x: float, y: float):
        if self._shootCheck():
            for _ in range(self.intensity):
                bullet = self._create_bullet(
                    self.bullet_name, x, y, self.force,
                    random.uniform(self.spread[0], self.spread[1]) if self.spread[1] > 0 else 0
                )
                self.bullets.append(bullet)
                bullet.sound.play(0, 800)
                self.clip.shot()
    
    def _shootCheck(self) -> bool:
        if self.trigger() and self.clock > self.interval and self.clip.can_i_shoot():
            self.clock = 0
            return True
        return False
    
    def tick(self, dt: float, x: float, y: float):
        super().tick(dt)
        self.clip.tick(dt)
        
        self.shot(x, y)

        for bullet in self.bullets:
            bullet.tick(dt)
    
    def draw(self, screen):
        for bullet in self.bullets:
            bullet.draw(screen)


class GunBuilder:
    def __init__(self):
        self.gun: Gun | None = None
        self.trigger: Callable | None = None
        self.bullet_name: str | None = None
        self.force: int | None = None
        self.interval: float | None = None
        self.spread: int = 0
        self.clip: Clip | None = None
        self.intensity: int = 1
        self.is_player: bool = True
    
    def set_trigger(self, trigger: Callable):
        self.trigger = trigger
        return self
    
    def set_bullet_name(self, bullet_name: str):
        self.bullet_name = bullet_name
        return self
    
    def set_force(self, force: int):
        self.force = force
        return self
    
    def set_interval(self, interval: float):
        self.interval = interval
        return self
    
    def set_spread(self, spread: int):
        self.spread = spread
        return self
    
    def set_clip(self, max_ammo: int, reload_time: float, active_reload: bool = False):
        self.clip = Clip(max_ammo, reload_time, active_reload)
        return self
    
    def set_intensity(self, intensity: int):
        self.intensity = intensity
        return self
    
    def set_is_player(self, is_player: bool):
        self.is_player = is_player
        return self
    
    def build_gun(self) -> Gun:
        self.gun = Gun(
            self.trigger, self.bullet_name, self.force, self.interval, self.clip, self.spread, self.intensity,
            self.is_player
        )
        return self.gun


class GunBuilderDirector:
    def __init__(self, builder: GunBuilder, gun_name: str | None = None):
        self.gun_name: str | None = gun_name
        self.builder: GunBuilder = builder
        
        self.gun_data: dir = { }
        self.clip_data: dir = { }
        
        self.__reload_file()
    
    def __reload_file(self):
        with open('./gameData/guns.json', 'r') as f:
            self.config: dir = json.load(f)
            guns = self.config["guns"]
            self.gun_data = list(filter(lambda gun: gun['name'] == self.gun_name, guns))[0]
            self.clip_data = self.gun_data['clip']
    
    def choose_gun(self, gun_name: str):
        self.gun_name = gun_name
        self.__reload_file()
    
    def build(self, trigger: Callable, is_player: bool) -> Gun:
        g = (
            self.builder
            .set_trigger(trigger)
            .set_clip(self.clip_data['max_ammo'], self.clip_data['reload_time'], self.clip_data['active_reload'])
            .set_force(self.gun_data['force'])
            .set_interval(self.gun_data['interval'])
            .set_bullet_name(self.gun_data['bullet_name'])
            .set_is_player(is_player)
        )
        if "spread" in self.gun_data and "intensity" in self.gun_data:
            return g.set_spread(self.gun_data['spread']).set_intensity(self.gun_data['intensity']).build_gun()
        else:
            return g.build_gun()


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
            par = self.particle(self.game, self.slot.weapon, 2, 1, self.force,
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


class Laser(Weapon):
    def __init__(self, game, slot, key, laserType, shooting_time, reload_time):
        super().__init__(game, slot, key)
        self.laser = laserType(game, self, self.slot.pos.x, self.slot.pos.y)
        self.clip = LaserClip(game, shooting_time, reload_time)
        self.active = False

    def shot(self):
        self.active = True

    def _shootCheck(self, condition):
        if condition and self.clip.can_i_shoot():
            self.shot()
        elif not self.clip.can_i_shoot() or not condition:
            self.active = False

    def tick(self):
        super().tick()
        self.clip.tick()
        self.laser.tick()
        pressed = pygame.key.get_pressed()

        if self.is_player:
            self._shootCheck((pressed[pygame.K_KP_0] or pressed[self.key]))
        else:
            self.key = self.slot.ship.is_shooting
            self._shootCheck(self.key)

    def draw(self):
        self.laser.draw()


class Laser1(Laser):
    def __init__(self, game, slot, key=pygame.K_KP_0):
        super().__init__(
            game, slot, key,
            laserType=LaserL,
            shooting_time=10.0,
            reload_time=5.0
        )
