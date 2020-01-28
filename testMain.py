import pygame
import neat
import Snake




BLOCK_SIZE = 10 #block height/width in pixels
WINDOWS_WIDTH = 30*BLOCK_SIZE
WINDOWS_HEIGHT = 30*BLOCK_SIZE

display = pygame.display.set_mode([WINDOWS_WIDTH, WINDOWS_HEIGHT])

icon = pygame.transform.scale(pygame.image.load("icon.png").convert_alpha(), (900,900))
pygame.display.set_icon(icon)



#pygame.display.set_caption("SnAIke")


def draw_game(ground, snake):

    #pygame.draw.rect(display, (0,0,0), (ground.x, ground.y, ground.width*BLOCK_SIZE, ground.height*BLOCK_SIZE))
    pygame.draw.rect(display, (255,0,0), (ground.fruit[0]*BLOCK_SIZE, ground.fruit[1]*BLOCK_SIZE, BLOCK_SIZE*2, BLOCK_SIZE*2))
    for part in snake.body:
        pygame.draw.rect(display, (255,255,255), ((part[0])*BLOCK_SIZE, part[1]*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def main():
    ground = Snake.Ground(30,30)
    snake = Snake.Snake(15,15)
    clock = pygame.time.Clock()

    reward = 0#debug
    overall_reward = 0#debug
    cnt = 0 #debug

    run = True
    while run:
        flag = False#debug
        pygame.display.set_caption("SnAIke: " + str(snake.score))
        clock.tick(30)

        prev_distanceX = snake.distanceX(ground)#debug
        prev_distanceY = snake.distanceY(ground)#debug

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break
            if event.type == pygame.KEYDOWN:
                #SNAKE CANNOT GO BACKWARDS IF IT HAS MORE THAN 1 BLOCK LENGTH
                if event.key == pygame.K_UP and not (snake.speedY == 1 and not len(snake.body) == 1):
                    snake.speedY = -1
                    snake.speedX = 0
                    flag = True
                elif event.key == pygame.K_DOWN and not (snake.speedY == -1 and not len(snake.body) == 1):
                    snake.speedY = 1
                    snake.speedX = 0
                    flag = True
                elif event.key == pygame.K_LEFT and not (snake.speedX == 1 and not len(snake.body) == 1):
                    snake.speedX = -1
                    snake.speedY = 0
                    flag = True
                elif event.key == pygame.K_RIGHT and not (snake.speedX == -1 and not len(snake.body) == 1):
                    snake.speedX = 1
                    snake.speedY = 0
                    flag = True

        #if not flag:
           # snake.speedX = 0
            #snake.speedY = 0

        #if(not snake.move(ground)): pygame.quit()
        snake.move(ground)
        snake.eat(ground)

        cnt+=1

        reward = 1 * (abs(prev_distanceX) - abs(snake.distanceX(ground))) + 1 * (abs(prev_distanceY) - abs(snake.distanceY(ground)))
        overall_reward += reward

        if flag:
            #print("X distance: ", snake.distanceX(ground))
            #print("Y distance: ", snake.distanceY(ground))
            #print("Together distance: ", snake.distance(ground))
            print("Reward: ", reward)
            print("Overall: ", overall_reward)
            cnt = 0



        draw_game(ground, snake)
        pygame.display.update()
        display.fill((0,0,0))
main()
