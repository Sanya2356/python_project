import os
import pygame

# Общие настройки
WIDTH, HEIGHT = 1200, 600
FPS = 60

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Путь к ресурсам
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# Папки с персонажами и локациями
CHARACTERS = ["Ermak", "Sub_Zero", "Scorpion", "Reptile", "Smoke", "Noob_Saibot", "Rein"]
CHARACTER_DIRS = {char: os.path.join(ASSETS_DIR, char) for char in CHARACTERS}

LOCATIONS = [os.path.join(ASSETS_DIR, f"Loc{i}.jpg") for i in range(1, 5)]

# Кнопки управления
P1_KEYS = {
    "left": pygame.K_a,
    "right": pygame.K_d,
    'jump': pygame.K_w,
    'duck': pygame.K_s,
    "kick": pygame.K_z,
    "punch": pygame.K_x,
}

P2_KEYS = {
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT,
    'jump': pygame.K_UP,
    'duck': pygame.K_DOWN,
    "kick": pygame.K_KP1,
    "punch": pygame.K_KP2,
}

# Размеры персонажа
CHAR_WIDTH, CHAR_HEIGHT = 80, 150

MAX_HEALTH = 480

# Папка с изображениями для меню выбора персонажей
SELECT_IMAGES_DIR = os.path.join(ASSETS_DIR, "select")
