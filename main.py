from xml.etree.ElementTree import tostring
import pygame
import numpy as np
import random

class Ball:
    def __init__(self, position):
        self.pos = np.array(position, dtype=np.float64)
        self.v = np.array([random.randint(-7, 7), random.randint(-7, 7)], dtype=np.float64)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.radius = random.randint(10,30)

        if self.v[0] == 0:
            self.v[0] = 3
        
        if self.v[1] == 0:
            self.v[1] = -3

collisions = 0
def check_ball_collision(ball1, ball2):
    dist = np.linalg.norm(ball1.pos - ball2.pos)
    if dist < ball1.radius + ball2.radius:
        overlap = ball1.radius + ball2.radius - dist
        direction = (ball1.pos - ball2.pos) / dist
        ball1.pos += direction * (overlap / 2)
        ball2.pos -= direction * (overlap / 2)

        v1 = ball1.v - np.dot(ball1.v - ball2.v, direction) * direction
        v2 = ball2.v - np.dot(ball2.v - ball1.v, -direction) * -direction
        ball1.v, ball2.v = v1, v2
        ball1.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        ball2.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        global collisions
        collisions += 1

def rainbow_col(value):
    step = (value // 256) % 6
    pos = value % 256

    if step == 0:
        return (255, pos, 0)
    if step == 1:
        return (255-pos, 255, 0)
    if step == 2:
        return (0, 255, pos)
    if step == 3:
        return (0, 255-pos, 255)
    if step == 4:
        return (pos, 0, 255)
    if step == 5:
        return (255, 0, 255-pos)

pygame.init()
width = 800
height = 800
window = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

pygame.font.init()
my_font = pygame.font.SysFont('Ariel', 48)

black = (0, 0, 0)
white = (255, 255, 255)
circle_center = np.array([width / 2, height / 2], dtype=np.float64)
circle_radius = 350
ball_pos = np.array([width / 2, height / 2 - 120], dtype=np.float64)
balls = [
    Ball(ball_pos), Ball(ball_pos + np.array([100, 0])), Ball(ball_pos + np.array([50, 100])),
    Ball(ball_pos + np.array([-100, 200])), Ball(ball_pos + np.array([-200, 200])), Ball(ball_pos + np.array([-150, 100]))
]
rainbowval = 0
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for i, ball in enumerate(balls):
        ball.pos += ball.v 
        dist = np.linalg.norm(ball.pos - circle_center)
        if dist + ball.radius > circle_radius:
            d = ball.pos - circle_center
            d_unit = d / np.linalg.norm(d)
            ball.pos = circle_center + (circle_radius - ball.radius) * d_unit
            t = np.array([-d[1], d[0]], dtype=np.float64)
            proj_v_t = (np.dot(ball.v, t) / np.dot(t, t)) * t
            ball.v = 2 * proj_v_t - ball.v
            ball.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            collisions += 1
        
        for j in range(i + 1, len(balls)):
            check_ball_collision(ball, balls[j])
    
    currentRGBcol = rainbow_col(rainbowval)

    window.fill(black)
    # triangle 1
    pygame.draw.line(window, white, balls[0].pos, balls[1].pos, 10)
    pygame.draw.line(window, white, balls[1].pos, balls[2].pos, 10)
    pygame.draw.line(window, white, balls[2].pos, balls[0].pos, 10)
    # triangle 2
    pygame.draw.line(window, white, balls[3].pos, balls[4].pos, 10)
    pygame.draw.line(window, white, balls[4].pos, balls[5].pos, 10)
    pygame.draw.line(window, white, balls[5].pos, balls[3].pos, 10)

    for ball in balls:
        pygame.draw.circle(window, ball.color, ball.pos.astype(int), ball.radius)
    
    pygame.draw.circle(window, currentRGBcol, circle_center.astype(int), circle_radius, 5)
    
    text_surface = my_font.render(f'Collisions: {collisions}', False, (255, 255, 255))
    window.blit(text_surface, (0,0))

    pygame.display.flip()
    clock.tick(60)

    rainbowval = (rainbowval + 5) % (256 * 6)

pygame.quit()
