from collections import defaultdict

try:
    from . import raycast as rc
except:
    import raycast as rc

class Object:
    def __init__(self, location, symbol, color, visible, game_map=None):
        self.location = location
        self.symbol = symbol
        self.color = color
        self.visible = visible
        self.map = game_map

    def move(self, velocity):
        # moves the object according to given velocity, if possible by self.map
        if self.map and not self.map[self.location + velocity].blocked:
            self.location += velocity

    def __str__(self):
        return "Object: {} {} {} {}".format(self.location, self.symbol, self.color, self.visible, self.map)



class Player(Object):


    '''
        The playable player object
    '''
    def __init__(self, location, symbol, color, game_map, **kwargs):
        super().__init__(location, symbol, color, True, game_map)
        
        self.explored = set()

        self.fov = kwargs.get("fov", 100)

        self.update_fov()


    def move(self, velocity):
        super().move(velocity)
        
        self.update_fov()

    def update_fov(self):

        self.explored.add(self.location)
        visible = rc.cast_rays(self, self.map, self.fov)

        self.visible = set(visible)
        self.explored = self.explored.union(set(visible))


    
