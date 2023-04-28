import pygame
import pygame.locals as pl
import pygame_textinput
from kjy import qwerty


pygame.init()

# No arguments needed to get started
textinput = pygame_textinput.TextInputVisualizer()

# But more customization possible: Pass your own font object

screen = pygame.display.set_mode((1000, 200))
clock = pygame.time.Clock()

# Pygame now allows natively to enable key repeat:
pygame.key.set_repeat(200, 25)

while True:
    screen.fill((225, 225, 225))

    events = pygame.event.get()

    # Feed it with events every frame
    textinput.update(events)


    # Get its surface to blit onto the screen
    screen.blit(textinput.surface, (10, 10))


    # Check if user is exiting or pressed return
    for event in events:
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            print(f"User pressed enter! Input so far: {textinput.value}")

    pygame.display.update()
    clock.tick(30)


