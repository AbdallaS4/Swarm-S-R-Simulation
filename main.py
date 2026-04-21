import pygame
import random
 
from environment import (WIDTH, HEIGHT, generate_terrain, generate_resources,
                          draw_environment, draw_heatmap)
from robot   import Robot
from swarm   import random_walk, boids, hive_swarm, separation
from memory  import SharedMemory
from metrics import count_found, all_found, MetricsTracker
 
# ── Init ───────────────────────────────────────────────────────────────────────
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Swarm S&R — COMP1682")
clock      = pygame.time.Clock()
font_big   = pygame.font.SysFont("consolas", 20, bold=True)
font_small = pygame.font.SysFont("consolas", 14)
 
# ── Colours ────────────────────────────────────────────────────────────────────
C_BG     = (15, 18, 30)
C_CARD   = (28, 34, 52)
C_BORDER = (0, 180, 255)
C_HOVER  = (0, 210, 140)
C_WHITE  = (220, 230, 255)
C_GREY   = (110, 120, 145)
C_HUD    = (0, 200, 255)
C_HUD2   = (170, 180, 200)
 
# ── Menu buttons ───────────────────────────────────────────────────────────────
OPTIONS = [
    ("boids",  "Boids / Flocking",  "Cohesion + alignment"),
    ("random", "Random Walk",       "Uncoordinated baseline"),
    ("hive",   "Hive (Frontier)",   "Seeks unexplored cells"),
]
BW, BH, BGAP = 400, 68, 12
BY0 = HEIGHT // 2 - (len(OPTIONS) * (BH + BGAP)) // 2
BTNS = [pygame.Rect(WIDTH // 2 - BW // 2, BY0 + i * (BH + BGAP), BW, BH)
        for i in range(len(OPTIONS))]
 
 
def draw_menu(mx, my):
    screen.fill(C_BG)
    t = font_big.render("SWARM SEARCH & RESCUE", True, C_BORDER)
    screen.blit(t, (WIDTH // 2 - t.get_width() // 2, 75))
    s = font_small.render("Choose a coordination strategy  [1] [2] [3]", True, C_GREY)
    screen.blit(s, (WIDTH // 2 - s.get_width() // 2, 108))
 
    for i, (_, label, desc) in enumerate(OPTIONS):
        r   = BTNS[i]
        hot = r.collidepoint(mx, my)
        pygame.draw.rect(screen, C_CARD,            r, border_radius=8)
        pygame.draw.rect(screen, C_HOVER if hot else C_BORDER, r, 2, border_radius=8)
        screen.blit(font_small.render(f"[{i+1}]", True, C_HOVER if hot else C_BORDER),
                    (r.x + 14, r.y + 12))
        screen.blit(font_big.render(label, True, C_WHITE if hot else C_GREY),
                    (r.x + 52, r.y + 8))
        screen.blit(font_small.render(desc, True, C_GREY),
                    (r.x + 52, r.y + 38))
    pygame.display.flip()
 
 
def build_world():
    rng       = random.Random(7)
    memory    = SharedMemory(WIDTH, HEIGHT)
    obstacles = generate_terrain(WIDTH, HEIGHT)
    resources = generate_resources(20, WIDTH, HEIGHT, obstacles, rng=rng)
    robots    = [Robot(rng.randint(80, WIDTH - 80),
                       rng.randint(80, HEIGHT - 80)) for _ in range(12)]
    tracker   = MetricsTracker(len(resources))
    return memory, obstacles, resources, robots, tracker
 
 

state    = "menu"
strategy = None
memory = obstacles = resources = robots = tracker = None
show_heat = show_trail = show_range = False
 
running = True
while running:
    mx, my = pygame.mouse.get_pos()
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
 
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
 
            if state == "menu":
                pick = {pygame.K_1: "boids", pygame.K_2: "random",
                        pygame.K_3: "hive"}.get(event.key)
                if pick:
                    strategy = pick
                    memory, obstacles, resources, robots, tracker = build_world()
                    state = "sim"
            else:
                if event.key == pygame.K_h: show_heat  = not show_heat
                if event.key == pygame.K_t: show_trail = not show_trail
                if event.key == pygame.K_r: show_range = not show_range
 
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if state == "menu":
                for i, r in enumerate(BTNS):
                    if r.collidepoint(mx, my):
                        strategy = OPTIONS[i][0]
                        memory, obstacles, resources, robots, tracker = build_world()
                        state = "sim"
                        break
 
    #  Render 
    if state == "menu":
        draw_menu(mx, my)
 
    elif state == "sim":
        screen.fill((10, 12, 22))
        draw_environment(screen, obstacles, resources)
 
        if show_heat:
            draw_heatmap(screen, memory)
 
        for robot in robots:
            if strategy == "boids":
                boids(robot, robots)
            elif strategy == "random":
                random_walk(robot)
            elif strategy == "hive":
                hive_swarm(robot, robots, memory)
            separation(robot, robots)
            robot.update(WIDTH, HEIGHT, obstacles, resources, memory)
            robot.draw(screen, show_trail=show_trail, show_range=show_range)
 
        tracker.tick(resources, memory)
        found   = count_found(resources)
        cov     = memory.coverage() * 100
 
        hud = [
            (f"Strategy : {strategy.upper()}", C_HUD),
            (f"Found    : {found} / {len(resources)}", C_HUD2),
            (f"Coverage : {cov:.1f}%",                 C_HUD2),
            (f"Frame    : {tracker.frame}",             C_HUD2),
            ("",                                        C_HUD2),
            ("[H] heatmap  [T] trails  [R] ranges",     C_GREY),
        ]
        for i, (line, col) in enumerate(hud):
            screen.blit(font_small.render(line, True, col), (10, 10 + i * 18))
 
        if all_found(resources):
            msg = font_big.render(
                f"All survivors found!  ({tracker.frame} frames)", True, (0, 255, 140))
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 14))
 
        pygame.display.flip()
 
    clock.tick(60)
 
#  Exit 
pygame.quit()
if tracker:
    print("\n=== Run Summary ===")
    for k, v in tracker.summary(memory).items():
        print(f"  {k:<20}: {v}")
 