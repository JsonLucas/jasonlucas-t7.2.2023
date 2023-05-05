from random import randrange
from dino_runner.utils.constants import BIRD, SCREEN_WIDTH

class Bird:
    def __init__(self):
        self.image = BIRD[0]
        self.birdRect = self.image.get_rect()
        self.birdRect.x = SCREEN_WIDTH + self.image.get_width() * 2
        self.birdRect.y = randrange(210, 230, 5)
        self.birdRect.width = self.image.get_width()
        self.birdRect.height = self.image.get_height()
        self.flyCount = 0
        self.oscillate = 110
        self.alternate = False
        
    def update(self, player, gameSpeed):
        collision = self.birdRect.colliderect(player.dino_rect)
        self.changeOscillator()
        if self.alternate:
            self.oscillate -= 2.5
        else:
            self.oscillate += 2.5
        if collision:
            if player.hasPowerUp:
                self.birdRect.x = SCREEN_WIDTH + self.image.get_width() * 3
                self.birdRect.y = randrange(210, 230, 5)
                return False        
        if self.flyCount > 9:
            self.flyCount = 0
        self.image = BIRD[self.flyCount//5]
        if self.birdRect.topright[0] < 0:
            self.birdRect.x = SCREEN_WIDTH + self.image.get_width() * 3
            self.birdRect.y = randrange(210, 230, 5)
        self.birdRect.x -= gameSpeed
        self.birdRect.y += self.oscillate
        self.flyCount += 1
        return collision
    
    def draw(self, screen):
        screen.blit(self.image, (self.birdRect.x, self.birdRect.y))
        
    def changeOscillator(self):
        if self.oscillate >= 20:
            self.alternate = True
        elif self.oscillate <= -20:
            self.alternate = False