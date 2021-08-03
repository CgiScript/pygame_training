import pygame
import random

pygame.init()
pygame.font.init()

BLACK = [0,0,0]
GREEN = [0,255,0]

state = "main_menu"
clock = pygame.time.Clock()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode([WIDTH, HEIGHT])

font = pygame.font.SysFont('Comic Sans MS', 70)
score_font = pygame.font.SysFont('Comic Sans MS', 15)

difficulty = 10
wall = False
obstacle = False

def game_screen():
    
    global state, obstacle
    
    score = 0
    score_text = font.render("{}".format(score),True,(255,255,255))
    size = 25
    
    snake = pygame.Surface([size, size])
    snake.fill(GREEN)
    snake_rect = snake.get_rect()
    snake_rect.x = screen.get_rect().centerx
    snake_rect.y = screen.get_rect().centery
    snake_direction = "right"
    

    food = pygame.Surface((size,size))
    food.fill((255,0,0))
    food_rect = food.get_rect()

    # generate obstacle
    if obstacle:
        line1 = pygame.Surface((500, 25))
        line2 = pygame.Surface((500, 25))
        line1_rect = line1.get_rect()
        line2_rect = line2.get_rect()
        line1.fill((255,255,255)); line2.fill((255,255,255))
        line1_rect.x, line2_rect.x = 150, 150
        line1_rect.y, line2_rect.y = 200, 400
        obstacle_list = [line1_rect, line2_rect]

    def generate_cell():
        cell = pygame.Surface([size, size])
        cell.fill(GREEN)
        return cell
    
    # create initial body cells
    
    snake_body = [generate_cell() for i in range(5)]    
    body_rects = [body.get_rect() for body in snake_body]    
    for body in snake_body:
        body.fill(GREEN)
    body_dict = dict(zip(snake_body, body_rects))

    # place body cells to center of screen
    
    body_rects[0].x = snake_rect.x - size
    body_rects[0].y = snake_rect.y        
    for i in range(1,len(body_rects)):
        body_rects[i].x = body_rects[i-1].x - size
        body_rects[i].y = body_rects[i-1].y
    
    def generate_food():
        global obstacle
        nonlocal obstacle_list

        food_rect.x = random.randint(0,31) * size
        food_rect.y = random.randint(0,23) * size

        if obstacle:
            for obst in obstacle_list:
                if obst.colliderect(food_rect):
                    food_rect.y -= 50
                    
    generate_food()

    def arrange():
        
        for i in range(len(body_rects)-1,0,-1):
            body_rects[i].x = body_rects[i-1].x
            body_rects[i].y = body_rects[i-1].y
        body_rects[0].x = snake_rect.x
        body_rects[0].y = snake_rect.y

    def move():
        
        arrange()
        
        if snake_direction == "right":
            snake_rect.x += size
        if snake_direction == "left":
            snake_rect.x -= size
        if snake_direction == "up":
            snake_rect.y -= size
        if snake_direction == "down":
            snake_rect.y += size

    def draw_obstacle():   

        screen.blit(line1, line1_rect)
        screen.blit(line2, line2_rect)

    def check_collide():
        
        global state
        nonlocal score, score_text

        if snake_rect.colliderect(food_rect):
            generate_food()
            cell = generate_cell()
            cell_rect = cell.get_rect()
            cell_rect.x = body_rects[len(body_rects)-1].x
            cell_rect.y = body_rects[len(body_rects)-1].y
            snake_body.append(cell)
            body_rects.append(cell_rect)
            body_dict[cell] = cell_rect
            score = score + 2
            score_text = font.render("{}".format(score),True,(255,255,255))            

        if not wall:
            if snake_rect.right > WIDTH:
                snake_rect.x = 0
            if snake_rect.x < 0:
                snake_rect.x = WIDTH
            if snake_rect.y < 0:
                snake_rect.y = HEIGHT - size
            if snake_rect.bottom > HEIGHT:
                snake_rect.y = 0
        else:
            if snake_rect.right > WIDTH or snake_rect.x < 0:
                state = "main_menu"
            if snake_rect.top < 0 or snake_rect.y > HEIGHT:
                state = "main_menu"
            

        for body in body_rects:
            if snake_rect.colliderect(body):
                state = "main_menu"
        if obstacle:
            for obs in obstacle_list:
                if snake_rect.colliderect(obs):
                    state = "main_menu"
                

   
    while state == "game_play":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = "exit"
            if event.type == pygame.KEYDOWN:                
                if event.key == pygame.K_UP and snake_direction != "down":
                    snake_direction = "up"
                    break
                if event.key == pygame.K_DOWN and snake_direction != "up":
                    snake_direction = "down"
                    break
                if event.key == pygame.K_LEFT and snake_direction != "right":
                    snake_direction = "left"
                    break
                if event.key == pygame.K_RIGHT and snake_direction != "left":
                    snake_direction = "right"
                    break                    
                if event.key == pygame.K_ESCAPE:
                    state = "main_menu"
        
        screen.fill((24,24,25))
        screen.blit(score_text, (400,0))        
        if obstacle:
            draw_obstacle()
        move()
        check_collide()
        screen.blit(snake, snake_rect)
        screen.blit(food, food_rect)
        for body, rect in body_dict.items():
            screen.blit(body, rect)
        pygame.display.update()
        clock.tick(difficulty)

def main_menu():
    
    global state

    play_text = font.render('Play', True, (255, 255, 255))
    options_text = font.render('Options', True, (255, 255, 255))
    play_text_rect = play_text.get_rect()
    options_text_rect = options_text.get_rect()
    play_text_rect.center = (400,200)
    options_text_rect.center = (400,400)

    opt_box = pygame.Surface((800,100))
    opt_box.fill((0,50,50))
    opt_box_rect = opt_box.get_rect()
    opt_box_rect.center = play_text_rect.center

    option = "play"
    
    def opt_move():
        nonlocal option
        if opt_box_rect.centery == 400:
            opt_box_rect.centery -= 200
            option = "play"
        else:
            opt_box_rect.centery += 200
            option = "options"        

    while state == "main_menu":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = "exit"
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_RETURN) and (option == "play"):
                    state = "game_play"
                if (event.key == pygame.K_RETURN) and (option == "options"):
                    state = "option_menu" 
                if event.key == pygame.K_ESCAPE:
                    state = "exit"
                if event.key == pygame.K_DOWN:
                    opt_move()
                if event.key == pygame.K_UP:
                    opt_move()
                    
        screen.fill((24,24,25))
        screen.blit(opt_box, opt_box_rect)
        screen.blit(play_text, play_text_rect)
        screen.blit(options_text, options_text_rect)        
        pygame.display.update()
        clock.tick(10)


def options():
    
    global state, wall, obstacle, difficulty

    speed_text = font.render('Speed: {}'.format(difficulty), True, (255, 255, 255))
    wall_text = font.render('Wall: {}'.format(str(wall)), True, (255, 255, 255))
    obstacles_text = font.render('Obstacles: {}'.format(str(obstacle)), True, (255, 255, 255))
    speed_text_rect = speed_text.get_rect()
    wall_text_rect = wall_text.get_rect()
    obstacles_text_rect = obstacles_text.get_rect()
    
    speed_text_rect.center = (400, 100)
    wall_text_rect.center = (400, 300)
    obstacles_text_rect.center = (400, 500)

    opt_box = pygame.Surface((800,100))
    opt_box.fill((0,50,50))
    opt_box_rect = opt_box.get_rect()
    opt_box_rect.center = speed_text_rect.center

    option_list = ["speed", "wall", "obstacles"]
    index = 0
    option = option_list[index]
    
    def opt_move(y):
        
        nonlocal index, option
        
        opt_box_rect.centery += 200 * y
        if opt_box_rect.centery > 500:
            opt_box_rect.centery = 100
            index = 0
            option = option_list[index]
            return
        if opt_box_rect.centery < 100:
            opt_box_rect.centery = 500
            index = 2
            option = option_list[index]
            return
        index += y  
        option = option_list[index]
               
        
    while state == "option_menu":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = "exit"
            if event.type == pygame.KEYDOWN:                
                if event.key == pygame.K_ESCAPE:
                    state = "main_menu"
                if event.key == pygame.K_DOWN:
                    opt_move(1)
                if event.key == pygame.K_UP:
                    opt_move(-1)
                if event.key == pygame.K_RETURN:
                    if option == "speed":
                        difficulty = 20 if difficulty == 10 else 10
                        speed_text = font.render('Speed: {}'.format(difficulty), True, (255, 255, 255))
                    if option == "wall":
                        wall = True if not wall else False
                        wall_text = font.render('Wall: {}'.format(str(wall)), True, (255, 255, 255))
                    if option == "obstacles":
                        obstacle = True if not obstacle else False
                        obstacles_text = font.render('Obstacles: {}'.format(str(obstacle)), True, (255, 255, 255))

                    
        screen.fill((24,24,25))
        screen.blit(opt_box, opt_box_rect)
        screen.blit(speed_text, speed_text_rect)
        screen.blit(obstacles_text, obstacles_text_rect)
        screen.blit(wall_text, wall_text_rect)
        pygame.display.update()
        clock.tick(10)
    

def state_manager():
    
    global state
    
    while True:
        if state == "main_menu":
            main_menu()
        if state == "game_play":
            game_screen()
        if state == "option_menu":
            options()
        if state == "exit":
            break
        
state_manager()        
pygame.quit()
