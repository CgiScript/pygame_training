import pygame

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
game = True


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((150,15))
        self.image.fill((0,200,150))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        



platform_list = pygame.sprite.Group(Platform(100,500),
                                    Platform(300,400),Platform(500,300))


class Box(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50,100))
        self.image.fill((0,200,0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 150, 300
        self.move_right = False
        self.move_left = False
        self.change_y = 10
        
    def move(self):
        if self.move_right:
            self.rect.x += 5
        if self.move_left:
            self.rect.x -= 5

    def jump(self):
        self.change_y = -15
            
    def calc_gravity(self):
        if self.change_y < 10:
            self.change_y += 1
        if self.change_y > 10:
            self.change_y = 10
        
        self.rect.y += self.change_y
        #check if player on the floor
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
        #check if player on any of platforms    
        for platform in platform_list:
            if self.rect.colliderect(platform.rect):
                self.rect.bottom = platform.rect.top
        
    def update(self):        
        self.move()
        self.calc_gravity()
    



player = Box()

while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player.move_right = True
            if event.key == pygame.K_LEFT:
                player.move_left = True
            if event.key == pygame.K_SPACE:
                player.jump()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                player.move_right = False
            if event.key == pygame.K_LEFT:
                player.move_left = False
            

    screen.fill((0,0,0))
    player.update()
    screen.blit(player.image, player.rect)
    platform_list.draw(screen)
    pygame.display.update()
    clock.tick(30)
pygame.quit()
