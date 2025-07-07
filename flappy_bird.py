import pygame
import random
import sys
import os

# Game constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GROUND_HEIGHT = 80
BIRD_X = 50
GRAVITY = 0.25
FLAP_STRENGTH = -6
PIPE_SPEED = 2
PIPE_GAP = 150
PIPE_FREQUENCY = 1500  # milliseconds
BIRD_IMAGE_PATH = os.path.join("assets", "bird.png")
BIRD_SIZE = (34, 24)  # width, height used if sprite is loaded


class Bird:
    def __init__(self, image=None):
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.radius = 15
        self.image = image
        if self.image:
            self.radius = self.image.get_width() // 2

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def rect(self):
        return pygame.Rect(BIRD_X - self.radius, self.y - self.radius,
                           self.radius * 2, self.radius * 2)

    def draw(self, screen):
        if self.image:
            rect = self.image.get_rect(center=(BIRD_X, int(self.y)))
            screen.blit(self.image, rect)
        else:
            pygame.draw.rect(screen, (255, 255, 0), self.rect())


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


def draw_pipe(screen, pipe):
    top_rect = pygame.Rect(pipe.x, 0, 50, pipe.top_height)
    bottom_rect = pygame.Rect(
        pipe.x,
        pipe.top_height + PIPE_GAP,
        50,
        SCREEN_HEIGHT - GROUND_HEIGHT - (pipe.top_height + PIPE_GAP),
    )
    pygame.draw.rect(screen, (0, 255, 0), top_rect)
    pygame.draw.rect(screen, (0, 255, 0), bottom_rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    bird_image = None
    try:
        image = pygame.image.load(BIRD_IMAGE_PATH).convert_alpha()
        bird_image = pygame.transform.smoothscale(image, BIRD_SIZE)
    except pygame.error:
        pass

    bird = Bird(bird_image)
    pipes = []
    score = 0
    last_pipe = pygame.time.get_ticks()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.flap()

        # Spawn pipes
        now = pygame.time.get_ticks()
        if now - last_pipe > PIPE_FREQUENCY:
            pipes.append(Pipe(SCREEN_WIDTH))
            last_pipe = now

        # Update game objects
        bird.update()
        for pipe in list(pipes):
            pipe.update()
            if pipe.offscreen():
                pipes.remove(pipe)
                score += 1
        # Collision detection
        if bird.y > SCREEN_HEIGHT - GROUND_HEIGHT or bird.y < 0:
            running = False
        for pipe in pipes:
            if pipe.collides_with(bird.rect()):
                running = False
                break

        # Drawing
        screen.fill((135, 206, 235))  # sky blue
        for pipe in pipes:
            draw_pipe(screen, pipe)
        bird.draw(screen)
        pygame.draw.rect(screen, (222, 184, 135), (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))
        score_surf = font.render(str(score), True, (0, 0, 0))
        screen.blit(score_surf, (SCREEN_WIDTH // 2, 20))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    print(f"Game over! Your score: {score}")


if __name__ == "__main__":
    main()
