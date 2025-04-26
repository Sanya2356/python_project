import pygame
import sys
import os
from config import *
from fighter import Fighter
from utils import draw_health_bar
from menu import CharacterSelectMenu

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fighting Game")

clock = pygame.time.Clock()

# Загружаем и масштабируем локации из assets
backgrounds = []
for i in range(1, 5):
    path = os.path.join(ASSETS_DIR, f"Loc{i}.jpg")
    if not os.path.exists(path):
        print(f"Ошибка: локация {path} не найдена!")
        pygame.quit()
        sys.exit()
    bg = pygame.image.load(path).convert()
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    backgrounds.append(bg)

current_location_index = 0  # Индекс текущей локации

def main():
    global current_location_index

    # Запускаем меню выбора персонажей
    menu = CharacterSelectMenu(screen)
    p1_char, p2_char = menu.run()

    # Выбираем локацию и меняем индекс циклично
    background = backgrounds[current_location_index]
    current_location_index = (current_location_index + 1) % len(backgrounds)

    # Инициализация бойцов
    player1 = Fighter(100, HEIGHT - CHAR_HEIGHT - 50, p1_char, P1_KEYS)
    player2 = Fighter(WIDTH - 100 - CHAR_WIDTH, HEIGHT - CHAR_HEIGHT - 50, p2_char, P2_KEYS, flip=True)

    winner = None
    win_time = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys_pressed = pygame.key.get_pressed()

        if winner is None:
            # Игровой процесс
            player1.move(keys_pressed)
            player2.move(keys_pressed)

            player1.attack_hits(player2)
            player2.attack_hits(player1)

            # Проверяем победителя
            if player1.health <= 0 and winner is None:
                winner = player2
                winner.current_state = "win"
                win_time = pygame.time.get_ticks()
            elif player2.health <= 0 and winner is None:
                winner = player1
                winner.current_state = "win"
                win_time = pygame.time.get_ticks()

        else:
            # Показываем анимацию победы и ждём 3 секунды
            now = pygame.time.get_ticks()
            if now - win_time >= 3000:
                # Через 3 секунды возвращаемся в меню, перезапускаем main
                main()
                return

        # Отрисовка
        screen.blit(background, (0, 0))

        player1.draw(screen)
        player2.draw(screen)

        draw_health_bar(screen, 50, 20, max(player1.health, 0), MAX_HEALTH)
        draw_health_bar(screen, WIDTH - 250, 20, max(player2.health, 0), MAX_HEALTH)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
