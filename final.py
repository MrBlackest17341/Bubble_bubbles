import pygame
import random

# Инициализация pygame
pygame.init()

# Размеры экрана
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Final")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Загрузка фона
background = pygame.image.load("фон.jpg").convert()

# Частота обновления экрана
clock = pygame.time.Clock()
FPS = 60

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png").convert_alpha()  # Загрузка изображения
        self.image = pygame.transform.scale(self.image, (50, 50))    # Масштабирование, если нужно
        self.rect = self.image.get_rect()
        self.rect.center = (100, SCREEN_HEIGHT // 2)
        self.speed = 5
        self.health = 100

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

# Класс босса
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("boss.png").convert_alpha()   # Загрузка изображения
        self.image = pygame.transform.scale(self.image, (500, 200)) # Масштабирование, если нужно
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH - 100, SCREEN_HEIGHT // 2)
        self.health = 100

    def update(self):
        if self.health <= 0:
            self.kill()

# Класс пули
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("bullet.png").convert_alpha()   # Загрузка изображения
        self.image = pygame.transform.scale(self.image, (50, 50)) # Масштабирование, если нужно
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > SCREEN_WIDTH:
            self.kill()

# Класс падающих объектов
class FallingObject(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((1, 1))
        self.image = pygame.image.load("камень.png").convert_alpha()   # Загрузка изображения
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = random.randint(1, 3)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Создание спрайтов
def create_sprites():
    player = Player()
    boss = Boss()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(boss)

    bullets = pygame.sprite.Group()
    falling_objects = pygame.sprite.Group()

    return player, boss, all_sprites, bullets, falling_objects

# Основной игровой цикл
def game_loop():
    player, boss, all_sprites, bullets, falling_objects = create_sprites()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Создание пули
                    bullet = Bullet(player.rect.right, player.rect.centery)
                    all_sprites.add(bullet)
                    bullets.add(bullet)

        # Создание падающих объектов
        if random.randint(0, 100) < 2:  # Уменьшаем вероятность падения объектов
            falling_object = FallingObject()
            all_sprites.add(falling_object)
            falling_objects.add(falling_object)

        # Обновление
        all_sprites.update()

        # Проверка столкновений пуль с боссом
        hits = pygame.sprite.spritecollide(boss, bullets, True)
        for hit in hits:
            boss.health -= 10

        # Проверка столкновений игрока с падающими объектами
        hits = pygame.sprite.spritecollide(player, falling_objects, True)
        for hit in hits:
            player.health -= 10
            if player.health <= 0:
                running = False

        # Отрисовка
        screen.blit(background, (0, 0))  # Отображение фона
        all_sprites.draw(screen)

        # Отображение здоровья босса
        pygame.draw.rect(screen, (255, 0, 0), (boss.rect.left, boss.rect.top - 10, 100, 5))
        pygame.draw.rect(screen, (0, 255, 0), (boss.rect.left, boss.rect.top - 10, boss.health, 5))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

# Запуск игры
game_loop()
