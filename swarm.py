import math

def separation(robot, robots):
    for other in robots:
        if other != robot:
            dist = math.hypot(robot.x - other.x, robot.y - other.y)
            if dist < 20:
                robot.angle += math.pi / 4