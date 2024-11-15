import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))

bg = pygame.image.load("background.jpeg").convert()
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

pygame.display.set_caption("SpaceShip Game")
clock = pygame.time.Clock()

#Sounds
moon_sfx = pygame.mixer.Sound("mixkit-game-ball-tap-2073.wav")
ship_sound = pygame.mixer.Sound("low-spaceship-rumble-195722.mp3")
victory_sound = pygame.mixer.Sound("victory.mp3")

#Fonts
title_font = pygame.font.SysFont("Comic Sans", 74)  # Large font for the title
sub_font = pygame.font.SysFont("Comic Sans", 14)    # Smaller font for instructions

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Spawn Timer
SPAWN_INTERVAL = 1000  # 1 second
last_spawn_time = pygame.time.get_ticks()

icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# Sprite Loader/Render?
player_image = pygame.image.load("realplayer.jpeg")  # Replace with your sprite image
moon_image = pygame.image.load("moon.jpeg")


# Title screen
def title_screen():
    title_text = title_font.render("SpaceShip Game", True, (255, 0, 0))
    instruction_text = sub_font.render("Press Any Key to Start (GPT helped a lot, but I DID alot too plz), also this game is NOT unique and ends at 100 moons.", True, WHITE)

    while True:
        window.fill(BLACK)
        window.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 100))
        window.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2 + 50))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                return  # Exit the title screen when a key is pressed


#Win Screen
def win_screen():
    big_text = title_font.render("You won!", True, (255, 0, 0))
    small_text = sub_font.render("Congrats, you beat the game!! (press any key to exit)", True, (255, 0, 0))

    while True:
        window.fill(BLACK)
        victory_sound.play()
        window.blit(big_text, (WIDTH // 2 - big_text.get_width() // 2, HEIGHT // 2 - 100))
        window.blit(small_text, (WIDTH // 2 - small_text.get_width() // 2, HEIGHT // 2 + 50))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                return  # Exit the title screen when a key is pressed


# Create a Sprite class

class Moon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("moon.jpeg")
        self.image = pygame.transform.scale(moon_image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()  # Call the parent class (Sprite) constructor
        self.original_image = pygame.image.load("realplayer.jpeg").convert_alpha()  # Store original image
        self.original_image = pygame.transform.scale(player_image, (50, 50))
        self.image = self.original_image

        self.rect = self.image.get_rect()  # Get the rectangle (for positioning)
        self.rect.topleft = (x, y)  # Set the initial position of the sprite
        self.speed = 3
        self.sound_playing = False

    # Game loop
    def update(self):
        """Update the sprite's position (called every frame)."""
        keys = pygame.key.get_pressed()  # Get key states
        moving = False

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed  # Move left
            self.image = pygame.transform.rotate(self.original_image, 90)  # Rotate from original image
            moving = True
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed  # Move right
            self.image = pygame.transform.rotate(self.original_image, -90)  # Rotate from original image
            moving = True
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed  # Move up
            self.image = pygame.transform.rotate(self.original_image, 0)  # Rotate from original image
            moving = True
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed  # Move down
            self.image = pygame.transform.rotate(self.original_image, 180)  # Rotate from original image
            moving = True

        if moving and not self.sound_playing:
            ship_sound.play()  # Loop indefinitely
            self.sound_playing= True
        elif not moving and self.sound_playing:
            ship_sound.stop()  # Stop sound when not moving
            self.sound_playing = False

        self.rect = self.image.get_rect(center=self.rect.center)


# Create a Player instance
player = Player(375, 275)  # Start near the center of the screen

# Create a sprite group and add the player to it
player_group = pygame.sprite.Group(player)  # A single player sprite
moon_group = pygame.sprite.Group()  # Group to store all enemies

moons_collected = 0


title_screen()
# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update all sprites
    moon_group.update()
    player_group.update()

    current_time = pygame.time.get_ticks()
    if current_time - last_spawn_time > SPAWN_INTERVAL:
        moon = Moon()
        spawner = moon_group.add(moon)
        last_spawn_time = current_time

    moon_collect = pygame.sprite.spritecollide(player, moon_group, True) # True to collect moons
    moons_collected += len(moon_collect)  # Increase moon count

    if moons_collected == 100:
        win_screen()
        pygame.quit()
        sys.exit()
    # Drawing Objects onto screen

    window.blit(bg, (0, 0))
    player_group.draw(window)
    moon_group.draw(window)  # Draw all sprites

    font = pygame.font.Font(None, 30)
    text = font.render(f"Moons Collected: {moons_collected}", True, (255, 255, 255))
    window.blit(text, (10, 10))

    # Update the display
    pygame.display.flip()
    clock.tick(60)



# Quit Pygame
pygame.quit()
sys.exit()
