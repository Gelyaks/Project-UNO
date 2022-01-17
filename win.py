import pygame
import random

screen_rect = (0, 0, 741, 800)
all_sprites = pygame.sprite.Group()


class Particle(pygame.sprite.Sprite):
    fire = [pygame.image.load("data/fire.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = 0.1

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position):
    particle_count = 20
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


def win():
    sc_width, sc_height = 741, 800
    screen = pygame.display.set_mode((sc_width, sc_height))
    pygame.display.set_caption('You won!')
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit()
        create_particles((370, 100))

        all_sprites.update()
        screen.fill((0, 0, 0))
        fon = pygame.image.load('data/fon1.png')
        screen.blit(fon, (0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == '__main__':
    win()