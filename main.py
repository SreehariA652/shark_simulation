import pygame
import math
import random

pygame.init()


width, height = 1100, 800

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Shark simulation")

shark_image = pygame.image.load("shark.png").convert_alpha() # find the image and load it and keep the transparency of the image
shark_image = pygame.transform.scale(shark_image, (200, 200))


#fish's position
fish = []

for i in range(100):
    fish.append({
        "x": random.randint(50, width - 50),
        "y": random.randint(50, height - 50),
        "speed": random.uniform(0.1, 0.5),
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

    return rotated_fish, fish_rect

shark_x = width / 2
shark_y = height / 2 #so the shark alwasy starts in the middle of the screen

shark_rect = shark_image.get_rect(center=(shark_x, shark_y))
shark_mask = pygame.mask.from_surface(shark_image) # makes the transparent parts 0 and visible parts 1, so we can use it to check for collisions with the fish

screen.blit(shark_image, shark_rect)



running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # fish_x += 0.5 # Move the fish to the right by 0.5 pixels (since it is a loop, it will keep moving to the right)
    # Change the fish's direction slightly
    
    dead_fish = []

    for f in fish:

        neighbour_count = 0
        neighbour_dx = 0
        neighbour_dy = 0
        seperation_dx = 0
        seperation_dy = 0

        f["angle"] += random.uniform(-0.03, 0.03)

        f["x"] += math.cos(f["angle"]) * f["speed"]
        f["y"] += math.sin(f["angle"]) * f["speed"]

        if f["x"] <= 15 or f["x"] >= width - 15:
            f["angle"] = math.pi - f["angle"]

        if f["y"] <= 15 or f["y"] >= height - 15:
            f["angle"] = -f["angle"]

        for other in fish: # f is the current fish, other is the other fishes in the list
            if other is not f: # can also use != to check if they are not the same fish
                distance = math.sqrt(
                    (f["x"] - other["x"]) ** 2 + (f["y"] - other["y"]) ** 2 # basically calculates the straight line distance between the two fishes using the Pythagorean theorem
                )
                if distance < 50: # if the distance between the two fishes is less than 50 pixels, then treat it like a neighbout
                    neighbour_count += 1
                    neighbour_dx += math.cos(other["angle"])
                    neighbour_dy += math.sin(other["angle"]) #for each neighbour, we add their x and y components of their direction to the total x and y components of the neighbours' directions

                    seperation_dx += f["x"] - other["x"]
                    seperation_dy += f["y"] - other["y"]

        if neighbour_count > 0:
            average_dx = neighbour_dx / neighbour_count
            average_dy = neighbour_dy / neighbour_count

            target_angle = math.atan2(average_dy, average_dx) #caluculates the general angle the fishes are going 
            angle_difference = (target_angle - f["angle"] + math.pi) % (2 * math.pi) - math.pi # calculates the shortest way to turn towards the neighbours
            f["angle"] += angle_difference * 0.01 # oly turn a small amount towards the way(0.05 = 5%)

            if seperation_dx != 0 or seperation_dy != 0:
                seperation_angle = math.atan2(seperation_dy, seperation_dx)

                angle_difference = (seperation_angle - f["angle"] + math.pi) % (2 * math.pi) - math.pi
                f["angle"] += angle_difference * 0.004


    for f in dead_fish:
        fish.remove(f)

    screen.fill((30, 150, 255)) # Fill the screen with a blue color

    for f in fish:
        rotated_fish, fish_rect = draw_fish(
            screen,
            f["x"],
            f["y"],
            f["angle"]
        )

        fish_mask = pygame.mask.from_surface(rotated_fish)

        offset = (
            fish_rect.left - shark_rect.left,
            fish_rect.top - shark_rect.top
        )

        if shark_mask.overlap(fish_mask, offset):
            # Fish has touched the shark
            dead_fish.append(f) 

    screen.blit(shark_image, shark_rect) # Draw the shark image on the screen at its current position
        
    pygame.display.flip()
pygame.quit()