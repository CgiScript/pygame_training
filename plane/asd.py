import pygame
pygame.init()

pygame.display.set_caption("Animation Training")
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen_rect = screen.get_rect()
clock = pygame.time.Clock()
game = True



bg = pygame.transform.scale(pygame.image.load("BG.png").convert(),(800,600))
bg1 = pygame.transform.scale(pygame.image.load("BG.png").convert(),(800,600))
bg_rect = bg.get_rect()
bg1_rect = bg1.get_rect()
bg1_rect.x, bg1_rect.y = bg_rect.right, bg_rect.y

def infinite_bg():
    global bg_rect, bg1_rect
    bg_rect.x -= 2
    bg1_rect.x -= 2
    if bg_rect.right == 0:
        bg_rect.x = bg1_rect.right
    if bg1_rect.right == 0:
        bg1_rect.x = bg_rect.right
    screen.blit(bg, bg_rect)
    screen.blit(bg1, bg1_rect)


class Bullet(pygame.sprite.Sprite):
    def __init__(self,plane):
        super().__init__()
        self.images = [pygame.image.load("bullet{}.png".format(i)).convert_alpha() for i in range(1,6)]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = plane.right, plane.centery
        self.timer = 0
        
    def update(self,dt):
        self.timer += dt
        if self.timer > 50:
            self.index += 1
            self.timer = 0
            if self.index > len(self.images) - 1:
                self.index = 0               
            self.image = self.images[self.index]
            
        self.rect.x += 15
        
        


    

class Plane(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.state = "idle"
        self.idle_images = [pygame.transform.scale(pygame.image.load("fly{}.png".format(i)).convert_alpha(),(200,136))
                            for i in range(1,3)]
        self.shoot_images = [pygame.transform.scale(pygame.image.load("shoot{}.png".format(i)).convert_alpha(),(200,136))
                             for i in range(1,6)]
        self.index = 0
        self.image = self.idle_images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 100, 280
        self.time = 0
        self.move_right = False
        self.move_left = False
        self.move_up = False
        self.move_down = False
        self.bullet_list = pygame.sprite.Group()
        self.shooting_sound = pygame.mixer.Sound("shoot.mp3")

    def move(self):
        if self.move_right and self.rect.right < 400:
            self.rect.x += 8
        if self.move_left and self.rect.x > 0:
            self.rect.x -= 8
        if self.move_up and self.rect.y > 50:
            self.rect.y -= 8
        if self.move_down and self.rect.bottom < 500:
            self.rect.y += 8
            
    def shoot(self):
        self.bullet_list.add(Bullet(self.rect))
        self.shooting_sound.play()

    def update(self,dt):
        self.move()
        self.animate(dt)
        self.bullet_list.update(dt)
        for bullet in self.bullet_list:
            if bullet.rect.x > 800:
                self.bullet_list.remove(bullet)
        
    def animate(self,dt):
        if self.state == "idle":
            images = self.idle_images
        if self.state == "shoot":
            images = self.shoot_images
            
        self.time += dt
        if self.time > 100:
            self.time = 0
            self.index += 1
            if self.index > len(images)-1:
                self.index = 0
                if self.state == "shoot":
                    self.state = "idle"
            self.image = images[self.index]


player = Plane()

while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player.move_right = True
            if event.key == pygame.K_LEFT:
                player.move_left = True
            if event.key == pygame.K_UP:
                player.move_up = True
            if event.key == pygame.K_DOWN:
                player.move_down = True
            if event.key == pygame.K_SPACE:
                player.state = "shoot"
                player.shoot()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                player.move_right = False
            if event.key == pygame.K_LEFT:
                player.move_left = False
            if event.key == pygame.K_UP:
                player.move_up = False
            if event.key == pygame.K_DOWN:
                player.move_down = False
            
    
    dt = clock.tick(30)
    infinite_bg()    
    screen.blit(player.image, player.rect)
    player.update(dt)
    player.bullet_list.draw(screen)
    pygame.display.update()   


pygame.quit()
