from random import randrange
from dino_runner.utils.constants import BIRD, SCREEN_WIDTH


class Bird:
    def __init__(self):
        self.image = BIRD[0]
        self.birdRect = self.image.get_rect()
        self.birdRect.x = SCREEN_WIDTH
        self.birdRect.y = randrange(100, 275, 25)
        self.flyCount = 0
        
    def update(self, player, gameSpeed):
        collision = self.birdRect.colliderect(player)
        if self.flyCount > 9:
            self.flyCount = 0
        self.image = BIRD[self.flyCount//5]
        if self.birdRect.topright[0] < 0:
            self.birdRect.x = SCREEN_WIDTH
            self.birdRect.y = randrange(100, 275, 25)
        self.birdRect.x -= gameSpeed        
        self.flyCount += 1
        return collision
    
    def draw(self, screen):
        screen.blit(self.image, (self.birdRect.x, self.birdRect.y))