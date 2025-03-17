import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("player.png").convert_alpha()  # Загрузка изображения персонажа
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 0.8  # Сила гравитации
        self.speed = 5  # Скорость движения
        self.jump_speed = -15  # Скорость прыжка
        self.on_ground = False  # Флаг, указывающий, находится ли игрок на земле

    def update(self, platforms):
        # Применение гравитации
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Проверка коллизий с платформами по вертикали
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.velocity_y > 0:  # Падение вниз
                    self.rect.bottom = platform.top
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0:  # Движение вверх
                    self.rect.top = platform.bottom
                    self.velocity_y = 0

        # Движение по горизонтали
        self.rect.x += self.velocity_x

        # Проверка коллизий с платформами по горизонтали
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.velocity_x > 0:  # Движение вправо
                    self.rect.right = platform.left
                elif self.velocity_x < 0:  # Движение влево
                    self.rect.left = platform.right

    def move_left(self):
        self.velocity_x = -self.speed  # Устанавливаем скорость влево

    def move_right(self):
        self.velocity_x = self.speed  # Устанавливаем скорость вправо

    def stop(self):
        self.velocity_x = 0  # Останавливаем движение

    def jump(self):
        if self.on_ground:  # Проверяем, на земле ли игрок
            self.velocity_y = self.jump_speed  # Устанавливаем скорость прыжка
            self.on_ground = False  # Игрок больше не на земле