import pygame
import random

BLACK   = [0,0,0]
RED     = [255,0,0]
GREEN   = [0,255,0]

pygame.init()

class Paddle(pygame.sprite.Sprite):
    def __init__(self, centerx, bottom):
        super().__init__()
        self.width, self.height = 130,20 
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.bottom  = bottom
        self.move_right   = False
        self.move_left    = False
        
        
    def update(self):
        if self.move_right:
            self.rect.x += 10
        if self.move_left:
            self.rect.x -= 10

class Ball(pygame.sprite.Sprite):
    def __init__(self, screen, centerx, bottom, paddle):
        super().__init__()
        self.image = pygame.Surface([15,15])
        self.image.fill([250,250,250])
        self.rect  = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.bottom  = bottom

        self.screen = screen
        self.paddle = paddle
        self.outofscreen = False
        self.dx = 5
        self.dy = -5
        
    def bounce(self):
        self.dy *= -1      

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if (self.rect.right > self.screen.right) or (self.rect.left < 0):
            self.dx *= -1
        if (self.rect.top < 0):
            self.dy *= -1
        if (self.rect.top > self.screen.bottom):
            self.outofscreen = True          
         
        if pygame.sprite.collide_rect(self, self.paddle):
            if self.rect.bottom - self.paddle.rect.top <= 20 and self.dy > 0:
                self.bounce()
            if abs(self.rect.right - self.paddle.rect.left) <= 20 and self.dx > 0:
                self.dx *= -1
                if self.dy > 0:
                    self.bounce()
            if abs(self.rect.left - self.paddle.rect.right) <= 20 and self.dx < 0:
                self.dx *= -1
                if self.dy > 0:
                    self.bounce()

        
class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image  = pygame.Surface([100, 25])
        self.image.fill([random.randint(0,255),random.randint(0,255),random.randint(0,255)])
        self.rect   = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
            


class PaddleContainer(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

class BallContainer(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

class BrickContainer(pygame.sprite.Group):
    def __init__(self):
        super().__init__()


class Game():
    def __init__(self):
        self.width, self.height  = 800,600
        self.screen = pygame.display.set_mode([self.width, self.height])
        self.loop   = True
        self.clock  = pygame.time.Clock()

        self.brick_container = BrickContainer()
        self.ball_container = BallContainer()
        self.paddle_container = PaddleContainer()     

        self.paddle = Paddle(self.screen.get_rect().centerx, self.screen.get_rect().bottom)
        self.ball   = Ball(self.screen.get_rect(), self.paddle.rect.centerx, self.paddle.rect.top, self.paddle)                        
        self.ball_container.add(self.ball)
        self.paddle_container.add(self.paddle)
        for y in range(3,17):
            for x in range(1,7):
                self.brick = Brick(x*100, y*25)
                self.brick_container.add(self.brick)
        

    def main_loop(self):
        while self.loop:
            self.clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.loop = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.paddle.move_right = True
                    if event.key == pygame.K_LEFT:
                        self.paddle.move_left  = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.paddle.move_right = False
                    if event.key == pygame.K_LEFT:
                        self.paddle.move_left  = False

            if pygame.sprite.spritecollide(self.ball, self.brick_container, True):
                self.ball.bounce()
            if not self.brick_container:
                self.loop = False
            if self.ball.outofscreen:
                self.loop = False
                    
            self.screen.fill([0,30,30])
            
            self.paddle_container.draw(self.screen)
            self.ball_container.draw(self.screen)
            self.brick_container.draw(self.screen)
            
            self.paddle_container.update()
            self.ball_container.update()
            self.brick_container.update()
            
            pygame.display.update()
            

        
        
class GameState():
    def __init__(self):
        self.state = "intro"
        self.clock = pygame.time.Clock()

    def intro(self):
        intro  = True
        font = pygame.font.SysFont('Calibri Bold', 40)
        text = font.render('PRESS ANY KEY TO START', True, (255, 255, 255))
        screen = pygame.display.set_mode([800, 600])
        while intro:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        intro = False
                        self.state = "exit"
                    if event.type == pygame.KEYDOWN:
                        self.state = "game_on"
                        intro = False
            screen.fill([0,30,30])
            screen.blit(text,(200,300))
            pygame.display.update()            
            self.clock.tick(60)
        
    def game(self):
        game = Game()
        game.main_loop()

    def state_manager(self):
        while not self.state == "exit":
            if self.state == "intro":
                self.intro()
            if self.state == "game_on":
                self.game()
                self.state = "intro"
        pygame.quit()


game_state = GameState()
game_state.state_manager()

        


