import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 840, 550
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Paper Scissors")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Fonts
font = pygame.font.SysFont(None, 40)

# Game variables
choices = ["Rock", "Paper", "Scissors"]
player_score = 0
computer_score = 0

def draw_text(text, x, y, color=BLACK):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def draw_button(text, x, y, w, h):
    pygame.draw.rect(screen, GRAY, (x, y, w, h))
    draw_text(text, x + 10, y + 10)

def get_winner(player, computer):
    if player == computer:
        return "Tie"
    elif (player == "Rock" and computer == "Scissors") or \
         (player == "Paper" and computer == "Rock") or \
         (player == "Scissors" and computer == "Paper"):
        return "Player"
    else:
        return "Computer"

def draw_health_bar(x, y, score):
    bar_width = 200
    filled = (score / 5) * bar_width
    pygame.draw.rect(screen, RED, (x, y, bar_width, 20))
    pygame.draw.rect(screen, GREEN, (x, y, filled, 20))

# Main game loop
running = True
result = ""
player_choice = ""
computer_choice = ""

while running:
    screen.fill(WHITE)
    
    draw_text("Choose Rock, Paper, or Scissors", 100, 30)
    draw_button("Rock", 50, 100, 150, 50)
    draw_button("Paper", 250, 100, 150, 50)
    draw_button("Scissors", 450, 100, 150, 50)

    draw_text(f"Your Choice: {player_choice}", 50, 200)
    draw_text(f"Computer: {computer_choice}", 50, 250)
    draw_text(f"Result: {result}", 50, 300)
    
    draw_text("Player HP", 50, 400)
    draw_health_bar(210, 405, player_score)
    
    draw_text("Computer HP", 410, 400)
    draw_health_bar(600, 405, computer_score)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if 50 <= mx <= 200 and 100 <= my <= 150:
                player_choice = "Rock"
            elif 250 <= mx <= 400 and 100 <= my <= 150:
                player_choice = "Paper"
            elif 450 <= mx <= 600 and 100 <= my <= 150:
                player_choice = "Scissors"
            else:
                continue

            computer_choice = random.choice(choices)
            winner = get_winner(player_choice, computer_choice)
            if winner == "Player":
                result = "You Win!"
                player_score += 1
            elif winner == "Computer":
                result = "You Lose!"
                computer_score += 1
            else:
                result = "It's a Tie!"

            if player_score == 5 or computer_score == 5:
                result += " Game Over!"
                draw_text("Click anywhere to restart", 200, 350)
                pygame.display.update()
                pygame.time.delay(2000)
                player_score = 0
                computer_score = 0
                result = ""
                player_choice = ""
                computer_choice = ""

    pygame.display.update()

pygame.quit()
sys.exit()
