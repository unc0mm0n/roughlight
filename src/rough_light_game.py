from . import utils
from . import objects

START = (0, 0)
STARTING_LIFE = 10

WHITE = (255, 255, 255)

class RoughLightGame:

    def __init__(self, game_map, width, height, **kwargs):

        self.map = game_map
        self.width = width
        self.height = height

        self.objects = kwargs.get('objects', list())
        self.start = kwargs.get('start', utils.Vector(0, 0))

        # player initialization
        self.player = kwargs.get('player', None)
        if not self.player:
            self.player = objects.Player(self.start, b'@', WHITE,
                                         self.map, STARTING_LIFE, fov=20)

        self.objects.append(self.player)

        # Add room lables to map
        count = 0
        for room in self.map.rooms:
            label = objects.Object(room.get_center(), chr(ord('a')+count), WHITE, True, False)
            self.objects.append(label)
            count += 1

    def is_blocked(self, location):
        if self.map[location].blocks:
            return True

        return any(object.location == location and object.blocks for object in self.objects)


    def visible_objects(self):
        res = []
        for object in self.objects:
            if object.visible and object.location in self.player.seen:
                if self.map.in_area(self.width, self.height, object.location, self.player.location):
                    res.append(object)
        return reversed(res)
                

    def move_player(self, direction):
        if not self.is_blocked(self.player.location + direction):
            self.player.move(direction)

    def is_blocked(self, location):
        if self.map[location].blocks:
            return True

        return any(object.blocks and object.location == location for object in self.objects)

    def get_area(self, width, height):
        # Get the current area the player is in based on desired size and players location
        return self.map.get_area(width, height, self.player.location)


