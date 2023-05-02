import pygame

from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.cactus import Cactus
from dino_runner.components.cloud import Cloud
from dino_runner.components.bird import Bird

from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS

INCREASE_VEL_VALUE = 2.5


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.gameFps = FPS
        self.points = 0
        self.player = Dinosaur()
        self.cactus = []
        self.cloud = []
        self.bird = Bird()
        self.font = pygame.font.SysFont('arialblack', 25, True, True)
        self.hasCollision = False

    def run(self):
        # Game loop: events - update - draw
        for i in range(4):
            cloud = Cloud()
            self.cloud.append(cloud)

        for j in range(4):
            cactus = Cactus()
            self.cactus.append(cactus)
        self.playing = True
        while self.playing:
            # if not self.hasCollision:
                self.hasCollision = self.update()
            # else:
                # pass
        pygame.quit()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    print('teste')

    def update(self): 
        points = self.showMessage(f'Points: {self.points}', 25, (255, 0, 0))
        self.points += 1
        self.events()
        self.draw(points)
        userInput = pygame.key.get_pressed()
        self.player.update(userInput)
        for i in range(self.cloud.__len__()):
            self.cloud[i].update(self.game_speed)
            
        for j in range(self.cactus.__len__()):
            hasCollision = self.cactus[j].update(self.player.dino_rect, self.game_speed)
            if hasCollision == True:
                return True
        
        if self.points >= 550:
            hasCollision = self.bird.update(self.player, self.game_speed)
            if hasCollision == True:
                return True

    def draw(self, text: pygame.Surface):
        if self.points % 1000 == 0:
            # self.gameFps += INCREASE_VEL_VALUE
            self.game_speed += INCREASE_VEL_VALUE
        self.clock.tick(self.gameFps)
        self.screen.fill((0, 0, 0))
        self.draw_background()

        self.player.draw(self.screen)
        for i in range(self.cloud.__len__()):
            self.cloud[i].draw(self.screen)
            
        for j in range(self.cactus.__len__()):
            if j%2 == 0:
                self.cactus[j].draw(self.screen, j//3, 'small')
            else:
                self.cactus[j].draw(self.screen, j//3, 'large')
        
        if self.points >= 550:
            self.bird.draw(self.screen)
        
        self.screen.blit(text, (SCREEN_WIDTH - text.get_width() - 10, 5))
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed
        
    def showMessage(self, text: str, fontSize: float, color):
        font = pygame.font.SysFont('arial', fontSize, True, False)
        message = f'{text}'
        formatedText = font.render(message, False, color)
        return formatedText