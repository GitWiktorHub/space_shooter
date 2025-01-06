import pygame
from pygame.locals import *
from mycode.bullets import *
from mycode.cannons import *
from mycode.enemies import *
from mycode.levels import *
from mycode.other import *
from mycode.player import *
from mycode.ships import *
from mycode.UI import *
from tests.test11_line import width, height


class Game(object):
    """
    The main class in the program.
    It is used to connect things into one game.
    """

    def __init__(self,
        player: Player,
        mouse: Mouse,
        menuHandler: MenuHandler,
                 levelManager: LevelManager,
                 screen: pygame.Surface,
                 max_tps: float = 100.0,
                 caption: str = "Planet defender"
                 ):
        self.tps_max = max_tps

        #initialization
        pygame.init()
        self.screen: pygame.Surface = screen
        self.tps_clock = pygame.time.Clock()
        self.dt = 0.0
        pygame.display.set_caption(caption)

        #running
        self.isrun = True

        #loading objects
        self.player = player
        self.mouse = mouse

        self.levelManager = levelManager
        
        self.menuHandler = menuHandler
        
        while self.isrun:
            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isrun = False
            
            # Update time
            self.dt = self.tps_clock.get_time() / 1000
            self.tps_clock.tick(self.tps_max)
            
            # Draw the background
            self.screen.fill((0, 0, 0))
            
            # Move and draw objects
            self.tick()
            self.draw()
            
            # Do the next tick
            pygame.display.update()
        
        # Exit
        pygame.quit()
        quit()

    def tick(self):
        self.menuHandler.tick()

    def draw(self):
        self.menuHandler.draw()

if __name__ == "__main__":
    width, height = (750, 750)
    screen = pygame.display.set_mode((width, height))
    
    player = Player()
    mouse = Mouse()
    
    menuHandler = MenuHandler(self, MainMenu)

    enemySpawner: EnemySpawner = EnemySpawner(self)
    waveManager: WaveManager = WaveManager(self, "./gameData/levels.json", enemySpawner)
    levelManager: LevelManager = LevelManager(waveManager)
    
    game: Game = Game(player, mouse, menuHandler, levelManager, screen, 100.0)
