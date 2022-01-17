import sys
import pygame
from uno import main
import sqlite3


def base():
    conn = sqlite3.connect('cards.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS cards(
                    num INT,
                    eng TEXT,
                    color INT);""")
    conn.commit()

    more = [('0', 'zero', 'blue'), ('1', 'one', 'blue'), ('2', 'two', 'blue'),
            ('3', 'three', 'blue'),
            ('4', 'four', 'blue'),
            ('5', 'five', 'blue'), ('6', 'six', 'blue'),
            ('7', 'seven', 'blue'), ('8', 'eight', 'blue'),
            ('9', 'nine', 'blue'), ('0', 'zero', 'red'), ('1', 'one', 'red'), ('2', 'two', 'red'),
            ('3', 'three', 'red'),
            ('4', 'four', 'red'),
            ('5', 'five', 'red'), ('6', 'six', 'red'),
            ('7', 'seven', 'red'), ('8', 'eight', 'red'),
            ('9', 'nine', 'red'), ('0', 'zero', 'yellow'), ('1', 'one', 'yellow'), ('2', 'two', 'yellow'),
            ('3', 'three', 'yellow'),
            ('4', 'four', 'yellow'),
            ('5', 'five', 'yellow'), ('6', 'six', 'yellow'),
            ('7', 'seven', 'yellow'), ('8', 'eight', 'yellow'),
            ('9', 'nine', 'yellow'), ('0', 'zero', 'green'), ('1', 'one', 'green'), ('2', 'two', 'green'),
            ('3', 'three', 'green'),
            ('4', 'four', 'green'),
            ('5', 'five', 'green'), ('6', 'six', 'green'),
            ('7', 'seven', 'green'), ('8', 'eight', 'green'),
            ('9', 'nine', 'green')]
    cur.executemany("INSERT INTO cards VALUES(?, ?, ?);", more)
    conn.commit()


base()
pygame.init()
pygame.key.set_repeat(200, 70)
FPS = 50
WIDTH = 949
HEIGHT = 268
STEP = 10
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Welcome to UNO')
start_button = pygame.draw.rect(screen, (0, 0, 240), (150, 20, 100, 50))
continue_button = pygame.draw.rect(screen, (0, 244, 0), (150, 160, 100, 50))
quit_button = pygame.draw.rect(screen, (244, 0, 0), (150, 230, 100, 50))


def button(screen, position, text):
    font = pygame.font.SysFont("Showcard Gothic", 50)
    text_render = font.render(text, 1, (255,215,0))
    x, y, w, h = text_render.get_rect()
    x, y = position
    pygame.draw.line(screen, (127, 24, 13), (x, y), (x + w, y), 5)
    pygame.draw.line(screen, (127, 24, 13), (x, y - 2), (x, y + h), 5)
    pygame.draw.line(screen, (127, 24, 13), (x, y + h), (x + w, y + h), 5)
    pygame.draw.line(screen, (127, 24, 13), (x + w, y + h), [x + w, y], 5)
    pygame.draw.rect(screen, (180, 0, 0), (x, y, w, h), border_radius=8)
    return screen.blit(text_render, (x, y))


def start(level):
    main(level)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = pygame.transform.scale(pygame.image.load('data/fon4.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont('Segoe UI Black', 30)
    text = font.render('Привет!', True, (255, 215, 0))
    text2 = font.render('Это UNO.', True, (255, 215, 0))
    text3 = font.render('Давай поиграем?', True, (255, 215, 0))

    textpos = (630, 10)
    textpos2 = (630, 40)
    textpos3 = (630, 70)

    screen.blit(text, textpos)
    screen.blit(text2, textpos2)
    screen.blit(text3, textpos3)

    b1 = button(screen, (710, 190), "Quit")
    b3 = button(screen, (630, 120), "HARD")
    b2 = button(screen, (780, 120), "EASY")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                key_to_start = event.key == pygame.K_s or event.key == pygame.K_RIGHT or event.key == pygame.K_UP
                if key_to_start:
                    start('easy')
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b1.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                elif b2.collidepoint(pygame.mouse.get_pos()):
                    start('easy')
                elif b3.collidepoint(pygame.mouse.get_pos()):
                    start('hard')
        pygame.display.flip()
        clock.tick(FPS)


start_screen()
running = True
while running:
    WIDTH, HEIGHT = pygame.display.get_window_size()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            terminate()
    screen.fill(pygame.Color(0, 0, 0))
    pygame.display.flip()
    clock.tick(FPS)
