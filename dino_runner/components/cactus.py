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
        self.cactusRect.width = self.image.get_width()
        self.cactusRect.height = self.image.get_height()
        pass
    
    def update(self, player, gameSpeed):
        collision = self.cactusRect.colliderect(player.dino_rect)
        if collision:
            self.cactusRect.normalize()
            if player.hasPowerUp:
                self.cactusRect.x = SCREEN_WIDTH + (self.image.get_width() * 2)
                self.cactusRect.y = randrange(50, 200, 50)
                return False
        if self.cactusRect.bottomleft[0] < 0:
            self.cactusRect.x = SCREEN_WIDTH + (self.image.get_width() * 2)
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