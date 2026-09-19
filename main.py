import pygame

pygame.init()

width, height = 1000, 700

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Shark simulation")

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 150, 255)) # Fill the screen with a blue color
    pygame.display.flip()
pygame.quit()