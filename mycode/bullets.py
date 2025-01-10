import pygame
from pygame import mixer
from pygame.math import Vector2

from mycode.physics import PygamePhysics
from mycode.displayable import Displayer
from mycode.projectile import Projectile
from mycode.spacecraft import Spacecraft

mixer.init()


class Bullet(Projectile):
    def __init__(
        self, physics: PygamePhysics, damage: int, rotation: float, sound_path: str, image: pygame.Surface,
        scale: float = 1.0
    ):
        super().__init__(physics, damage, rotation)
        
        self.displayer = Displayer(image, scale)
        self.displayer.image = pygame.transform.rotate(image, 90)
        
        if sound_path != "":
            self.sound = mixer.Sound(sound_path)
            self.sound.set_volume(0.1)

        self.line = None

        self.steered_by_menu = False
    
    def check_collision(self, ship: Spacecraft):
        if self.line is not None:
            if (ship.displayer.mask.overlap(
                    self.displayer.mask, (
                            (self.physics.pos.x - self.displayer.width / 2) - ship.displayer.hitbox.x,
                            (self.physics.pos.y - self.displayer.height / 2) - ship.displayer.hitbox.y)
            ) or ship.displayer.hitbox.clipline(self.line)):
                return True
            return False
        elif ship.displayer.mask.overlap(
                self.displayer.mask, (
                        (self.physics.pos.x - self.displayer.width / 2) - ship.displayer.hitbox.x,
                        (self.physics.pos.y - self.displayer.height / 2) - ship.displayer.hitbox.y)
        ):
            return True
        return False
    
    def tick(self, dt):
        # Checking if the target of a bullet is in between of last bullet position and new bullet position
        # making it too far jump per one frame

        # drawing a line
        # if self.vel.y * self.game.dt > self.height or self.vel.x * self.game.dt > self.width:
        new_pos: Vector2 = self.physics.pos + (((self.physics.vel * self.physics.current_slip) + self.physics.acc) * dt)
        self.line = ((self.physics.pos.x, self.physics.pos.y), (new_pos.x, new_pos.y))
        
        # TODO: check collision and position somewhere else
        '''
        
        # if self.physics.pos.y < 0:
        #     del self   <- This does not remove a Bullet from a list,
        #     return
        
        # if self.gun.is_player:
        #     for enemy in self.game.menuHandler.currentMenu.enemies:
        #         if self.check_collision(enemy):
        #             enemy.hp.get_damage(self.damage)
        #             try:
        #                 self.gun.bullets.remove(self)
        #             except ValueError:
        #                 pass
        # else:
        #     if self.check_collision(self.game.player.current_ship):
        #         self.game.player.current_ship.hp.get_damage(self.damage)
        #         try:
        #             if not self.steered_by_menu:
        #                 self.gun.bullets.remove(self)
        #             else:
        #                 self.game.menuHandler.currentMenu.other_bullets.remove(self)
        #         except ValueError:
        #             pass
        '''
        
        self.physics.tick(dt)
        self.displayer.tick(self.physics.pos.x, self.physics.pos.y)
    
    def draw(self, screen: pygame.Surface):
        self.displayer.draw(screen, self.physics.pos.x, self.physics.pos.y)


# Will be replaced by BulletBuilder
# class BulletSmallBlue(ImageBullet):
#     def __init__(self, game, gun, x, y, force, angle=0):
#         super().__init__(
#             game, gun, x, y,
#             path="./images/Laser Sprites/01.png",
#             mass=2,
#             force=force,
#             angle=angle,
#             damage=5,
#             sound="./sounds/shot_sounds/laser-light-gun.wav",
#             scale=0.5
#         )
#
# class ShotgunBulletFire(ImageBullet):
#     def __init__(self, game, gun, x, y, force, angle=0):
#         super().__init__(
#             game, gun, x, y,
#             path="./images/shotgun_bullet.png",
#             mass=1,
#             force=force,
#             angle=angle,
#             damage=1,
#             sound="./sounds/shot_sounds/laser-light-gun.wav",
#             scale=0.1
#         )


