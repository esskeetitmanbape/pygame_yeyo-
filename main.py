import pygame
import sys
import os

pygame.init()
width, height = 1280, 720
level_number = 'I'


class Person(pygame.sprite.Sprite):
    global level_number

    def __init__(self, x, y, level_number):
        super(Person, self).__init__()
        self.player_x = x
        self.player_y = y
        self.speed = 5
        self.level_number = level_number
        original_image = pygame.image.load(os.path.join('data', 'person.png'))
        self.image = pygame.transform.scale(original_image, (18, 44.44))
        self.rect = self.image.get_rect()
        self.rect.center = (self.player_x, self.player_y)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if self.player_x > 20:  # Проверка, чтобы игрок не вышел за левую стену
                self.player_x -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if level_number == 'I':
                if self.player_x == 1260 and 410 < self.player_y < 420:
                    self.player_x = 10
                    self.level_number = 'II'
                    level_text.update(self.level_number)
                else:
                    if self.player_x < width - 20:  # Проверка, чтобы игрок не вышел за правую стену с условием уровня под номером I
                        self.player_x += self.speed
            else:
                if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                    if self.player_x < width - 20:  # Проверка, чтобы игрок не вышел за правую стену
                        self.player_x += self.speed
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            if self.player_y > 33:  # Проверка, чтобы игрок не вышел за верхнюю стену
                self.player_y -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            if self.player_y < height - 33:  # Проверка, чтобы игрок не вышел за нижнюю стену
                self.player_y += self.speed
        if keys[pygame.K_q]:
            print(self.player_x, self.player_y)
            print(self.level_number)
        self.rect.center = (self.player_x, self.player_y)


class LevelText(pygame.sprite.Sprite):
    def __init__(self, font, level_number):
        super().__init__()
        self.font = font
        self.level_number = level_number
        self.color = (199, 24, 149)
        self.rendered_text = self.font.render(f"Уровень {self.level_number}",
                                              True, self.color)
        self.rect = self.rendered_text.get_rect(center=(1280 // 2, 30))

    def update(self, level_number):
        self.level_number = level_number
        self.rendered_text = self.font.render(f"Уровень {self.level_number}",
                                              True, self.color)
        self.rect = self.rendered_text.get_rect(center=(1280 // 2, 30))

    def draw(self, screen):
        screen.blit(self.rendered_text, self.rect.topleft)


class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(NPC, self).__init__()
        self.npc_x = x
        self.npc_y = y
        original_image = pygame.image.load(os.path.join('data', 'npc.png'))
        self.image = pygame.transform.scale(original_image, (18, 44.44))
        self.rect = self.image.get_rect()
        self.rect.center = (self.npc_x, self.npc_y)

        self.dialogue_text = "YEYO!, я NPC! Нажми пробел, чтобы поговорить со мной."
        self.font = pygame.font.Font(None, 18)
        self.text_surface = self.font.render(self.dialogue_text, True,
                                             (199, 24, 149))
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.midtop = (self.npc_x, self.npc_y - 30)

        self.show_dialogue = False  # Переменная для отображения диалога

    def update(self, player_rect):
        # Проверка расстояния между игроком и NPC
        distance = pygame.math.Vector2(self.rect.center).distance_to(
            player_rect.center)

        # Отображение диалога, если игрок достаточно близко (например, расстояние менее 50 пикселей)
        self.show_dialogue = distance < 50

        # Обновление положения rect
        self.rect.topleft = (self.npc_x, self.npc_y)

    def draw_dialogue(self, screen):
        if self.show_dialogue:
            pygame.draw.rect(screen, (0, 0, 0),
                             (self.npc_x - 150, self.npc_y - 50, 0, 100))
            screen.blit(self.text_surface, self.text_rect.topleft)


def draw_cursor(screen):
    original_image = pygame.image.load(os.path.join('data', 'cursor.png'))
    image = pygame.transform.scale(original_image, (40, 40))
    mouse_x, mouse_y = pygame.mouse.get_pos()
    screen.blit(image, (mouse_x, mouse_y))


def walls(level_number):
    if level_number == 'I':
        pygame.draw.rect(screen, (199, 24, 149), (0, 0, width, 10))
        pygame.draw.rect(screen, (199, 24, 149), (0, height - 10, width, 10))
        pygame.draw.rect(screen, (199, 24, 149), (0, 0, 10, height))
        pygame.draw.rect(screen, (199, 24, 149), (width - 10, 0, 10, height))
    elif level_number == 'II':
        pygame.draw.rect(screen, (255, 255, 255), (0, 0, width, 10))
        pygame.draw.rect(screen, (255, 255, 255), (0, height - 10, width, 10))
        pygame.draw.rect(screen, (255, 255, 255), (0, 0, 10, height))
        pygame.draw.rect(screen, (255, 255, 255), (width - 10, 0, 10, height))


if __name__ == '__main__':
    width, height = 1280, 720
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('SYSTEM 3RASE')
    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 36)  # Шрифт и размер текста
    text_color = (199, 24, 149)  # Цвет текста

    level_text = LevelText(font, level_number)

    all_sprites = pygame.sprite.Group()
    person_group = pygame.sprite.Group()
    npc_group = pygame.sprite.Group()
    level_walls_group = pygame.sprite.Group()

    person = Person(1250, 415, level_number)
    person_group.add(person)
    all_sprites.add(person)

    npc = NPC(200, 200)
    npc_group.add(npc)
    all_sprites.add(npc)


    pygame.mouse.set_visible(False)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if npc.show_dialogue:
                    print("NPC говорит:", npc.dialogue_text)
            elif event.type == pygame.KEYDOWN:
                if level_number:
                    level_text.update(level_number)

        person_group.update()
        npc.update(person.rect)

        screen.fill((0, 0, 0))

        level_text.draw(screen)
        all_sprites.draw(screen)
        npc.draw_dialogue(screen)
        draw_cursor(screen)
        walls(level_number)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()