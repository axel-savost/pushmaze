import pyglet
import player
from pyglet.window import key
from pyglet import sprite

verbose = False
window = pyglet.window.Window()

# Images go here
img_block = pyglet.resource.image('res/img/block.png')
img_player = pyglet.resource.image('res/img/player.png')
img_coin = pyglet.resource.image('res/img/coin.png')
img_default = pyglet.resource.image('res/img/default.png')

player = player.Player(4,6)
things = [player]


SYMBOLS = {"wall": sprite.Sprite(img_block),
           "player": sprite.Sprite(img_player),
           "coin": sprite.Sprite(img_coin)}
DEFAULT_SYMBOL = sprite.Sprite(img_default)


@window.event
def on_draw():
    window.clear()

    for thing in things:

        if thing.looks_like in SYMBOLS:
            obj = SYMBOLS[thing.looks_like]
        else:
            obj = DEFAULT_SYMBOL
        obj.x = thing.x*32
        obj.y = thing.y*32
        obj.draw()


@window.event
def on_key_press(symbol, modifiers):
    global things

    if symbol == key.RIGHT:
        player.x += 1
    elif symbol == key.LEFT:
        player.x -= 1
    elif symbol == key.UP:
        player.y += 1
    elif symbol == key.DOWN:
        player.y -= 1
    if verbose:
        print(things)


pyglet.app.run()
event_loop = pyglet.app.EventLoop()


@event_loop.event
def on_window_close(window):
    event_loop.exit()
