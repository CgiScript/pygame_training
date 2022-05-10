import pygame
import math
import datetime

pygame.init()
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True


def calc_degree(degrees):
    x = math.cos(math.radians(degrees)) * 250
    y = math.sin(math.radians(degrees)) * 250
    return x+WIDTH/2, -(y-HEIGHT/2)
    

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False   
    screen.fill((10,10,10))
    pygame.draw.circle(screen, (100,0,0), (WIDTH/2,HEIGHT/2), WIDTH/2-20, 0)
    time = datetime.datetime.now()
    second = time.second
    minute = time.minute
    hour = time.hour
    pygame.draw.line(screen,(0,0,0),(WIDTH/2,HEIGHT/2) ,calc_degree(-(second*6)+90), 3)
    pygame.draw.line(screen,(0,0,0),(WIDTH/2,HEIGHT/2) ,calc_degree(-(minute*6)+90), 6)
    pygame.draw.line(screen,(0,0,0),(WIDTH/2,HEIGHT/2) ,calc_degree(-(hour*30)+90), 9)
    pygame.display.update()
    clock.tick(20)
pygame.quit()
