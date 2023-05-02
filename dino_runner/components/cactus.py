from random import randrange, randint
from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, SCREEN_WIDTH

SMALL_Y = 330
LARGE_Y = 310

class Cactus:
    def __init__(self):
        self.image = SMALL_CACTUS[0]
        self.cactusRect = self.image.get_rect()
        self.cactusRect.x = SCREEN_WIDTH
        self.cactusRect.y = SMALL_Y
        pass
    
    def update(self, player, gameSpeed):
        collision = self.cactusRect.colliderect(player)
        if self.cactusRect.bottomleft[0] < 0:
            self.cactusRect.x = SCREEN_WIDTH + randint(1, SCREEN_WIDTH)
            self.cactusRect.y = randrange(50, 200, 50)
            pass            
        self.cactusRect.x -= gameSpeed
        return collision

    def draw(self, screen, imageIndex = 0, type = 'small'):
        if type == 'small':
            self.image = SMALL_CACTUS[imageIndex]
            self.cactusRect.y = SMALL_Y
        else:
            self.image = LARGE_CACTUS[imageIndex]
            self.cactusRect.y = LARGE_Y
        screen.blit(self.image, (self.cactusRect.x, self.cactusRect.y))