import pygame
import sys
import os

pygame.init()

class Person(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Person, self).__init__()
        self.player_x = x
        self.player_y = y
        self.speed = 5
        original_image = pygame.image.load(os.path.join('data', 'person.png'))
        self.image = pygame.transform.scale(original_image, (18, 44.44))
        self.rect = self.image.get_rect()
        self.rect.center = (self.player_x, self.player_y)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.player_x -= self.speed
        if keys[pygame.K_d]:
            self.player_x += self.speed
        if keys[pygame.K_w]:
            self.player_y -= self.speed
        if keys[pygame.K_s]:
            self.player_y += self.speed
        self.rect.center = (self.player_x, self.player_y)

class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(NPC, self).__init__()
        self.npc_x = x
        self.npc_y = y
        original_image = pygame.image.load(os.path.join('data', 'npc.png'))
        self.image = pygame.transform.scale(original_image, (18, 44.44))
        self.rect = self.image.get_rect()
        self.rect.center = (self.npc_x, self.npc_y)

        self.dialogue_text = "Привет, я NPC! Нажми пробел, чтобы поговорить со мной."
        self.font = pygame.font.Font(None, 18)
        self.text_surface = self.font.render(self.dialogue_text, True, (0, 255, 0))
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.midtop = (self.npc_x, self.npc_y - 30)

        self.show_dialogue = False  # Переменная для отображения диалога

    def update(self, player_rect):
        # Проверка расстояния между игроком и NPC
        distance = pygame.math.Vector2(self.rect.center).distance_to(player_rect.center)

        # Отображение диалога, если игрок достаточно близко (например, расстояние менее 50 пикселей)
        self.show_dialogue = distance < 50

        # Обновление положения rect
        self.rect.topleft = (self.npc_x, self.npc_y)

    def draw_dialogue(self, screen):
        if self.show_dialogue:
            pygame.draw.rect(screen, (0, 0, 0), (self.npc_x - 150, self.npc_y - 50, 0, 100))
            screen.blit(self.text_surface, self.text_rect.topleft)


def draw_cursor(screen):
    original_image = pygame.image.load(os.path.join('data', 'cursor.png'))
    image = pygame.transform.scale(original_image, (40, 40))
    mouse_x, mouse_y = pygame.mouse.get_pos()
    screen.blit(image, (mouse_x, mouse_y))


if __name__ == '__main__':
    width, height = 1200, 800
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Error')
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    person_group = pygame.sprite.Group()
    npc_group = pygame.sprite.Group()

    person = Person(width, height)
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
                    print("NPC говорит: ", npc.dialogue_text)

        person_group.update()
        npc.update(person.rect)

        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        npc.draw_dialogue(screen)
        draw_cursor(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()
