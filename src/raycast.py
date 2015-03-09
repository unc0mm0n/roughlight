import math
from functools import lru_cache

CIRCLE = 2 * math.pi

def cast_rays(player, map, max_distance):
        
        ''' "Casts" rays and returns the visited integer cartasian coordinates
        Rays are calculated at a 360 degree angle, where an angle of 0 is facing down.'''

        step_size = CIRCLE / (max_distance**2 * 3)
        seen = list()
        # Calculate starting angle based on player's facing direction and FOV
        angle = 0

        while angle < CIRCLE:
            # Get the distance from the wall at given angle
            seen += cast_ray(player.location, angle, map, max_distance)
            # Fix the bobeye effect based on the player's angle and append it.

            # Advance the angle one tick.
            angle += step_size

        return seen

def cast_ray(start, angle, map, max_distance):
        ''' Cast an individual ray from start position at given angle.
            Return a list of all cells visited (integer coordinates on a cartesian grid).
            Each object inside util.Map is expected to have a block_sight boolean argument.
            Empty tiles (equal to None) are blocking'''

        x, y = start
        x += 0.5
        y += 0.5

        step_size = 1

        x_step = math.sin(angle) * step_size
        y_step = math.cos(angle) * step_size

        seen = []

        for _ in range(int(max_distance / step_size)):

            seen.append((int(x), int(y)))
            tile = map[int(x), int(y)]
            
            if tile.block_sight:
                return seen

            x = x + x_step
            y = y + y_step
        # Return seen locations
        return seen