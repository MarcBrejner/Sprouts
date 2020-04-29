class Grid():
    def __init__(self, width, height,default=0):
        self.width = width
        self.height = height
        self.data = [[default for y in range(height)] for x in range(width)]
    
    def set(self, x, y, value):
        self.data[y][x] = value
    
    def get(self, x, y):
        return self.data[y][x]
