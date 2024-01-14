import pygame
import sys
import os
from random import randint

pygame.init()
pygame.mixer.init()

# Константы
width, height = 1200, 800
PLAYER_WIDTH, PLAYER_HEIGHT = 18, 44
BOSS_WIDTH, BOSS_HEIGHT = 160, 90
TARGET_WIDTH, TARGET_HEIGHT = 30, 30
CURSOR_SIZE = 40

walk_sound = pygame.mixer.Sound(os.path.join('data', 'sound', 'walk.wav'))
death_sound = pygame.mixer.Sound(os.path.join('data', 'sound', 'death.wav'))
hit_hurt_sound = pygame.mixer.Sound(os.path.join('data', 'sound', 'hitHurt.wav'))
win_sound = pygame.mixer.Sound(os.path.join('data', 'sound', 'win.wav'))

# Глобальные переменные
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Error')
clock = pygame.time.Clock()

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super(Tile, self).__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Person(pygame.sprite.Sprite):
    last_play_time = 0

    def __init__(self, x, y, max_health=100):
        super(Person, self).__init__()
        self.speed = 5
        original_image = pygame.image.load(os.path.join('data', 'person.png'))
        self.image = pygame.transform.scale(original_image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.max_health = max_health
        self.health = self.max_health

    def update(self, tiles_group, target_down_list):

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_a]:
            dx = -self.speed
        
        if keys[pygame.K_d]:
            dx = self.speed
        
        if keys[pygame.K_w]:
            dy = -self.speed
        
        if keys[pygame.K_s]:
            dy = self.speed

        self.rect.x += dx
        self.handle_collisions(dx, 0, tiles_group, target_down_list)

        self.rect.y += dy
        self.handle_collisions(0, dy, tiles_group, target_down_list)

        current_time = pygame.time.get_ticks()

        if keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s]:
            current_time = pygame.time.get_ticks()
            if current_time - Person.last_play_time > 200:  # 200 миллисекунд задержки
                walk_sound.play()
                Person.last_play_time = current_time
        else:
            walk_sound.stop()
       

    def handle_collisions(self, dx, dy, tiles_group, target_down_list):
        collisions = pygame.sprite.spritecollide(self, tiles_group, False)

        for collision in collisions:
            if dx > 0:
                self.rect.right = collision.rect.left
            elif dx < 0:
                self.rect.left = collision.rect.right

            if dy > 0:
                self.rect.bottom = collision.rect.top
            elif dy < 0:
                self.rect.top = collision.rect.bottom

        for target in target_down_list:
            if pygame.sprite.collide_rect(self, target):
                self.health -= 10  # Уменьшение здоровья при коллизии с падающим квадратом

                if self.health <= 0:
                    # Перезапуск игры
                    reset_game()

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Boss, self).__init__()
        original_image = pygame.image.load(os.path.join('data', 'boss.png'))
        self.image = pygame.transform.scale(original_image, (BOSS_WIDTH, BOSS_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.health = 100

class TargetDown(pygame.sprite.Sprite):
    def __init__(self):
        super(TargetDown, self).__init__()
        self.px, self.py = randint(0, width - TARGET_WIDTH), -100
        self.speed = randint(3, 15)
        self.rect = pygame.Rect(self.px, self.py, TARGET_WIDTH, TARGET_HEIGHT)
        target_down_list.append(self)
    
    def update(self):
        self.py += self.speed
        self.rect.y = self.py

        if self.rect.top > height:
            target_down_list.remove(self)

    def draw(self):
        pygame.draw.rect(screen, pygame.Color('green'), self.rect) 

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)         

def draw_cursor(screen):
    cursor_image = pygame.transform.scale(pygame.image.load(os.path.join('data', 'cursor.png')), (CURSOR_SIZE, CURSOR_SIZE))
    mouse_x, mouse_y = pygame.mouse.get_pos()
    screen.blit(cursor_image, (mouse_x, mouse_y))

def create_level():
    all_sprites = pygame.sprite.Group()
    person_group = pygame.sprite.Group()

    level = [
        "                                           ",
        "                                           ",
        "                                           ",
        "                                           ",
        "                                           ",
        "                                           ",
        "                                           ",
        "                                           ",
        "                                           ",
        "                                           ",
        "                       B                   ",
        "                                           ",
        "                                           ",
        "                                           ",
        "                                           ",
        "                                           ",
        "                                           ",
        "                                           ",
        "                                           ",
        "                 WWWWWWWWWWWWWWWWWWWW      ",
        "                 W                  W      ",
        "                 W                  W      ",
        "                 W                  W      ",
        "                 W                  W      ",
        "                 W                  W      ",
        "                 W        P         W      ",
        "                 W                  W      ",
        "                 W                  W      ",
        "                 W                  W      ",
        "                 W                  W      ",
        "                 W                  W      ",
        "                 WWWWWWWWWWWWWWWWWWWW      ",
        "                                           ",
        "                                           ",
        "                                           ",
        "                                           ",
    ]

    tiles_group = pygame.sprite.Group()
    tile_size = 22

    for row_index, row in enumerate(level):
        for col_index, tile in enumerate(row):
            x = col_index * tile_size
            y = row_index * tile_size

            if tile == "W":
                wall_image = pygame.transform.scale(pygame.image.load(os.path.join('data', 'wall.png')), (tile_size, tile_size))
                wall_tile = Tile(x, y, wall_image)
                tiles_group.add(wall_tile)
                all_sprites.add(wall_tile)

            elif tile == "P":
                person = Person(x, y)
                person_group.add(person)
                all_sprites.add(person)

            elif tile == "B":
                boss = Boss(x, y)
                all_sprites.add(boss)
                tiles_group.add(boss)

    return tiles_group, all_sprites, person_group

def draw_health_bar(screen, boss):
    # Определите размер и положение полоски здоровья
    bar_width = 200
    bar_height = 20
    bar_x = (width - bar_width) // 2
    bar_y = height - 50

    # Определите цвета для полоски здоровья
    bar_color = (0, 255, 0)  # Зеленый
    outline_color = (255, 255, 255)  # Белый

    # Вычислите ширину здоровья относительно максимального значения (здесь 100)
    health_width = (boss.health / 100) * bar_width

    # Отрисуйте рамку и заполненную часть полоски здоровья
    pygame.draw.rect(screen, outline_color, (bar_x, bar_y, bar_width, bar_height), 2)
    pygame.draw.rect(screen, bar_color, (bar_x, bar_y, health_width, bar_height))

def decrease_boss_health(boss, amount):
    boss.health -= amount
    if boss.health < 0:
        boss.health = 0
        win_sound.play()

def start_menu():
    screen.fill((0, 0, 0))  # Fill the screen with black

    # Display menu text
    font = pygame.font.Font(None, 36)
    text = font.render("Press SPACE to start", True, (0, 255, 0))
    text_rect = text.get_rect(center=(width // 2, height // 2))
    screen.blit(text, text_rect)

    pygame.display.flip()

def reset_game():
    global person, target_down_list, game_active
    person = Person(0, 0)
    boss.health = 100
    target_down_list = []
    game_active = True
    death_sound.play()

def victory_menu():
    screen.fill((0, 0, 0))  # Fill the screen with black

    # Display victory text
    font = pygame.font.Font(None, 36)
    text = font.render("You defeated the boss! Press SPACE to play again", True, (0, 255, 0))
    text_rect = text.get_rect(center=(width // 2, height // 2))
    screen.blit(text, text_rect)

    pygame.display.flip()

person = Person(0, 0)
target_down_list = []

boss = Boss(0, 0)

pygame.mouse.set_visible(False)

tiles_group, all_sprites, person_group = create_level()

timer_down1 = 60
timer_down2 = 30

running = True
game_active = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and game_active:
            if event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()
                for target in target_down_list:
                    if target.is_clicked(mouse_pos):
                        boss.health -= 20
                        target_down_list.remove(target)
                        hit_hurt_sound.play()
        elif event.type == pygame.KEYDOWN and not game_active:
            if event.key == pygame.K_SPACE:
                reset_game()

    if game_active:
        if person.health <= 0:
            if boss.health > 0:
                reset_game()

        if boss.health <= 0:
            game_active = False
            win_sound.play()
            #victory_menu()

        if timer_down1 > 0:
            timer_down1 -= 1
        else:
            target_down1 = TargetDown()
            timer_down1 = randint(10, 30)

        if timer_down2 > 0:
            timer_down2 -= 1
        else:
            target_down2 = TargetDown()
            timer_down2 = randint(5, 15)

        for target in target_down_list:
            target.update()

        person_group.update(tiles_group, target_down_list)
        boss.update()

        screen.fill((0, 0, 0))

        for target in target_down_list:
            target.draw()

        tiles_group.draw(screen)
        all_sprites.draw(screen)
        draw_health_bar(screen, boss) 

        draw_cursor(screen)

    else:
        start_menu()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
