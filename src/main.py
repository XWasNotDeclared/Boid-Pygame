import pygame
import random
import math

# Khởi tạo
WIDTH, HEIGHT = 800, 600
NUM_FISH = 30
MAX_SPEED = 4
NEIGHBOR_RADIUS = 50
SEPARATION_DISTANCE = 20

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Fish:
    def __init__(self):
        self.pos = pygame.math.Vector2(random.randint(0, WIDTH), random.randint(0, HEIGHT))
        self.vel = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * MAX_SPEED

    def update(self, fishes):
        alignment = pygame.math.Vector2(0, 0)
        cohesion = pygame.math.Vector2(0, 0)
        separation = pygame.math.Vector2(0, 0)
        total = 0

        for other in fishes:
            if other == self:
                continue
            distance = self.pos.distance_to(other.pos)
            if distance < NEIGHBOR_RADIUS:
                alignment += other.vel
                cohesion += other.pos
                if distance < SEPARATION_DISTANCE:
                    separation -= (other.pos - self.pos)
                total += 1

        if total > 0:
            alignment = (alignment / total).normalize() * MAX_SPEED
            alignment -= self.vel
            cohesion = ((cohesion / total) - self.pos).normalize() * MAX_SPEED
            cohesion -= self.vel

            if separation.length() > 0:  # Kiểm tra độ dài trước khi chuẩn hóa
                separation = separation.normalize() * MAX_SPEED
                separation -= self.vel

        # Trọng số cho từng hành vi
        self.vel += alignment * 0.05 + cohesion * 0.01 + separation * 0.1
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)

        self.pos += self.vel
        self.wrap_around()

    def wrap_around(self):
        if self.pos.x < 0: self.pos.x = WIDTH
        elif self.pos.x > WIDTH: self.pos.x = 0
        if self.pos.y < 0: self.pos.y = HEIGHT
        elif self.pos.y > HEIGHT: self.pos.y = 0

    def draw(self, surface):
        angle = self.vel.angle_to(pygame.math.Vector2(1, 0))
        point1 = self.pos + self.vel.normalize() * 10
        point2 = self.pos + pygame.math.Vector2(-5, 3).rotate(-angle)
        point3 = self.pos + pygame.math.Vector2(-5, -3).rotate(-angle)
        pygame.draw.polygon(surface, (0, 150, 255), [point1, point2, point3])

# Tạo đàn cá
fishes = [Fish() for _ in range(NUM_FISH)]

running = True
while running:
    screen.fill((20, 20, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for fish in fishes:
        fish.update(fishes)
        fish.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
