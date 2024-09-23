import pygame
import random
import os
import sys

# Initialize Pygame
pygame.init()

# Set up display
screen_width, screen_height = 600, 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Love Catcher Game")

# Define colors
WHITE = (255, 255, 255)
PINK = (255, 192, 203)
RED = (255, 0, 0)

# Load background image
background = pygame.image.load('assets/background.jpg').convert()  # Add your background image
background = pygame.transform.scale(background, (screen_width, screen_height))

# Player variables
player_width = 50
player_height = 50
player_speed = 5

# Heart variables
heart_width = 30
heart_height = 30
heart_speed = 3

# Game variables
win_score = 10  # Winning score, 10 hearts collected
font = pygame.font.Font(None, 36)
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
# Load images
player = pygame.image.load('assets/player.png').convert_alpha()  # Add your custom image if you want
player = pygame.transform.scale(player, (player_width, player_height))

heart = pygame.image.load('assets/heart.png').convert_alpha()  # Heart image
heart = pygame.transform.scale(heart, (heart_width, heart_height))

# Load sounds
collect_sound = pygame.mixer.Sound('assets/collect.mp3')  # Sound for collecting a heart
win_sound = pygame.mixer.Sound('assets/win.mp3')  # Sound when the player wins
lose_sound = pygame.mixer.Sound('assets/lose.mp3')  # Sound when the player loses

# Load background music
pygame.mixer.music.load('assets/music.mp3')  # Add your background music file
pygame.mixer.music.play(-1)  # Play music in a loop indefinitely

# Function to reset the game
def reset_game():
    global player_x, player_y, heart_x, heart_y, score, lives, game_over, game_won
    # Player position
    player_x = screen_width // 2 - player_width // 2
    player_y = screen_height - player_height - 10

    # Heart position
    heart_x = random.randint(0, screen_width - heart_width)
    heart_y = -heart_height

    # Reset score and lives
    score = 0
    lives = 3
    game_over = False
    game_won = False

    # Resume music when the game restarts
    pygame.mixer.music.play(-1)

# Call reset_game to initialize variables
reset_game()

# Game loop
running = True
while running:
    screen.blit(background, (0, 0))  # Draw the background image

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
        player_x += player_speed

    # Restart game on spacebar press if the game is over or won
    if keys[pygame.K_SPACE] and (game_over or game_won):
        reset_game()

    if not game_over and not game_won:
        # Move heart down
        heart_y += heart_speed

        # Check if heart is caught
        if player_x < heart_x < player_x + player_width or player_x < heart_x + heart_width < player_x + player_width:
            if player_y < heart_y + heart_height < player_y + player_height:
                score += 1
                collect_sound.play()  # Play sound when heart is caught
                heart_x = random.randint(0, screen_width - heart_width)
                heart_y = -heart_height

                # Check if the player won
                if score >= win_score:
                    game_won = True
                    pygame.mixer.music.stop()  # Stop music when the player wins
                    win_sound.play()

        # If heart hits the bottom
        if heart_y > screen_height:
            lives -= 1
            heart_x = random.randint(0, screen_width - heart_width)
            heart_y = -heart_height

            if lives == 0:
                game_over = True
                pygame.mixer.music.stop()  # Stop music when the player loses
                lose_sound.play()

    # Draw player and heart
    screen.blit(player, (player_x, player_y))
    screen.blit(heart, (heart_x, heart_y))

    # Draw score and lives
    score_text = font.render(f"Score: {score}", True, RED)
    lives_text = font.render(f"Lives: {lives}", True, RED)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 50))

    # Game over or win message
    if game_over:
        game_over_text = font.render("Game Over! You lost. Press Space to Restart", True, RED)
        game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(game_over_text, game_over_rect)

    if game_won:
        win_text = font.render("You Won! I Love You 💖 Press Space to Restart", True, RED)
        win_rect = win_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(win_text, win_rect)

    # Update display
    pygame.display.flip()
    pygame.time.Clock().tick(60)

# Quit game
pygame.quit()
