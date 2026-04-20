import pygame
import random
from robot import Robot
from environment import WIDTH, HEIGHT, obstacles, targets, draw_environment
from swarm import separation
from metrics import all_targets_found, count_found_targets

NUM_ROBOTS = 10

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

robots = [Robot(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(NUM_ROBOTS)]

time_steps = 0
running = True

while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_environment(screen)

    for robot in robots:
        separation(robot, robots)
        robot.update(WIDTH, HEIGHT, obstacles, targets)
        robot.draw(screen)

    # Metrics
    time_steps += 1
    found = count_found_targets(robots)

    if all_targets_found(robots, targets):
        print("All targets found in:", time_steps, "steps")
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
