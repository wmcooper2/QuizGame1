import math
import util
import pyglet
from pyglet.window import key

#setup resource dirs
resource_dir = "./resources"
pyglet.resource.path = [resource_dir]
pyglet.resource.reindex()

class Background(pyglet.sprite.Sprite):

    background_img = pyglet.resource.image("quiz1.png")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Player(pyglet.sprite.Sprite):

    randomized = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keys = dict(left=False, right=False, up=False, down=False)
        self.key_handler = key.KeyStateHandler()
        self.spot = self.x #point it is spawned (off screen r)        
        self.has_spot = False
        self.speed = 3
        self.item = "None"


    def update(self, dt):
        self.check_spots()
        print("player = ", self.image)
        print(util.Line.spots)
        print(util.Line.spots_avail)
        self.move_player()

    def move_player(self):
        """Player moves to their assigned spot."""
        if self.x != self.spot:
            if self.x < self.spot:
                self.x += self.speed
            if self.x > self.spot:
                self.x -= self.speed 

    def check_spots(self):
        """Looks for an available spot closest to the upper platform."""
        def spot_available(spot):
            return util.Line.spots_avail[util.Line.spots.index(spot)] 

        def spot_unavailable(spot):
            util.Line.spots_avail[util.Line.spots.index(spot)] = False

        for spot in util.Line.spots:
            if spot_available(spot) and not self.has_spot:
                self.assign_spot(spot)
                self.has_spot = True 
#                util.Line.spots_avail[util.Line.spots.index(spot)] = False   
                spot_unavailable(spot)

    def assign_spot(self, new_spot):
        """Assigns a spot to the players."""
        self.spot = new_spot



class FloatingPlayer(Player):
    
    float_height = 0
    float_deg = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def floating(self):
        """Makes the character float up and down in place.
            Returns None."""
        radians = math.radians(FloatingPlayer.float_deg)
        FloatingPlayer.float_height = math.sin(radians)
        if FloatingPlayer.float_deg == 360:
            FloatingPlayer.float_deg = 0
            FloatingPlayer.float_height = 0
        FloatingPlayer.float_deg += 1
        self.y = self.y + (FloatingPlayer.float_height / 3) 
#        print("float_height = ", FloatingPlayer.float_height)
#        print("float_deg = ", FloatingPlayer.float_deg)

    def update2(self, dt): #changed name from 'update' to not conflict
        self.floating()
        self.y = self.y + (FloatingPlayer.float_height / 3) 
        if self.key_handler[key.LEFT]:
            self.x -= 1
        if self.key_handler[key.RIGHT]:
            self.x += 1
        if self.key_handler[key.UP]:
            self.y += 1
        if self.key_handler[key.DOWN]:
            self.y -= 1
        else:
            pass

class WalkingPlayer(Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def walk(self):
        """Update walking sequence images."""
        print("walking")

class FireLight(FloatingPlayer):
    
    fire_light_img = pyglet.resource.image("fire_light1.png")
    util.center_floating_player(fire_light_img)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
class Dragon(WalkingPlayer):
    
    dragon_img = pyglet.resource.image("dragon_walk1.png")
    util.center_walking_player(dragon_img)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class BigBoo(FloatingPlayer):
    
    big_boo_img = pyglet.resource.image("big_boo1_left.png")
    util.center_floating_player(big_boo_img)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class GreenKoopa(WalkingPlayer):
    
    green_koopa_img = pyglet.resource.image("green_koopa1_left.png")
    util.center_walking_player(green_koopa_img)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class BigMole(WalkingPlayer):
    
    big_mole_img = pyglet.resource.image("big_mole1_left.png")
    util.center_walking_player(big_mole_img)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Mario(WalkingPlayer):

    mario_img = pyglet.resource.image("mario_big_left_1.png")
    util.center_walking_player(mario_img)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

