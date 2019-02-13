import pyglet
import player
import block
import enemy
from pyglet.window import key
from pyglet import sprite

verbose = False
PLAYER_SPEED = 4
TILE_SIZE = 32
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

player = player.Player(x=256,y=256)
things = [player]
# Generate blocks around the edges
for i in range(0,640,TILE_SIZE):
    things.append(block.Block(i,0))
for i in range(TILE_SIZE,480,TILE_SIZE):
    things.append(block.Block(0,i))
for i in range(TILE_SIZE,640,TILE_SIZE):
    things.append(block.Block(i,448))
for i in range(TILE_SIZE,448,TILE_SIZE):
    things.append(block.Block(608,i))

things.append(block.Block(32,32))
things.append(block.Block(64,64))
things.append(block.Block(96,32))
things.append(block.Block(256,128))
things.append(enemy.Enemy(128,128))




SPRITES = {"block": spr_block,
           "player": spr_player,
           "ghost": spr_ghost}

def is_snapped():
    if player.x % TILE_SIZE == 0 and player.y % TILE_SIZE == 0:
        return True
    else:
        return False

def is_blocked(x,y):
    for t in things:
        if t.looks_like == "block" and t.x == x and t.y == y:
            return True

@window.event
def on_draw():
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
    if is_snapped():
        player.stop()

    if player.hspeed == 0 and player.vspeed == 0 and is_snapped():
        if rdown and not ldown:
            player.hspeed = PLAYER_SPEED
            SPRITES.get("player").rotation=90
        elif ldown and not rdown:
            player.hspeed = -PLAYER_SPEED
            SPRITES.get("player").rotation=270
        elif udown and not ddown:
            player.vspeed = PLAYER_SPEED
            SPRITES.get("player").rotation=0
        elif ddown and not udown:
            player.vspeed = -PLAYER_SPEED
            SPRITES.get("player").rotation=180

    if not is_blocked(player.x + player.hspeed*TILE_SIZE/PLAYER_SPEED, player.y + player.vspeed*TILE_SIZE/PLAYER_SPEED):
        player.step()

    if player.x < 0:
        player.x = 0
        player.stop()
    if player.y < 0:
        player.y = 0
        player.stop()
    if player.x > 640-TILE_SIZE:
        player.x = 640-TILE_SIZE
        player.stop()
    if player.y > 480-TILE_SIZE:
        player.y = 480-TILE_SIZE
        player.stop()

    


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
