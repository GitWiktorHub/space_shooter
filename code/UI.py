from code.ships import *
from code.player import *
import pygame
import os

def write(game, text, x, y, font_size, color=(0, 0, 0), font_style="Arial", is_centered=False,):
    font = pygame.font.SysFont(font_style, font_size)
    rend = font.render(text, True, color)
    if is_centered is True:
        x = (game.width - rend.get_rect().width)/2
        y = (game.height - rend.get_rect().height)/2
    game.screen.blit(rend, (x, y))

def write_on_surface(surface, text, x, y, font_size, color=(0, 0, 0), is_centered=False, font_style='Arial'):
    font = pygame.font.SysFont(font_style, font_size)
    rend = font.render(text, True, color)
    if is_centered is True:
        x = (surface.get_rect().width - rend.get_rect().width) / 2
        y = (surface.get_rect().height - rend.get_rect().height) / 2
    surface.blit(rend, (x, y))

class NoImageButton:
    def __init__(self, game, x, y, width, height, text):
        self.game = game
        self.y = y
        self.x = x
        self.width = width
        self.height = height

        self.surf = pygame.Surface((width, height))
        self.surf.fill((30, 30, 30))
        self.rect = self.surf.get_rect()
        self.rect.topleft = (x - width/2, y - height/2)

        self.text = text

    def check_click(self):
        action = False
        pos = pygame.mouse.get_pos()
        # check if the rect collides with the mouse
        if self.rect.collidepoint(pos):
            self.surf.fill((100, 100, 100))
            write_on_surface(self.surf, self.text, 0, 0, 28, (250, 250, 250), True)

            # check if the mouse is clicked
            if self.game.mouse.click():
                action = True
                # return action
        elif not self.rect.collidepoint(pos):
            self.surf.fill((30, 30, 30))
            write_on_surface(self.surf, self.text, 0, 0, 28, (200, 200, 200), True)
        return action

    def draw(self, surface):
        surface.blit(self.surf, (self.x - self.width / 2, self.y - self.height / 2))
        pygame.draw.rect(surface, (250, 250, 250), self.rect, 1)
        write_on_surface(self.surf, self.text, 0, 0, 28, (200, 200, 200), True)


class LevelButton(NoImageButton):
    def __init__(self, game, x, y, width, height, level_id:int):
        self.level_id = level_id
        self.text = f"Level {str(level_id)}"
        super().__init__(game, x, y, width, height, self.text)
    # def check_click(self):
    #     return super().check_click()
    def draw(self, surface):
        super().draw(surface)

class Button:
    def __init__(self, game, x:int, y:int, image:str, scale:float = 1.0, image2:str=""):
        self.game = game
        self.x = x
        self.y = y

        self.image = pygame.image.load(os.path.join(image)).convert_alpha()

        width = self.image.get_width()
        height = self.image.get_height()

        self.image = pygame.transform.scale(self.image, (int(width * scale), int(height * scale)))

        # create an image2 if the path is not empty
        if not image2 == "":
            self.image2 = pygame.image.load(os.path.join(image2)).convert_alpha()
            self.image2 = pygame.transform.scale(self.image2, (int(width * scale), int(height * scale)))

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.img = self.image

    def check_click(self):
        action = False
        pos = pygame.mouse.get_pos()
        # check if the rect collides with the mouse
        if self.rect.collidepoint(pos):
            self.img = self.image2
            # check if the mouse is clicked
            if self.game.mouse.click():
                action = True
        elif not self.rect.collidepoint(pos):
            self.img = self.image

        return action

    def draw(self, surface):
        surface.blit(self.img, (self.x - self.width/2, self.y - self.height/2))

class MainMenu:
    def __init__(self, game):
        self.game = game
        size = game.screen.get_size()

        self.title_image = pygame.image.load("./images/Game_title.png")
        self.title_image = pygame.transform.scale(self.title_image, (int(self.title_image.get_width() * 2), int(self.title_image.get_height() * 2)))

        self.button_play = Button(game, size[0]/2, size[1]/2, "./images/button_play.png", 1.0, "./images/button_play_hover.png")
        self.buttons = [self.button_play]
        self.background = pygame.image.load("./images/background.png").convert_alpha()

    def tick_menu(self):
        for button in self.buttons:
            if button.check_click():
                self.game.showing = "gamemenu"

    def draw_menu(self):
        self.game.screen.blit(self.background, (0, 0))
        self.game.screen.blit(self.title_image, (self.game.width/2 - self.title_image.get_width()/2, 150 - self.title_image.get_height()/2))
        for button in self.buttons:
            button.draw(self.game.screen)

class GameMenu:
    def __init__(self, game):
        self.game = game
        size = game.screen.get_size()
        self.button_endless = Button(game, size[0]/5, size[1]/5, "./images/button_endless.png", 1.0, "./images/button_endless_hover.png")
        self.button_levels = Button(game, size[0]/2, size[1]/5, "./images/button_levels.png", 1.0, "./images/button_levels_hover.png")
        self.button_two_players = Button(game, size[0]*4/5, size[1]/5, "./images/button_two_players.png", 1.0, "./images/button_two_players_hover.png")
        self.button_ship = Button(game, size[0]/4, self.game.height-50, "./images/button_ship.png", 1.0, "./images/button_ship_hover.png")
        self.button_hangar = Button(game, size[0]/2, self.game.height-50, "./images/button_hangar.png", 1.0, "./images/button_hangar_hover.png")
        self.button_shop = Button(game, size[0]*3/4, self.game.height-50, "./images/button_shop.png", 1.0, "./images/button_shop_hover.png")
        self.buttons = [self.button_endless,
                        self.button_levels,
                        self.button_two_players,
                        self.button_ship,
                        self.button_hangar,
                        self.button_shop
                        ]
        self.background = pygame.image.load("./images/background.png").convert_alpha()
        self.ship = self.game.player.current_ship
        self.ship.pos = Vector2(self.game.width/2, self.game.height/2)
        self.ship.vel = Vector2(0, 0)
        self.ship.acc = Vector2(0, 0)
        self.ship.bullets.clear()
        self.ship.hp.maximise_hp()
        self.game.other_bullets.clear()

        # coin
        self.coin = pygame.image.load("./images/coin.png").convert_alpha()
        width = self.coin.get_width()
        height = self.coin.get_height()
        self.coin = pygame.transform.scale(self.coin, (int(width * 5), int(height * 5)))


    def tick_menu(self):
        if self.button_levels.check_click():
            self.game.showing = "levelsmenu"

    def draw_menu(self):
        self.game.screen.blit(self.background, (0, 0))
        for button in self.buttons:
            button.draw(self.game.screen)
        self.ship.draw()
        self.game.screen.blit(self.coin, (450, 300))
        write(self.game, str(self.game.player.coins), 500, 300, 36, (200, 200, 200))

        write(self.game, f"Health points: {str(self.game.player.current_ship.hp.max_hp)}", 50, 300, 28, (200, 200, 200))
        write(self.game, f"Shot force: {str(self.game.player.current_ship.shot_force)}", 50, 350, 28, (200, 200, 200))
        write(self.game, f"Moving force: {str(self.game.player.current_ship.mov_force)}", 50, 400, 28, (200, 200, 200))
        write(self.game, f"Mass: {str(self.game.player.current_ship.mass)}", 50, 450, 28, (200, 200, 200))

class LevelsMenu:
    def __init__(self, game):
        self.game = game
        self.buttons = []
        for i, level in enumerate(self.game.levels):
            if (i+1) % 3 == 1:
                self.buttons.append(LevelButton(self.game, self.game.width/5, self._calculate_level_y(i+1), 200, 100, i+1))
            elif (i+1) % 3 == 2:
                self.buttons.append(LevelButton(self.game, self.game.width/2, self._calculate_level_y(i+1), 200, 100, i+1))
            elif (i+1) % 3 == 0:
                self.buttons.append(LevelButton(self.game, self.game.width*4/5, self._calculate_level_y(i+1), 200, 100, i+1))

    def tick_menu(self):
        for i, button in enumerate(self.buttons):
            # tu nie może być printa sprawdzającego check_click()
            if button.check_click():
                self.game.level_pointer = i
                self.game.showing = "game"

    def _calculate_level_y(self, level_id):
        a = level_id % 3
        if a == 0: a = 3
        b = level_id - a
        y = 100 + b * 50
        return y

    def draw_menu(self):
        for button in self.buttons:
            button.draw(self.game.screen)
        #     if button.level_id % 3 == 1:
        #         button.draw(self.game.screen, self.game.width/5, self._calculate_level_y(button.level_id))
        #     if button.level_id % 3 == 2:
        #         button.draw(self.game.screen, self.game.width/2, self._calculate_level_y(button.level_id))
        #     if button.level_id % 3 == 0:
        #         button.draw(self.game.screen, self.game.width*4/5, self._calculate_level_y(button.level_id))

class ResumeMenu:
    def __init__(self, game):
        self.game = game
        self.buttons = []

    def tick_menu(self):
        pass
    def draw_menu(self):
        pass

class SettingsMenu:
    def __init__(self, game):
        self.game = game
        self.buttons = []

    def tick_menu(self):
        pass
    def draw_menu(self):
        pass