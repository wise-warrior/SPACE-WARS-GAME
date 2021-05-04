import pygame as pg
import random as rd
import math
from pygame import mixer

# initialise pygame
pg.init()
clock = pg.time.Clock()


# create the Screen
screen = pg.display.set_mode((800,600))
pg.display.set_caption(" SPACE WARS ")
icon = pg.image.load('ufo.png')
pg.display.set_icon(icon)


# Player Display on Screen
player = pg.image.load('player new mod.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy Display on Screen
enemy = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 6
for i in range (no_of_enemies) :
    enemy.append(pg.image.load('new enemy.png'))
    enemyX.append(rd.randint(0, 735))
    enemyY.append(rd.randint(10, 90))
    enemyX_change.append(1.5)
    enemyY_change.append(20)


# Bullet Display on Screen
# ready - u can't see the bullet on screen
# fire - bullet currently moving
Bullet = pg.image.load('bullet 3.png')
BulletX = 0
BulletY = 480
BulletX_change = 0
BulletY_change = 8
Bullet_state = "ready"

# Background
background = pg.image.load('final Background.png')

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Score
score = 0
font = pg.font.Font('freesansbold.ttf' , 32)
textX = 10
textY = 10
over_font = pg.font.Font('freesansbold.ttf' , 70)


def show_score (x,y) :
    score_val = font.render("Your Score : " + str(score) , True , (255,255,255))
    screen.blit (score_val , (x,y))

def game_over () :
    over_text  = over_font.render("GAME OVER" , True, (255, 255, 255))
    screen.blit(over_text, (200 , 250))

def players (x,y) :
    screen.blit(player , (x,y))

def enemys (x,y,i) :
    screen.blit(enemy[i] , (x,y))

def fire_bullet (x,y) :
    global Bullet_state
    Bullet_state = "fire"
    screen.blit (Bullet , (x + 32 ,y + 10))

def collision (enemyX , enemyY , BulletX , BulletY) :
    distance = math.sqrt((math.pow(enemyX - BulletX,2)) + (math.pow(enemyY - BulletY,2)))
    if distance < 27 :
        return True
    else :
        return False


# Game Loop
run = True
while run :
    # RGB = Red Green Blue
    screen.fill((0, 0, 0))
    screen.blit(background , (0,0))

    for event in pg.event.get() :
        if event.type == pg.QUIT :
            run = False

        # Player Movement based on keystrokes.
        if event.type == pg.KEYDOWN :
            if event.key == pg.K_LEFT :
                playerX_change = -4
            if event.key == pg.K_RIGHT :
                playerX_change = 4
            if event.key == pg.K_SPACE :
                if Bullet_state is "ready" :
                    Bullet_Sound = mixer.Sound('laser.wav')
                    Bullet_Sound.play()
                    BulletX = playerX
                    fire_bullet (BulletX , BulletY)

        if event.type == pg.KEYUP :
            if event.key == pg.K_LEFT or event.key  == pg.K_RIGHT :
                playerX_change = 0

    # check for player to stay inside boundary
    playerX += playerX_change
    if playerX <= 0 :
        playerX = 0
    elif playerX >= 736 :
        playerX = 736

    # Enemy Movement and score increment
    for i in range (no_of_enemies) :

        # Game Over Code
        if enemyY[i] > 440 :
            for j in range (no_of_enemies) :
                enemyY[j] = 2000
            game_over ()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0 :
            enemyX[i] = 1.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 680 :
            enemyX[i] = -1.5
            enemyY[i] += enemyY_change[i]
        # Collision Check
        collide = collision(enemyX[i], enemyY[i], BulletX, BulletY)
        if collide:
            Exp_Sound = mixer.Sound('explosion.wav')
            Exp_Sound.play()
            BulletY = 480
            Bullet_state = "ready"
            score += 1
            enemyX[i] = rd.randint(0, 735)
            enemyY[i] = rd.randint(10, 90)
        enemys(enemyX[i] , enemyY[i] , i)


    # Bullet Movement
    if BulletY <= 0 :
        BulletY = 480
        Bullet_state = "ready"


    if Bullet_state is "fire" :
        fire_bullet (BulletX , BulletY)
        BulletY -= BulletY_change



    players (playerX , playerY)
    show_score (textX , textY)
    pg.display.update()