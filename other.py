import pygame

class HP:
    def __init__(self, game, amount, width, height, x, y, color=(250, 250, 250)):
        self.game = game
        self.amount = amount

        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.color = color
        self.bgcolor = (255, 0, 0)#(color[0] - 100, color[1] - 100, color[2] - 100)

        self.back = pygame.Rect(self.x - self.width/2, self.y - self.height/2, self.width, self.height)

        self.unit = self.width / self.amount

        self.block = pygame.Rect(self.x - self.width/2, self.y - self.height/2, self.unit * self.amount, self.height)

    def decrease_by(self, amount):
        self.amount -= amount
        self.tick()
        self.draw()

    def tick(self):
        self.block = pygame.Rect(self.x - self.width/2, self.y - self.height/2, self.unit * self.amount, self.height)

    def draw(self):
        # self.game.screen.blit(self.surf, (self.x - self.width/2, self.y - self.height/2))
        pygame.draw.rect(self.game.screen, self.bgcolor, self.back)
        pygame.draw.rect(self.game.screen, self.color, self.block)

class DeluxeHP:
    def __init__(self):
        self.current_hp = 200
        self.hp = 500
        self.max_hp = 1000
        self.bar_length = 400
        self.health_ratio = self.max_hp / self.bar_length
        self.change_speed = 5

    def get_damage(self, amount):
        if self.hp > 0:
            self.hp -= amount
        if self.hp < 0:
            self.hp = 0

    def get_health(self, amount):
        if self.hp < self.max_hp:
            self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def tick(self):
        transition_width = 0
        transition_color = (255, 0, 0)

        if self.current_hp < self.hp:
            self.current_hp += self.change_speed
            transition_width = int((self.hp - self.current_hp) / self.health_ratio)
            transition_color = (0, 255, 0)

            health_bar_width = int(self.current_hp / self.health_ratio)
            health_bar = pygame.Rect(10, 45, health_bar_width, 25)
            transition_bar = pygame.Rect(health_bar.right, 45, transition_width, 25)

            pygame.draw.rect(screen, (255, 0, 0), health_bar)
            pygame.draw.rect(screen, transition_color, transition_bar)
            pygame.draw.rect(screen, (255, 255, 255), (10, 45, self.bar_length, 25), 2)


        elif self.current_hp > self.hp:
            self.current_hp -= self.change_speed
            transition_width = int((self.current_hp - self.hp) / self.health_ratio)
            transition_color = (255, 255, 0)

            health_bar_width = int(self.hp / self.health_ratio)
            health_bar = pygame.Rect(10, 45, health_bar_width, 25)
            transition_bar = pygame.Rect(health_bar.right, 45, transition_width, 25)

            pygame.draw.rect(screen, (255, 0, 0), health_bar)
            pygame.draw.rect(screen, transition_color, transition_bar)
            pygame.draw.rect(screen, (255, 255, 255), (10, 45, self.bar_length, 25), 2)


        else:
            health_bar_width = int(self.current_hp / self.health_ratio)
            health_bar = pygame.Rect(10, 45, health_bar_width, 25)
            transition_bar = pygame.Rect(health_bar.right, 45, transition_width, 25)

            pygame.draw.rect(screen, (255, 0, 0), health_bar)
            pygame.draw.rect(screen, transition_color, transition_bar)
            pygame.draw.rect(screen, (255, 255, 255), (10, 45, self.bar_length, 25), 2)
