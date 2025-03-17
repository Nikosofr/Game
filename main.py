import pygame
import sys
import json

pygame.init()

# Константы
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Окно игры
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Летающий персонаж")
clock = pygame.time.Clock()

# Глобальная переменная
wall_inner_img = None

# Загрузка уровня

def load_level(filename):
    global wall_inner_img
    with open(filename, encoding="utf-8") as f:
        data = json.load(f)
        wall_inner_img = pygame.image.load(data["wall"]).convert_alpha()
    return data

# Отрисовка уровня

def draw_level(level_data):
    tile_size = level_data["tile_size"]
    grid = level_data["grid"]
    boundary = pygame.Rect(0, 0, len(grid[0]) * tile_size, len(grid) * tile_size)
    pygame.draw.rect(screen, WHITE, boundary, 5)

    platforms = []
    for y, row in enumerate(grid):
        for x, tile in enumerate(row):
            if tile == 2:
                pos = (x * tile_size, y * tile_size)
                screen.blit(wall_inner_img, pos)
                platforms.append(pygame.Rect(*pos, tile_size, tile_size))

    return platforms, boundary

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("player.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 0.8
        self.speed = 5
        self.jump_speed = -15
        self.on_ground = False

    def update(self, platforms, boundary):
        keys = pygame.key.get_pressed()

        # Горизонтальное движение
        if keys[pygame.K_LEFT]:
            self.velocity_x = -self.speed
        elif keys[pygame.K_RIGHT]:
            self.velocity_x = self.speed
        else:
            self.velocity_x = 0

        # Прыжок
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = self.jump_speed
            self.on_ground = False

        # Гравитация
        self.velocity_y += self.gravity

        # Перемещение и коллизии
        self.rect.x += self.velocity_x
        self.check_collision(platforms, 'horizontal')
        self.rect.y += self.velocity_y
        self.check_collision(platforms, 'vertical')

        # Ограничение по границе
        if not boundary.contains(self.rect):
            self.rect.clamp_ip(boundary)
            self.velocity_y = 0
            self.on_ground = True

    def check_collision(self, platforms, direction):
        for platform in platforms:
            if self.rect.colliderect(platform):
                if direction == 'horizontal':
                    if self.velocity_x > 0:
                        self.rect.right = platform.left
                    elif self.velocity_x < 0:
                        self.rect.left = platform.right
                elif direction == 'vertical':
                    if self.velocity_y > 0:
                        self.rect.bottom = platform.top
                        self.velocity_y = 0
                        self.on_ground = True
                    elif self.velocity_y < 0:
                        self.rect.top = platform.bottom
                        self.velocity_y = 0

# Главная функция
def main():
    running = True
    player = Player(100, 100)
    level = load_level("level_easy.json")

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)
        platforms, boundary = draw_level(level)
        player.update(platforms, boundary)
        screen.blit(player.image, player.rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
