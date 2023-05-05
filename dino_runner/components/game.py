import pygame

from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.cactus import Cactus
from dino_runner.components.cloud import Cloud
from dino_runner.components.bird import Bird
from dino_runner.components.playerTries import PlayerTries
from dino_runner.components.power import Power

from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, SOUNDS

INCREASE_VEL_VALUE = 2.5
NUM_OBSTACLES = 4
POWERS = {
    'hammer': Power('hammer'),
    'shield': Power('shield'),
    'heart': Power('heart')
}


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
        self.playerTries = PlayerTries()
        self.cactus = []
        self.cloud = []
        self.bird = Bird()
        self.power = POWERS
        self.lastPower = 'heart'  # primeiro power up
        self.font = pygame.font.SysFont('arial', 25, True, True)
        self.rgb = {'r': 255, 'g': 255, 'b': 255}
        self.hasCollision = False
        self.changeBg = False
        self.endgame = False

    def execute(self):
        self.endgame = True

        while self.endgame:
            if not self.playing:
                self.gameOver()

        pygame.display.quit()
        pygame.quit()

    def run(self):
        # Game loop: events - update - draw
        self.clearScreen()

        self.playing = True
        while self.playing:
            self.hasCollision = self.update()
            self.verificateCollision()

        if self.endgame:
            self.execute()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        points = self.showMessage(f'Points: {self.points}', 25, (90, 90, 90))
        self.points += 1
        self.events()
        self.draw(points)
        userInput = pygame.key.get_pressed()

        self.player.update(userInput)
        self.playerTries.update(self.player)

        if self.points >= 200:
            self.power[self.lastPower].update(
                self.player, self.game_speed, self.lastPower)

        for i in range(self.cloud.__len__()):
            self.cloud[i].update(self.game_speed)

        for j in range(self.cactus.__len__()):
            hasCollision = self.cactus[j].update(self.player, self.game_speed)
            if hasCollision == True:
                return True

        if self.points >= 550:
            hasCollision = self.bird.update(self.player, self.game_speed)
            if hasCollision == True:
                return True

        if self.points % 1000 == 0:
            SOUNDS['score'].play()

        if self.points > 0:
            if self.points % 100 == 0:
                self.changeBg = self.bgAlternator()
        self.changeBgColor()

    def draw(self, text: pygame.Surface):
        if self.points % 1000 == 0:
            # self.gameFps += INCREASE_VEL_VALUE
            self.game_speed += INCREASE_VEL_VALUE
        self.clock.tick(self.gameFps)
        self.screen.fill((self.rgb['r'], self.rgb['g'], self.rgb['b']))
        self.draw_background()

        self.player.draw(self.screen)

        if self.points >= 200:
            if not self.player.hasPowerUp:
                self.power[self.lastPower].draw(self.screen)
                if self.points % 200 == 0:
                    if self.lastPower == 'heart':
                        self.lastPower = 'shield'
                    elif self.lastPower == 'shield':
                        self.lastPower = 'hammer'
                    else:
                        self.lastPower = 'heart'
            else:
                message = f'Power Up duration: {self.power[self.lastPower].duration}'
                formated = self.showMessage(message, 20, (90, 90, 90))
                self.screen.blit(formated, (5, SCREEN_HEIGHT - formated.get_height() - 5))

        for i in range(self.player.hp//1000):
            self.playerTries.draw(self.screen, i)

        for i in range(self.cloud.__len__()):
            self.cloud[i].draw(self.screen)

        for j in range(self.cactus.__len__()):
            if j % 2 == 0:
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

    def verificateCollision(self):
        if self.hasCollision:
            if not self.player.hasPowerUp:
                SOUNDS['death'].play()
                if self.playerTries.numTries > 0:
                    self.player.hp -= self.player.hp//self.playerTries.numTries
                    self.clearScreen()
                    self.hasCollision = False
                else:
                    self.playing = False
                    self.endgame = True

    def changeBgColor(self):
        if self.changeBg:
            if self.rgb['r'] > 0 and self.rgb['g'] > 0 and self.rgb['b'] > 0:
                self.rgb['r'] -= 15
                self.rgb['g'] -= 15
                self.rgb['b'] -= 15
        else:
            if self.rgb['r'] < 255 and self.rgb['g'] < 255 and self.rgb['b'] < 255:
                self.rgb['r'] += 15
                self.rgb['g'] += 15
                self.rgb['b'] += 15

    def clearScreen(self):
        self.bird.birdRect.y = SCREEN_WIDTH
        self.seedCactus()
        if self.cloud.__len__() == 0:
            self.seedCloud()
            self.player.hp = 3500
        self.player.dino_rect.x = 0
        self.hasCollision = False

    def seedCactus(self):
        self.cactus.clear()
        for i in range(NUM_OBSTACLES):
            cactus = Cactus()
            self.cactus.append(cactus)

    def seedCloud(self):
        self.cloud.clear()
        for i in range(4):
            cloud = Cloud()
            self.cloud.append(cloud)

    def pauseMenu(self):
        pass

    def gameOver(self):
        self.clearScreen()
        self.cloud.clear()
        self.screen.fill((255, 255, 255))
        message = self.showMessage('Game Over', 40, (0, 0, 0))
        self.screen.blit(message, (SCREEN_WIDTH//2 - message.get_width()//2, SCREEN_HEIGHT//4))

        message = self.showMessage(f'Pontuação: {self.points}', 20, (0, 0, 0))
        self.screen.blit(message, (SCREEN_WIDTH//2 - message.get_width()//2, SCREEN_HEIGHT//3))

        message = self.showMessage(
            'Pressione \"R\" para reiniciar ou \"F\" para finalizar.', 20, (0, 0, 0))
        self.screen.blit(message, (SCREEN_WIDTH//2 - message.get_width()//2, SCREEN_HEIGHT//2 - message.get_height()))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    pygame.quit()
                elif event.key == pygame.K_r:
                    self.points = 0
                    if self.player.dino_jump:
                        self.player.dino_jump = False
                        self.player.dino_rect.y = 310
                    self.cloud.clear()
                    self.power = POWERS
                    self.endgame = False
                    self.run()

        pygame.display.update()
        pygame.display.flip()

    def bgAlternator(self):
        return not self.changeBg
