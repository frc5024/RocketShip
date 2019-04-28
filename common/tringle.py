import math

class Tringle:
    def __init__(self, distance, angle):
        self.h = distance
        self.a = math.cos(angle) * self.h
        self.o = math.sin(angle) * self.h