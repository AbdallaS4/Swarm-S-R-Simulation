import pygame
import random
import math

class Robot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = random.uniform(0, 2 * math.pi)
        self.speed = 2
        self.radius = 5
        self.found_targets = []

    def move(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

    def avoid_walls(self, width, height):
        if self.x <= 0 or self.x >= width:
            self.angle = math.pi - self.angle
        if self.y <= 0 or self.y >= height:
            self.angle = -self.angle

    def avoid_obstacles(self, obstacles):
        for obs in obstacles:
            if obs.collidepoint(self.x, self.y):
                self.angle += math.pi  # simple turn away

    def random_turn(self):
        self.angle += random.uniform(-0.2, 0.2)

    def check_targets(self, targets):
        for t in targets:
            dist = math.hypot(self.x - t[0], self.y - t[1])
            if dist < 10 and t not in self.found_targets:
                self.found_targets.append(t)

    def update(self, width, height, obstacles, targets):
        self.move()
        self.avoid_walls(width, height)
        self.avoid_obstacles(obstacles)
        self.random_turn()
        self.check_targets(targets)

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 0, 255), (int(self.x), int(self.y)), self.radius)