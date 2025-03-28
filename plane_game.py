import pygame
import random

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kintsu")

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Загрузка изображений
PLAYER_IMG = pygame.transform.scale(pygame.image.load("player.png").convert_alpha(), (50, 50))
ENEMY_IMGS = [
    pygame.transform.scale(pygame.image.load("enemy1.png").convert_alpha(), (60, 60)),
    pygame.transform.scale(pygame.image.load("enemy2.png").convert_alpha(), (60, 60)),
    pygame.transform.scale(pygame.image.load("enemy3.png").convert_alpha(), (60, 60))
]
BOSS_IMG = pygame.transform.scale(pygame.image.load("boss.png").convert_alpha(), (100, 100))
VICTORY_IMG = pygame.transform.scale(pygame.image.load("victory.png").convert_alpha(), (300, 50))  # Размер картинки победы

# Класс игрока
class Player:
    def __init__(self):
        self.image = PLAYER_IMG
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - 100
        self.speed = 5

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.width:
            self.x += self.speed

# Класс пули игрока
class Bullet:
    def __init__(self, x, y):
        self.width = 5
        self.height = 10
        self.x = x + 22
        self.y = y
        self.speed = 7

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))

    def move(self):
        self.y -= self.speed

# Класс пули босса
class BossBullet:
    def __init__(self, x, y):
        self.width = 5
        self.height = 10
        self.x = x + 47
        self.y = y + 100
        self.speed = 5

    def draw(self):
        pygame.draw.rect(screen, YELLOW, (self.x, self.y, self.width, self.height))

    def move(self):
        self.y += self.speed

# Класс врага
class Enemy:
    def __init__(self):
        self.image = random.choice(ENEMY_IMGS)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = random.randint(0, WIDTH - self.width)
        self.y = -self.height
        self.speed_y = 3
        self.speed_x = random.choice([-2, 2])

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.y += self.speed_y
        self.x += self.speed_x
        if self.x <= 0 or self.x >= WIDTH - self.width:
            self.speed_x *= -1

# Класс босса
class Boss:
    def __init__(self):
        self.image = BOSS_IMG
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = WIDTH // 2 - self.width // 2
        self.y = 50
        self.speed = 3
        self.health = 20
        self.direction = 1

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.x += self.speed * self.direction
        if self.x <= 0 or self.x >= WIDTH - self.width:
            self.direction *= -1

# Основные переменные
player = Player()
bullets = []
boss_bullets = []
enemies = []
boss = None
score = 0
clock = pygame.time.Clock()
running = True
spawn_timer = 0
boss_spawned = False
game_won = False
victory_timer = 0
boss_shoot_timer = 0

# Главный цикл игры
while running:
    screen.fill(BLACK)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and not game_won:
            if event.key == pygame.K_SPACE:
                bullets.append(Bullet(player.x, player.y))

    if not game_won:
        # Управление игроком
        keys = pygame.key.get_pressed()
        player.move(keys)
        player.draw()

        # Создание врагов
        spawn_timer += 1
        if spawn_timer > 120 and not boss_spawned:
            enemies.append(Enemy())
            spawn_timer = 0

        # Появление босса после 10 очков
        if score >= 10 and not boss_spawned:
            boss = Boss()
            boss_spawned = True
            enemies = []

        # Движение и отрисовка пуль игрока
        for bullet in bullets[:]:
            bullet.move()
            bullet.draw()
            if bullet.y < 0:
                bullets.remove(bullet)

        # Движение и отрисовка врагов
        for enemy in enemies[:]:
            enemy.move()
            enemy.draw()
            if enemy.y > HEIGHT:
                enemies.remove(enemy)
            for bullet in bullets[:]:
                if (enemy.x < bullet.x < enemy.x + enemy.width and
                    enemy.y < bullet.y < enemy.y + enemy.height):
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    score += 1
                    break

        # Логика босса
        if boss:
            boss.move()
            boss.draw()

            # Стрельба босса
            boss_shoot_timer += 1
            if boss_shoot_timer > 60:
                boss_bullets.append(BossBullet(boss.x, boss.y))
                boss_shoot_timer = 0

            # Движение и отрисовка пуль босса
            for b_bullet in boss_bullets[:]:
                b_bullet.move()
                b_bullet.draw()
                if b_bullet.y > HEIGHT:
                    boss_bullets.remove(b_bullet)

            # Проверка попадания в босса
            for bullet in bullets[:]:
                if (boss.x < bullet.x < boss.x + boss.width and
                    boss.y < bullet.y < boss.y + boss.height):
                    bullets.remove(bullet)
                    boss.health -= 1
                    if boss.health <= 0:
                        game_won = True
                        victory_timer = 300

            # Отображение здоровья босса
            font = pygame.font.SysFont(None, 50)
            health_text = font.render(f"BOSS HP: {boss.health}", True, WHITE)
            screen.blit(health_text, (10, 60))

    # Если победили
    if game_won:

        
        # Отображение картинки победы
        screen.blit(VICTORY_IMG, (WIDTH // 2 - VICTORY_IMG.get_width() // 2, HEIGHT // 2 + 50))
        
        victory_timer -= 1
        if victory_timer <= 0:
            pass

    # Отображение счёта
    font = pygame.font.SysFont(None, 50)
    score_text = font.render(f"SCORE: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Обновление экрана
    pygame.display.flip()
    clock.tick(60)

# Завершение игры
pygame.quit()
print(f"Игра окончена! Ваш SCORE: {score}")