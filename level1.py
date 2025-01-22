import pygame
import sys

# Инициализация pygame
pygame.init()

# Размеры экрана
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mini Mario with Platforms")

# Загрузка фона
background = pygame.image.load("фонлес.jpg").convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)

# Частота обновления экрана
clock = pygame.time.Clock()
FPS = 60

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png").convert_alpha()  # Загрузка изображения
        self.image = pygame.transform.scale(self.image, (50, 50))  
        self.rect = self.image.get_rect()
        self.rect.topleft = (50, SCREEN_HEIGHT - 80)
        self.speed = 5
        self.gravity = 1
        self.jump_speed = -15
        self.velocity_y = 0
        self.is_jumping = False

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.velocity_y = self.jump_speed
            self.is_jumping = True

        # Гравитация
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Проверка на платформы
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            self.rect.bottom = hits[0].rect.top
            self.is_jumping = False
            self.velocity_y = 0

        # Проверка на землю
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.is_jumping = False

# Класс шипов
class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("шипы.png").convert_alpha()  # Загрузка изображения
        self.image = pygame.transform.scale(self.image, (50, 50)) 
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Класс финиша
class Finish(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Класс платформы
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Создание спрайтов
player = Player()
spikes = pygame.sprite.Group()
platforms = pygame.sprite.Group()
finish = Finish(SCREEN_WIDTH - 60, SCREEN_HEIGHT - 80)

# Добавление шипов
for i in range(5):
    spike = Spike(300 + i * 200, SCREEN_HEIGHT - 50)
    spikes.add(spike)

# Добавление платформ
platform_data = [
    (200, SCREEN_HEIGHT - 150, 100, 20),
    (400, SCREEN_HEIGHT - 200, 100, 20),
    (600, SCREEN_HEIGHT - 250, 150, 20),
    (800, SCREEN_HEIGHT - 300, 100, 20),
    (1000, SCREEN_HEIGHT - 350, 200, 20)
]
for x, y, width, height in platform_data:
    platform = Platform(x, y, width, height)
    platforms.add(platform)

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(spikes)
all_sprites.add(platforms)
all_sprites.add(finish)

# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление
    all_sprites.update()

    # Проверка столкновений с шипами
    if pygame.sprite.spritecollideany(player, spikes):
        print("Game Over!")
        running = False

    # Проверка на финиш
    if pygame.sprite.collide_rect(player, finish):
        print("You Win!")
        running = False

    # Отрисовка
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
