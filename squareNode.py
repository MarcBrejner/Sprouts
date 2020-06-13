import pygame
WHITE = (255, 255, 255)
counter = 0
 
class SquareNode(pygame.sprite.Sprite):
    #This class represents a car. It derives from the "Sprite" class in Pygame.

    def __init__(self, color, width, height,x,y,cnt,label):
        # Call the parent class (Sprite) constructor
        super().__init__()
        
        # Pass in the color of the car, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.counter = cnt
        self.width = width
        self.height = height
        self.label = label
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.radius = 10
 
        # Draw the car (a rectangle!)
        #pygame.draw.rect(self.image, color, [0, 0, width, height])
        

        pygame.draw.circle(self.image, color, (self.width//2, self.height//2), self.radius)
        
        # Instead we could load a proper pciture of a car...
        # self.image = pygame.image.load("car.png").convert_alpha()
 
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def filll(self,color):
        self.image.fill(color)

    def incrementCounter(self):
        self.counter += 1;

    def getCounter(self):
        return self.counter

    def getCoordinates(self):
        return (self.rect.centerx, self.rect.centery)

    def isFull(self):
        if (self.counter >= 3):
            return True
        else:
            return False
    