import pygame
import random
 
WIDTH  = 900
HEIGHT = 650
 

WALL_COLOR     = (45, 52, 72)
RESOURCE_COLOR = (220, 60, 60)
FOUND_COLOR    = (60, 220, 120)
RING_COLOR     = (140, 40, 40)   # dim ring around unfound survivors
 
 
class Resource:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.found = False
 
 
def generate_terrain(w, h):
    """Fixed-seed obstacle layout — same map every run."""
    rng = random.Random(42)
    obstacles = []
 
    for _ in range(5):
        x = rng.randint(120, w - 220)
        y = rng.randint(120, h - 220)
        obstacles.append(pygame.Rect(x,      y,      130, 18))
        obstacles.append(pygame.Rect(x,      y,      18,  130))
        obstacles.append(pygame.Rect(x + 90, y + 80, 80,  18))
 
    for i in range(0, w, 200):
        obstacles.append(pygame.Rect(i,       110,     90, 18))
        obstacles.append(pygame.Rect(i + 100, h - 130, 90, 18))
 
    for j in range(0, h, 220):
        obstacles.append(pygame.Rect(w // 2 - 10, j + 40, 18, 80))
 
    return obstacles
 
 
def valid_spawn(x, y, obstacles, margin=12):
    probe = pygame.Rect(x - margin, y - margin, margin * 2, margin * 2)
    return not any(o.colliderect(probe) for o in obstacles)
 
 
def generate_resources(n, w, h, obstacles, rng=None):
    if rng is None:
        rng = random.Random(99)
    resources = []
    attempts  = 0
    while len(resources) < n and attempts < 10000:
        x = rng.randint(40, w - 40)
        y = rng.randint(40, h - 40)
        if valid_spawn(x, y, obstacles):
            resources.append(Resource(x, y))
        attempts += 1
    return resources
 
 
def draw_environment(screen, obstacles, resources):
    # Walls
    for o in obstacles:
        pygame.draw.rect(screen, WALL_COLOR, o)
 
    # Survivors
    for r in resources:
        pos = (int(r.x), int(r.y))
        if r.found:
            pygame.draw.circle(screen, FOUND_COLOR, pos, 6)
        else:
            pygame.draw.circle(screen, RING_COLOR,     pos, 11, 1)  # outer ring
            pygame.draw.circle(screen, RESOURCE_COLOR, pos, 6)      # filled dot
 
 
def draw_heatmap(screen, memory):
    """Blit a pre-built SRCALPHA surface showing visited cells."""
    cell  = memory.grid
    max_v = float(memory.visited.max())
    if max_v == 0:
        return
 
    
    surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    for gx in range(memory.w):
        for gy in range(memory.h):
            v = memory.visited[gx][gy]
            if v > 0:
                intensity = int(min(v / max_v * 150, 150))
                surf.fill(
                    (0, 180, 255, intensity),
                    pygame.Rect(gx * cell, gy * cell, cell, cell)
                )
    screen.blit(surf, (0, 0))