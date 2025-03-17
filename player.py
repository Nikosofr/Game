import pygame

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

        # Применение гравитации
        self.velocity_y += self.gravity

        # Перемещение по горизонтали
        self.rect.x += self.velocity_x
        self.check_collision(platforms, 'horizontal')

        # Перемещение по вертикали
        self.rect.y += self.velocity_y
        self.check_collision(platforms, 'vertical')

        # Ограничение движения игрока по внешней границе
        if not boundary.contains(self.rect):
            if self.rect.left < boundary.left:
                self.rect.left = boundary.left
            if self.rect.right > boundary.right:
                self.rect.right = boundary.right
            if self.rect.top < boundary.top:
                self.rect.top = boundary.top
            if self.rect.bottom > boundary.bottom:
                self.rect.bottom = boundary.bottom
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
