import pyglet


def center_image(image):
    """Centers the anchor point in the image."""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2

def center_floating_player(image):
    """Centers the anchor point in the image."""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2

def center_walking_player(image):
    """Centers the anchor point in the image."""
    image.anchor_x = image.width // 2

def center_ground_sprite(obj):
    obj.anchor_x = obj.width // 2
    obj.anchor_y = 0

class Line():

    player_spots = [] #filled by Line.line_up() 
    player_spots_occupied = []
    item_spots = []
    item_spots_occupied = []

    def __init__(self, num_players = 0, screen_w = 0, num_items = 0, *args, **kwargs):
        self.num_players = num_players
        self.screen_w = screen_w
        self.num_items = num_items

    def line_up(self):
        """Sets the available player positions on the screen.
            Returns None."""
        for place in range(self.num_players):
            if len(self.player_spots) == 0:
                first_spot = (self.screen_w // 2) - 100
                self.player_spots.append(first_spot)
            else:
                next_spot = (self.screen_w // 2) + (90 * place)
                self.player_spots.append(next_spot)
        for place in self.player_spots:
            self.player_spots_occupied.append(False)#changed from True

        print("player_spots          = ", self.player_spots)
        print("player_spots_occupied = ", self.player_spots_occupied)

    def item_line_up(self, items):
        """Sets the available item positions on the screen.
            Returns None."""
        index = 0
        for item in range(self.num_items):
            if len(self.item_spots) == 0:
                first_spot = (self.screen_w // 2) - 200
                self.item_spots.append(first_spot)
            else:
                next_spot = (self.screen_w // 2) - 200 - (16 * item) #problem with width math
                self.item_spots.append(next_spot)
            index += 1
        for item in self.item_spots:
            self.item_spots_occupied.append(False) #changed from True
    
        print("item_spots          = ", self.item_spots)
        print("item_spots_occupied = ", self.item_spots_occupied)









