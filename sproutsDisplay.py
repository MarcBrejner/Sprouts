import pygame

class SproutsDisplay:
    GREEN = (20, 255, 140)
    GREY = (210, 210 ,210)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    PURPLE = (255, 0, 255)

    def __init__(self, screenwidth, screenheight,pygame):
        size = (screenwidth, screenheight)
        self.size = size
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Sprouts")
        self.screen.fill(SproutsDisplay.GREEN)

    def updateScreen(self,pygame):
        pygame.display.flip()
