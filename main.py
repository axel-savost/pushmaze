import pyglet
import player
import block
import enemy
import constants
from pyglet.window import key
from pyglet import sprite

frame = 0
window = pyglet.window.Window()
batch = pyglet.graphics.Batch()

# key booleans
rdown = False
udown = False
ldown = False
ddown = False
pdown = False

# Images go here
temp = pyglet.resource.image('res/img/Player.png')
temp.anchor_x = 16
temp.anchor_y = 16
spr_player = sprite.Sprite(temp)

spr_sandbl = sprite.Sprite(pyglet.resource.image('res/img/BlockSand.png'),batch=batch)
spr_metalbl = sprite.Sprite(pyglet.resource.image('res/img/BlockMetal.png'),batch=batch)
spr_ghost = sprite.Sprite(pyglet.resource.image('res/img/EnemyGhost.png'),batch=batch)
spr_default = sprite.Sprite(pyglet.resource.image('res/img/DEFAULT.png'),batch=batch)

# Testing purposes only
spr_teston = sprite.Sprite(pyglet.resource.image('res/img/TESTON.png'),batch=batch)
spr_testoff = sprite.Sprite(pyglet.resource.image('res/img/TESTOFF.png'),batch=batch)

# Backgrounds
bg_gravel = sprite.Sprite(pyglet.resource.image('res/img/BG_Gravel.png'))
bg_grass = sprite.Sprite(pyglet.resource.image('res/img/BG_Grass.png'))

snd_crush = pyglet.resource.media("res/snd/Crush.ogg", streaming=False)
snd_bounce = pyglet.resource.media("res/snd/Bounce.ogg", streaming=False)
snd_powerup = pyglet.resource.media("res/snd/Powerup.ogg", streaming=False)
snd_shoot = pyglet.resource.media("res/snd/Shoot.ogg", streaming=False)
snd_settle = pyglet.resource.media("res/snd/Settle.ogg", streaming=False)
snd_shoot = pyglet.resource.media("res/snd/Shoot.ogg", streaming=False)

spr_player.anchor_x=16
spr_player.anchor_y=16

player = player.Player(x=320,y=320)
things = [player]
# Generate blocks around the edges
for i in range(0,constants.WINDOW_WIDTH,constants.TILE_SIZE):
    things.append(block.Block(i,0))
for i in range(constants.TILE_SIZE,constants.WINDOW_HEIGHT,constants.TILE_SIZE):
    things.append(block.Block(0,i))
for i in range(constants.TILE_SIZE,constants.WINDOW_WIDTH,constants.TILE_SIZE):
    things.append(block.Block(i,448))
for i in range(constants.TILE_SIZE,448,constants.TILE_SIZE):
    things.append(block.Block(608,i))

for i in range(32,608,constants.TILE_SIZE*2):
    things.append(block.Block(i,192))

for i in range(64,608,constants.TILE_SIZE*2):
    things.append(block.Block(i,256))

# Enemies
for i in range(32,608,constants.TILE_SIZE*2):
    things.append(enemy.Enemy(i,32))

SPRITES = {"block": spr_sandbl,
           "player": spr_player,
           "ghost": spr_ghost}

def is_snapped(entity):
    if entity.x % constants.TILE_SIZE == 0 and entity.y % constants.TILE_SIZE == 0:
        return True
    else:
        return False

def is_blocked(x,y):
    if x<0 or y<0 or x>constants.WINDOW_WIDTH-constants.TILE_SIZE or y>constants.WINDOW_HEIGHT-constants.TILE_SIZE:
        return True

    return not get_entity(x,y,"block") is None

def is_colliding(a,b):
    if a == b:
        return False
    if a.x + constants.TILE_SIZE > b.x and a.x < b.x + constants.TILE_SIZE:
        if a.y + constants.TILE_SIZE > b.y and a.y < b.y + constants.TILE_SIZE:
            return True

    return False

def get_entity(x, y, look):
    for t in things:
        if t.looks_like == look and t.x + constants.TILE_SIZE > x and t.x <= x and t.y + constants.TILE_SIZE > y and t.y <= y:
            return t

    return None

@window.event
def on_draw():
    global frame

    window.clear()

    for h in range(2):
        for n in range(3):
            bg_grass.x = n * 256
            bg_grass.y = h * 256
            bg_grass.draw()

    if is_blocked(frame*2 % constants.WINDOW_WIDTH,frame*2 % constants.WINDOW_HEIGHT):
        drawthis = spr_testoff
    else:
        drawthis = spr_teston
    
    drawthis.x = frame*2 % constants.WINDOW_WIDTH
    drawthis.y = frame*2 % constants.WINDOW_HEIGHT
    drawthis.draw()


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

        if thing.looks_like == "block":
            spr.opacity = 255 * (1 - thing.crushed)
        spr.draw()

def update(dt):
    global rdown, ldown, udown, ddown, pdown, frame

    frame += 1

    if is_snapped(player): #If on the grid
        player.stop() #Stop moving

        pressing = False

        #Rotate if movement keys are pressed
        if rdown and not ldown:
            SPRITES.get("player").rotation=90
            player.hfacing = 1
            player.vfacing = 0
            pressing = True
        elif ldown and not rdown:
            SPRITES.get("player").rotation=270
            player.hfacing = -1
            player.vfacing = 0
            pressing = True
        elif udown and not ddown:
            SPRITES.get("player").rotation=0
            player.hfacing = 0
            player.vfacing = 1
            pressing = True
        elif ddown and not udown:
            SPRITES.get("player").rotation=180
            player.hfacing = 0
            player.vfacing = -1
            pressing = True

        bl = get_entity(player.x + player.hfacing*constants.TILE_SIZE, player.y + player.vfacing*constants.TILE_SIZE,"block")
        bl2 = get_entity(player.x + player.hfacing*constants.TILE_SIZE*2, player.y + player.vfacing*constants.TILE_SIZE*2,"block")

        if bl is None:
            if pressing:
                player.hspeed = player.hfacing * constants.PLAYER_SPEED
                player.vspeed = player.vfacing * constants.PLAYER_SPEED
                player.step() # On the grid and free space ahead
        elif pdown:
            if not bl.is_moving():
                if not bl2 is None:
                    if bl.crushed == 0:
                        snd_crush.play()
                        bl.crush()
                else:
                    bl.get_pushed(player.hfacing,player.vfacing)
                    snd_shoot.play()

    else: #If not on the grid
        player.step() # Not on the grid, nowhere to go but forward

 


    for b in things:
        if b.looks_like == "block":
            if b.crushed >= 1:
                things.remove(b)
                continue

            f = get_entity(b.x + constants.TILE_SIZE + b.hspeed, b.y + constants.TILE_SIZE + b.vspeed,"block")

            if b.is_moving() and not f is None and not f is b:
                b.collide_with(f)
                #snd_bounce.play()
                print(str(b) + " collided with " + str(f))


            b.update()

    
    #Stop player from going out of bounds
    if player.x < 0:
        player.x = 0
        player.stop()
    if player.y < 0:
        player.y = 0
        player.stop()
    if player.x > constants.WINDOW_WIDTH-constants.TILE_SIZE:
        player.x = constants.WINDOW_WIDTH-constants.TILE_SIZE
        player.stop()
    if player.y > constants.WINDOW_HEIGHT-constants.TILE_SIZE:
        player.y = constants.WINDOW_HEIGHT-constants.TILE_SIZE
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
    

pyglet.clock.schedule_interval(update, 1/float(constants.GAME_FPS))
pyglet.app.run()
event_loop = pyglet.app.EventLoop()
event_loop.run()

@event_loop.event
def on_window_close(window):
    event_loop.exit()
