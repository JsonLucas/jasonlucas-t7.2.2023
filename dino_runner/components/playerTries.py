from dino_runner.utils.constants import SCREEN_WIDTH, SOUNDS, HEART

X = 5
Y = 5
TRIES = 3

class PlayerTries:
    def __init__(self):
        self.image = HEART
        self.heartRect = self.image.get_rect()
        self.heartRect.x = X
        self.heartRect.y = Y
        self.numTries = TRIES
        
    def update(self, player):
        self.numTries = player.hp//1000
    
    def draw(self, screen, spacing):
        screen.blit(self.image, (self.heartRect.x + (self.image.get_width() * spacing), self.heartRect.y))
        