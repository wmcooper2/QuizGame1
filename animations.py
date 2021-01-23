#std lib
from typing import Any

#custom
from constants import Constants as c
import util as u


def transfer_item() -> None:
    """The animation of giving the item to a player."""
    item = c.TRANSFER_ITEM
    player = u.player_in_front()
    
    if item:
        #always update animation
        item.disappear_animation()

        #item rise and disappear
        if item.is_visible() and item.is_on_platform() and item.is_left_of_p1():
            item.dest_y = item.y + item.disappear_limit
            item.toggle_disappear()

        #item over player, item not visible at this point
        if not item.is_visible() and item.is_at_disappear_limit():
            item.opacity = item.min_opacity
            item.move_over_player()

        #item over player, much closer to it, item becomes visible at this point
        if item.is_over_p1() and item.is_at_disappear_limit():
            item.dest_y = player.y

            # over shoot the dest_y to allow the floating players to grab the items
            item.y, item.dest_y = player.y + item.disappear_limit, player.y - c.SCREEN_H
            item.toggle_disappear()

        #item is at the same spot as the player, x and y axes
        if item.is_at_or_below_p1():
            player.item = item
            c.TRANSFER_ITEM = None      #remove reference as c.TRANSFER_ITEM

