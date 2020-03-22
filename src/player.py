import pyglet


class Player(pyglet.sprite.Sprite):
    def __init__(self, img, go_right_img, go_left_img, rest_images, anim_images, name, *args, **kwargs):
        # not using rest_images
        super().__init__(img, *args, **kwargs)
        self.inventory = []
        self.points = 0
        self.point_index = 0
        self.spot_in_line = self.x
        self.name = name
        self.img = img

        # for setup only
        # go_right_img and go_left_img are centered in the child class
        self.seq_right = go_right_img
        self.grid_right = pyglet.image.ImageGrid(
            self.seq_right, 1, anim_images)
        self.seq_left = go_left_img
        self.grid_left = pyglet.image.ImageGrid(self.seq_left, 1, anim_images)

        # these images are drawn to the screen
        self.look_left = img
        self.go_right = pyglet.image.Animation.from_image_sequence(
            self.grid_right, 0.1, loop=True)
        self.go_left = pyglet.image.Animation.from_image_sequence(
            self.grid_left, 0.1, loop=True)
        self.scale = 1.5

    def _pos_delta(self):
        """Return the difference between the players current x-pos and where it's going.
            Example:
                self.spot_in_line = 100     # where it's going (where it needs to be).
                self.x = 50                 # where it is currently
                return 50 - 100             # -50

            Notes:
                a negative return value means that the player is to the left of where it is going and thus will move to the right until it reaches it's spot_in_line.
        """
        return self.x - self.spot_in_line

    def _update_pos(self) -> None:
        """Shifts the player's image horizontally. Returns None.
            Example:
                if self._pos_delta() > 0: then the character will move left
                if self._pos_delta() < 0: then the character will move right
        """
        diff = self._pos_delta()
        if diff > 0 and diff > 3:
            self.x -= 3
        elif diff > 0 and diff <= 3:
            self.x -= 1
        elif diff < 0 and abs(diff) > 3:
            self.x += 3
        elif diff < 0 and abs(diff) <= 3:
            self.x += 1

    def _take_item(self):
        """Sets player's item to player's pos. Returns None."""
        if self.inventory:
            self.inventory[0].y = self.height//2

    def update(self):
        self._update_img()
        self._update_pos()
        # self._take_item()
