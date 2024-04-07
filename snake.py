import pygame
import random

pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 0, 0)
green = (0, 255, 0)
blue = (50, 153, 213)

dis_width = 300
dis_height = 200
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()

snake_block = 10
snake_speed = 15

font_style = pygame.font.SysFont(None, 30)
score_font = pygame.font.SysFont(None, 25)

game_over_sound = pygame.mixer.Sound("game_over.wav")
game_over_sound.set_volume(0.2)

def message(msg_lines, color, font=font_style):
    y_offset = 0
    for line in msg_lines:
        mesg = font.render(line, True, color)
        dis.blit(mesg, [dis_width / 6, dis_height / 3 + y_offset])
        y_offset += mesg.get_height() + 5 

def game_over_screen(score):
    selected_option = 1

    while True:
        dis.fill(black)
        
        message(["GG!"], white, font=pygame.font.SysFont(None, 40))
        message(["", "Your Score: " + str(score)], white)
        message(["", "", "1 - Play again"], green if selected_option == 1 else white)
        message(["", "", "", "2 - Quit"], green if selected_option == 2 else white)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = 1
                elif event.key == pygame.K_DOWN:
                    selected_option = 2
                elif event.key == pygame.K_RETURN:
                    return selected_option

def gameLoop():
    game_over = False

    while not game_over:
        x1 = dis_width / 2
        y1 = dis_height / 2

        x1_change = 0
        y1_change = 0

        snake_List = []
        length_of_snake = 1

        foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
        foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

        score = 0

        while not game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and x1_change != snake_block:
                        x1_change = -snake_block
                        y1_change = 0
                    elif event.key == pygame.K_RIGHT and x1_change != -snake_block:
                        x1_change = snake_block
                        y1_change = 0
                    elif event.key == pygame.K_UP and y1_change != snake_block:
                        y1_change = -snake_block
                        x1_change = 0
                    elif event.key == pygame.K_DOWN and y1_change != -snake_block:
                        y1_change = snake_block
                        x1_change = 0

            if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
                break
            x1 += x1_change
            y1 += y1_change
            dis.fill(black)
            pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])
            snake_head = []
            snake_head.append(x1)
            snake_head.append(y1)
            snake_List.append(snake_head)
            if len(snake_List) > length_of_snake:
                del snake_List[0]

            for x in snake_List[:-1]:
                if x == snake_head:
                    game_over = True
                    break

            for segment in snake_List:
                pygame.draw.rect(dis, green, [segment[0], segment[1], snake_block, snake_block])

            pygame.display.update()

            if x1 == foodx and y1 == foody:
                foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
                foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
                length_of_snake += 1
                score += 10

            clock.tick(snake_speed)

        game_over_sound.play()
        option = game_over_screen(score)
        if option == 1:
            continue
        elif option == 2:
            break

    pygame.quit()
    quit()

gameLoop()
