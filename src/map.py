import math
import random
from . import utils

class Tile:
    ''' A tile object holding the properties of a single tile
        as well as any Events that might occur in it
    '''

    def __init__(self, color, blocked, block_sight=None, events=None):
        self.color = color
        self.blocked = blocked

        if not block_sight:
            self.block_sight = blocked

        self.events = events

    def shallow_copy(self):
        return Tile(self.color, self.blocked, self.block_sight, self.events)


class Map:

    ''' A map object to handle the game world and player position
        Keeps track of the world in a dictionary of Vector locations,
        the value of each location should be a tile object.
    '''

    def __init__(self, initial_grid={}, rooms=[], default=None):
        self.grid = initial_grid
        self.rooms = rooms

        self.default = default

    def __getitem__(self, key):
        try:
            return self.grid[key]
        except KeyError:
            return self.default

    def __setitem__(self, key, value):
        self.grid[key] = value

    def __str__(self):
        return "Map object \nDefault: {0} \nGrid: {1}".format(self.default, self.grid)

    def in_area(self, width, height, location1, location2):
        ''' returns true if location1 and location2 are within the same offset of width and height '''
        if (width == 0 or height == 0):
            raise ValueError('width and height must not be 0')

        x1 = math.floor(location1[0]/width) * width
        y1 = math.floor(location1[1]/height) * height
        
        x2 = math.floor(location2[0]/width) * width
        y2 = math.floor(location2[1]/height) * height

        return x1 == x2 and y1 == y2

    def get_area(self, width, height, location):
        ''' Returns the area of given size that location is in as a 2 dimensional list
            Treating point (0, 0) as the bottom left corner of an area.
        '''
        if (width == 0 or height == 0):
            raise ValueError('width and height must not be 0')

        x_offset = math.floor(location[0]/width) * width
        y_offset = math.floor(location[1]/height) * height

        return [[self[x + x_offset, height - y + y_offset - 1] for y in range(height)] for x in range(width)]

    def set_rect(self, rect, tile, is_room=False):
        ''' sets a rectangular area of dimensions w*h, with the buttom left corner at
            corner_x, corner_y, as shallow copies of given tile. '''
        for x in range(rect.x1, rect.x2):
            for y in range(rect.y1, rect.y2):
                self[x, y] = tile.shallow_copy()

        if is_room:
            self.rooms.append(rect)

    def set_connection(self, location1, location2, width, tile):
        ''' creates a connection from location 1 to location 2 at given width
            by creating a rectangle horizontally and then vertically
        '''

        # get the rightmost x location
        start_x = min(location1[0], location2[0]) - width // 2
        # get the bottom y location
        start_y = min(location1[1], location2[1])

        # create a rect from right x location to left x location with given width.
        # half the width is added to each side of the rect to compensate for the offset of the vertical rect
        rect_h = utils.Rect(start_x, location1[1] - width // 2, abs(location1[0]-location2[0]) + width, width)

        # create a rect from bottom y location to top y with given width.
        rect_v = utils.Rect(location2[0] - width // 2, start_y, width, abs(location1[1]-location2[1]))

        # draw the rects
        self.set_rect(rect_h, tile)
        self.set_rect(rect_v, tile)

    @classmethod
    def Random(cls, area_rect, room_number, min_room_size, max_room_size, center, default, room_tile, timeout=1000):
        ''' generate a random map inside area_rect, WARNING: Will enter an infinite loop if not given enough space in area_rect. '''

        map = cls(default=default)

        room_timeout = timeout

        # Generate center room around the player
        w = max_room_size
        h = max_room_size
        center_room = utils.Rect(center[0] - w // 2, center[1] - h // 2, w, h)
        map.set_rect(center_room, room_tile, True)

        last_center = center

        # until we get to the required number of rooms
        while len(map.rooms) < room_number:

            # generate a random rect
            w = random.randrange(min_room_size, max_room_size + 1)
            h = random.randrange(min_room_size, max_room_size + 1)

            x = random.randrange(area_rect.x1, area_rect.x2)
            y = random.randrange(area_rect.y1, area_rect.y2)

            room = utils.Rect(x, y, w, h)

            # If it doesn't intersect with any other rect
            intersects = False

            if not area_rect.contains(room):
                intersects = True
            
            else:
                for other_room in map.rooms:
                    if room.intersects(other_room):
                        intersects = True

            if intersects:
                room_timeout -= 1
                if not room_timeout:
                    print("Error: room failing exceeded, generation stopped")
                    break
                continue

            # add the room to the map
            map.set_rect(room, room_tile, True)

            # add a path from the center of the previous room to the center of the room
            center = (x + w // 2, y + h // 2)
            tunnel_w = random.randrange(2, 2 + w // 4)
            map.set_connection(last_center, center, tunnel_w, room_tile)
            # remember the center of the new room
            last_center = center
            # reset room timeout
            room_timeout = timeout

        return map

if __name__ == '__main__':

    def pprint(arr):
        for row in arr:
            for col in row:
                print(col, end='')
            print()

    sample = {(1, 1): 'a', (2, 2): 'b', (1, 2): 'c', (3, 3): 'd'}
    a = Map(sample, '.')
    pprint(a.get_area(2, 2, (1, 2)))
    pprint(a.get_area(2, 2, (2, 2)))
    pprint(a.get_area(2, 2, (1, 1)))
    pprint(a.get_area(2, 2, (2, 1)))

    pprint(a.get_area(3, 3, (0, 0)))
    pprint(a.get_area(3, 3, (3, 3)))

    print(a)

