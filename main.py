import pyglet
import player
from pyglet.window import key
from pyglet import sprite

verbose = False
window = pyglet.window.Window()

# Images go here
temp = pyglet.resource.image('res/img/player.png')
temp.anchor_x = 16
temp.anchor_y = 16
spr_player = sprite.Sprite(temp)

spr_block = sprite.Sprite(pyglet.resource.image('res/img/block.png'))
spr_ghost = sprite.Sprite(pyglet.resource.image('res/img/ghost.png'))
spr_default = sprite.Sprite(pyglet.resource.image('res/img/default.png'))

spr_player.anchor_x=16
spr_player.anchor_y=16

player = player.Player(x=4,y=6)
things = [player]


SPRITES = {"wall": spr_block,
           "player": spr_player,
           "ghost": spr_ghost}


@window.event
def on_draw():
    player.step()

    window.clear()

    for thing in things:

        if thing.looks_like in SPRITES:
            spr = SPRITES[thing.looks_like]
        else:
            spr = spr_default
        spr.x = thing.x
        spr.y = thing.y

        if thing.looks_like == "player":
            spr.x+=16
            spr.y+=16
        spr.draw()

def update(dt):
    player.step()



@window.event
def on_key_press(symbol, modifiers):
    global things

    if symbol == key.RIGHT:
        player.hspeed = 4
        player.vspeed = 0
        SPRITES.get("player").rotation=90
    elif symbol == key.LEFT:
        player.hspeed = -4
        player.vspeed = 0
        SPRITES.get("player").rotation=270
    elif symbol == key.UP:
        player.hspeed = 0
        player.vspeed = 4
        SPRITES.get("player").rotation=0
    elif symbol == key.DOWN:
        player.hspeed = 0
        player.vspeed = -4
        SPRITES.get("player").rotation=180
    if verbose:
        print(things)

@window.event
def on_key_release(symbol, modifiers):
    if symbol == key.RIGHT:
        player.hspeed = 0
    elif symbol == key.LEFT:
        player.hspeed = 0
    elif symbol == key.UP:
        player.vspeed = 0
    elif symbol == key.DOWN:
        player.vspeed = 0
    

pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()
event_loop = pyglet.app.EventLoop()
event_loop.run()



@event_loop.event
def on_window_close(window):
    event_loop.exit()
