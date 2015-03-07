import libtcodpy as libtcod
import src.objects
import src.map
import src.utils as utils

SCREEN_WIDTH = 100
SCREEN_HEIGHT = 56
LIMIT_FPS = 30

COLOR_DARK_WALL = libtcod.Color(0, 0, 30)
COLOR_DARK_GROUND = libtcod.Color(20, 20, 80)

SAMPLE_MAP = src.map.Map({
    (10, 10): src.map.Tile(libtcod.yellow, True),
    (8, 4): src.map.Tile(COLOR_DARK_WALL, True),
    (8, 5): src.map.Tile(COLOR_DARK_WALL, True),
    (8, 6): src.map.Tile(COLOR_DARK_WALL, True),
    (8, 7): src.map.Tile(COLOR_DARK_WALL, True),
    (8, 8): src.map.Tile(COLOR_DARK_WALL, True),
    (8, 9): src.map.Tile(COLOR_DARK_WALL, True),
    (8, 10): src.map.Tile(COLOR_DARK_WALL, True)
}, src.map.Tile(COLOR_DARK_GROUND, False))

FONT = b'arial8x8.png'
TITLE = b'Rough Light'

KEY_MOVEMENT_VECTORS = {
    libtcod.KEY_UP: utils.Vector(0, 1),
    libtcod.KEY_DOWN: utils.Vector(0, -1),
    libtcod.KEY_LEFT: utils.Vector(-1, 0),
    libtcod.KEY_RIGHT: utils.Vector(1, 0),
}

class Game:

    def __init__(self, game_map=SAMPLE_MAP, width=SCREEN_WIDTH, height=SCREEN_HEIGHT):

        # Window parameters, width and height are counted in characters
        self.width = width
        self.height = height
        self.close_game = False

        self.objects = []
        self.map = game_map

        # Add room lables to map
        count = 0
        for room in self.map.rooms:
            label = src.objects.Object(room.get_center(), chr(ord('a')+count), libtcod.white, False)
            print(label)
            self.objects.append(label)
            count += 1

        # libtcod initialization
        libtcod.console_set_custom_font(FONT,
            libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_TCOD)

        libtcod.console_init_root(self.width, self.height, TITLE, False)
        libtcod.sys_set_fps(LIMIT_FPS)

        # player initialization
        self.player = src.objects.Player(utils.Vector(50, 28), b'@', libtcod.white, self.map)
        self.objects.append(self.player)

        npc = src.objects.Object(utils.Vector(30, 28), b'@', libtcod.red, True)
        self.objects.append(npc)

    def run(self):
        # Game loop
        while not (libtcod.console_is_window_closed() or self.close_game):
            self.step()
            self.draw()
      
    def step(self):
        # Advances the game 1 frame
        self.handle_keys()

    def draw(self):

        # Get the current area the player is in based on own size and players location
        area = self.map.get_area(self.width, self.height, self.player.location)

        # And draw it
        for x, row in enumerate(area):
            for y, tile in enumerate(row):
                libtcod.console_set_char_background(0, x, y, tile.color, libtcod.BKGND_SET)



        # Draw all objects in given area
        drawn = []
        for object in self.objects:
            if object.visible:
                if (self.map.in_area(self.width, self.height, object.location, self.player.location)):
                    self.draw_object(object)
                    drawn.append(object)

        libtcod.console_flush()

        for object in drawn:
                self.clear_object(object)


    def draw_object(self, object, console=0):
        # Draw given object on given console
        x, y = self.convert_location(object.location)

        libtcod.console_set_default_foreground(console, object.color)
        libtcod.console_put_char(console, x, y, object.symbol, libtcod.BKGND_NONE)

    def clear_object(self, object, console=0):
        # Clear the state for the next frame
        x, y = self.convert_location(object.location)
        libtcod.console_put_char(console, x, y, ' ', libtcod.BKGND_NONE)

    def convert_location(self, location):
        ''' converts a cartasian coordinate into a coordinate to display on screen
            screen coordinates go from 0 to width and 0 to height
        '''
        return utils.Vector(location[0] % self.width, (-location[1] - 1) % self.height)

    def handle_keys(self):

        for key in KEY_MOVEMENT_VECTORS:
            if libtcod.console_is_key_pressed(key):
                self.player.move(KEY_MOVEMENT_VECTORS[key])


        key = libtcod.console_check_for_keypress()
        if key.vk == libtcod.KEY_ENTER and key.lalt:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        elif key.vk == libtcod.KEY_ESCAPE:
            self.close_game = True
                

if __name__ == '__main__':
    area = utils.Rect(-100, -100, 200, 200)
    default = src.map.Tile(COLOR_DARK_WALL, True)
    walkable = src.map.Tile(COLOR_DARK_GROUND, False)
    game_map = src.map.Map(default=default)

    #game_map.set_rect(src.utils.Rect(30, 14, 21, 28), walkable)
    #game_map.set_rect(src.utils.Rect(50, 24, 200, 8), walkable)

    #game_map.set_connection((0, 0), (50,28), 3, walkable)

    game_map = src.map.Map.Random(area, 26, 10, 10, utils.Vector(50, 28), default, walkable)
    #print(list(str(room) for room in game_map.rooms))
    game = Game(game_map);
    game.run()