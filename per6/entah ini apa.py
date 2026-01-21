import pygame, sys, time, math
pygame.init()

WIDTH, HEIGHT = 900, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MARIO FINAL VERSION")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("consolas",22)

GROUND_Y = HEIGHT-70
WORLD_WIDTH = 2600

# ===============================================================
#                        SPRITE PLAYER
# ===============================================================
def make_player(col=(255,80,80)):
    s = pygame.Surface((32,48), pygame.SRCALPHA)
    pygame.draw.rect(s,col,(0,10,32,38))
    pygame.draw.rect(s,(250,230,190),(8,0,18,15))
    pygame.draw.rect(s,(255,0,0),(0,10,32,12))
    pygame.draw.rect(s,(255,200,0),(6,26,20,20))
    return s

PLAYER_RUN  = [make_player((255,60,60)), make_player((255,90,90))]
PLAYER_JUMP = make_player((255,40,40))
PLAYER_IDLE = make_player()

player={
    "x":200,"y":GROUND_Y-48,
    "hp":5,"coins":0,
    "vel_y":0,"grounded":True,
    "facing":1,"alive":True,"frame":0,
    "respawn":(200,GROUND_Y-48)
}

# ===============================================================
#                   ATTACK / ABILITY / DASH
# ===============================================================
attack=False
atk_time=0

ability=False
ability_time=0

dash=False
dash_time=0
dash_cd=0       # cooldown tetap, tapi TIDAK MENGHENTIKAN GERAK

# ===============================================================
#                     WORLD OBSTACLE + PIT
# ===============================================================
obstacles=[
    pygame.Rect(0,GROUND_Y-10,WORLD_WIDTH,20),
    pygame.Rect(450,GROUND_Y-40,100,40),
    pygame.Rect(950,GROUND_Y-60,140,60),
    pygame.Rect(1500,GROUND_Y-40,100,40),
    pygame.Rect(1900,GROUND_Y-50,200,50)
]

pits=[pygame.Rect(700,GROUND_Y,140,80),
      pygame.Rect(1300,GROUND_Y,160,80),
      pygame.Rect(2250,GROUND_Y,140,80)]

coins=[{"x":x,"y":GROUND_Y-55,"take":False} for x in [500,650,1000,1350,1600,2000,2400]]

# ===============================================================
#                     ENEMY AI + HP
# ===============================================================
enemies=[]
for pos in [800,1100,1400,1750,2100,2500]:
    enemies.append({"x":pos,"y":GROUND_Y-48,"hp":3,
                    "speed":2,"vel_y":0,"grounded":True,
                    "dir":1,"dead":False})

def enemy_ai(e):
    old=e["x"]
    if abs(player["x"]-e["x"])<300 and not e["dead"]:
        e["x"]+=e["speed"]*(1 if player["x"]>e["x"] else -1)
    else:
        e["x"]+=e["speed"]*e["dir"]

    e["vel_y"]+=0.4
    e["y"]+=e["vel_y"]

    rect=pygame.Rect(e["x"],e["y"],40,48)
    for o in obstacles:
        if rect.colliderect(o):
            e["x"]=old; e["dir"]*=-1
            if e["y"]+48>=o.y:
                e["y"]=o.y-48; e["vel_y"]=0; e["grounded"]=True

def collide(px,py):
    rect=pygame.Rect(px,py,32,48)
    return any(rect.colliderect(o) for o in obstacles)

# ===============================================================
#                          CAMERA
# ===============================================================
camera=0
def cam():
    global camera
    camera=max(0,min(player["x"]-WIDTH//2,WORLD_WIDTH-WIDTH))

# ===============================================================
#                         GAME LOOP
# ===============================================================
while True:
    dt=clock.tick(60)/1000
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit(); sys.exit()

    keys=pygame.key.get_pressed()

    if player["alive"]:

        # -------- MOVEMENT ---------
        SPEED=4+(3 if ability else 0)

        oldx=player["x"]
        if keys[pygame.K_a]:
            player["x"]-=SPEED; player["facing"]=-1
        if keys[pygame.K_d]:
            player["x"]+=SPEED; player["facing"]=1

        if collide(player["x"],player["y"]):
            player["x"]=oldx

        # -------- JUMP -------------
        if (keys[pygame.K_w] or keys[pygame.K_SPACE]) and player["grounded"]:
            player["vel_y"]=-13; player["grounded"]=False

        oldy=player["y"]
        player["y"]+=player["vel_y"]; player["vel_y"]+=0.55

        if player["y"]+48>=GROUND_Y:
            player["y"]=GROUND_Y-48; player["vel_y"]=0; player["grounded"]=True
        elif collide(player["x"],player["y"]):
            player["y"]=oldy; player["vel_y"]=0; player["grounded"]=True

        # -------- PIT = HP -1 -------
        for pit in pits:
            if pygame.Rect(player["x"],player["y"],32,48).colliderect(pit):
                player["hp"]-=1
                player["x"],player["y"]=player["respawn"]
                if player["hp"]<=0:player["alive"]=False

        # -------- ATTACK (J) -------
        if keys[pygame.K_j] and not attack:
            attack=True; atk_time=time.time()
            sword=pygame.Rect(player["x"]+30*player["facing"],player["y"]+15,45,15)
            for e in enemies:
                if not e["dead"] and sword.colliderect(pygame.Rect(e["x"],e["y"],40,48)):
                    e["hp"]-=1
                    if e["hp"]<=0:e["dead"]=True

        if attack and time.time()-atk_time>0.25: attack=False

        # -------- DASH TANPA DELAY (LSHIFT) --------
        if keys[pygame.K_LSHIFT] and time.time()>dash_cd:
            dash=True; dash_time=time.time()
            dash_cd=time.time()+1.2   # cooldown tetap ada tapi bebas bergerak

        # movement tetap berjalan, dash hanya menambah **speed burst**
        if dash:
            player["x"]+=player["facing"]*22
            if time.time()-dash_time>0.18: dash=False

        # -------- ABILITY (K) 5 DETIK --------
        if keys[pygame.K_k] and player["coins"]>=5 and not ability:
            ability=True; ability_time=time.time(); player["coins"]-=5

        if ability and time.time()-ability_time>5:
            ability=False

        # -------- PICK COINS -------
        for c in coins:
            if not c["take"] and abs(player["x"]-c["x"])<35:
                c["take"]=True; player["coins"]+=1

        # -------- ENEMY ----------
        for e in enemies:
            if not e["dead"]:
                enemy_ai(e)
                if pygame.Rect(player["x"],player["y"],32,48).colliderect(pygame.Rect(e["x"],e["y"],40,48)):
                    player["hp"]-=0.02
                    if player["hp"]<=0:player["alive"]=False

    cam()

    # ===========================================================
    #                           DRAW
    # ===========================================================
    window.fill((120,200,255))

    for x in range(0,WORLD_WIDTH,60):
        pygame.draw.rect(window,(80,200,60),(x-camera,GROUND_Y,60,80))
        pygame.draw.line(window,(40,150,40),(x-camera,GROUND_Y),(x-camera+60,GROUND_Y),4)

    for o in obstacles: pygame.draw.rect(window,(110,90,55),(o.x-camera,o.y,o.w,o.h))
    for p in pits: pygame.draw.rect(window,(0,0,0),(p.x-camera,p.y,p.w,p.h))

    for c in coins:
        if not c["take"]:pygame.draw.circle(window,(255,230,0),(c["x"]-camera,c["y"]),12)

    for e in enemies:
        if not e["dead"]:
            pygame.draw.rect(window,(255,120,0),(e["x"]-camera,e["y"],40,48))
            pygame.draw.rect(window,(255,0,0),(e["x"]-camera,e["y"]-10,e["hp"]*12,6))

    # Sprite PLAYER
    sprite=PLAYER_IDLE
    if not player["grounded"]:sprite=PLAYER_JUMP
    elif keys[pygame.K_a] or keys[pygame.K_d]:
        sprite=PLAYER_RUN[(player["frame"]//10)%2]; player["frame"]+=1

    if player["facing"]==-1: sprite=pygame.transform.flip(sprite,True,False)

    scale=1.4 if ability else 1
    spr=pygame.transform.scale(sprite,(int(32*scale),int(48*scale)))
    window.blit(spr,(player["x"]-camera,player["y"]-(48*scale-48)))

    if attack:
        pygame.draw.rect(window,(255,255,255),
            (player["x"]+30*player["facing"]-camera,player["y"]+15,45,15))

    if dash:
        pygame.draw.rect(window,(255,255,255),(player["x"]-camera+6*player["facing"],player["y"]+12,25,8))

    pygame.draw.rect(window,(255,0,0),(20,50,player["hp"]*40,12))
    window.blit(FONT.render(f"Coins : {player['coins']}",True,(0,0,0)),(20,15))
    window.blit(FONT.render("ABILITY ACTIVE" if ability else ("READY (K)" if player["coins"]>=5 else "NEED 5 COIN"),True,(0,0,0)),(20,80))

    pygame.display.update()
