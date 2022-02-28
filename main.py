import os
import sys

import pygame


def load_level(filename):
    try:
        filename = "levels/" + filename
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
        max_width = max(map(len, level_map))
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))
    except Exception as e:
        print(e)
        sys.exit(0)


def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mario.png')

tile_width = tile_height = 50

FPS = 50
WIDTH = 600
HEIGHT = 600


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Управление на стрелках",
                  "Ходить можно только по клеткам с травой"]

    fon = pygame.transform.scale(load_image('bg1.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                pygame.display.flip()
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def move(self, dir):
        """ 0 - down
            1 - left
            2 - up
            3 - right"""
        test_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.w, self.rect.h)
        if dir == 0:
            test_rect.y += tile_height
        elif dir == 1:
            test_rect.x -= tile_width
        elif dir == 2:
            test_rect.y -= tile_height
        elif dir == 3:
            test_rect.x += tile_width
        bad = False
        for i in tiles_group:
            if i.image == tile_images['wall'] and i.rect.colliderect(test_rect):
                bad = True
        if not bad:
            self.rect = test_rect


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


pygame.init()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

level_name = input('Введите название уровня')

player, level_x, level_y = generate_level(load_level(level_name))

camera = Camera()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

start_screen()
screen.fill(0)
running = True
while running:
    screen.fill(0)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.move(2)
            elif event.key == pygame.K_DOWN:
                player.move(0)
            elif event.key == pygame.K_LEFT:
                player.move(1)
            elif event.key == pygame.K_RIGHT:
                player.move(3)

    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)
    all_sprites.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()

