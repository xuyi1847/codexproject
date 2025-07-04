import pygame
from pygame.locals import DOUBLEBUF, OPENGL, K_SPACE, QUIT, KEYDOWN
from OpenGL.GL import *
from OpenGL.GLU import *
import random

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GROUND_HEIGHT = 80
BIRD_X = 50
GRAVITY = 0.25
FLAP_STRENGTH = -6
PIPE_SPEED = 2
PIPE_GAP = 150
PIPE_FREQUENCY = 1500  # milliseconds
DEPTH = 20  # thickness of objects for the 3D look


class Bird:
    def __init__(self):
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.radius = 15

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def rect(self):
        return pygame.Rect(BIRD_X - self.radius, self.y - self.radius,
                           self.radius * 2, self.radius * 2)


class Pipe:
    def __init__(self, x):
        self.x = x
        self.top_height = random.randint(50, SCREEN_HEIGHT - GROUND_HEIGHT - PIPE_GAP - 50)

    def update(self):
        self.x -= PIPE_SPEED

    def collides_with(self, rect):
        top_rect = pygame.Rect(self.x, 0, 50, self.top_height)
        bottom_rect = pygame.Rect(
            self.x,
            self.top_height + PIPE_GAP,
            50,
            SCREEN_HEIGHT - GROUND_HEIGHT - (self.top_height + PIPE_GAP),
        )
        return rect.colliderect(top_rect) or rect.colliderect(bottom_rect)

    def offscreen(self):
        return self.x < -50


def draw_box(x, y, width, height, depth, color):
    r, g, b = [c / 255.0 for c in color]
    glColor3f(r, g, b)
    x2 = x + width
    y2 = y + height
    z2 = depth
    glBegin(GL_QUADS)
    # front
    glVertex3f(x, y, 0)
    glVertex3f(x2, y, 0)
    glVertex3f(x2, y2, 0)
    glVertex3f(x, y2, 0)
    # back
    glVertex3f(x, y, z2)
    glVertex3f(x2, y, z2)
    glVertex3f(x2, y2, z2)
    glVertex3f(x, y2, z2)
    # left
    glVertex3f(x, y, 0)
    glVertex3f(x, y, z2)
    glVertex3f(x, y2, z2)
    glVertex3f(x, y2, 0)
    # right
    glVertex3f(x2, y, 0)
    glVertex3f(x2, y, z2)
    glVertex3f(x2, y2, z2)
    glVertex3f(x2, y2, 0)
    # top
    glVertex3f(x, y2, 0)
    glVertex3f(x2, y2, 0)
    glVertex3f(x2, y2, z2)
    glVertex3f(x, y2, z2)
    # bottom
    glVertex3f(x, y, 0)
    glVertex3f(x2, y, 0)
    glVertex3f(x2, y, z2)
    glVertex3f(x, y, z2)
    glEnd()


def draw_pipe(pipe):
    draw_box(pipe.x, 0, 50, pipe.top_height, DEPTH, (0, 255, 0))
    draw_box(
        pipe.x,
        pipe.top_height + PIPE_GAP,
        50,
        SCREEN_HEIGHT - GROUND_HEIGHT - (pipe.top_height + PIPE_GAP),
        DEPTH,
        (0, 255, 0),
    )


def main():
    pygame.init()
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF | OPENGL)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, -100, 100)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0, 0, -50)
    glRotatef(20, 1, 0, 0)  # tilt for perspective

    clock = pygame.time.Clock()

    bird = Bird()
    pipes = []
    score = 0
    last_pipe = pygame.time.get_ticks()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN and event.key == K_SPACE:
                bird.flap()

        now = pygame.time.get_ticks()
        if now - last_pipe > PIPE_FREQUENCY:
            pipes.append(Pipe(SCREEN_WIDTH))
            last_pipe = now

        bird.update()
        for pipe in list(pipes):
            pipe.update()
            if pipe.offscreen():
                pipes.remove(pipe)
                score += 1

        if bird.y > SCREEN_HEIGHT - GROUND_HEIGHT or bird.y < 0:
            running = False
        for pipe in pipes:
            if pipe.collides_with(bird.rect()):
                running = False
                break

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0, 0, -50)
        glRotatef(20, 1, 0, 0)

        for pipe in pipes:
            draw_pipe(pipe)
        draw_box(BIRD_X - bird.radius, bird.y - bird.radius, bird.radius * 2, bird.radius * 2, DEPTH, (255, 255, 0))
        draw_box(0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT, DEPTH, (222, 184, 135))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    print(f"Game over! Your score: {score}")


if __name__ == "__main__":
    main()
