import pygame
import random
from pygame import mixer

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Space Invaders")


mixer.music.load('background.wav')
mixer.music.play(-1)


img = pygame.image.load('ufo.png')
pygame.display.set_icon(img)

# Player
player_img = pygame.image.load('space-invaders.png')
X = 370
Y = 460
Player_img = pygame.transform.scale(player_img, (64, 64))
change = 0

num_of_enemies = 6

enemy_img = pygame.image.load('space-ship.png')
Enem = []
Enemy_X = []
Enemy_Y = []
Enemy_X_Change = []
Enemy_Y_Change = []
num_of_enemies = random.randint(1, 12)

for i in range(num_of_enemies):
    Enem.append(pygame.transform.scale(enemy_img, (64, 64)))
    Enemy_X.append(random.randint(0, 735))
    Enemy_Y.append(random.randint(50, 150))
    Enemy_X_Change.append(4)
    Enemy_Y_Change.append(30)

bg_img = pygame.image.load('Bg.jpg')
Background = pygame.transform.scale(bg_img, (800, 600))

bullet = pygame.image.load('bullet.png')
Bullet = pygame.transform.scale(bullet, (32, 32))
Bullet_X = 0
Bullet_Y = 460
Bullet_Y_Change = 10
bullet_state = 'ready'

score_val = 0
font = pygame.font.Font('freesansbold.ttf', 32)
Text_X = 10
Text_Y = 10

game_over_font = pygame.font.Font('freesansbold.ttf',64)

def player(x, y):
    screen.blit(Player_img, (x, y))


def game_over_text():
    over = game_over_font.render(" GAME OVER ",True,(0,0,0))
    screen.blit(over,(200,250))

def enemy(x, y, i):
    screen.blit(Enem[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(Bullet, (x + 16, y + 10))


def Show_Score(x, y):
    score = font.render('Score:' + str(score_val), True, (255, 255, 255))
    screen.blit(score, (x,y))

def collision(x1, y1, x2, y2):
    distance = (((x2 - x1) ** 2) + ((y2 - y1) ** 2)) ** 0.5
    if distance < 27:
        return True
    else:
        return False


# The game loop
run = True
while run:

    screen.fill((255, 255, 255))

    screen.blit(Background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                change = -5
            if event.key == pygame.K_RIGHT:
                change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound= mixer.Sound('laser.wav')
                    bullet_sound.play()
                    Bullet_X = X
                    fire_bullet(Bullet_X, Bullet_Y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                change = 0

    X += change

    if X <= 0:
        X = 0
    elif X >= 736:
        X = 736

    for i in range(num_of_enemies):

        if Enemy_Y[i] > 440:
            for j in range(num_of_enemies):
                Enemy_Y[j]=2000
            game_over_text()
            break

        Enemy_X[i] += Enemy_X_Change[i]
        if Enemy_X[i] <= 0:
            Enemy_X_Change[i] = 3
            Enemy_Y[i] += Enemy_Y_Change[i]
        elif Enemy_X[i] >= 736:
            Enemy_X_Change[i] = -3
            Enemy_Y[i] += Enemy_Y_Change[i]
        Col = collision(Enemy_X[i], Enemy_Y[i], Bullet_X, Bullet_Y)

        if Col:
            exp_sound = mixer.Sound('explosion.wav')
            exp_sound.play()
            Bullet_Y = 460
            bullet_state = 'ready'
            score_val += 1
            Enemy_X[i] = random.randint(0, 735)
            Enemy_Y[i] = random.randint(50, 150)
            Show_Score(Text_X,Text_Y)
            
        enemy(Enemy_X[i], Enemy_Y[i], i)

    if Bullet_Y <= 0:
        Bullet_Y = 460
        bullet_state = 'ready'

    if bullet_state == 'fire':
        fire_bullet(Bullet_X, Bullet_Y)
        Bullet_Y -= Bullet_Y_Change

    Show_Score(Text_X, Text_Y)
    player(X, Y)
    pygame.display.update()
