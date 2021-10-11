import pygame
from Configuration import *

pygame.display.set_caption("Plot The Graph")
screen = pygame.display.set_mode(SCREENSIZE, pygame.RESIZABLE)


def run():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()


if __name__ == '__main__':
    run()
