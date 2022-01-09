# Space Invaders Full Game
# main.py

import pygame
import random
import math
from pygame import mixer
import time

running = True

pygame.init()
# initialize pygame

screen = pygame.display.set_mode((800, 600))
# create the screen, 800 wide, 600 tall

bg = pygame.image.load("bg.png")
# adding a backround
time.sleep(1.5)
# adding music
mixer.music.load("80s countdown music.mp3")
mixer.music.play(-1)

# changing the title, logo, and backround color
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)
# makes the image in the title and changes the name


playerImg = pygame.image.load("space-invaders.png")
playerX = 370
playerY = 480

playerX_change = 0
playerY_change = 0

# alien
alienImg = []
alienX = []
alienY = []
alienX_change = []
alienY_change = []
alienNum = 6

game_over_loop = False

for i in range(alienNum):
    alienImg.append(pygame.image.load("alien.png"))
    alienX.append((random.randint(0, 735)))
    alienY.append(random.randint(50, 150))
    alienX_change.append(0.4)
    alienY_change.append(60)

# create enemy that spawns at a random position within a parameter


# bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletY_change = 4
bullet_state = "ready"
# bullet_state = 'ready' means you cant see the bullet
# 'fire' state would mean the bullet is moving
# creates a bullet

# score display
global score_value
score_value = 0

font = pygame.font.Font("arial.ttf", 32)

textX = 20
textY = 20

# game over text func
go_font = pygame.font.Font("arial.ttf", 64)


def game_over_text(x, y):
    go_text = go_font.render("Game Over", True, (255, 0, 0))
    screen.blit(go_text, (x, y))


# level display func
global level
level = 0
level_font = pygame.font.Font("arial.ttf", 32)


def level_display(x, y):
    level_text = level_font.render("Level: " + str(level), True, (50, 88, 178))
    screen.blit(level_text, (x, y))


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (50, 88, 178))
    screen.blit(score, (x, y))
    global level
    if score_value in range(0, 25):
        level = 1
    elif score_value in range(26, 50):
        level = 2
    elif score_value in range(51, 100):
        level = 3
    elif score_value in range(101, 150):
        level = 4
    elif score_value in range(151, 200):
        level = 5
    elif score_value >= 201:
        level = 6


def player(x, y):
    screen.blit(playerImg, (x, y))
    # draw the image of player


def alien(x, y, i):
    screen.blit(alienImg[i], (x, y))
    # draw the image of alien


def fire_bullet(x, y):
    global bullet_state
    # makes bullet_state accessible anywhere
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))
    # draw the image of player


def is_collision(alienX, alienY, bulletX, bulletY):
    distance = math.sqrt((math.pow(alienX - bulletX, 2)) + (math.pow(alienY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


lvlup_font = pygame.font.Font("arial.ttf", 64)


def level_up(x, y):
    lvlup_text = lvlup_font.render("Level " + str(level), True, (0, 255, 0))
    screen.blit(lvlup_text, (x, y))


global timer
timer = 0
global activate_lvlup_display
activate_lvlup_display = False
level_marker = 0
# Game Loop
while running:
    screen.fill((0, 0, 0))
    # screen.fill(()) has its arg as a tuple; 3 values R, G, B
    screen.blit(bg, (0, 0))
    line_color = (100, 0, 0)
    pygame.draw.line(screen, line_color, (0, 475), (800, 475), 5)
    if level > level_marker:
        timer = 500
        activate_lvlup_display = True
    if timer >= 0 and activate_lvlup_display == True:
        level_up(285, 200)
        timer -= 1
    level_marker = level
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1.1
            elif event.key == pygame.K_RIGHT:
                playerX_change = 1.1
            elif event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("bulletsfx.mp3")
                    bullet_sound.set_volume(0.3)
                    bullet_sound.play()
                    # bullet sfx
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            playerX_change = 0

    playerX += playerX_change
    # changes the x value of the player based on the key pressed
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # alien movement
    for i in range(alienNum):
        # game over
        if alienY[i] > 440:
            for j in range(alienNum):
                alienY[j] = 2000
            game_over_text(225, 200)
            break
        # alien movement
        alienX[i] += alienX_change[i]
        if alienX[i] <= 0:
            if level == 1:
                alienX_change[i] = 0.4
            elif level == 2:
                alienX_change[i] = 0.5
            elif level == 3:
                alienX_change[i] = 0.6
            elif level == 4:
                alienX_change[i] = 0.7
            elif level == 5:
                alienX_change[i] = 0.8
            elif level == 6:
                alienX_change[i] = 1
            alienY[i] += alienY_change[i]
        elif alienX[i] >= 736:
            if level == 1:
                alienX_change[i] = -0.4
            elif level == 2:
                alienX_change[i] = -0.5
            elif level == 3:
                alienX_change[i] = -0.6
            elif level == 4:
                alienX_change[i] = -0.7
            elif level == 5:
                alienX_change[i] = -0.8
            elif level == 6:
                alienX_change[i] = -1
            alienY[i] += alienY_change[i]
        # collision
        collision = is_collision(alienX[i], alienY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.set_volume(0.2)
            explosion_sound.play()
            # explosion sfx
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            alienX[i] = random.randint(0, 735)
            alienY[i] = random.randint(50, 150)
        alien(alienX[i], alienY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    # calls the player func to draw the player
    show_score(textX, textY)
    # displays score
    level_display(650, 20)
    pygame.display.update()
    # updates the screen.
# keeps the window open until 'exit' event occurs
