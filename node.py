import pygame
WHITE = (255, 255, 255)
counter = 0
 
class Node(pygame.sprite.Sprite):
    #This class represents a node, and derives from the sprite class of pygame.

    def __init__(self, color, width, height,x,y,cnt,label):
        # Call the parent class (Sprite) constructor
        super().__init__()
        
        #Set fields
        self.counter = cnt #Degree of the node
        self.width = width #Width of the rect that the circle is placed on
        self.height = height # Height -- || --
        self.label = label #Label, ie. node-number
        self.image = pygame.Surface([width, height]) #The surface that the node is placed on
        self.image.fill(WHITE) #transparent
        self.image.set_colorkey(WHITE)
        self.radius = 7 #Radius of the circle representing the node
        
        #Drawing the circle that represents the node
        pygame.draw.circle(self.image, color, (self.width//2, self.height//2), self.radius)
         
        # Fetch the rectangle object that the node is placed on
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def filll(self,color): #Change the color, not currently in use
        self.image.fill(color)

    def incrementCounter(self): #Increment the counter, used whenever a new line connected to the node is accepted
        self.counter += 1;

    def getCounter(self): #Get current degree of the node
        return self.counter

    def getCoordinates(self): #Get the coordinates of the point that the node represents.
        return (self.rect.centerx, self.rect.centery)

    def isFull(self): #Returns a boolean representing whether or not the node is full.
        if (self.counter >= 3):
            return True
        else:
            return False
    