import os
import pygame
import sys
from config import *

class Fighter:
    def __init__(self, x, y, char_name, keys, flip=False):
        self.x = x
        self.y = y
        self.char_name = char_name
        self.keys = keys
        self.flip = flip

        self.animations = {}
        anim_states = ["death", "idle", "walk", "duck", "jump", "hit", "punch", "kick", "win"]
        for state in anim_states:
            path = os.path.join(CHARACTER_DIRS[self.char_name], f"{state}.png")
            if not os.path.exists(path):
                print(f"Ошибка: {path} не найден!")
                pygame.quit()
                sys.exit()
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (CHAR_WIDTH, CHAR_HEIGHT))
            self.animations[state] = img

        self.current_state = "idle"
        self.image = self.animations[self.current_state]

        self.stand_rect = pygame.Rect(self.x, self.y, CHAR_WIDTH, CHAR_HEIGHT)
        self.duck_rect = pygame.Rect(self.x, self.y + CHAR_HEIGHT // 2, CHAR_WIDTH, CHAR_HEIGHT // 2)

        self.is_jumping = False
        self.jump_vel = 15
        self.gravity = 1
        self.vertical_vel = 0

        self.health = MAX_HEALTH
        self.speed = 5

        self.is_attacking = False
        self.attack_cooldown = 0
        self.attack_type = None

        self.facing_right = not flip

        self.is_dead = False
        self.is_winning = False

        self.hit_timer = 0

        self.rect = self.stand_rect.copy()

        # Флаг, чтобы атака срабатывала 1 раз за атаку
        self.attack_done = False

    def set_win(self):
        self.is_winning = True
        self.current_state = "win"
        self.image = self.animations["win"]

    def move(self, keys_pressed):
        if self.is_dead:
            self.current_state = "death"
            self.image = self.animations[self.current_state]
            return

        if self.is_winning:
            return

        if self.hit_timer > 0:
            self.hit_timer -= 1

        dx = 0

        if not self.is_jumping and not (self.keys.get('duck') and keys_pressed[self.keys['duck']]):
            if keys_pressed[self.keys['left']]:
                dx = -self.speed
                self.facing_right = False
            elif keys_pressed[self.keys['right']]:
                dx = self.speed
                self.facing_right = True

        if not self.is_jumping:
            if self.keys.get('jump') and keys_pressed[self.keys['jump']]:
                self.is_jumping = True
                self.vertical_vel = -self.jump_vel

        if self.is_jumping:
            self.y += self.vertical_vel
            self.vertical_vel += self.gravity

            if self.y >= HEIGHT - CHAR_HEIGHT - 50:
                self.y = HEIGHT - CHAR_HEIGHT - 50
                self.is_jumping = False
                self.vertical_vel = 0

        is_ducking = False
        if not self.is_jumping and self.keys.get('duck') and keys_pressed[self.keys['duck']]:
            is_ducking = True

        self.x += dx
        self.x = max(0, min(self.x, WIDTH - CHAR_WIDTH))

        if is_ducking:
            self.rect = self.duck_rect.copy()
            self.rect.topleft = (self.x, self.y + CHAR_HEIGHT // 2)
        else:
            self.rect = self.stand_rect.copy()
            self.rect.topleft = (self.x, self.y)

        # Управляем атакой и кулдауном
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            # Атака длится, флаг активности True
            self.is_attacking = True
        else:
            # Можно начать новую атаку
            self.is_attacking = False
            self.attack_type = None
            self.attack_done = False  # Сброс флага успешной атаки

            # Начинаем новую атаку, если кнопка нажата
            if keys_pressed[self.keys['punch']]:
                self.is_attacking = True
                self.attack_cooldown = 30  # длительность анимации и атаки
                self.attack_type = "punch"
            elif keys_pressed[self.keys['kick']]:
                self.is_attacking = True
                self.attack_cooldown = 30
                self.attack_type = "kick"

        # Анимация с приоритетами
        if self.hit_timer > 0:
            self.current_state = "hit"
        elif self.is_attacking:
            self.current_state = self.attack_type
        elif self.is_jumping:
            self.current_state = "jump"
        elif is_ducking:
            self.current_state = "duck"
        elif dx != 0:
            self.current_state = "walk"
        else:
            self.current_state = "idle"

        if self.health <= 0:
            self.is_dead = True
            self.current_state = "death"

        self.image = self.animations[self.current_state]

    def attack_hits(self, other):
        # Срабатывает удар только один раз за атаку
        if self.is_attacking and not self.attack_done and not self.is_dead:
            attack_range = 50
            if self.facing_right:
                attack_rect = pygame.Rect(self.x + CHAR_WIDTH, self.y + 30, attack_range, 30)
            else:
                attack_rect = pygame.Rect(self.x - attack_range, self.y + 30, attack_range, 30)

            if attack_rect.colliderect(other.rect):
                if other.health > 0:
                    other.health -= 10
                    other.hit_timer = 15
                    other.current_state = "hit"
                    self.attack_done = True  # Удар выполнен

    def draw(self, surface):
        img = self.image
        if self.flip:
            img = pygame.transform.flip(img, True, False)
        surface.blit(img, self.rect.topleft)
