
import pygame
import random
import sys

pygame.init()


WIDTH, HEIGHT = 800, 600
TILE_SIZE = 40
ROWS, COLS = HEIGHT // TILE_SIZE, WIDTH // TILE_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tanks")


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
GREEN = (0, 200, 0)
GRAY = (150, 150, 150)
YELLOW = (255, 255, 0)


font = pygame.font.SysFont("Arial", 36)

clock = pygame.time.Clock()


def generate_maze():
    walls = []
    for y in range(ROWS):
        for x in range(COLS):
            if random.random() < 0.2:
                walls.append(pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
    return walls


class Bullet:
    def __init__(self, x, y, dx, dy, color):
        self.rect = pygame.Rect(x-5, y-5, 10, 10)
        self.dx = dx
        self.dy = dy
        self.color = color

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)


class Tank:
    def __init__(self, x, y, color, controls, is_bot=False):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.color = color
        self.controls = controls
        self.bullets = []
        self.speed = 4
        self.cooldown = 0
        self.is_bot = is_bot
        self.direction = 'up'
        self.hp = 3

    def move(self, keys, walls, target=None):
        dx, dy = 0, 0

        if self.is_bot:
            if random.random() < 0.02:
                self.direction = random.choice(['up', 'down', 'left', 'right'])
            self.shoot()

            if self.direction == 'up': dy = -self.speed
            elif self.direction == 'down': dy = self.speed
            elif self.direction == 'left': dx = -self.speed
            elif self.direction == 'right': dx = self.speed
        else:
            if keys[self.controls['up']]: dy = -self.speed; self.direction = 'up'
            if keys[self.controls['down']]: dy = self.speed; self.direction = 'down'
            if keys[self.controls['left']]: dx = -self.speed; self.direction = 'left'
            if keys[self.controls['right']]: dx = self.speed; self.direction = 'right'

            if keys[self.controls['shoot']] and self.cooldown == 0:
                self.shoot()

        new_rect = self.rect.move(dx, dy)
        if new_rect.left >= 0 and new_rect.right <= WIDTH and new_rect.top >= 0 and new_rect.bottom <= HEIGHT:
            if not any(new_rect.colliderect(w) for w in walls):
                self.rect = new_rect

        if self.cooldown > 0:
            self.cooldown -= 1

    def shoot(self):
        dx, dy = 0, 0
        if self.direction == 'up': dy = -8
        elif self.direction == 'down': dy = 8
        elif self.direction == 'left': dx = -8
        elif self.direction == 'right': dx = 8

        bullet = Bullet(self.rect.centerx, self.rect.centery, dx, dy, self.color)
        self.bullets.append(bullet)
        self.cooldown = 20

    def draw(self, surface):
       
        pygame.draw.rect(surface, self.color, self.rect)

       
        barrel_length = TILE_SIZE // 2
        barrel_width = 6
        cx, cy = self.rect.center
        if self.direction == 'up':
            barrel = pygame.Rect(cx - barrel_width//2, self.rect.top - barrel_length, barrel_width, barrel_length)
        elif self.direction == 'down':
            barrel = pygame.Rect(cx - barrel_width//2, self.rect.bottom, barrel_width, barrel_length)
        elif self.direction == 'left':
            barrel = pygame.Rect(self.rect.left - barrel_length, cy - barrel_width//2, barrel_length, barrel_width)
        elif self.direction == 'right':
            barrel = pygame.Rect(self.rect.right, cy - barrel_width//2, barrel_length, barrel_width)
        pygame.draw.rect(surface, YELLOW, barrel)

        for bullet in self.bullets:
            bullet.draw(surface)

def draw_walls(walls):
    for wall in walls:
        pygame.draw.rect(screen, GRAY, wall)

def handle_bullets(tank1, tank2, walls):
    for tank in [tank1, tank2]:
        for bullet in tank.bullets[:]:
            bullet.move()
            if not screen.get_rect().contains(bullet.rect):
                tank.bullets.remove(bullet)
                continue
            hit_wall = None
            for wall in walls:
                if bullet.rect.colliderect(wall):
                    hit_wall = wall
                    break
            if hit_wall:
                walls.remove(hit_wall)
                tank.bullets.remove(bullet)
                continue
            other = tank2 if tank == tank1 else tank1
            if bullet.rect.colliderect(other.rect):
                other.hp -= 1
                tank.bullets.remove(bullet)

def draw_hp(tank1, tank2, vs_bot):
    hp1 = font.render(f"P1 HP: {tank1.hp}", True, RED)
    hp2 = font.render(f"{'Bot' if vs_bot else 'P2'} HP: {tank2.hp}", True, GREEN if vs_bot else BLUE)
    screen.blit(hp1, (10, 10))
    screen.blit(hp2, (WIDTH - 200, 10))

def draw_text(text, x, y):
    label = font.render(text, True, WHITE)
    rect = label.get_rect(center=(x, y))
    screen.blit(label, rect)

def main_menu():
    while True:
        screen.fill(BLACK)
        draw_text("TANK GAME", WIDTH // 2, HEIGHT // 4)
        draw_text("1. Игрок против игрока", WIDTH // 2, HEIGHT // 2 - 30)
        draw_text("2. Игрок против бота", WIDTH // 2, HEIGHT // 2 + 30)
        draw_text("ESC для выхода", WIDTH // 2, HEIGHT // 2 + 90)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return False
                if event.key == pygame.K_2:
                    return True
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

def game_loop(vs_bot):
    walls = generate_maze()
    p1 = Tank(100, 100, RED, {'up': pygame.K_w, 'down': pygame.K_s,
                              'left': pygame.K_a, 'right': pygame.K_d,
                              'shoot': pygame.K_SPACE})
    if vs_bot:
        p2 = Tank(WIDTH - 140, HEIGHT - 140, GREEN, {}, is_bot=True)
    else:
        p2 = Tank(WIDTH - 140, HEIGHT - 140, BLUE, {'up': pygame.K_UP, 'down': pygame.K_DOWN,
                                                    'left': pygame.K_LEFT, 'right': pygame.K_RIGHT,
                                                    'shoot': pygame.K_RETURN})
    while True:
        screen.fill(BLACK)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        p1.move(keys, walls)
        p2.move(keys, walls, target=p1)

        handle_bullets(p1, p2, walls)
        draw_walls(walls)
        p1.draw(screen)
        p2.draw(screen)
        draw_hp(p1, p2, vs_bot)

        if p1.hp <= 0 or p2.hp <= 0:
            winner = "Bot" if vs_bot and p2.hp > 0 else "Player 2" if not vs_bot and p2.hp > 0 else "Player 1"
            draw_text(f"{winner} wins!", WIDTH//2, HEIGHT//2)
            pygame.display.flip()
            pygame.time.delay(3000)
            return

        pygame.display.flip()
        clock.tick(60)


while True:
    bot_mode = main_menu()
    game_loop(bot_mode)
