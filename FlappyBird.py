import math
import os,sys
from random import randint
from collections import deque
import pygame
from pygame.locals import *

FPS = 60
ANIMATION_SPEED = 0.18
WIN_WIDTH = 392*2
WIN_HEIGHT = 511


class Bird(pygame.sprite.Sprite):
    # flappy bird's everything

    WIDTH = 70
    HEIGHT = 70
    SINK_SPEED = 0.18
    CLIMB_SPEED = 0.20
    CLIMB_DURATION = 333.3

    def __init__(self, x, y, msec_to_climb, images):

        # x,y = flappy birds initial position

        super(Bird, self).__init__()
        self.x, self.y = x, y
        self.msec_to_climb = msec_to_climb
        self._img_wingup, self._img_wingdown = images
        self._mask_wingup = pygame.mask.from_surface(self._img_wingup)
        self._mask_wingdown = pygame.mask.from_surface(self._img_wingdown)

    def update(self, delta_frames=1):
        # update flappy birds current position

        if self.msec_to_climb > 0:
            frac_climb_done = 1 - self.msec_to_climb/Bird.CLIMB_DURATION
            self.y -= (Bird.CLIMB_SPEED * frames_to_msec(delta_frames) *
                       (1 - math.cos(frac_climb_done * math.pi)))
            self.msec_to_climb -= frames_to_msec(delta_frames)
        else:
            self.y += Bird.SINK_SPEED * frames_to_msec(delta_frames)



    @property
    def image(self):
        # make bird fly (wing up down)

        if pygame.time.get_ticks() % 500 >= 250:
            return self._img_wingup
        else:
            return self._img_wingdown



    @property
    def mask(self):
        # collision detection
        # something said about bitmask** study

        if pygame.time.get_ticks() % 500 >= 250:
            return self._mask_wingup
        else:
            return self._mask_wingdown

    @property
    def rect(self):
        return Rect(self.x, self.y, Bird.WIDTH, Bird.HEIGHT)


class PipePair(pygame.sprite.Sprite):
    # making pipe pairs on screen as obstacle

    WIDTH = 60
    PIECE_HEIGHT = 24
    ADD_INTERVAL = 2500

    def __init__(self, pipe_end_img, pipe_body_img):
        # creating random pipe pairs

        self.x = float(WIN_WIDTH - 1)
        self.score_counted = False

        self.image = pygame.Surface((PipePair.WIDTH, WIN_HEIGHT), SRCALPHA)
        self.image.convert()
        self.image.fill((0, 0, 0, 0))
        total_pipe_body_pieces = int(
            (WIN_HEIGHT -
             3 * Bird.HEIGHT -
             3 * PipePair.PIECE_HEIGHT) /
            PipePair.PIECE_HEIGHT
        )
        self.bottom_pieces = randint(1, total_pipe_body_pieces)
        self.top_pieces = total_pipe_body_pieces - self.bottom_pieces

        # pipe down

        for i in range(1, self.bottom_pieces + 1):
            piece_pos = (0, WIN_HEIGHT - i*PipePair.PIECE_HEIGHT)
            self.image.blit(pipe_body_img, piece_pos)

        bottom_pipe_end_y = WIN_HEIGHT - self.bottom_height_px
        bottom_end_piece_pos = (0, bottom_pipe_end_y - PipePair.PIECE_HEIGHT)
        self.image.blit(pipe_end_img, bottom_end_piece_pos)

        # pipe up
        for i in range(self.top_pieces):
            self.image.blit(pipe_body_img,(0, i * PipePair.PIECE_HEIGHT))

        top_pipe_end_y = self.top_height_px
        self.image.blit(pipe_end_img,(0, top_pipe_end_y))

        self.top_pieces += 1
        self.bottom_pieces += 1

        self.mask = pygame.mask.from_surface(self.image)


    @property
    def top_height_px(self):
        return self.top_pieces * PipePair.PIECE_HEIGHT


    @property
    def bottom_height_px(self):
        return self.bottom_pieces * PipePair.PIECE_HEIGHT


    @property
    def visible(self):
        return -PipePair.WIDTH < self.x < WIN_WIDTH



    @property
    def rect(self):
        return Rect(self.x, 0, PipePair.WIDTH, PipePair.PIECE_HEIGHT)


    def update(self, delta_frames=1):
        # update the position of the pipe pairs
        self.x -= ANIMATION_SPEED*frames_to_msec(delta_frames)

    def collides_with(self, bird):
        # pilar er sathe bari khailo kina
        return pygame.sprite.collide_mask(self, bird)


def load_images():
    def load_image(img_file_name):
        file_name = os.path.join('.','images', img_file_name)
        img = pygame.image.load(file_name)
        img.convert()
        return img

    return {
            'background': load_image('background1.jpg'),
            'pipe-end': load_image('pipe_end1.png'),
            'pipe-body': load_image('pipe_body1.png'),
            'bird-wingup': load_image('wing_up.png'),
            'bird-wingdown': load_image('wing_down.png')
    }


def frames_to_msec(frames,fps=FPS):
    return (1000.0 * frames)/fps


def msec_to_frames(milliseconds, fps=FPS):
    return (fps * milliseconds)/1000.0


def main():
    # start here

    pygame.init()
    display_surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption('Flappy Bird new world')
    clock = pygame.time.Clock()
    score_font = pygame.font.SysFont(None, 32, bold=True)

    images = load_images()

    bird= Bird(50,int(WIN_HEIGHT/2 - Bird.HEIGHT/2), 2, (images['bird-wingup'], images['bird-wingdown']))
    pipes = deque()

    frame_clock = 0
    score = 0
    done = paused = False

    while not done:
        clock.tick(FPS)

        if not (paused or frame_clock % msec_to_frames(PipePair.ADD_INTERVAL)):
            pp = PipePair(images['pipe-end'],images['pipe-body'])
            pipes.append(pp)

        for c in pygame.event.get():
            if c.type== QUIT or (c.type ==KEYUP and c.key==K_ESCAPE):
                done = True
                break
            elif c.type == KEYUP and c.key in (K_PAUSE, K_p):
                paused = not paused
            elif c.type == MOUSEBUTTONUP or (c.type == KEYUP and
                    c.key in (K_UP, K_RETURN, K_SPACE)):
                bird.msec_to_climb = Bird.CLIMB_DURATION

        if paused:
            continue

        pipe_collision = any(p.collides_with(bird) for p in pipes)
        if pipe_collision or 0 >= bird.y or bird.y >= WIN_HEIGHT-Bird.HEIGHT:
            done = True

        for x in (0, WIN_WIDTH/2):
            display_surface.blit(images['background'],(x,0))

        while pipes and not pipes[0].visible:
            pipes.popleft()

        for p in pipes:
            p.update()
            display_surface.blit(p.image, p.rect)

        bird.update()
        display_surface.blit(bird.image, bird.rect)


        # score part

        for p in pipes:
            if p.x + PipePair.WIDTH < bird.x and not p.score_counted:
                score += 1
                p.score_counted = True

        score_surface = score_font.render(str(score), True, (255, 255, 255))
        score_x = WIN_WIDTH/2 - score_surface.get_width()/2
        display_surface.blit(score_surface, (score_x, PipePair.PIECE_HEIGHT))

        pygame.display.flip()
        frame_clock += 1

    def draw_text(text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    #print('Game over! Score: %i'% score)
    ans ="Game over! Score: "
    ans+=str(score)
    running = True
    mainClock = pygame.time.Clock()
    screen = pygame.display.set_mode((500, 400), 0, 32)
    font = pygame.font.SysFont(None, 25)
    while running:
        screen.fill((255, 255, 205))
        draw_text(ans, font, (255, 0, 0), screen, 160, 180)
        pio = "Press ESC to go back to Menu"
        draw_text(pio, font, (255, 223, 0), screen, 120, 200)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        mainClock.tick(60)


