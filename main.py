import pygame
import neat
import Snake




BLOCK_SIZE = 10 #block height/width in pixels
WINDOWS_WIDTH = 600
WINDOWS_HEIGHT = 600

display = pygame.display.set_mode([WINDOWS_WIDTH, WINDOWS_HEIGHT])

icon = pygame.transform.scale(pygame.image.load("icon.png").convert_alpha(), (900,900))
pygame.display.set_icon(icon)



#pygame.display.set_caption("SnAIke")


def draw_game(ground, snake):

    #pygame.draw.rect(display, (0,0,0), (ground.x, ground.y, ground.width*BLOCK_SIZE, ground.height*BLOCK_SIZE))
    pygame.draw.rect(display, (255,0,0), (ground.fruit[0]*BLOCK_SIZE, ground.fruit[1]*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    for part in snake.body:
        pygame.draw.rect(display, (255,255,255), ((part[0])*BLOCK_SIZE, part[1]*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def main():
    ground = Snake.Ground(60,60)
    snake = Snake.Snake(30,30)
    clock = pygame.time.Clock()



    run = True
    while run:
        pygame.display.set_caption("SnAIke: " + str(snake.score))
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.speedY = -1
                    snake.speedX = 0
                elif event.key == pygame.K_DOWN:
                    snake.speedY = 1
                    snake.speedX = 0
                elif event.key == pygame.K_LEFT:
                    snake.speedX = -1
                    snake.speedY = 0
                elif event.key == pygame.K_RIGHT:
                    snake.speedX = 1
                    snake.speedY = 0

        if(not snake.move(ground)): pygame.quit()
        snake.eat(ground)

        draw_game(ground, snake)
        pygame.display.update()
        display.fill((0,0,0))
main()