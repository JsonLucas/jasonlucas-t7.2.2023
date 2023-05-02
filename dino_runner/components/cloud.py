from random import randrange
from dino_runner.utils.constants import CLOUD, SCREEN_WIDTH

class Cloud:
    def __init__(self):
        self.image = CLOUD
        self.cloudRect = self.image.get_rect()
        self.cloudRect.x = SCREEN_WIDTH - randrange(30, 300, 90)
        self.cloudRect.y = randrange(50, 200, 50)
    
    def update(self, gameSpeed):
        if self.cloudRect.topright[0] < 0:
            self.cloudRect.x = SCREEN_WIDTH
            self.cloudRect.y = randrange(50, 200, 50)
        self.cloudRect.x -= gameSpeed
        pass
    
    def draw(self, screen):
        screen.blit(self.image, (self.cloudRect.x, self.cloudRect.y))