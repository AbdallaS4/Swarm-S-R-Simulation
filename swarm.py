import random
import math
 
 
def _neighbours(robot, robots, radius=120):
    return [r for r in robots
            if r is not robot and math.hypot(robot.x - r.x, robot.y - r.y) < radius]
 
 

 
def random_walk(robot):
    """Stochastic perturbation — baseline strategy."""
    robot.vx += random.uniform(-0.4, 0.4)
    robot.vy += random.uniform(-0.4, 0.4)
 
 
def separation(robot, robots, min_dist=25):
    """Collision avoidance — applied on top of every strategy."""
    for other in robots:
        if other is robot:
            continue
        d = math.hypot(robot.x - other.x, robot.y - other.y)
        if 0 < d < min_dist:
            robot.vx += (robot.x - other.x) / d * 1.2
            robot.vy += (robot.y - other.y) / d * 1.2
 
 
def boids(robot, robots):
    """
    Reynolds (1987): cohesion + alignment within local neighbourhood.
    Separation is handled separately by separation().
    """
    nb = _neighbours(robot, robots)
    if nb:
       
        cx = sum(r.x for r in nb) / len(nb)
        cy = sum(r.y for r in nb) / len(nb)
        robot.vx += (cx - robot.x) * 0.003
        robot.vy += (cy - robot.y) * 0.003
        # Alignment — match average heading
        robot.vx += (sum(r.vx for r in nb) / len(nb) - robot.vx) * 0.05
        robot.vy += (sum(r.vy for r in nb) / len(nb) - robot.vy) * 0.05
    else:
        random_walk(robot)
 
 
def hive_swarm(robot, robots, memory):
    """
    Frontier-based coordination (Yamauchi 1998).
    Robot steers toward nearest unexplored cell 70 % of the time.
    """
    if random.random() < 0.3:
        random_walk(robot)
        return
 
    frontiers = memory.get_frontiers()
    if not frontiers:
        random_walk(robot)
        return
 
    tx, ty = min(frontiers, key=lambda f: math.hypot(f[0] - robot.x, f[1] - robot.y))
    dx = tx - robot.x
    dy = ty - robot.y
    dist = math.hypot(dx, dy) or 1.0
    robot.vx += dx / dist * 0.15
    robot.vy += dy / dist * 0.15
 