import pygame
import sys
import json

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
PLAYER_SPEED = 5  # Скорость игрока

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Создание окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Летающий персонаж")
clock = pygame.time.Clock()

# Класс персонажа
class Player:
    def __init__(self):
        self.image = pygame.image.load("player.png").convert_alpha()  # Загрузка изображения
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.velocity_x = 0  # Горизонтальная скорость
        self.velocity_y = 0  # Вертикальная скорость

    def update(self, obstacles):
        keys = pygame.key.get_pressed()

        # Управление движением
        if keys[pygame.K_LEFT]:
            self.velocity_x = -PLAYER_SPEED
        elif keys[pygame.K_RIGHT]:
            self.velocity_x = PLAYER_SPEED
        else:
            self.velocity_x = 0  # Останавливаем движение по горизонтали, если клавиши не нажаты

        if keys[pygame.K_UP]:
            self.velocity_y = -PLAYER_SPEED
        elif keys[pygame.K_DOWN]:
            self.velocity_y = PLAYER_SPEED
        else:
            self.velocity_y = 0  # Останавливаем движение по вертикали, если клавиши не нажаты

        # Обновление позиции
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # Проверка на столкновение с препятствиями
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle):
                # Возвращаем персонажа на предыдущую позицию при столкновении
                self.rect.x -= self.velocity_x
                self.rect.y -= self.velocity_y

# Класс кнопки
class Button:
    def __init__(self, text, x, y, width, height, color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen):
        # Отрисовка кнопки
        pygame.draw.rect(screen, self.color, self.rect)

        # Текст кнопки
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# Функция для загрузки уровня из JSON
def load_level(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)

# Функция для отрисовки уровня
def draw_level(level_data, player):
    # Отрисовка фона
    if level_data["background"] == "black":
        screen.fill(BLACK)  # Заливаем фон черным цветом
    else:
        background = pygame.image.load(level_data["background"])
        screen.blit(background, (0, 0))

    # Отрисовка внешней стенки как цельного прямоугольника
    grid = level_data["grid"]
    tile_size = level_data["tile_size"]
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Уменьшаем размеры рамки
    outer_wall_rect = pygame.Rect(0, 0, cols * tile_size, rows * tile_size)
    pygame.draw.rect(screen, WHITE, outer_wall_rect, 5)  # Толщина рамки 5 пикселей

    # Отрисовка внутренних стен
    wall_inner = pygame.image.load(level_data["wall"])
    obstacles = []  # Список для хранения препятствий
    for y, row in enumerate(grid):
        for x, tile in enumerate(row):
            if tile == 2:  # Внутренняя стена
                screen.blit(wall_inner, (x * tile_size, y * tile_size))
                obstacles.append(pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size))  # Добавляем препятствие

    # Отрисовка персонажа
    screen.blit(player.image, player.rect)

    return obstacles  # Возвращаем список препятствий

# Основной игровой цикл
def main():
    running = True
    current_level = None  # Текущий уровень (None — меню, "easy" — легкий уровень, "hard" — сложный уровень)

    # Создание кнопок
    button_easy = Button("Легкий", 300, 200, 200, 50, GRAY)
    button_hard = Button("Сложный", 300, 300, 200, 50, GRAY)

    # Персонаж
    player = Player()

    while running:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if current_level is None:  # Если мы в меню
                    if button_easy.is_clicked(mouse_pos):
                        current_level = load_level("level_easy.json")  # Загружаем легкий уровень
                    if button_hard.is_clicked(mouse_pos):
                        current_level = load_level("level_hard.json")  # Загружаем сложный уровень

        # Обновление персонажа
        if current_level is not None:
            obstacles = draw_level(current_level, player)
            player.update(obstacles)

        # Отрисовка
        screen.fill(WHITE)

        if current_level is None:
            # Отрисовка меню
            button_easy.draw(screen)
            button_hard.draw(screen)
        else:
            # Отрисовка уровня
            draw_level(current_level, player)

        # Обновление экрана
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()