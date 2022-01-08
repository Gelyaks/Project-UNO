import os
import sys
import pygame
from uno import main


pygame.init()
pygame.key.set_repeat(200, 70)
FPS = 50
WIDTH = 650
HEIGHT = 400
STEP = 10
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('UNO')
start_button = pygame.draw.rect(screen, (0, 0, 240), (150, 90, 100, 50))
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
    font = pygame.font.SysFont("Arial", 50)
    text_render = font.render(text, 1, (255, 0, 0))
    x, y, w, h = text_render.get_rect()
    x, y = position
    pygame.draw.line(screen, (150, 150, 150), (x, y), (x + w, y), 5)
    pygame.draw.line(screen, (150, 150, 150), (x, y - 2), (x, y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x, y + h), (x + w, y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x + w, y + h), [x + w, y], 5)
    pygame.draw.rect(screen, (100, 100, 100), (x, y, w, h))
    return screen.blit(text_render, (x, y))


def start():
    main()


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ['Привет!', 'Это UNO']
    fon = pygame.transform.scale(load_image('fon1.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont('Segoe Print', 20)
    text_coord = 10
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('violet'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = text_coord
        intro_rect.x = 10
        screen.blit(string_rendered, intro_rect)
        text_coord += intro_rect.height + 10
    b1 = button(screen, (400, 300), "Quit")
    b2 = button(screen, (500, 300), "Start")
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
