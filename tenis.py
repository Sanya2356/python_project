import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Colorful Tennis Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 36)
large_font = pygame.font.SysFont("Arial", 72)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)       # Player 1
BLUE = (0, 0, 255)      # Player 2
GREEN = (0, 200, 0)     # Bot

PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 20
BALL_SPEED = 5
PADDLE_SPEED = 6
MAX_SCORE = 5
BOT_SPEED = 4

def draw_text(text, font, color, surface, x, y, center=True):
    render = font.render(text, True, color)
    rect = render.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(render, rect)

def main_menu():
    while True:
        screen.fill(BLACK)
        draw_text("TENNIS GAME", large_font, WHITE, screen, WIDTH//2, HEIGHT//4)
        draw_text("1. Player vs Player", font, WHITE, screen, WIDTH//2, HEIGHT//2 - 30)
        draw_text("2. Player vs Bot", font, WHITE, screen, WIDTH//2, HEIGHT//2 + 30)
        draw_text("ESC to Quit", font, WHITE, screen, WIDTH//2, HEIGHT//2 + 90)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "pvp"
                if event.key == pygame.K_2:
                    return "bot"
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

def game_loop(vs_bot=False):
    player1 = pygame.Rect(30, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    player2 = pygame.Rect(WIDTH - 40, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)
    ball_dx, ball_dy = BALL_SPEED, BALL_SPEED
    score1, score2 = 0, 0
    ball_color = WHITE

    def reset_ball():
        nonlocal ball_dx, ball_dy, ball_color
        ball.center = (WIDTH // 2, HEIGHT // 2)
        ball_dx *= -1
        ball_dy *= -1
        ball_color = WHITE

    while True:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and player1.top > 0:
            player1.y -= PADDLE_SPEED
        if keys[pygame.K_s] and player1.bottom < HEIGHT:
            player1.y += PADDLE_SPEED

       
        if vs_bot:
            if ball.centery > player2.centery and player2.bottom < HEIGHT:
                player2.y += BOT_SPEED
            elif ball.centery < player2.centery and player2.top > 0:
                player2.y -= BOT_SPEED
        else:
            if keys[pygame.K_UP] and player2.top > 0:
                player2.y -= PADDLE_SPEED
            if keys[pygame.K_DOWN] and player2.bottom < HEIGHT:
                player2.y += PADDLE_SPEED

        
        ball.x += ball_dx
        ball.y += ball_dy

    
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_dy *= -1
        if ball.colliderect(player1):
            ball_dx *= -1
            ball_color = RED
        if ball.colliderect(player2):
            ball_dx *= -1
            ball_color = GREEN if vs_bot else BLUE

        
        if ball.left <= 0:
            score2 += 1
            reset_ball()
        if ball.right >= WIDTH:
            score1 += 1
            reset_ball()

        
        if score1 >= MAX_SCORE or score2 >= MAX_SCORE:
            winner = "Player 1" if score1 > score2 else "Bot" if vs_bot else "Player 2"
            draw_text(f"{winner} Wins!", large_font, WHITE, screen, WIDTH//2, HEIGHT//2)
            pygame.display.flip()
            pygame.time.delay(3000)
            return

        
        pygame.draw.rect(screen, RED, player1)
        pygame.draw.rect(screen, GREEN if vs_bot else BLUE, player2)
        pygame.draw.ellipse(screen, ball_color, ball)
        pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))
        draw_text(str(score1), font, RED, screen, WIDTH//4, 20)
        draw_text(str(score2), font, GREEN if vs_bot else BLUE, screen, WIDTH*3//4, 20)

        pygame.display.flip()
        clock.tick(60)


while True:
    mode = main_menu()
    game_loop(vs_bot=(mode == "bot"))
