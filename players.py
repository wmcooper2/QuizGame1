#std lib
import math

#3rd party
import pyglet

#custom
import util
from constants import constants as c

#setup image directory
resource_dir = "./resources"
pyglet.resource.path = [resource_dir]
pyglet.resource.reindex()

#convenience variables
IMG = pyglet.resource.image
GRID = pyglet.image.ImageGrid
ANIM = pyglet.image.Animation.from_image_sequence
SPRITE = pyglet.sprite.Sprite

class Background(SPRITE):
    background_img = IMG("quiz1.png")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Player(SPRITE):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.spot = self.x      #initially off screen, changed immediately
        self.delta_x = 0        #intially zero, changed immediately

        #empty list returns false, don't need self.item
        self.item = False

        self.speed = "walk"
        self.moving = False
        self.rotating_players = False
        self.inventory = []
        self.points = 0
        self.point_index = 0

    def update(self, dt):
        self.delta_x = self.x - self.spot
        #TODO, make util.Line.player_spots[-1] into "main_position"
        if c.GAME_JUST_STARTED or self.spot == util.Line.player_spots[-1]:
            self.speed = "run"
#         if self.spot == util.Line.player_spots[-1]: #if the player is in the ready position
#             self.speed = "run"
        self.move()

#     def has_item(self):
#         """Checks if the player has an item in their inventory. Returns None."""
#         if len(self.inventory) == 0:
#             return False
#         elif len(self.inventory) > 0:
#             return True

    def use_item(self):
        """Player uses the item in their inventory. Returns None."""
        self.item = True
        item = self.inventory[0]
        if item.item_not_used == True:
            item.effect()                       
            item.item_not_used = False          #dont need to reset to False, instance is destroyed after use. 

    def game_in_play(self):
        """Sets c.GAME_JUST_STARTED to False. Returns None."""
        c.GAME_JUST_STARTED = False

    def move(self):
        """Moves the player. Returns None."""
        if self.speed == "walk":
            self.walk()
        if self.speed == "run":
            self.run()

    def walk(self):
        """Walks the player left or right.
            Returns None."""
        delta = self.delta_x
        #update sprite image
        if delta != 0 and self.moving == False:
            self.moving = True
            if delta > 0:
                self.image = self.walk_left_anim
            if delta < 0:
                self.image = self.walk_right_anim
        elif delta == 0:
            self.image = self.stand_left_anim 
            self.moving = False
        #move left or right
        if delta > 0:
            self.x -= 1
        if delta < 0:
            self.x += 1

    def run(self):
        """Runs the player left or right.
            Returns None."""
        delta = self.delta_x
        #update sprite image
        if delta != 0 and self.moving == False:
            self.moving = True
            if delta > 0:
                self.image = self.run_left_anim
            if delta < 0:
                self.image = self.run_right_anim
        elif delta == 0:
            self.image = self.stand_left_anim 
            self.moving = False
            self.speed = "walk"
        #move left or right
        if delta > 0 and delta > 3:
            self.x -= 3
        if delta > 0 and delta <= 3:
            self.x -= 1
        if delta < 0 and abs(delta) > 3:
            self.x += 3
        if delta < 0 and abs(delta) <= 3:
            self.x += 1

    def delta_x(self):
        """Get the distance between objects position and spot position.
            Returns Integer."""
        return self.x - self.spot

class FloatingPlayer(Player):
    """Creates a player that floats cyclicly in the air."""    
 
    float_height = 0
    float_deg = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def float(self):
        """Makes the character float up and down in place.
            Returns None."""
        radians = math.radians(FloatingPlayer.float_deg)
        FloatingPlayer.float_height = math.sin(radians)
        if FloatingPlayer.float_deg == 360:
            FloatingPlayer.float_deg = 0
            FloatingPlayer.float_height = 0
        FloatingPlayer.float_deg += 1
        self.y = self.y + (FloatingPlayer.float_height / 3) 

class WalkingPlayer(Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
class Yammy(SPRITE):
    
    stand_right = IMG("yammystandright.png")    
    action_right_img = IMG("yammyactionright.png")
    action_right_seq = GRID(action_right_img, 1, 2)
    action_right_anim = ANIM(action_right_seq, 0.2, False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.disappear = False
        self.disappear_rate = 3
        self.max_opacity = 255
        self.min_opacity = 0

    def update(self) -> None:
        """Yammy's main update loop."""
        self.disappear_animation()

    def toggle_disappear(self) -> None:
        """Toggle self.disappear flag."""
        if self.opacity <= self.min_opacity or self.opacity >= self.max_opacity:
            self.disappear = not self.disappear

    def disappear_animation(self) -> None:
        """Make Yammy disappear/reappear."""
        if self.disappear:
            self.opacity -= self.disappear_rate
        else:
            self.opacity += self.disappear_rate
        if self.opacity >= self.max_opacity:
            self.opacity = self.max_opacity
        elif self.opacity <= self.min_opacity:
            self.opacity = self.min_opacity

    def wave_wand(self) -> None:
        """Yammy waves his magic wand."""
        self.image = self.action_right_anim

class FireLight(FloatingPlayer):
    
    stand_left = IMG("firelightwalkleft.png")
    util.center_floating_player(stand_left)
    stand_left_seq = GRID(stand_left, 1, 2)
    stand_left_anim = ANIM(stand_left_seq, 0.1, True) 
    walk_right = IMG("firelightwalkright.png")
    walk_right_seq = GRID(walk_right, 1, 2)
    walk_right_anim = ANIM(walk_right_seq, 0.1, True)
    walk_left = IMG("firelightwalkleft.png")
    walk_left_seq = GRID(walk_left, 1, 2)
    walk_left_anim = ANIM(walk_left_seq, 0.1, True)
    run_right_anim = ANIM(walk_right_seq, 0.05, True)
    run_left_anim = ANIM(walk_left_seq, 0.05, True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Dragon(WalkingPlayer):
    
    stand_left = IMG("dragonstandleft.png")
    util.center_walking_player(stand_left)
    stand_left_seq = GRID(stand_left, 1, 1)
    stand_left_anim = ANIM(stand_left_seq, 1, True) 
    walk_right = IMG("dragonwalkright.png")
    walk_right_seq = GRID(walk_right, 1, 2)
    walk_right_anim = ANIM(walk_right_seq, 0.1, True)
    walk_left = IMG("dragonwalkleft.png")
    walk_left_seq = GRID(walk_left, 1, 2)
    walk_left_anim = ANIM(walk_left_seq, 0.1, True)
    run_right_anim = ANIM(walk_right_seq, 0.05, True)
    run_left_anim = ANIM(walk_left_seq, 0.05, True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class BigBoo(FloatingPlayer):
    
    stand_left = IMG("bigboostandleft.png")
    util.center_floating_player(stand_left)
    stand_left_seq = GRID(stand_left, 1, 1)
    stand_left_anim = ANIM(stand_left_seq, 1, True) 
    walk_right = IMG("bigboowalkright.png")
    walk_right_seq = GRID(walk_right, 1, 1)
    walk_right_anim = ANIM(walk_right_seq, 0.1, True)
    walk_left = IMG("bigboowalkleft.png")
    walk_left_seq = GRID(walk_left, 1, 1)
    walk_left_anim = ANIM(walk_left_seq, 0.1, True)
    run_right_anim = ANIM(walk_right_seq, 0.05, True)
    run_left_anim = ANIM(walk_left_seq, 0.05, True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class GreenKoopa(WalkingPlayer):
    
    stand_left = IMG("greenkoopastandleft.png")
    util.center_walking_player(stand_left)
    stand_left_seq = GRID(stand_left, 1, 1)
    stand_left_anim = ANIM(stand_left_seq, 1, True) 
    walk_right = IMG("greenkoopawalkright.png")
    walk_right_seq = GRID(walk_right, 1, 2)
    walk_right_anim = ANIM(walk_right_seq, 0.1, True)
    walk_left = IMG("greenkoopawalkleft.png")
    walk_left_seq = GRID(walk_left, 1, 2)
    walk_left_anim = ANIM(walk_left_seq, 0.1, True)
    run_right_anim = ANIM(walk_right_seq, 0.05, True)
    run_left_anim = ANIM(walk_left_seq, 0.05, True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class BigMole(WalkingPlayer):
    
    stand_left = IMG("bigmolestandleft.png")
    util.center_walking_player(stand_left)
    stand_left_seq = GRID(stand_left, 1,1)
    stand_left_anim = ANIM(stand_left_seq, 1, True) 
    walk_right = IMG("bigmolewalkright.png")
    walk_right_seq = GRID(walk_right, 1, 2)
    walk_right_anim = ANIM(walk_right_seq, 0.1, True)
    walk_left = IMG("bigmolewalkleft.png")
    walk_left_seq = GRID(walk_left, 1, 2)
    walk_left_anim = ANIM(walk_left_seq, 0.1, True)
    run_right_anim = ANIM(walk_right_seq, 0.05, True)
    run_left_anim = ANIM(walk_left_seq, 0.05, True)
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Mario(WalkingPlayer):

    stand_left = IMG("bigmariostandleft.png")
    util.center_walking_player(stand_left)
    stand_left_seq = GRID(stand_left, 1,1)
    stand_left_anim = ANIM(stand_left_seq, 1, True)
    walk_right_img = IMG("bigmariowalkright.png")
    walk_right_seq = GRID(walk_right_img, 1, 3)
    walk_right_anim = ANIM(walk_right_seq, 0.1, True)
    walk_left_img = IMG("bigmariowalkleft.png")
    walk_left_seq = GRID(walk_left_img, 1, 3)
    walk_left_anim = ANIM(walk_left_seq, 0.1, True)
    run_right_anim = ANIM(walk_right_seq, 0.05, True)
    run_left_anim = ANIM(walk_left_seq, 0.05, True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Luigi(WalkingPlayer):
    
#     stand_left = IMG("bigluigistandleft.png")
    stand_left = IMG("bigluigistandleft.png")
    util.center_walking_player(stand_left)
    stand_left_seq = GRID(stand_left, 1,1)
    stand_left_anim = ANIM(stand_left_seq, 1, True)
    walk_right_img = IMG("bigluigiwalkright.png")
    walk_right_seq = GRID(walk_right_img, 1, 2)
    walk_right_anim = ANIM(walk_right_seq, 0.1, True)
    walk_left_img = IMG("bigluigiwalkleft.png")
    walk_left_seq = GRID(walk_left_img, 1, 2)
    walk_left_anim = ANIM(walk_left_seq, 0.1, True)
    run_right_anim = ANIM(walk_right_seq, 0.05, True)
    run_left_anim = ANIM(walk_left_seq, 0.05, True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

def make_yammy():       #not a playing character
    yammy = Yammy(img=Yammy.stand_right, x=30, y=c.ITEM_PLATFORM_H, batch=c.MAIN_BATCH)
    yammy.scale = 2
    yammy.opacity = 0
    return yammy

def make_firelight():
    fire_light = FireLight(img=FireLight.stand_left, x=c.OFF_SCREEN_R, y=c.FLOAT_H, batch=c.MAIN_BATCH)
    fire_light.scale = 1.5
    return fire_light

def make_dragon():
    dragon = Dragon(img=Dragon.stand_left, x=c.OFF_SCREEN_R, y=c.WALK_H, batch=c.MAIN_BATCH)
    dragon.scale = 2
    return dragon

def make_big_boo():
    big_boo = BigBoo(img=BigBoo.stand_left, x=c.OFF_SCREEN_R, y=c.FLOAT_H, batch=c.MAIN_BATCH)
    return big_boo

def make_green_koopa():
    green_koopa = GreenKoopa(img=GreenKoopa.stand_left, x=c.OFF_SCREEN_R, y=c.WALK_H, batch=c.MAIN_BATCH) 
    green_koopa.scale = 2
    return green_koopa

def make_big_mole():
    big_mole = BigMole(img=BigMole.stand_left, x=c.OFF_SCREEN_R, y=c.WALK_H, batch=c.MAIN_BATCH)
    big_mole.scale = 1.5 
    return big_mole

def make_mario():
    mario = Mario(img=Mario.stand_left, x=c.OFF_SCREEN_R, y=c.WALK_H, batch=c.MAIN_BATCH)
    mario.scale = 2
    return mario

def make_luigi():
    luigi = Luigi(img=Luigi.stand_left, x=c.OFF_SCREEN_R, y=c.WALK_H, batch=c.MAIN_BATCH)
    luigi.scale = 2
    return luigi
