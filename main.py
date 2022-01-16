import os
import sys
import pygame
from easy import main, base
from hard import main1

pygame.init()
pygame.key.set_repeat(200, 70)
FPS = 50
WIDTH = 949
HEIGHT = 268
STEP = 10
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('UNO')
start_button = pygame.draw.rect(screen, (0, 0, 240), (150, 20, 100, 50))
continue_button = pygame.draw.rect(screen, (0, 244, 0), (150, 160, 100, 50))
quit_button = pygame.draw.rect(screen, (244, 0, 0), (150, 230, 100, 50))


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


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


def start():
    base()
    main()


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = pygame.transform.scale(load_image('fon4.png'), (WIDTH, HEIGHT))
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
                    start()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b1.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                elif b2.collidepoint(pygame.mouse.get_pos()):
                    start()
                elif b3.collidepoint(pygame.mouse.get_pos()):
                    main1()
        pygame.display.flip()
        clock.tick(FPS)


start_screen()


# Главный Игровой цикл
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
