import pygame
import sys

# Инициализация Pygame
pygame.init()

# Параметры окна
WIDTH, HEIGHT = 800, 400
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bubble Mario")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Частота кадров
FPS = 60
clock = pygame.time.Clock()

# Загрузка спрайтов
bubble_image = pygame.Surface((40, 40), pygame.SRCALPHA)
pygame.draw.circle(bubble_image, BLUE, (20, 20), 20)

ground_image = pygame.Surface((WIDTH, 40))
ground_image.fill(GREEN)

obstacle_image = pygame.Surface((40, 40))
obstacle_image.fill(RED)

# Игровые классы
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bubble_image
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = HEIGHT - 100
        self.velocity_y = 0
        self.on_ground = False

    def update(self):
        keys = pygame.key.get_pressed()

        # Горизонтальное движение
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

        # Прыжок
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = -15
            self.on_ground = False

        # Гравитация
        self.velocity_y += 1
        self.rect.y += self.velocity_y

        # Ограничение экрана
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > WIDTH - self.rect.width:
            self.rect.x = WIDTH - self.rect.width

        # Проверка столкновения с землей
        if self.rect.y >= HEIGHT - 80:
            self.rect.y = HEIGHT - 80
            self.velocity_y = 0
            self.on_ground = True

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = obstacle_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x -= 5
        if self.rect.x < -40:
            self.rect.x = WIDTH

# Создание игровых объектов
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

obstacles = pygame.sprite.Group()
for i in range(3):
    obstacle = Obstacle(WIDTH + i * 200, HEIGHT - 80)
    all_sprites.add(obstacle)
    obstacles.add(obstacle)

# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление объектов
    all_sprites.update()

    # Проверка столкновений
    if pygame.sprite.spritecollide(player, obstacles, False):
        print("Game Over")
        running = False

    # Отрисовка
    SCREEN.fill(WHITE)
    SCREEN.blit(ground_image, (0, HEIGHT - 40))
    all_sprites.draw(SCREEN)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
