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
batch = pyglet.graphics.Batch()

# key booleans
rdown = False
udown = False
ldown = False
ddown = False
pdown = False

# Images go here
temp = pyglet.resource.image('res/img/player.png')
temp.anchor_x = 16
temp.anchor_y = 16
spr_player = sprite.Sprite(temp)

spr_sandbl = sprite.Sprite(pyglet.resource.image('res/img/block_sand.png'),batch=batch)
spr_metalbl = sprite.Sprite(pyglet.resource.image('res/img/block_metal.png'),batch=batch)
spr_ghost = sprite.Sprite(pyglet.resource.image('res/img/ghost.png'),batch=batch)
spr_default = sprite.Sprite(pyglet.resource.image('res/img/default.png'),batch=batch)

bg_gravel = sprite.Sprite(pyglet.resource.image('res/img/bg_gravel.png'))
bg_grass = sprite.Sprite(pyglet.resource.image('res/img/bg_grass.png'))

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

for i in range(32,608,TILE_SIZE*2):
    things.append(block.Block(i,192))

for i in range(64,608,TILE_SIZE*2):
    things.append(block.Block(i,256))


things.append(enemy.Enemy(320,32))




SPRITES = {"block": spr_sandbl,
           "player": spr_player,
           "ghost": spr_ghost}

def is_snapped(entity):
    if entity.x % TILE_SIZE == 0 and entity.y % TILE_SIZE == 0:
        return True
    else:
        return False

def is_blocked(x,y):
    for t in things:
        if t.looks_like == "block" and t.x == x and t.y == y:
            return True

def is_colliding(a,b):
    if a.x + TILE_SIZE > b.x and a.x < b.x + TILE_SIZE:
        if a.y + TILE_SIZE > b.y and a.y < b.y + TILE_SIZE:
            return True

    return False

def get_entity(x, y, look):
    for t in things:
        if t.looks_like == look and t.x == x and t.y == y:
            return t

    print("Warning: Entity not found.")
    return 0

@window.event
def on_draw():
    window.clear()

    for h in range(2):
        for n in range(3):
            bg_grass.x = n * 256
            bg_grass.y = h * 256
            bg_grass.draw()

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
    global rdown, ldown, udown, ddown, pdown

    if is_snapped(player):
        player.stop()

    if player.hspeed == 0 and player.vspeed == 0 and is_snapped(player):
        if rdown and not ldown:
            player.hspeed = PLAYER_SPEED
            SPRITES.get("player").rotation=90
            player.hfacing = 1
            player.vfacing = 0
        elif ldown and not rdown:
            player.hspeed = -PLAYER_SPEED
            SPRITES.get("player").rotation=270
            player.hfacing = -1
            player.vfacing = 0
        elif udown and not ddown:
            player.vspeed = PLAYER_SPEED
            SPRITES.get("player").rotation=0
            player.hfacing = 0
            player.vfacing = 1
        elif ddown and not udown:
            player.vspeed = -PLAYER_SPEED
            SPRITES.get("player").rotation=180
            player.hfacing = 0
            player.vfacing = -1

    if not is_blocked(player.x + player.hspeed*TILE_SIZE/PLAYER_SPEED, player.y + player.vspeed*TILE_SIZE/PLAYER_SPEED):
        player.step()
    elif pdown and is_snapped(player):
        bl = get_entity(player.x + player.hfacing*TILE_SIZE, player.y + player.vfacing*TILE_SIZE,"block")
        if not bl.is_moving():
            bl.get_pushed(player.hfacing,player.vfacing)


    for b in things:
        if b.looks_like == "block":
            if b.is_moving():
                b.update()
                for q in things:
                    if not b == q and is_colliding(b,q) and q.looks_like == "block":
                        if b.hspeed == q.hspeed or b.vspeed == q.vspeed:
                            b.x -= b.hspeed
                            b.y -= b.vspeed
                            th = b.hspeed
                            tv = b.vspeed
                            b.hspeed = q.hspeed
                            b.vspeed = q.vspeed
                            q.hspeed = th
                            q.vspeed = tv
                            
                            break
                        else:
                            b.bounce()
                



    #Stop player from going out of bounds
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
    global rdown, ldown, udown, ddown, pdown

    if symbol == key.D:
        rdown = True
    elif symbol == key.A:
        ldown = True
    elif symbol == key.W:
        udown = True
    elif symbol == key.S:
        ddown = True
    elif symbol == key.SPACE:
        pdown = True

@window.event
def on_key_release(symbol, modifiers):
    global rdown, ldown, udown, ddown, pdown
    if symbol == key.D:
        rdown = False
    elif symbol == key.A:
        ldown = False
    elif symbol == key.W:
        udown = False
    elif symbol == key.S:
        ddown = False
    elif symbol == key.SPACE:
        pdown = False
    

pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()
event_loop = pyglet.app.EventLoop()
event_loop.run()

@event_loop.event
def on_window_close(window):
    event_loop.exit()
