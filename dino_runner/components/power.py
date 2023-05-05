from random import randrange
from dino_runner.utils.constants import SHIELD, HAMMER, HEART, SCREEN_WIDTH, SCREEN_HEIGHT

class Power:
    def __init__(self, type):
        if type == 'hammer':
            self.image = HAMMER
        elif type == 'shield':
            self.image = SHIELD
        else:
            self.image = HEART
        self.powerRect = self.image.get_rect()
        self.downPosition = SCREEN_WIDTH//randrange(1, 10, 1) - self.image.get_width()
        self.duration = 500

    def update(self, player, gameSpeed, powerType):
        collision = self.powerRect.colliderect(player.dino_rect)
        if player.hasPowerUp:
            self.duration -= 1
            if self.duration <= 0:
                self.downPosition = SCREEN_WIDTH//randrange(1, 10, 1) - self.image.get_width()
                player.hasPowerUp = False
                self.duration = 500
        
        if not collision:
            self.adjustPowerPosition(self.downPosition, self.powerRect.y + gameSpeed//4)
            if self.powerRect.topright[1] >= SCREEN_HEIGHT:
                self.downPosition = SCREEN_WIDTH//randrange(1, 10, 1) - self.image.get_width()
                self.adjustPowerPosition(self.downPosition, 0)
        else:
            self.adjustPowerPosition(self.downPosition, 0)
            if not powerType == 'heart':
                player.hasPowerUp = True
                player.powerType = powerType
            else:
                player.hp += 1000

    def draw(self, screen):
        screen.blit(self.image, (self.powerRect.x, self.powerRect.y))
        
    def adjustPowerPosition(self, x, y):
        self.powerRect.x = x
        self.powerRect.y = y
