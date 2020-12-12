import os, sys, pygame, random, array, gamemode, FlappyBird
import MAIN,spacein
import direction, bounds, timeout, menu
from pygame.locals import *

# Import game modules.
from loader import load_image
import player, maps, traffic, camera, tracks

mainClock = pygame.time.Clock()
from pygame.locals import *

bg = pygame.image.load('images\gm.jpg')
pygame.init()
pygame.display.set_caption('game base')
screen = pygame.display.set_mode((500, 400), 0, 32)

font = pygame.font.SysFont('Helvetica', 20)


def draw_text(text, font, color, surface, x, y):
	textobj = font.render(text, 1, color)
	textrect = textobj.get_rect()
	textrect.topleft = (x, y)
	surface.blit(textobj, textrect)


def addText(piu, x, y):
	screen.blit(font.render(piu, True, (0, 0, 0)), (x, y))
	pygame.display.update()


click = False


def main_menu():
	global click
	while True:

		screen.fill((0, 0, 0))
		screen.blit(bg,(0, 0))

		draw_text('PLAY !!', font, (255, 0, 0), screen, 220, 180)
		mx, my = pygame.mouse.get_pos()

		button_1 = pygame.Rect(70, 80, 150, 50)
		button_2 = pygame.Rect(70, 250, 150, 50)
		button_3 = pygame.Rect(290, 80, 150, 50)
		button_4 = pygame.Rect(290, 250, 150, 50)

		if button_1.collidepoint((mx, my))== True:
			if click:
				FlappyBird.main()
		if button_2.collidepoint((mx, my)):
			if click:
				import angry

		if button_3.collidepoint((mx, my)):
			if click:
				MAIN.main()
		if button_4.collidepoint((mx, my)):
			if click:
				spacein.main()

		pygame.draw.rect(screen, (255, 203, 0), button_1)
		addText('Flappy Bird', 80, 90)
		pygame.draw.rect(screen, (255, 203, 0), button_2)
		addText('Angry Bird', 80, 260)
		pygame.draw.rect(screen, (255, 203, 0), button_3)
		addText('Apple Race', 300, 90)
		pygame.draw.rect(screen, (255, 203, 0), button_4)
		addText('Space Invader', 300, 260)

		click = False
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True

		pygame.display.update()
		mainClock.tick(60)

main_menu()
