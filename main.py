import pyglet
import player
from pyglet.window import key
from pyglet import sprite

verbose = False
PLAYER_SPEED = 2
window = pyglet.window.Window()

# key booleans
rdown = False
udown = False
ldown = False
ddown = False

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
    player.stop()

    if rdown and not ldown:
        player.hspeed = PLAYER_SPEED
        SPRITES.get("player").rotation=90
    if ldown and not rdown:
        player.hspeed = -PLAYER_SPEED
        SPRITES.get("player").rotation=270
    if udown and not ddown:
        player.vspeed = PLAYER_SPEED
        SPRITES.get("player").rotation=0
    if ddown and not udown:
        player.vspeed = -PLAYER_SPEED
        SPRITES.get("player").rotation=180

    player.step()


@window.event
def on_key_press(symbol, modifiers):
    global rdown, ldown, udown, ddown

    if symbol == key.RIGHT:
        rdown = True
    elif symbol == key.LEFT:
        ldown = True
    elif symbol == key.UP:
        udown = True
    elif symbol == key.DOWN:
        ddown = True

@window.event
def on_key_release(symbol, modifiers):
    global rdown, ldown, udown, ddown
    if symbol == key.RIGHT:
        rdown = False
    elif symbol == key.LEFT:
        ldown = False
    elif symbol == key.UP:
        udown = False
    elif symbol == key.DOWN:
        ddown = False
    

pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()
event_loop = pyglet.app.EventLoop()
event_loop.run()



@event_loop.event
def on_window_close(window):
    event_loop.exit()
