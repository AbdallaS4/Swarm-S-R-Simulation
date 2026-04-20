import pygame
import random

WIDTH = 800
HEIGHT = 600

# Obstacles (rectangles)
obstacles = [
    pygame.Rect(200, 150, 100, 20),
    pygame.Rect(400, 300, 150, 20),
]

# Targets (search & rescue points)
targets = [(random.randint(50, 750), random.randint(50, 550)) for _ in range(5)]

def draw_environment(screen):
    # Draw obstacles
    for obs in obstacles:
        pygame.draw.rect(screen, (0, 0, 0), obs)

    # Draw targets
    for t in targets:
        pygame.draw.circle(screen, (255, 0, 0), t, 6)