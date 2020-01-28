import os
import pygame
import Snake
import neat
import visualize

BLOCK_SIZE = 10  # block height/width in pixels
WINDOWS_WIDTH = 30 * BLOCK_SIZE
WINDOWS_HEIGHT = 30 * BLOCK_SIZE
GAME_SPEED = 0.5
REWARD_CONST = 10
PUNISHING_CONST = 1.2

ACTIVATION_THRESHOLD = 0.8  # threshold for the activation function

A = 1

display = pygame.display.set_mode([WINDOWS_WIDTH, WINDOWS_HEIGHT])

icon = pygame.transform.scale(pygame.image.load("icon.png").convert_alpha(), (900, 900))
pygame.display.set_icon(icon)


# pygame.display.set_caption("SnAIke")


def draw_game(ground, snake):
    # pygame.draw.rect(display, (0,0,0), (ground.x, ground.y, ground.width*BLOCK_SIZE, ground.height*BLOCK_SIZE))
    pygame.draw.rect(display, (255, 0, 0),
                     (ground.fruit[0] * BLOCK_SIZE, ground.fruit[1] * BLOCK_SIZE, BLOCK_SIZE * 2, BLOCK_SIZE * 2))
    for part in snake.body:
        pygame.draw.rect(display, (255, 255, 255),
                         ((part[0]) * BLOCK_SIZE, part[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))


def fitness_function(genomes, config):
    for i, genome in enumerate(genomes):
        current_genome = genome[1]
        current_genome.fitness = 0.0
        current_nn = neat.nn.FeedForwardNetwork.create(current_genome, config)
        """snake.hungry_for = 0
        snake.score = 0
        snake.body = [[15,15]] #reset snake everytime it starts fresh"""

        one_output_counter = 0  # debug
        output_counter = 0

        snake = Snake.Snake(15, 15)
        run = True
        fresh_flag = True  # debugging/print snake id
        # curr_distance = snake.distance(ground)
        while run:
            reward = 0
            # output_counter = 0  # if there are more than 0 outputs higher than threshold then dont move
            # prev_distance = curr_distance
            pygame.display.set_caption("SnAIke: " + str(snake.score))
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()
                    break

            prev_distanceX = snake.distanceX(ground)
            prev_distanceY = snake.distanceY(ground)
            output = current_nn.activate([prev_distanceX,
                                          prev_distanceY])  # speedX. speedY were instead of distanceX, distanceY,snake.body[0][0], snake.body[0][1], ground.fruit[0], ground.fruit[1],
            output_counter = 0  # if there are more than 0 outputs higher than threshold then dont move
            # OUTPUT 0 - move UP
            # OUTPUT 1 - move DOWN
            # OUTPUT 2 - move LEFT
            # OUTPUT 3 - move RIGHT
            # snake is not given a permission to move diagonally

            potential_speedY = 0
            potential_speedX = 0

            # and not (snake.speedY == GAME_SPEED and not len(snake.body) == 1): #and output[1]<ACTIVATION_THRESHOLD
            # and output[2]<ACTIVATION_THRESHOLD and output[3]<ACTIVATION_THRESHOLD:

            if output[0] >= ACTIVATION_THRESHOLD:
                potential_speedY += -GAME_SPEED
                potential_speedX += 0
                output_counter += 1
                # print("Gore: " + str(output[0]) + str(output[1]) + str(output[2]) + str(output[3]))
            if output[1] >= ACTIVATION_THRESHOLD:  # and not (snake.speedY == -GAME_SPEED and not len(snake.body) == 1): #and output[1]>=ACTIVATION_THRESHOLD and output[2]<ACTIVATION_THRESHOLD and output[3]<ACTIVATION_THRESHOLD:
                potential_speedY += GAME_SPEED
                potential_speedX += 0
                output_counter += 1
                # print("Dole: " + str(output[0]) + str(output[1]) + str(output[2]) + str(output[3]))
            if output[2] >= ACTIVATION_THRESHOLD:  # and not (snake.speedX == GAME_SPEED and not len(snake.body) == 1): #and output[1]<ACTIVATION_THRESHOLD and output[2]>=ACTIVATION_THRESHOLD and output[3]<ACTIVATION_THRESHOLD:
                potential_speedX += -GAME_SPEED
                potential_speedY += 0
                output_counter += 1
                # print("Levo: " + str(output[0]) + str(output[1]) + str(output[2]) + str(output[3]))
            if output[3] >= ACTIVATION_THRESHOLD:  # and not (snake.speedX == -GAME_SPEED and not len(snake.body) == 1): #and output[1]<ACTIVATION_THRESHOLD and output[2]<ACTIVATION_THRESHOLD and output[3]>=ACTIVATION_THRESHOLD:
                potential_speedX += GAME_SPEED
                potential_speedY += 0
                output_counter += 1
                # print("Desno: " + str(output[0]) + str(output[1]) + str(output[2]) + str(output[3]))"""

            """if output_counter == 1:
                one_output_counter += 1
                snake.speedX = potential_speedX
                snake.speedY = potential_speedY
            else:
                # print(output) # ideja, da input ima i last output counter
                snake.speedX = 0
                snake.speedY = 0"""

            snake.speedY = potential_speedY
            snake.speedX = potential_speedX

            not_transitioned = snake.move(ground)

            if snake.eat(ground):
                reward += 10  # reward snake when it finds food
                prev_distanceX = snake.distanceX(
                    ground)  # so it doesnt get unfair punishment by randomly generating new fruit that is far away
                prev_distanceY = snake.distanceY(ground)

            # curr_distance = snake.distance(ground)
            # print(curr_distance, prev_distance)

            # print("PretX: ", prev_distanceX)
            # print("SadX: ", snake.distanceX(ground))
            # print("PretY: ", prev_distanceY)
            # print("SadY: ", snake.distanceY(ground))

            reward += A * (abs(prev_distanceX) - abs(snake.distanceX(ground))) + A * (
                        abs(prev_distanceY) - abs(snake.distanceY(ground)))

            # print("Reward increased: ", A*(abs(prev_distanceX) - abs(snake.distanceX(ground))) + A*(abs(prev_distanceY) - abs(snake.distanceY(ground))))

            # if output_counter == 1:
            current_genome.fitness += reward  # either get reward or dont move so 0 reward is given anyways
            # else:
            # current_genome.fitness -= 0.5

            if snake.hungry_for >= 180 / GAME_SPEED:
                run = False

            # print("Distanca: " + str(snake.distance(ground)))

            if fresh_flag == True:
                print("Current Genome: " + str(snake.id % 50))
                fresh_flag = False

            # print(current_genome.fitness)

            if run == False:
                print("Fitness: " + str(current_genome.fitness))
                # print("Num of decisions: ", one_output_counter)
                # print(str(output[0]) + str(output[1]) + str(output[2]) + str(output[3]))

            draw_game(ground, snake)
            pygame.display.update()
            display.fill((0, 0, 0))


# main()

def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    snake_population = neat.Population(config)
    # snake_population = neat.checkpoint.Checkpointer.restore_checkpoint("neat-checkpoint-16")  # load from a checkpoint

    snake_population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    snake_population.add_reporter(stats)
    snake_population.add_reporter(neat.Checkpointer(5))

    winner = snake_population.run(fitness_function)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    ground = Snake.Ground(30, 30)
    # snake_list = []
    clock = pygame.time.Clock()

    # for i in range(0, 50):
    # snake_list.append(Snake.Snake(15, 15))
    run(config_path)
