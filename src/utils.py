
import math

class Vector(tuple):
    def __new__(cls, *args):
        return super().__new__(cls, args)

    def __add__(self, other):
        return Vector(*(v+w for v, w in zip(self, other)))

    def __radd__(self, other):
        return Vector(*(w+v for v, w in zip(self, other)))

    def __mul__(self, scalar):
        return Vector(*(scalar * v for v in self))

    def __rmul__(self, scalar):
        return Vector(*(v * scalar for v in self))

    def __sub__(self, other):
        return Vector(*(v-w for v, w in zip(self, other)))

    def __rsub__(self, other):
        return Vector(*(w-v for v, w in zip(self, other)))

    def __truediv__(self, other):
        return Vector(*(v/w for v, w in zip(self, other)))

    def __rtruediv__(self, other):
        return Vector(*(w/v for v, w in zip(self, other)))

    def __pow__(self, scalar):
        return Vector(*(v**scalar for v in self))

    __iadd__ = __add__
    __isub__ = __sub__
    __imul__ = __mul__
    __itruediv__ = __truediv__
    __ipow__ = __pow__


    def magnitude(self):
        ''' returns the length of the vector '''
        return math.sqrt(sum(v**2 for v in self))

    def normalize(self):
        ''' returns a new Vector with a total magnitude of 1
            Will return the zero vector if it gets a zero vector
        '''
        mag = self.magnitude()
        if not mag:
            return self
        return Vector(*(v/mag for v in self))

    def to_int(self):
        return Vector(*(int(v) for v in self))

    def to_float(self):
        return Vector(*(float(v) for v in self))

class Rect():
    ''' defines a rectangular shape. '''
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def __str__(self):
        return "Rect ({}, {}) ({}, {})".format(self.x1, self.y1, self.x2, self.y2)

    def intersects(self, other):
        ''' returns true if two rectangles intersect'''
        return (self.x1 <= other.x2 and
                other.x1 <= self.x2 and
                self.y1 <= other.y2 and
                other.y1 <= self.y2)

    def contains(self, other):
        ''' returns true if other is completely inside self. '''
        return (self.x1 <= other.x1 and
                self.x2 >= other.x2 and
                self.y1 <= other.y1 and
                self.y2 >= other.y2)

    def get_center(self):
        return (self.x1 + (self.x2 - self.x1) // 2,
                self.y1 + (self.y2 - self.y1) // 2)

