import pygame
import random
import math
from pygame import mixer

def main():
    pygame.init()
    disp = pygame.display.set_mode([800, 600])
    bullet = mixer.Sound("bullet.wav")
    collision = mixer.Sound("collision.wav")
    # background
    backg = pygame.image.load("back6.jpg")
    mixer.music.load("background.mp3")
    mixer.music.play(-1)
    # player
    img1 = pygame.image.load("space3.png")
    px = 20
    py = 480
    px_change = 0
    py_change = 0

    # for enemy
    img2 = []
    ex = []
    ey = []
    ey_change = []

    for i in range(0, 5):
        img2.append(pygame.image.load("alien3.png"))
        ex.append(random.randint(50, 750))
        ey.append(random.randint(20, 100))
        ey_change.append(0.065)

    # for bullet
    img3 = pygame.image.load("bullet1.png")
    bx = 0
    by = 480
    by_change = 0
    state = 0

    # score
    score_value = 0
    score_font = pygame.font.SysFont("comicsansms", 35)

    # game over
    over_font = pygame.font.SysFont("comicsansms", 70)

    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                px_change = -1
                py_change = 0

            elif event.key == pygame.K_RIGHT:
                px_change = 1
                py_change = 0
            elif event.key == pygame.K_UP:
                if state == 0:
                    bullet.play()
                    bx = px
                    state = 1
                    by_change = -30

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                px_change = 0
                py_change = 0

        px = px + px_change  # player er jayga change

        by = by + by_change  # bulleter jayga change

        if px > 736:
            px = 736
        if px < 0:
            px = 0

        disp.fill((0, 0, 0))
        disp.blit(backg, (0, 0))
        if state == 1:
            disp.blit(img3, (bx + 16, by))
            if by <= 0:
                by = 480
                state = 0

        for i in range(0, 5):
            if ey[i] >= 480:
                over = over_font.render("GAME OVER :(", True, (192, 192, 192))
                disp.blit(over, (300, 500))
                for j in range(0, 5):
                    ey[j] = 2000
            distance = math.sqrt(((bx - ex[i]) ** 2) + ((by - ey[i]) ** 2))
            if distance < 25:
                collision.play()
                ex[i] = random.randint(50, 750)
                ey[i] = random.randint(20, 100)
                score_value += 1
            ey[i] = ey[i] + ey_change[i]  # alien er jayga change
            score = score_font.render("SCORE:" + str(score_value), True, (192, 192, 192))
            disp.blit(score, (10, 10))
            disp.blit(img2[i], (ex[i], ey[i]))
        disp.blit(img1, (px, py))
        pygame.display.flip()

    screen = pygame.display.set_mode((500, 400), 0, 32)

