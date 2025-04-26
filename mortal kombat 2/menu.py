import pygame
import os
import sys
from config import *

class CharacterSelectMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('arial', 30)
        self.clock = pygame.time.Clock()
        self.selected_index_p1 = 0
        self.selected_index_p2 = 0
        self.ready_p1 = False
        self.ready_p2 = False

        # Загрузка превью картинок из папки select (например ermak.jpg и т.п.)
        self.preview_images = []
        for char in CHARACTERS:
            preview_path = os.path.join(SELECT_IMAGES_DIR, f"{char.lower()}.jpg")
            if not os.path.exists(preview_path):
                print(f"Ошибка: {preview_path} не найден!")
                pygame.quit()
                sys.exit()
            img = pygame.image.load(preview_path).convert_alpha()
            img = pygame.transform.scale(img, (CHAR_WIDTH*2, CHAR_HEIGHT*2))
            self.preview_images.append(img)

        # Загрузка idle спрайтов персонажей (для отображения рядом с превью)
        self.idle_sprites = []
        for char in CHARACTERS:
            idle_path = os.path.join(CHARACTER_DIRS[char], "idle.png")
            if not os.path.exists(idle_path):
                print(f"Ошибка: {idle_path} не найден!")
                pygame.quit()
                sys.exit()
            img = pygame.image.load(idle_path).convert_alpha()
            img = pygame.transform.scale(img, (CHAR_WIDTH*2, CHAR_HEIGHT*2))
            self.idle_sprites.append(img)

    def run(self):
        while True:
            self.screen.fill(BLACK)

            # Тексты подсказок
            text1 = self.font.render("Player 1: A/D - выбрать, ENTER - подтвердить", True, WHITE)
            text2 = self.font.render("Player 2: Left/Right - выбрать, RETURN - подтвердить", True, WHITE)
            self.screen.blit(text1, (20, 20))
            self.screen.blit(text2, (20, 60))

            # Отрисовка превью персонажей для игроков
            p1_preview = self.preview_images[self.selected_index_p1]
            p2_preview = self.preview_images[self.selected_index_p2]

            self.screen.blit(p1_preview, (150, 100))
            self.screen.blit(p2_preview, (WIDTH - 350, 100))

            # Отрисовка idle спрайтов рядом
            p1_idle = self.idle_sprites[self.selected_index_p1]
            p2_idle = self.idle_sprites[self.selected_index_p2]

            self.screen.blit(p1_idle, (150, 270))
            self.screen.blit(p2_idle, (WIDTH - 350, 270))

            # Надписи READY
            if self.ready_p1:
                ready_text = self.font.render("READY", True, GREEN)
                self.screen.blit(ready_text, (150, 430))
            if self.ready_p2:
                ready_text = self.font.render("READY", True, GREEN)
                self.screen.blit(ready_text, (WIDTH - 350, 430))

            # Отрисовка имен персонажей под превью
            p1_name = self.font.render(CHARACTERS[self.selected_index_p1], True, WHITE)
            p2_name = self.font.render(CHARACTERS[self.selected_index_p2], True, WHITE)

            self.screen.blit(p1_name, (150, 70))
            self.screen.blit(p2_name, (WIDTH - 350, 70))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if not self.ready_p1:
                        if event.key == pygame.K_a:
                            self.selected_index_p1 = (self.selected_index_p1 - 1) % len(CHARACTERS)
                        elif event.key == pygame.K_d:
                            self.selected_index_p1 = (self.selected_index_p1 + 1) % len(CHARACTERS)
                        elif event.key == pygame.K_RETURN:
                            self.ready_p1 = True

                    if not self.ready_p2:
                        if event.key == pygame.K_LEFT:
                            self.selected_index_p2 = (self.selected_index_p2 - 1) % len(CHARACTERS)
                        elif event.key == pygame.K_RIGHT:
                            self.selected_index_p2 = (self.selected_index_p2 + 1) % len(CHARACTERS)
                        elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                            self.ready_p2 = True

                    # Если оба готовы — выйти из меню
                    if self.ready_p1 and self.ready_p2:
                        return CHARACTERS[self.selected_index_p1], CHARACTERS[self.selected_index_p2]

            self.clock.tick(FPS)
