import math
import util
import pyglet
from pyglet import clock

#setup image directory
resource_dir = "./resources"
pyglet.resource.path = [resource_dir]
pyglet.resource.reindex()

class Background(pyglet.sprite.Sprite):

    background_img = pyglet.resource.image("quiz1.png")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Player(pyglet.sprite.Sprite):

    randomized = False
    game_just_started = True 
    debug = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.spot = self.x      #initially off screen, changed immediately
        self.delta_x = 0        #intially zero, changed immediately
        self.item = False
        self.speed = "walk"
        self.moving = False
        self.rotating_players = False
        self.inventory = []
        self.points = 0
            
    def update(self, dt):
        self.delta_x = self.x - self.spot
        if Player.game_just_started:
            self.speed = "run"
        if self.spot == util.Line.player_spots[-1]: #if the player is in the ready position
            self.speed = "run"
        self.move()

    def has_item(self):
        """Checks if the player has an item in their inventory. Returns None."""
        if len(self.inventory) == 0:
            return False
        elif len(self.inventory) > 0:
            return True

    def use_item(self):
        """Player uses the item in their inventory. Returns None."""
        self.item = True
        item = self.inventory[0]
        if item.item_not_used == True:
            item.effect()                       
            item.item_not_used = False          #dont need to reset to False, instance is destroyed after use. 

    def game_in_play(self):
        """Sets self.game_just_started to False. Returns None."""
        Player.game_just_started = False

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
        
class Yammy(pyglet.sprite.Sprite):
    
    stand_right = pyglet.resource.image("yammy_stand_right.png")    
    action_right_img = pyglet.resource.image("yammy_action_right.png")
    action_right_seq = pyglet.image.ImageGrid(action_right_img, 1, 2)
    action_right_anim = pyglet.image.Animation.from_image_sequence(action_right_seq, 0.2, False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.transition_direction = "out"
        self.transitioning = False
        self.inventory = []
        self.transition_rate = 3
        self.victim = "" 

    def update(self):
        """Yammy's main update loop. Returns None."""
        self.transition()
        self.give_item()
    
    def transition_out(self):
        """Fades first inventory item out. Returns None."""
        self.inventory[0].opacity -=1

    def transition_in(self):
        """Fades first inventory item in. Returns None."""
        self.inventory[0].opacity += 1

    def toggle_transition_direction(self):
        """Toggles transition_direction attribute between in and out. Returns None."""
        if self.transition_direction == "in":
            self.transition_direction = "out"
        elif self.transition_direction == "out":
            self.transition_direction = "in"

    def transition(self):
        """Toggles fading animation. Returns None."""
        if self.transitioning:
            if self.transition_direction == "in":
                self.opacity += self.transition_rate
            if self.transition_direction == "out":
                self.opacity -= self.transition_rate
            if self.opacity >= 255:
                self.opacity = 255 
                self.transitioning = False
            if self.opacity <= 0:
                self.opacity = 0
                self.transitioning = False

    def wave_wand(self):
        """Yammy waves his magic wand. Returns None."""
        self.image = self.action_right_anim

    def take_item(self, item):
        """Adds item to Yammy's inventory. Returns None."""
        self.inventory.append(item)

    def give_item(self):
        """Gives an item to a player. Returns String."""
        if self.inventory:
            yammys_item = self.inventory[0]
            if yammys_item.opacity == 0 and yammys_item.delta_y == 0:
                yammys_item.spot_x = self.victim.spot
                yammys_item.x = self.victim.spot
                yammys_item.falling = True                  #reset flag 
                yammys_item.toggle_transition_direction()
                yammys_item.transitioning = True            #change flag
            if yammys_item.y <= self.victim.y:
                yammys_item.falling = False                 #reset flag
                self.victim.inventory.append(yammys_item)   #give item to game_objects[0]
                print("game_objects[0].inventory = ", self.victim.inventory)    
                self.inventory.remove(yammys_item)          #remove reference to item

class FireLight(FloatingPlayer):
    
    stand_left = pyglet.resource.image("fire_light_walk_left.png")
    util.center_floating_player(stand_left)
    stand_left_seq = pyglet.image.ImageGrid(stand_left, 1, 2)
    stand_left_anim = pyglet.image.Animation.from_image_sequence(stand_left_seq, 0.1, True) 
    walk_right = pyglet.resource.image("fire_light_walk_right.png")
    walk_right_seq = pyglet.image.ImageGrid(walk_right, 1, 2)
    walk_right_anim = pyglet.image.Animation.from_image_sequence(walk_right_seq, 0.1, True)
    walk_left = pyglet.resource.image("fire_light_walk_left.png")
    walk_left_seq = pyglet.image.ImageGrid(walk_left, 1, 2)
    walk_left_anim = pyglet.image.Animation.from_image_sequence(walk_left_seq, 0.1, True)
    run_right_anim = pyglet.image.Animation.from_image_sequence(walk_right_seq, 0.05, True)
    run_left_anim = pyglet.image.Animation.from_image_sequence(walk_left_seq, 0.05, True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Dragon(WalkingPlayer):
    
    stand_left = pyglet.resource.image("dragon_stand_left.png")
    util.center_walking_player(stand_left)
    stand_left_seq = pyglet.image.ImageGrid(stand_left, 1, 1)
    stand_left_anim = pyglet.image.Animation.from_image_sequence(stand_left_seq, 1, True) 
    walk_right = pyglet.resource.image("dragon_walk_right.png")
    walk_right_seq = pyglet.image.ImageGrid(walk_right, 1, 2)
    walk_right_anim = pyglet.image.Animation.from_image_sequence(walk_right_seq, 0.1, True)
    walk_left = pyglet.resource.image("dragon_walk_left.png")
    walk_left_seq = pyglet.image.ImageGrid(walk_left, 1, 2)
    walk_left_anim = pyglet.image.Animation.from_image_sequence(walk_left_seq, 0.1, True)
    run_right_anim = pyglet.image.Animation.from_image_sequence(walk_right_seq, 0.05, True)
    run_left_anim = pyglet.image.Animation.from_image_sequence(walk_left_seq, 0.05, True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class BigBoo(FloatingPlayer):
    
    stand_left = pyglet.resource.image("big_boo_stand_left.png")
    util.center_floating_player(stand_left)
    stand_left_seq = pyglet.image.ImageGrid(stand_left, 1, 1)
    stand_left_anim = pyglet.image.Animation.from_image_sequence(stand_left_seq, 1, True) 
    walk_right = pyglet.resource.image("big_boo_walk_right.png")
    walk_right_seq = pyglet.image.ImageGrid(walk_right, 1, 1)
    walk_right_anim = pyglet.image.Animation.from_image_sequence(walk_right_seq, 0.1, True)
    walk_left = pyglet.resource.image("big_boo_walk_left.png")
    walk_left_seq = pyglet.image.ImageGrid(walk_left, 1, 1)
    walk_left_anim = pyglet.image.Animation.from_image_sequence(walk_left_seq, 0.1, True)
    run_right_anim = pyglet.image.Animation.from_image_sequence(walk_right_seq, 0.05, True)
    run_left_anim = pyglet.image.Animation.from_image_sequence(walk_left_seq, 0.05, True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class GreenKoopa(WalkingPlayer):
    
    stand_left = pyglet.resource.image("green_koopa_stand_left.png")
    util.center_walking_player(stand_left)
    stand_left_seq = pyglet.image.ImageGrid(stand_left, 1, 1)
    stand_left_anim = pyglet.image.Animation.from_image_sequence(stand_left_seq, 1, True) 
    walk_right = pyglet.resource.image("green_koopa_walk_right.png")
    walk_right_seq = pyglet.image.ImageGrid(walk_right, 1, 2)
    walk_right_anim = pyglet.image.Animation.from_image_sequence(walk_right_seq, 0.1, True)
    walk_left = pyglet.resource.image("green_koopa_walk_left.png")
    walk_left_seq = pyglet.image.ImageGrid(walk_left, 1, 2)
    walk_left_anim = pyglet.image.Animation.from_image_sequence(walk_left_seq, 0.1, True)
    run_right_anim = pyglet.image.Animation.from_image_sequence(walk_right_seq, 0.05, True)
    run_left_anim = pyglet.image.Animation.from_image_sequence(walk_left_seq, 0.05, True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class BigMole(WalkingPlayer):
    
    stand_left = pyglet.resource.image("big_mole_stand_left.png")
    util.center_walking_player(stand_left)
    stand_left_seq = pyglet.image.ImageGrid(stand_left, 1,1)
    stand_left_anim = pyglet.image.Animation.from_image_sequence(stand_left_seq, 1, True) 
    walk_right = pyglet.resource.image("big_mole_walk_right.png")
    walk_right_seq = pyglet.image.ImageGrid(walk_right, 1, 2)
    walk_right_anim = pyglet.image.Animation.from_image_sequence(walk_right_seq, 0.1, True)
    walk_left = pyglet.resource.image("big_mole_walk_left.png")
    walk_left_seq = pyglet.image.ImageGrid(walk_left, 1, 2)
    walk_left_anim = pyglet.image.Animation.from_image_sequence(walk_left_seq, 0.1, True)
    run_right_anim = pyglet.image.Animation.from_image_sequence(walk_right_seq, 0.05, True)
    run_left_anim = pyglet.image.Animation.from_image_sequence(walk_left_seq, 0.05, True)
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Mario(WalkingPlayer):

    stand_left = pyglet.resource.image("big_mario_standing_left.png")
    util.center_walking_player(stand_left)
    stand_left_seq = pyglet.image.ImageGrid(stand_left, 1,1)
    stand_left_anim = pyglet.image.Animation.from_image_sequence(stand_left_seq, 1, True)
    walk_right_img = pyglet.resource.image("mario_walking_right.png")
    walk_right_seq = pyglet.image.ImageGrid(walk_right_img, 1, 3)
    walk_right_anim = pyglet.image.Animation.from_image_sequence(walk_right_seq, 0.1, True)
    walk_left_img = pyglet.resource.image("mario_walking_left.png")
    walk_left_seq = pyglet.image.ImageGrid(walk_left_img, 1, 3)
    walk_left_anim = pyglet.image.Animation.from_image_sequence(walk_left_seq, 0.1, True)
    run_right_anim = pyglet.image.Animation.from_image_sequence(walk_right_seq, 0.05, True)
    run_left_anim = pyglet.image.Animation.from_image_sequence(walk_left_seq, 0.05, True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
