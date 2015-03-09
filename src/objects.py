from collections import defaultdict

try:
    from . import raycast as rc
except:
    import raycast as rc

class Object:
    def __init__(self, location, symbol, color, visible, blocks=True):
        self.location = location
        self.symbol = symbol
        self.color = color
        self.visible = visible
        self.blocks = blocks

    def move(self, velocity):
        # moves the object according to given velocity
        self.location += velocity

    def __str__(self):
        return "Object: {} {} {} {}".format(self.location, self.symbol, self.color, self.visible, self.map)

class Creature(Object):
    def __init__(self, location, symbol, color, life, **kwargs):
        super().__init__(location, symbol, color, True, True)
        self.life = life

        self.immortal = kwargs.get("immortal", False)

    def is_dead(self):
        return not self.immortal and life <= 0

class Player(Creature):

    '''
        The playable player object
    '''
    def __init__(self, location, symbol, color, game_map, life, **kwargs):
        super().__init__(location, symbol, color, life)
        
        self.explored = set()
        self.map = game_map

        self.fov = kwargs.get("fov", 100)

        self.update_fov()


    def move(self, velocity):
        super().move(velocity)
        
        self.update_fov()

    def update_fov(self):

        self.explored.add(self.location)
        visible = rc.cast_rays(self, self.map, self.fov)

        self.seen = set(visible)
        self.explored = self.explored.union(set(visible))


    
