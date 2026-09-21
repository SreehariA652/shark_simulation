import pygame
import math
import random

pygame.init()

width, height = 1100, 800

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Shark simulation")

#fish's position
fish = []

for i in range(50):
    fish.append({
        "x": random.randint(50, width - 50),
        "y": random.randint(50, height - 50),
        "speed": 0.5,
        "angle": random.uniform(0, 2 * math.pi)
    })

def draw_fish(screen, x, y, angle):
    fish_surface = pygame.Surface((40, 24), pygame.SRCALPHA)

    # Fish body
    body = pygame.Rect(5, 3, 10, 6)
    pygame.draw.ellipse(fish_surface, (255, 200, 50), body)

    # Fish tail
    tail = [
        (5, 6),
        (0, 3),
        (0, 9)
    ]
    pygame.draw.polygon(fish_surface, (255, 170, 40), tail)

    # Rotate the fish
    rotated_fish = pygame.transform.rotate(
        fish_surface,
        -math.degrees(angle)
    )

    # Put the rotated fish at its position
    fish_rect = rotated_fish.get_rect(center=(x, y))
    screen.blit(rotated_fish, fish_rect)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # fish_x += 0.5 # Move the fish to the right by 0.5 pixels (since it is a loop, it will keep moving to the right)
    # Change the fish's direction slightly
    for f in fish:
        f["angle"] += random.uniform(-0.03, 0.03)

        f["x"] += math.cos(f["angle"]) * f["speed"]
        f["y"] += math.sin(f["angle"]) * f["speed"]

        if f["x"] <= 15 or f["x"] >= width - 15:
            f["angle"] = math.pi - f["angle"]

        if f["y"] <= 15 or f["y"] >= height - 15:
            f["angle"] = -f["angle"]

    screen.fill((30, 150, 255)) # Fill the screen with a blue color

    for f in fish:
        draw_fish(screen, f["x"], f["y"], f["angle"])
    pygame.display.flip()
pygame.quit()