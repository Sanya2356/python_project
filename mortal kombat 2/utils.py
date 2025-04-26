import pygame
from config import *

def draw_health_bar(surface, x, y, health, max_health):
    ratio = health / max_health
    pygame.draw.rect(surface, RED, (x, y, 200, 20))
    pygame.draw.rect(surface, GREEN, (x, y, 200 * ratio, 20))
    pygame.draw.rect(surface, BLACK, (x, y, 200, 20), 2)
