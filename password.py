import pygame
import random
import string
import os
import json

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 600, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Password Generator")

# Fonts
FONT = pygame.font.Font(None, 32)
BIG_FONT = pygame.font.Font(None, 40)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 100, 255)
GRAY = (200, 200, 200)

# File to store passwords
SAVE_FILE = "passwords.json"

# UI Input boxes
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = GRAY
        self.text = text
        self.txt_surface = FONT.render(text, True, BLACK)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.active = False
            else:
                self.text += event.unicode
            self.txt_surface = FONT.render(self.text, True, BLACK)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))

# Generate Password
def generate_password(length):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

# Save password
def save_password(label, password):
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r') as f:
            data = json.load(f)
    else:
        data = {}
    data[label] = password
    with open(SAVE_FILE, 'w') as f:
        json.dump(data, f)

# Retrieve password
def retrieve_password(label):
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r') as f:
            data = json.load(f)
        return data.get(label, "Not found")
    return "Not found"

# Main loop
def main():
    clock = pygame.time.Clock()

    length_input = InputBox(150, 50, 100, 32)
    label_input = InputBox(150, 100, 200, 32)
    retrieve_input = InputBox(150, 300, 200, 32)

    password = ''
    retrieved_password = ''

    run = True
    while run:
        win.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            length_input.handle_event(event)
            label_input.handle_event(event)
            retrieve_input.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # Generate Button
                if 380 <= x <= 500 and 50 <= y <= 90:
                    if length_input.text.isdigit():
                        length = int(length_input.text)
                        password = generate_password(length)
                        save_password(label_input.text.strip(), password)
                # Retrieve Button
                if 380 <= x <= 500 and 300 <= y <= 340:
                    retrieved_password = retrieve_password(retrieve_input.text.strip())

        # Draw UI
        length_input.draw(win)
        label_input.draw(win)
        retrieve_input.draw(win)

        win.blit(FONT.render("Length:", True, BLACK), (50, 55))
        win.blit(FONT.render("Label:", True, BLACK), (50, 105))
        win.blit(FONT.render("Saved Label (to Retrieve):", True, BLACK), (50, 270))

        # Buttons
        pygame.draw.rect(win, BLUE, (380, 50, 120, 40))
        win.blit(FONT.render("Generate", True, WHITE), (395, 60))

        pygame.draw.rect(win, BLUE, (380, 300, 120, 40))
        win.blit(FONT.render("Retrieve", True, WHITE), (395, 310))

        # Show Password
        win.blit(BIG_FONT.render(f"Generated: {password}", True, BLACK), (50, 160))
        win.blit(BIG_FONT.render(f"Found: {retrieved_password}", True, BLACK), (50, 360))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

main()
