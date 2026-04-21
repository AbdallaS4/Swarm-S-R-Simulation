import pygame
import math
import random
 
 
class Robot:
    def __init__(self, x, y, role="scout"):
        self.x   = float(x)
        self.y   = float(y)
        self.vx  = random.uniform(-1.0, 1.0)
        self.vy  = random.uniform(-1.0, 1.0)
        self.speed       = 2.5
        self.radius      = 5
        self.sense_range = 15
        self.role        = role
        self.trail       = []
        self.trail_len   = 25
 
    # ── Physics ────────────────────────────────────────────────────────────────
 
    def _clamp_speed(self):
        mag = math.hypot(self.vx, self.vy)
        if mag > self.speed and mag > 0:
            self.vx = self.vx / mag * self.speed
            self.vy = self.vy / mag * self.speed
 
    def _move(self):
        self.trail.append((int(self.x), int(self.y)))
        if len(self.trail) > self.trail_len:
            self.trail.pop(0)
        self.x += self.vx
        self.y += self.vy
 
    def _bounce_walls(self, w, h):
        m = 12
        if self.x < m:         self.x = m;         self.vx =  abs(self.vx)
        elif self.x > w - m:   self.x = w - m;     self.vx = -abs(self.vx)
        if self.y < m:         self.y = m;         self.vy =  abs(self.vy)
        elif self.y > h - m:   self.y = h - m;     self.vy = -abs(self.vy)
 
    def _avoid_obstacles(self, obstacles):
        rb = pygame.Rect(self.x - self.radius, self.y - self.radius,
                         self.radius * 2, self.radius * 2)
        for o in obstacles:
            if o.colliderect(rb):
                dx = self.x - o.centerx
                dy = self.y - o.centery
                dist = math.hypot(dx, dy) or 1.0
                self.vx += dx / dist * 0.8
                self.vy += dy / dist * 0.8
                self.x  += dx / dist * 2
                self.y  += dy / dist * 2
 
    def _sense(self, resources, memory):
        for r in resources:
            if not r.found:
                if math.hypot(self.x - r.x, self.y - r.y) < self.sense_range:
                    r.found = True
                    memory.add_found(r.x, r.y)
 
    # ── Public API ─────────────────────────────────────────────────────────────
 
    def update(self, w, h, obstacles, resources, memory):
        self._clamp_speed()
        self._move()
        self._bounce_walls(w, h)
        self._avoid_obstacles(obstacles)
        self._sense(resources, memory)
        memory.mark(self.x, self.y)
 
    def draw(self, screen, show_trail=False, show_range=False):
        ix, iy = int(self.x), int(self.y)
 
        if show_trail and len(self.trail) > 1:
            for i in range(1, len(self.trail)):
                shade = int(80 * i / len(self.trail))
                pygame.draw.line(screen, (0, shade, 80),
                                 self.trail[i-1], self.trail[i], 1)
 
        if show_range:
            pygame.draw.circle(screen, (50, 50, 90), (ix, iy), self.sense_range, 1)
 
        colour = (0, 160, 255) if self.role == "scout" else (0, 210, 110)
        pygame.draw.circle(screen, colour, (ix, iy), self.radius)
 
        # Heading arrow
        mag = math.hypot(self.vx, self.vy) or 0.01
        nx  = ix + int(self.vx / mag * 8)
        ny  = iy + int(self.vy / mag * 8)
        pygame.draw.line(screen, (255, 255, 255), (ix, iy), (nx, ny), 1)
 